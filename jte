#! /usr/bin/python3

import argparse
from cmath import e
from nis import match
import os
import pprint
import Modules.CustomLogging as customLogging
from typing import Dict, Any
import codecs
import sys
import glob

import Modules.RendererContext as Context

import Modules.Parser.JsonParser as jsonParser
import Modules.Parser.YamlParser as yamlParser
import Modules.Parser.EnvFileParser as envFileParser

def writeFile(outputFile : codecs.StreamReaderWriter, data: str) -> None:
        if ( outputFile.writable ) :
            outputFile.write(data)

def openFile(fileName: str) -> codecs.StreamReaderWriter :
    with codecs.open(fileName, "azer", errors='strict') as fileDescriptor:
        return fileDescriptor

def customizeOne( args: Dict ):

    context = Context.RendererContext( customControler=None,
        templateReferencePath= args.reference_path)

    dataDictionnary: Dict = None

    formatChoice : Dict[str, Any] = { 
        'json' : lambda : jsonParser.ImportJsonFile(args.input),
        'yaml' : lambda : yamlParser.ImportYamlFile(args.input),
        'yml' : lambda : yamlParser.ImportYamlFile(args.input),
        'env' : lambda : envFileParser.ImportEnvFile(args.input)
    }

    if ( args.format in formatChoice.keys() ) :
        dataDictionnary = formatChoice[args.format]()
    else :
        raise Exception( f'Unknown format : {args.format} waiting for any of {formatChoice.keys()}')

    # require python 3.10
    # match False:
    #     case "json" :
    #         dataDictionnary = jsonParser.ImportJsonFile(args.input)
    #     case "yaml":
    #         dataDictionnary = yamlParser.ImportYamlFile(args.input)
    #     case "env":
    #         dataDictionnary = envFileParser.ImportEnvFile(args.input)
    #     case _:
    #         raise Exception(f'Unkown format : {args.format}')

    renderedTemplate = context.renderTemplate(
        templatePath= args.template,
        output= args.output,
        data=dataDictionnary )


def customizeMulti( args: Dict, configFileAsList: Dict ):
    
    logger.info("config file mode")
    
    expandedDict: Dict = {}

    for templateFileName, templateAttributes in configFileAsList.items():
        if templateAttributes['expandGlobInTemplateName']:
            logger.info(f"expanding expression '{templateFileName}' ...")
            for expandedTemplateFileName in glob.glob(templateFileName):
                logger.info(f"file mathing found '{expandedTemplateFileName}' to process ...")
                expandedDict[expandedTemplateFileName] = templateAttributes.copy()
                length = len(expandedTemplateFileName)
                expandedDict[expandedTemplateFileName]['outputFile'] = expandedTemplateFileName[0:length - 3]
        else:
            expandedDict[templateFileName] = templateAttributes

    for templateFileName, templateAttributes in expandedDict.items():
        logger.info(f"processing template file '{templateFileName}' ...")
        args.template = templateFileName
        args.format = templateAttributes['contextFormat']
        args.output = templateAttributes['outputFile']

        if 'templatingContext' in templateAttributes:
           args.input = templateAttributes['templatingContext']

        customizeOne(args)

# =============================================
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='customize a jinja template file')

    parser.add_argument('-c', '--config-file', required=False,
        default= None)

    parser.add_argument('-dr', '--dry-run', default = False, required=False, action='store_true' )
    
    parser.add_argument('-i', '--input', required=False)
    parser.add_argument('-f', '--format', required=False)
    parser.add_argument('-o', '--output', required=False)
    parser.add_argument('-t', '--template', required=False)
    parser.add_argument('-r', '--reference-path', 
        default=os.getcwd(), required=False)
    
    args=parser.parse_args()
    if not args.config_file is None :
        if args.format is not None \
            or args.output is not None \
            or args.template is not None :
                parser.error("-c exclude -f, -o and -t")
    else :
        if args.template is None:
            parser.error("-t is mandatory (when not using -c)")
        if args.format is None:
            args.format = 'json'
        if args.input is None:
            args.input = sys.stdin
        if args.output is None:
            args.output = sys.stdout

    logger = customLogging.BuildCustomLogger("root")
    logger.info("program beginning ...")
    logger.info(f"reference path is '{args.reference_path}'")

    os.chdir(args.reference_path)

    pp = pprint.PrettyPrinter(depth=6)
    logger.info(pprint.pformat( args ))

    if not args.config_file is None:
        logger.info(f"loading config file '{args.config_file}' ...")
        # config: Dict = jsonParser.ImportJsonFile(args.config_file)
        config: Dict = yamlParser.ImportYamlFile(args.config_file)
        customizeMulti(args, config)
    else:
        customizeOne(args)
    

    logger.info("script clean end")

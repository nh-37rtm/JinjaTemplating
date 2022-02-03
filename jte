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

def main( args: Dict ):

    context = Context.RendererContext( customControler=None )

    dataDictionnary: Dict = None

    formatChoice : Dict[str, Any] = { 
        'json' : lambda : jsonParser.ImportJsonFile(args.input),
        'yaml' : lambda : yamlParser.ImportYamlFile(args.input),
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

# =============================================
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='customize a jinja template file')

    parser.add_argument('-i', '--input', required=False, 
        default= sys.stdin)
    parser.add_argument('-f', '--format', required=False, 
        default= 'json')
    parser.add_argument('-o', '--output', required=False,
        default= sys.stdout)
    parser.add_argument('-t', '--template', required=True)
    parser.add_argument('-dr', '--dry-run', default = False, required=False, action='store_true' )
    
    args=parser.parse_args()
    logger = customLogging.BuildCustomLogger("root")

    logger.info("program beginning ...")

    pp = pprint.PrettyPrinter(depth=6)
    logger.info(pprint.pformat( args ))

    main(args)

    logger.info("script clean end")

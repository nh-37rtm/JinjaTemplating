from cmath import e
from nis import match
import os
import pprint
import Modules.CustomLogging as customLogging
from typing import Dict, Any, List
import codecs
import sys
import glob
import copy

import subprocess

import Modules.Parser.JsonParser as jsonParser
import Modules.Parser.YamlParser as yamlParser
import Modules.Parser.EnvFileParser as envFileParser
import Modules.CustomLogging as customLogging
import Modules.RendererContext as Context


logger = customLogging.BuildCustomLogger("root")

def writeFile(outputFile : codecs.StreamReaderWriter, data: str) -> None:
        if ( outputFile.writable ) :
            outputFile.write(data)

def openFile(fileName: str) -> codecs.StreamReaderWriter :
    with codecs.open(fileName, "azer", errors='strict') as fileDescriptor:
        return fileDescriptor

def validateOutput( args: Dict ):

    validatorActions: Dict = {}

    validators : Dict[str, Any] = { 
        'json' : lambda : jsonParser.ImportJsonFile(args.output),
        'yaml' : lambda : yamlParser.ImportYamlFile(args.output, True),
        'kube' : lambda : subprocess.check_output(['kubectl', 'apply', '-f', args.output, '--dry-run=client']),
        'kustomize' : lambda : subprocess.check_output(['kubectl', 'apply', '-k', os.path.dirname(args.output), '--dry-run=client'])
    }

    for validator in args.output_validator:
        if ( validator in validators.keys() ) :
            validatorActions[validator] = validators[validator]
        else :
            raise Exception( f'Unknown format : {validator} waiting for any of {validators.keys()}')

    logger.info(f"running validators on output {args.output} ...")

    for validatorName, validateAction in validatorActions.items():
        logger.info(f"passing the {validatorName} validator ...")
        validateAction()
        logger.info(f"validator passed successfully !")

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

    if len(args.output_validator) > 0:
        validateOutput(args)


def customizeMulti( args: Dict, configFileAsList: Dict ):
    
    logger.info("config file mode")
    
    expandedDict: Dict = {}

    for templateFileName, templateAttributes in configFileAsList.items():
        if 'expandGlobInTemplateName' in templateAttributes:
            logger.info(f"expanding expression '{templateFileName}' ...")
            for expandedTemplateFileName in glob.glob(templateFileName):
                logger.info(f"file mathing found '{expandedTemplateFileName}' to process ...")
                expandedDict[expandedTemplateFileName] = templateAttributes.copy()
                length = len(expandedTemplateFileName)
                expandedDict[expandedTemplateFileName]['outputFile'] = expandedTemplateFileName[0:length - 3]
        else:
            expandedDict[templateFileName] = templateAttributes

    templateNumber: int = 0
    for templateFileName, templateAttributes in expandedDict.items():
        templateArgs = copy.deepcopy(args)
        logger.info(f"processing template file '{templateFileName}' ...")
        templateArgs.template = templateFileName
        templateArgs.format = templateAttributes['contextFormat']
        templateArgs.output = templateAttributes['outputFile']

        if 'outputValidator' in templateAttributes:
            templateArgs.output_validator = [ templateAttributes['outputValidator'] ]
            ## TODO verifier la diff str os.stdout ...
            if templateArgs.output is None:
                parser.error("cannot validate if no output file set")
        else:
            templateArgs.output_validator = []
        #TODO manage override

        if 'templatingContext' in templateAttributes:
           templateArgs.input = templateAttributes['templatingContext']
        templateNumber+=1
        customizeOne(templateArgs)

    logger.info(f"{templateNumber} templates processed")

def validateArgsAndRun(args):

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
            if not args.output_validator is None:
                parser.error("cannot validate if no output file set")
            args.output = sys.stdout

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
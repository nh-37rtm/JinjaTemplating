import codecs
import copy
import glob
import io
import os
import pprint
import subprocess
import sys
import typing as t
from argparse import ArgumentParser

import jinja_templating.modules.custom_logging as customLogging
import jinja_templating.modules.renderer_context as Context

import jinja_templating.modules.parser.env_file_parser as envFileParser
import jinja_templating.modules.parser.json_parser as jsonParser
import jinja_templating.modules.parser.yaml_parser as yamlParser

logger = customLogging.BuildCustomLogger("root")

parser = ArgumentParser(description='Argument parser')

def writeFile(outputFile : codecs.StreamReaderWriter, data: str) -> None:
        if ( outputFile.writable ) :
            outputFile.write(data)

def openFile(fileName: str) -> codecs.StreamReaderWriter :
    with codecs.open(fileName, "azer", errors='strict') as fileDescriptor:
        return fileDescriptor

def validateOutput( args: dict ):

    validatorActions: dict = {}

    if isinstance(args.output, io.TextIOWrapper):
        logger.warning('cannot validate stream')
        return

    validators : dict[str, t.Any] = { 
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

def customizeOne( args: dict ):

    context = Context.RendererContext( custom_controller=None,
        template_reference_path= args.reference_path)

    data_dictionnary: dict = None

    formatChoice : dict[str, t.Any] = { 
        'json' : lambda : jsonParser.ImportJsonFile(args.input),
        'yaml' : lambda : yamlParser.ImportYamlFile(args.input),
        'yml' : lambda : yamlParser.ImportYamlFile(args.input),
        'env' : lambda : envFileParser.ImportEnvFile(args.input)
    }

    if ( args.format in formatChoice.keys() ) :
        data_dictionnary = formatChoice[args.format]()
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

    template_name_length = len(args.template)

    context.render_template(
        template_path= args.template,
        output= args.template[0:template_name_length - 3],
        data=data_dictionnary )

    if args.output_validator is not None and len(args.output_validator) > 0:
        validateOutput(args)

def customizeMultiImplicitDir( args: dict ):
    if not os.path.isdir(args.template):
        raise('should be a directory')
    
    glob.glob(args.template)

def customizeMulti( args: dict, config_file_as_list: dict ):
    
    logger.info("config file mode")
    
    expandedDict: dict = {}

    for templateFileName, templateAttributes in config_file_as_list.items():
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
        config: dict = yamlParser.ImportYamlFile(args.config_file)
        customizeMulti(args, config)
    else:
        # if( os.path.isdir(args.template) )
        customizeOne(args)

    logger.info("script clean end")
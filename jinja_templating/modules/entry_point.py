import codecs
import copy
import glob
import io
import os
import pprint
import subprocess
import sys
import typing as t
from argparse import ArgumentParser, Namespace

import jinja_templating.modules.custom_logging as customLogging
import jinja_templating.modules.renderer_context as Context

from jinja_templating.models.customize_one_parameters import CustomizeOneParameters
import jinja_templating.modules.parser.env_file_parser as envFileParser
import jinja_templating.modules.parser.json_parser as jsonParser
import jinja_templating.modules.parser.yaml_parser as yamlParser

logger = customLogging.BuildCustomLogger("root")

parser = ArgumentParser(description='Argument parser')

def writeFile(output_file : codecs.StreamReaderWriter, data: str) -> None:
        if ( output_file.writable ) :
            output_file.write(data)

def openFile(file_name: str) -> codecs.StreamReaderWriter :
    with codecs.open(file_name, "azer", errors='strict') as file_descriptor:
        return file_descriptor

def validate_output( args: CustomizeOneParameters ):

    validator_actions: dict = {}

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
            validator_actions[validator] = validators[validator]
        else :
            raise ValueError(f'Unknown format : {validator} waiting for any of {validators.keys()}')

    logger.info("running validators on output %s ...", args.output)

    for validator_name, validate_action in validator_actions.items():
        logger.info("passing the %s validator ...", validator_name)
        validate_action()
        logger.info("validator passed successfully !")

def customize_one( args: CustomizeOneParameters ):

    context = Context.RendererContext( custom_controller=None,
        template_reference_path= args.reference_path)

    data_dictionnary: dict[str, t.Callable]
    
    format_choice : dict[str, t.Callable] = { 
        'json' : lambda : jsonParser.ImportJsonFile(args.input_data),
        'yaml' : lambda : yamlParser.ImportYamlFile(args.input_data),
        'yml' : lambda : yamlParser.ImportYamlFile(args.input_data),
        'env' : lambda : envFileParser.ImportEnvFile(args.input_data)
    }

    if ( args.format in format_choice.keys() ) :
        data_dictionnary = format_choice[args.format]()
    else :
        raise ValueError( f'Unknown format : {args.format} waiting for any of {format_choice.keys()}')

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

    if isinstance(args.output, io.TextIOWrapper):
        logger.warning('output is a stream, output validator will be ignored')
        context.render_template(
            template_path= args.template,
            output= args.output,
            data=data_dictionnary )
    else:
        context.render_template(
            template_path= args.template,
            output= args.template[0:template_name_length - 3],
            data=data_dictionnary )

    if args.output_validator is not None and len(args.output_validator) > 0:
        validate_output(args)

def customize_multi_implicit_dir( args: CustomizeOneParameters ):
    """Customize multiple templates using implicit directory discovery."""
    if not os.path.isdir(args.template):
        raise ValueError('should be a directory')
    
    glob.glob(args.template)

def customize_multi( args: CustomizeOneParameters, config_file_as_list: dict ):
    
    logger.info("config file mode")
    
    expanded_dict: dict = {}

    for template_file_name, template_attributes in config_file_as_list.items():
        if 'expandGlobInTemplateName' in template_attributes:
            logger.info("expanding expression '%s' ...", template_file_name)
            for expanded_template_file_name in glob.glob(template_file_name):
                logger.info("file mathing found '%s' to process ...", expanded_template_file_name)
                expanded_dict[expanded_template_file_name] = template_attributes.copy()
                length = len(expanded_template_file_name)
                expanded_dict[expanded_template_file_name]['outputFile'] = expanded_template_file_name[0:length - 3]
        else:
            expanded_dict[template_file_name] = template_attributes

    template_number: int = 0
    for template_file_name, template_attributes in expanded_dict.items():
        template_args = copy.deepcopy(args)
        logger.info("processing template file '%s' ...", template_file_name)
        template_args.template = template_file_name
        template_args.format = template_attributes['contextFormat']
        template_args.output = template_attributes['outputFile']

        if 'outputValidator' in template_attributes:
            template_args.output_validator = template_attributes['outputValidator']
            ## TODO verifier la diff str os.stdout ...
            if template_args.output is None:
                parser.error("cannot validate if no output file set")
        else:
            logger.info("no output validator for template '%s'", template_file_name)
        #TODO manage override

        if 'templatingContext' in template_attributes:
           template_args.input_data = template_attributes['templatingContext']
        template_number+=1
        customize_one(template_args)

    logger.info("%d templates processed", template_number)


def rationalize_raw_args(raw_args: Namespace) -> CustomizeOneParameters:
    
    if not raw_args.config_file is None :
        if raw_args.format is not None \
            or raw_args.output is not None \
            or raw_args.template is not None :
                parser.error("-c exclude -f, -o and -t")
    else :
        if raw_args.template is None:
            parser.error("-t is mandatory (when not using -c)")
        if raw_args.format is None:
            raw_args.format = 'env'
        if raw_args.input is None:
            raw_args.input = sys.stdin
        if raw_args.output is None:
            raw_args.output = sys.stdout
            if not raw_args.output_validator is None:
                parser.error("cannot validate if no output file set")

    rp_reference_path: str
    rp_template_dir: str = os.path.dirname(os.path.realpath(raw_args.template))
    template_file_name: str = os.path.basename(raw_args.template)

    logger.info('template real path is: %s', os.path.join(rp_template_dir, template_file_name))

    if raw_args.reference_path is not None:
        rp_reference_path = os.path.realpath(raw_args.reference_path)
        if not os.path.commonpath([rp_reference_path, rp_template_dir]):
            parser.error(f"reference path '{rp_reference_path}' should be a parent of template directory '{rp_template_dir}' (jinja2 constraint)")
    else:
        rp_reference_path = rp_template_dir
        
    rationalized_arguments: CustomizeOneParameters = CustomizeOneParameters(
        reference_path = rp_reference_path,
        input_data= os.path.realpath(raw_args.input) \
                if isinstance(raw_args.input, str) \
                else raw_args.input,
        output= os.path.realpath(raw_args.output) \
            if isinstance(raw_args.output, str) \
            else raw_args.output,
        template= template_file_name,
        input_format= raw_args.format,
        )
    
    return rationalized_arguments


def validate_args_and_run(args: CustomizeOneParameters):

    logger.info("program beginning ...")
    logger.info("reference path is '%s'", args.reference_path)

    os.chdir(args.reference_path)

    pprint.PrettyPrinter(depth=6)
    logger.info(pprint.pformat( args ))

    if not args.config_file is None:
        logger.info("loading config file '%s' ...", args.config_file)
        # config: Dict = jsonParser.ImportJsonFile(args.config_file)
        config = yamlParser.ImportYamlFile(args.config_file)
        customize_multi(args, config)
    else:
        # if( os.path.isdir(args.template) )
        customize_one(args)

    logger.info("script clean end")


def main():

    parser.add_argument('-c', '--config-file', required=False,
        default= None)

    parser.add_argument('-dr', '--dry-run', default = False, required=False, action='store_true' )
    
    parser.add_argument('-i', '--input', required=False, help= 'must be relative to current dir, default is stdin')
    parser.add_argument('-f', '--format', required=False, help='json | yaml | env')
    parser.add_argument('-o', '--output', required=False)
    parser.add_argument('-t', '--template', required=False)
    parser.add_argument('-r', '--reference-path', required=False, help= 'reference path for -i and -o, default is stdout')
    parser.add_argument('-v', '--output-validator', 
        action='append', required=False)

    raw_args=parser.parse_args()   
    
    args = rationalize_raw_args(raw_args)
    validate_args_and_run(args)

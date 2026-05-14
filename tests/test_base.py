import pprint
import logging

import os

from pytest import fixture

import jinja_templating.modules.entry_point as EntryPoint

from jinja_templating.models.customize_one_parameters import CustomizeOneParameters
from jinja_templating.modules.parser.env_file_parser import ImportEnvFile
from jinja_templating.modules.custom_logging import BuildCustomLogger


@fixture(name="logger")
def fix0() -> logging.Logger :
    return BuildCustomLogger("tests")

def test_EnvFileParser(logger: logging.Logger):
    result = ImportEnvFile( "./tests/resources/envFileTest")  
    pp = pprint.PrettyPrinter(depth=6)
    logger.debug(pp.pformat(result) )



def test_render_in_template():
    t: CustomizeOneParameters = CustomizeOneParameters(
        reference_path = os.path.realpath('./tests/resources/'),
        input_data= os.path.realpath("./tests/resources/envFileTest"),
        template= 'renderInRender.j2',
        input_format= 'env' )

    EntryPoint.validate_args_and_run(t)
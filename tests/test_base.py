import pprint
import logging

import os

from pytest import fixture


from jinja_templating.modules.entry_point import validateArgsAndRun

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



def test_render_in_template(logger: logging.Logger):
    t: CustomizeOneParameters = CustomizeOneParameters(
        reference_path = os.path.realpath('./tests/resources'),
        input= os.path.realpath("./tests/resources/envFileTest"),
        template= 'renderInRender.j2',
        input_format= 'env' )

    validateArgsAndRun(t)
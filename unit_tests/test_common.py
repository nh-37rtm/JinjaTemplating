import unittest
import sys
import os

from MyObject import MyObject
import typing
sys.path.append(os.path.dirname(__file__) + '/../jinja_templating')

import modules.parser.env_file_parser as envFileParser
import modules.entry_point as ep
from models.customize_one_parameters import CustomizeOneParameters
import pprint

class Test(unittest.TestCase):

    def test_EnvFileParser(self):
        result = envFileParser.ImportEnvFile( "./unit_tests/resources/envFileTest")
        pp = pprint.PrettyPrinter(depth=6)
        print(pp.pformat(result))


    def test_render_in_template(self):
        t: CustomizeOneParameters = CustomizeOneParameters(
            reference_path = os.path.realpath('.'),
            input= os.path.realpath("./unit_tests/resources/envFileTest"),
            template= './unit_tests/resources/renderInRender.j2',
            input_format= 'env' )

        ep.validateArgsAndRun(t)

if __name__ == '__main__':
    unittest.main()
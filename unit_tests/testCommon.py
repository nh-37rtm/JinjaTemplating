import unittest
import sys
import os

from MyObject import MyObject
import typing
sys.path.append(os.path.dirname(__file__) + '/..')

import Modules.Parser.EnvFileParser as envFileParser
import Modules.EntryPoint as ep
from Models.CustomizeOneParameters import CustomizeOneParameters
import pprint

class Test(unittest.TestCase):

    def test_EnvFileParser(self):
        result = envFileParser.ImportEnvFile( "./jinja-templating/Tests/Resources/envFileTest")
        pp = pprint.PrettyPrinter(depth=6)
        print(pp.pformat(result))


    def test_render_in_template(self):
        t: CustomizeOneParameters = CustomizeOneParameters(
            reference_path = os.path.realpath('./jinja-templating/Tests/Resources'),
            input= os.path.realpath("./jinja-templating/Tests/Resources/envFileTest"),
            template= 'renderInRender.j2',
            input_format= 'env' )

        ep.validateArgsAndRun(t)

if __name__ == '__main__':
    unittest.main()
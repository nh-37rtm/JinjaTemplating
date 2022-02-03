import unittest
import Modules.Parser.EnvFileParser as envFileParser
import pprint


class Test(unittest.TestCase):

    def test_EnvFileParser(self):
        result = envFileParser.ImportEnvFile( "./Tests/Resources/envFileTest")
        pp = pprint.PrettyPrinter(depth=6)
        print(pp.pformat(result))

if __name__ == '__main__':
    unittest.main()
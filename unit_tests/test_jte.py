

import os
import sys
import unittest

from models.customize_one_parameters import CustomizeOneParameters

import modules.entry_point as ep

sys.path.append(os.path.dirname(__file__) + '/../jinja_templating')



class Test(unittest.TestCase):

    # def test_jte(self):
        
    #     os.environ['ARGV'] = '--reference-path . --input ./unit_tests/resources/envFileTest -t ./unit_tests/resources/openvpn/openvpn.conf.j2 --input-format env'
    #     EntryPoint.main()
        

    def test_render_in_template(self):
        t: CustomizeOneParameters = CustomizeOneParameters(
            reference_path = os.path.realpath('.'),
            input_text= os.path.realpath("./unit_tests/resources/envFileTest"),
            template= './unit_tests/resources/openvpn/openvpn.conf.j2',
            input_format= 'env' )

        ep.validate_args_and_run(t)

if __name__ == '__main__':
    unittest.main()
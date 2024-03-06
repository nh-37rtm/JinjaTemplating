from setuptools import setup

setup(
   name="jinja-templating",
   requires=[ "jinja2", "pyyaml"],
   version='0.1.0',
   description='templating engine using jinja2',
   extras_require = {
       'dev': ['pylint', 'pytest'],
   },
   scripts= [ 'jte' ]
)
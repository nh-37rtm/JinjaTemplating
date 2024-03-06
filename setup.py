from setuptools import setup

setup(
   name="jinja-templating",
   requires=[ "jinja2", "pyyaml"],
#    extras_require = {
#        'dev': ['pylint', 'pytest'],
#    },
    packages= ['.'],
#  package_dir= { 'src': "jinja_templating" },
#    install_requires=[
#          'Jinja2>=3',
#          'PyYAML'
#      ]
)
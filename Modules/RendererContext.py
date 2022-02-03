from jinja2 import FileSystemLoader, Template, Environment
import os
import logging
import sys
import codecs

from typing import List

class RendererContext:

    logger_ = logging.getLogger("root")
    templateBaseDir_ : str = None

    # default constructor
    def __init__(self, customControler):
        self.jinjaTemplateLoader_ = FileSystemLoader(os.getcwd())
        self.jinjaTemplateEnv_ = Environment(loader=self.jinjaTemplateLoader_)
        self.controler = customControler

    def renderTemplate(
        self, 
        templatePath: str, 
        data: object, 
        output: codecs.StreamReaderWriter = sys.stdout,
        dryRunSwitch: bool = False) -> str:
            
            # TODO implement infinite loops detection
            
            self.templateBaseDir_ =  os.path.dirname(templatePath)
            self.logger_.info(f'rendering {templatePath} ...')

            try :
                template = self.jinjaTemplateEnv_.get_template(templatePath)
                if ( not dryRunSwitch ):
                    template.stream(data, context= self, os=os).dump(output)
            except Exception as e:
                self.logger_.error(f'ko : {e}')
            else :
                self.logger_.info(f'{templatePath} rendered')
            finally :
                if type(output) == 'codecs.StreamReaderWriter' :
                    output.close()

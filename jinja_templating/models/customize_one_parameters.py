import os
import sys

class CustomizeOneParameters():

    reference_path: str
    format: str
    input: str
    template: str
    output_validator: str

    def __init__(self, reference_path, input: str, input_format: str, template: str):
        self.reference_path = reference_path
        self.format = input_format
        self.output_validator = [ "yaml" ]
        self.input = input
        self.output = sys.stdout
        self.template = template
        self.config_file = None
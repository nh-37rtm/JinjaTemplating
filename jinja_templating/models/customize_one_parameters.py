import io
from typing import Any, AnyStr, Union


class CustomizeOneParameters():

    reference_path: str
    format: str
    input_data: Union[str, io.TextIOWrapper]
    output: Union[str, io.TextIOWrapper]
    template: str
    output_validator: list[str]

    def __init__( 
                 self, reference_path, input_data: Union[str, io.TextIOWrapper], input_format: str, 
                 output: Union[str, io.TextIOWrapper], template: str):
        self.reference_path = reference_path
        self.format = input_format
        self.output_validator = [ "yaml" ]
        self.input_data = input_data
        self.output = output
        self.template = template
        self.config_file = None
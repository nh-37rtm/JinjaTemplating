from typing import Dict, Union, TextIO


def readFile(file: Union[str, TextIO]) -> Dict:
    return dict(tuple(line.replace('\n', '').split('=')) for line
                        in file.readlines() 
                            if not line.startswith('#') 
                            and not line.isspace())

def ImportEnvFile( filePath: Union[str, TextIO] ) -> Dict:

    if isinstance( filePath, str ):
        with open(filePath, 'r', encoding='utf-8') as file:
            return readFile(file)
    else:
        return readFile(filePath)


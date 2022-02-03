from typing import Dict

def ImportEnvFile( filePath: str ) -> Dict:
    with open(filePath, 'r', encoding='utf-8') as file:
        return dict(tuple(line.replace('\n', '').split('=')) for line
                in file.readlines() 
                    if not line.startswith('#') 
                    and not line.isspace())


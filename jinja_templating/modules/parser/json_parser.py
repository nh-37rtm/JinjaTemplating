import json

def ImportJsonFile( filePath: str ):
    with open(filePath, 'r', encoding='utf-8') as file:
        result = json.load(file)
        return result
import yaml

def ImportYamlFile(filePath : str):
    with open(filePath, 'r', encoding='utf-8') as file:
        result = yaml.load(file)
        return result



import yaml

def ImportYamlFile(filePath : str):
    with open(filePath, 'r', encoding='utf-8') as file:
        result = yaml.safe_load(file)
        return result



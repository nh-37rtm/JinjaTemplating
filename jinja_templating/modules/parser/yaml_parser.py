import yaml

def ImportYamlFile(filePath : str, multipleDocsAllowed : bool = False):
    with open(filePath, 'r', encoding='utf-8') as file:
        result = None
        if ( multipleDocsAllowed ):
            result = list(yaml.safe_load_all(file))
            if result is None:
                raise ValueError("no documents found in the generated yaml file !")
        else:
            result = yaml.safe_load(file)
        return result



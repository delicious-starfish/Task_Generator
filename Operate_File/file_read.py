import json

def read_json(json_path):
    """

    :param json_path: a relative path to find the config.json
    :return: a dictionary about the json's contents
    """

    with open(json_path,"r",encoding="utf-8") as file:
        dict = json.load(file)
        return dict
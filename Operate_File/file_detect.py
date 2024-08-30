import os

def detected_json_upload(input_folder_path):
    """

    :param
    input_folder_path: an absolute path to tell where the input_folder is

    :return: a boolean that tells whether a json is uploaded
    """
    platforms = ['bilibili', 'ximalaya', 'youtube']

    for platform in platforms:
        json_folder_path = os.path.join(input_folder_path, platform)
        if len(os.listdir(json_folder_path)) > 0:
            return True
    return False

def detectPlatform_getTaskName(input_folder_path):
    """
    detect the platform through which folder the json file is put
    and get the task name through the name of json file

    :param input_folder_path:an absolute path to tell where the input_folder is

    :return: Str: the type of platform, Str: the name of the task
    """
    platforms = ['bilibili','ximalaya','youtube']

    for platform in platforms:
        json_folder_path = os.path.join(input_folder_path, platform)
        if len(os.listdir(json_folder_path)) > 0:
            task_name = os.listdir(json_folder_path)[0].split(".")[0]
            return platform,task_name
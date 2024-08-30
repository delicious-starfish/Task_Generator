import os
import json

from Operate_File.file_read import read_json
from Operate_File.file_build import build_dir

cfg = read_json('config.json')

def move_previous_audio():
    previous_task_file_name = find_previous_task() #找到最近的task文件，用于指明目录下哪些需要移走,返回task的文件名
    if previous_task_file_name == 'Not Found':
        return
    processed_folder_dict = extract_folder_from_task(previous_task_file_name) #一个字典，key为文件夹名,value为平台名
    prepare_destination_folders()
    for taskname in processed_folder_dict.keys():
        platform = processed_folder_dict[taskname]
        move_task_folder(platform,taskname)

def generate_new_task(task_file_name):
    audio_list = get_audio_from('bilibili')
    with open(cfg['task_output_folder'] + task_file_name,'w',encoding = 'utf-8') as f:
        for audio in audio_list:
            f.write(json.dumps(audio,ensure_ascii=False) + '\n')

    audio_list = get_audio_from('youtube')
    with open(cfg['task_output_folder'] + task_file_name,'a',encoding = 'utf-8') as f:
        for audio in audio_list:
            f.write(json.dumps(audio,ensure_ascii=False) + '\n')

    audio_list = get_audio_from('archive')
    with open(cfg['task_output_folder'] + task_file_name,'a',encoding = 'utf-8') as f:
        for audio in audio_list:
            f.write(json.dumps(audio,ensure_ascii=False) + '\n')

def prepare_destination_folders():
    platforms = ['bilibili','youtube','archive']
    for platform in platforms:
        path = os.path.join(cfg['move_destination'],platform)
        build_dir(path)
        
        

def extract_folder_from_task(task_file_name):
    with open(os.path.join(cfg['task_output_folder'], task_file_name),'r') as f:
        audio_list = f.readlines()

    task_dict = {}
    for audio in audio_list:
        audio = audio.split('/')
        platform = audio[-4]
        taskname = audio[-3]
        
        if not (taskname in task_dict.keys() and task_dict[taskname] == platform):
            # 不同平台可能有相同的任务名
            task_dict[taskname] = platform

    return task_dict
    

def find_previous_task():
    if len(os.listdir(cfg['task_output_folder'])) == 0:
        return "Not Found"
    
    latest_time = 0
    latest_task_name = ""
    for file in os.listdir(cfg['task_output_folder']):
        file_create_time = os.stat(os.path.join(cfg['task_output_folder'], file)).st_ctime
        if latest_time < file_create_time:
            latest_time = file_create_time
            latest_task_name = file
    return latest_task_name

def move_task_folder(platform,taskname):
    path = get_task_folder_path(platform,taskname)
    dst = os.path.join(cfg["task_destination"],platform,taskname)

    os.rename(path,dst)

def get_task_folder_path(platform,taskname):
    if platform == 'bilibili':
        return os.path.join(cfg["bili_folder"],platform,taskname)
    else:
        return os.path.join(cfg['dl_file_folder'],platform,taskname)
    
def get_audio_from(platform):
    if platform == 'bilibili':
        base_directory = cfg['bili_folder']
    else:
        base_directory = cfg['dl_file_folder']
    
    audio_list = []
    for audio_folder in os.listdir(base_directory):
        full_path = os.path.join(base_directory, platform, audio_folder, 'audio')
        for audio in os.listdir(full_path):
            path = os.path.join(full_path,audio)
            audio_list.append(path)
    
    return audio_list
        
if __name__ == '__main__':

    move_previous_audio()

    new_id = find_previous_task()
    if new_id == 'Not Found':
        new_id = '1'
    else:
        new_id = new_id.split('.')[0]
        new_id = str(int(new_id) + 1)
    
    new_task_name = new_id + '.task'
    generate_new_task(new_task_name)
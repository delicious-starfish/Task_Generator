import os

from Operate_File.file_read import read_json

cfg = read_json('config.json')

def move_previous_audio():
    previous_task_file_name = find_previous_task() #找到最近的task文件，用于指明目录下哪些需要移走,返回task的文件名
    if previous_task_file_name == 'Not Found':
        return
    processed_folder_dict_list = extract_folder_from_task(previous_task_file_name) #一个字典，key为文件夹名,value为平台名

def extract_folder_from_task(task_file_name):
    with open(os.path.join(cfg['task_output_folder'], task_file_name),'r') as f:
        audio_list = f.readlines()
    for i in range(20):
        print(audio_list[i])
    return []
    

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

if __name__ == '__main__':

    move_previous_audio()


    # generate_new_task()
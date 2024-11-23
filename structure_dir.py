import json
import os

structure_path = 'format.json'

def expand_json(data: dict, path: str = ""):
    path_list = []
    for key, val in data.items():
        current_path = f"{path}{key}/"
        if isinstance(val, dict):
            path_list.extend(expand_json(val, current_path))
        else:
            print(f"{current_path}\b")  
            path_list.append(current_path)  
    path_list.append(path)
    return path_list

with open(structure_path, 'r') as f:
    data = json.load(f)

list_of_paths = expand_json(data)


for path in list_of_paths:
    os.makedirs(f'GATE-yearwise/{path}', exist_ok=True)

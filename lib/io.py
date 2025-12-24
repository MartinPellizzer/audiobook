import os
import csv
import json

#######################
# ;folder
#######################

def folder_create(folderpath):
    chunks = folderpath.split('/')
    chunk_curr = ''
    for chunk in chunks:
        chunk_curr += chunk + '/'
        if not os.path.exists(chunk_curr):
            os.makedirs(chunk_curr)

def folder_create_from_filepath(filepath):
    chunks = filepath.split('/')
    chunk_curr = ''
    for chunk in chunks[:-1]:
        chunk_curr += chunk + '/'
        if not os.path.exists(chunk_curr):
            os.makedirs(chunk_curr)

def folders_recursive_gen(folderpath):
    folderpath_cur = ''
    for chunk in folderpath.split('/'):
        folderpath_cur += f'{chunk}/'
        try: os.mkdir(f'{folderpath_cur}')
        except: pass

#######################
# ;file
#######################

def file_read(path):
    with open(path) as f:
        content = f.read()
    return content

def file_append(path, text):
    with open(path, 'a') as f:
        f.write(text)

def file_write(path, text):
    with open(path, 'w') as f:
        f.write(text)

def csv_read(filepath, delimiter='\\'):
    rows = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if row != []:
                rows.append(row)
    return rows

#######################
# ;csv
#######################
def csv_to_dict(filepath, delimiter='\\'):
    rows = csv_read(filepath, delimiter=delimiter)
    row_header = rows[0]
    rows_body = rows[1:]
    obj_list = []
    for row in rows_body:
        obj = {}
        for element_i, e in enumerate(row):
            obj[row_header[element_i]] = e.strip()
        obj_list.append(obj)
    return obj_list

#######################
# ;json
#######################
def json_create(filepath):
    if not os.path.exists(filepath):
        json_write(filepath, {})

def json_read_old(filepath, create=False):
    if create == True: json_create(filepath)
    with open(filepath) as f:
        data = json.load(f)
    return data

def json_read(filepath, create=False):
    if create:
        folder_create_from_filepath(filepath)
        if not os.path.exists(filepath):
            file_append(filepath, '')
        if file_read(filepath).strip() == '':
            file_append(filepath, '{}')
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def json_write(filepath, data):
    j = json.dumps(data, indent=4)
    with open(filepath, 'w') as f:
        print(j, file=f)


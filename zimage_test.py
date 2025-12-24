import os

from lib import zimage

hub_folderpath = f'psychology'
script_filepath = f'{hub_folderpath}/script.txt'

with open(script_filepath) as f: script_content = f.read()
if script_content.strip() == '': 
    print('ERR: No content in final.txt')
    quit()
content = script_content.split('!!!')[0]

image_lines = []
text_lines = []
for line in content.split('\n'):
    line = line.strip()
    if line == '': continue
    if '---' in line: continue
    if '###' in line: continue
    if line.startswith('**'): continue
    line = line.replace('*', '')
    if line[0] == '[':
        line = line.replace('[', '').replace(']', '')
        line = line.lower()
        line = line.replace('lemon balm', 'melissa officinalis')
        image_lines.append(line)
    else:
        text_lines.append(line)

while True:
    # for filename in os.listdir(f'{hub_folderpath}/tmp/images'):
        # os.remove(f'{hub_folderpath}/tmp/images/{filename}')
    i = 0
    for line in image_lines[:3]:
        line = line.strip().replace('.', '')
        i_str = ''
        if i >= 1000: i_str = f'{i}'
        elif i >= 100: i_str = f'0{i}'
        elif i >= 10: i_str = f'00{i}'
        else: i_str = f'000{i}'
        i += 1
        output_filepath = f'{hub_folderpath}/test-images/img-{i_str}.jpg'
        with open(f'{hub_folderpath}/prompt.txt') as f: prompt = f.read()
        prompt = prompt.replace('[line]', line)
        print(prompt)
        print()
        image = zimage.image_create(output_filepath=output_filepath, prompt=prompt, width=1024, height=1024, seed=-1)
    input('regenerate >> ')


import os

import tkinter as tk
from PIL import Image, ImageTk

from lib import g
from lib import media

final_filepath = f'{g.base_folderpath}/tmp/texts/final.txt'

def image_resize_ratio(image):
    target_width, target_height = 1280, 720
    src_width, src_height = 1216, 832
    scale = max(target_width / src_width, target_height / src_height)
    new_width = int(src_width * scale)
    new_height = int(src_height * scale)
    image = image.resize((new_width, new_height), Image.LANCZOS)
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    image = image.crop((left, top, right, bottom))
    return image

def image_lines_load():
    with open(final_filepath) as f: final_content = f.read()
    content = final_content.split('!!!')[0]
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
    return image_lines

image_lines = image_lines_load()

def show_image(index):
    global img_label, tk_img, current_index
    current_index = index % len(images)
    img = Image.open(images[current_index])
    img = img.resize((window_w//2, window_h//2), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    img_label.config(image=tk_img)
    img_label.image = tk_img
    root.title(f'Image Viewer - {images[current_index]}')

def prev_image(event=None):
    global current_index
    current_index -= 1
    show_image(current_index)
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, image_lines[current_index])

def next_image(event=None):
    global current_index
    current_index += 1
    show_image(current_index)
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, image_lines[current_index])

def regen_image(event=None):
    # line = image_lines[current_index]
    line = text_area.get('1.0', tk.END).strip()
    image_prompt = f'{line}, illustrative, botanical, figurative, dry brush, splatter effect, salt texture, paper texture, pastel tones'
    print(image_prompt)
    image = media.image_gen(image_prompt, 1216, 832, steps=20, cfg=6.0)
    image = image_resize_ratio(image)
    i = current_index
    i_str = ''
    if i >= 1000: i_str = f'{i}'
    elif i >= 100: i_str = f'0{i}'
    elif i >= 10: i_str = f'00{i}'
    else: i_str = f'000{i}'
    image.save(f'{images_folderpath}/img-{i_str}.jpg')
    show_image(current_index)
    return "break"

def disable_enter(event=None):
    return 'break'

root = tk.Tk()
root.title('test')
window_w, window_h = 1280, 720
# root.geometry('1920x1080')
root.geometry(f'{window_w}x{window_h}')

images = []

images_folderpath = f'{g.base_folderpath}/tmp/images'
for filename in sorted(os.listdir(images_folderpath)):
    image_filename = f'{images_folderpath}/{filename}'
    images.append(image_filename)

current_index = 0

tk_img = None
img_label = tk.Label(root)
img_label.pack()

text_area = tk.Text(root, height=5, width=100)
text_area.pack(pady=10)
text_area.delete('1.0', tk.END)
text_area.insert(tk.END, image_lines[current_index])

prev_btn = tk.Button(root, text='Prev', command=prev_image, width=100)
prev_btn.pack(side='left', padx=5)

next_btn = tk.Button(root, text='Next', command=next_image, width=100)
next_btn.pack(side='right', padx=5)

root.bind('<Left>', prev_image)
root.bind('<Right>', next_image)
root.bind('<Control-Key-Return>', regen_image)
root.bind('<Control-Enter>', regen_image)

root.bind('<Return>', disable_enter)

show_image(current_index)

root.mainloop()

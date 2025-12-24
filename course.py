import os
import shutil

from kokoro import KPipeline
import soundfile as sf 

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import polish

slide_w = 1280
slide_h = 720
###
course_slug = 'tincture-making'
course_folderpath = f'/home/ubuntu/vault/terrawhisper/database/shop/courses/{course_slug}'
###
src_folderpath = f'{course_folderpath}/src'
src_modules_foldernames = sorted(os.listdir(src_folderpath))
###
tmp_folderpath = f'{course_folderpath}/tmp'
tmp_slides_folderpath = f'{course_folderpath}/tmp/slides'
tmp_audio_clips_folderpath = f'{tmp_folderpath}/clips'
tmp_video_clips_folderpath = f'{tmp_folderpath}/video-clips'
###
dst_folderpath = f'{course_folderpath}/dst'
dst_video_clips_folderpath = f'{dst_folderpath}/video-clips'

def slide_footer_draw(draw, color):
    line = f'{course_name} | Copyright TerraWhisper.com'
    font_size = 16
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((32, slide_h - font_size - 16), line, color, font=font)
    ###
    line = f'Module {module_i+1} - Lesson {lesson_i+1}'
    font_size = 16
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w - line_w - 32, slide_h - font_size - 16), line, color, font=font)
    draw.rectangle(((0, slide_h - font_size - 16 - 16), (slide_w, slide_h - font_size - 16 - 16)), fill=color)

def slide_intro_gen(style, slide_num=-1, course_name=''):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = course_name
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, slide_h//2 - line_h*2), line, color, font=font)
    ### lesson num
    line = f'Module {module_i+1} - Lesson {lesson_i+1}'
    font_size = 64
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, slide_h//2 - line_h//2), line, color, font=font)
    ### lesson title
    lesson_name = lesson_filename.replace('_', ' ')
    if lesson_name[0].isdigit: lesson_name = ' '.join(lesson_name.split(' ')[1:])
    line = f'{lesson_name}'
    font_size = 64
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, slide_h//2 + line_h), line, color, font=font)
    ### slide footer
    slide_footer_draw(draw, color)
    ### save
    i = slide_num
    i_str = ''
    if i >= 10000: i_str = f'{i}'
    elif i >= 1000: i_str = f'0{i}'
    elif i >= 100: i_str = f'00{i}'
    elif i >= 10: i_str = f'000{i}'
    else: i_str = f'0000{i}'
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')

def slide_general(style, slide_num=-1):
    ### style
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    ### get content from script
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    title = ''
    for line in lines:
        if line.startswith('[step_2_title] '): 
            line = line.replace('[step_2_title] ', '').strip()
            title = line
        elif line.startswith('[step_2_content] '): 
            line = line.replace('[step_2_content] ', '').strip()
            content = line
    ### img
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = title
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, 80), line, color, font=font)
    ### content
    draw_slide_content(content, draw, color)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    if slide_num == -1:
        img.save(f'{tmp_slides_folderpath}/00006.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00006.png')
    else:
        i = slide_num
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        img.save(f'{tmp_slides_folderpath}/{i_str}.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')


def slide_why_gen(style):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### what script
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    text = ''
    for line in lines:
        if line.startswith('[what] '): 
            line = line.replace('[what] ', '')
            text = line
            break
    ### set font
    line = 'Why Matters?'
    font_size = 64
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, slide_h//2 - line_h//2), line, color, font=font)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    img.save(f'{tmp_slides_folderpath}/00001.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00001.png')

def slide_what_gen(style):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### what script
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    text = ''
    for line in lines:
        if line.startswith('[what] '): 
            line = line.replace('[what] ', '')
            text = line
            break
    ### set font
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    ### slide footer
    slide_footer_draw(draw, color)
    ### split lines
    print(text)
    lines = []
    line = ''
    for word in text.split(' '):
        _, _, line_w, line_h = font.getbbox(line)
        _, _, word_w, word_h = font.getbbox(word)
        if line_w + word_w < 800:
            line += f'{word} '
        else:
            lines.append(line.strip())
            line = f'{word} '
    if line.strip() != '':
        lines.append(line)
    y_cur = int(slide_h*0.5)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((slide_w//2 - line_w//2, y_cur), line, g.color_carbon_powder, font=font)
        y_cur += line_h * 1.2
    ###
    img.save(f'{tmp_slides_folderpath}/00002.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00002.png')

def slide_steps_1_gen(style):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = 'Let\'s break it down into 3 simple steps:'
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, 80), line, color, font=font)
    ### get steps
    steps = []
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    for line in lines:
        if line.startswith('Step '): steps.append(line)
    step_1_x = int(slide_w*0.20)
    step_2_x = int(slide_w*0.50)
    step_3_x = int(slide_w*0.80)
    ### step 1
    step = steps[0].replace('Step ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_1_x - line_w//2, int(slide_h*0.33)), step_num, color, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_1_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, color, font=font)
    ### step 2
    step = steps[1].replace('Step ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_2_x - line_w//2, int(slide_h*0.33)), step_num, g.color_carbon_ash, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_2_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, g.color_carbon_ash, font=font)
    ### step 3
    step = steps[2].replace('Step ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_3_x - line_w//2, int(slide_h*0.33)), step_num, g.color_carbon_ash, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_3_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, g.color_carbon_ash, font=font)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    img.save(f'{tmp_slides_folderpath}/00003.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00003.png')

def draw_slide_content(content, draw, color):
    ### content
    lines = [line.strip() for line in content.split('|')]
    ### get max line length
    max_length = 0
    for line in lines:
        if len(line) > max_length: max_length = len(line)
    ### set font size based on max length
    if max_length < 10:
        font_size = 128
        if len(lines) > 3:
            font_size = 64
    else:
        font_size = 64
    ### calc content height
    content_h = 0
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        content_h += font_size
    ### draw lines centered
    y_cur = slide_h//2 - content_h//2
    for line_i, line in enumerate(lines):
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((slide_w//2 - line_w//2, y_cur), line, color, font=font)
        y_cur += line_h

def slide_step_1_gen(style, slide_num=-1):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    ### get content from script
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    title = ''
    for line in lines:
        if line.startswith('[step_1_title] '): 
            line = line.replace('[step_1_title] ', '').strip()
            title = line
        elif line.startswith('[step_1_content] '): 
            line = line.replace('[step_1_content] ', '').strip()
            content = line
    ### img
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = title
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, 80), line, color, font=font)
    ### content
    draw_slide_content(content, draw, color)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    if slide_num == -1:
        img.save(f'{tmp_slides_folderpath}/00004.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00004.png')
    else:
        i = slide_num
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        img.save(f'{tmp_slides_folderpath}/{i_str}.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')

def content_to_lines(content, draw, color, font, p_w):
    lines = []
    line = ''
    for word in content.split():
        _, _, word_w, word_h = font.getbbox(word)
        _, _, line_w, line_h = font.getbbox(line)
        if line_w + word_w < p_w:
            line += f'{word} '
        else:
            lines.append(line.strip())
            line = f'{word} '
    if line.strip() != '':
        lines.append(line.strip())
    return lines

def slide_steps_2_gen(style):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = 'Let\'s break it down into 3 simple steps:'
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, 80), line, color, font=font)
    ### get steps
    steps = []
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    for line in lines:
        if line.startswith('Step '): steps.append(line)
    step_1_x = int(slide_w*0.20)
    step_2_x = int(slide_w*0.50)
    step_3_x = int(slide_w*0.80)
    ### step 1
    step = steps[0].replace('Step ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_1_x - line_w//2, int(slide_h*0.33)), step_num, g.color_carbon_ash, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_1_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, g.color_carbon_ash, font=font)
    ### step 2
    step = steps[1].replace('Step ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_2_x - line_w//2, int(slide_h*0.33)), step_num, g.color_linen, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_2_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, g.color_linen, font=font)
    ### step 3
    step = steps[2].replace('Step ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_3_x - line_w//2, int(slide_h*0.33)), step_num, g.color_carbon_ash, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_3_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, g.color_carbon_ash, font=font)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    img.save(f'{tmp_slides_folderpath}/00005.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00005.png')

def slide_step_2_gen(style, slide_num=-1):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    ### get content from script
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    title = ''
    for line in lines:
        if line.startswith('[step_2_title] '): 
            line = line.replace('[step_2_title] ', '').strip()
            title = line
        elif line.startswith('[step_2_content] '): 
            line = line.replace('[step_2_content] ', '').strip()
            content = line
    ### img
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = title
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, 80), line, color, font=font)
    ### content
    draw_slide_content(content, draw, color)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    if slide_num == -1:
        img.save(f'{tmp_slides_folderpath}/00006.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00006.png')
    else:
        i = slide_num
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        img.save(f'{tmp_slides_folderpath}/{i_str}.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')

def slide_steps_3_gen(style):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = 'Let\'s break it down into 3 simple steps:'
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, 80), line, color, font=font)
    ### get steps
    steps = []
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    for line in lines:
        if line.startswith('Step '): steps.append(line)
    step_1_x = int(slide_w*0.20)
    step_2_x = int(slide_w*0.50)
    step_3_x = int(slide_w*0.80)
    ### step 1
    step = steps[0].replace('Step ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_1_x - line_w//2, int(slide_h*0.33)), step_num, g.color_carbon_ash, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_1_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, g.color_carbon_ash, font=font)
    ### step 2
    step = steps[1].replace('Step ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_2_x - line_w//2, int(slide_h*0.33)), step_num, g.color_carbon_ash, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_2_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, g.color_carbon_ash, font=font)
    ### step 3
    step = steps[2].replace('Step ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_3_x - line_w//2, int(slide_h*0.33)), step_num, g.color_linen, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_3_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, g.color_linen, font=font)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    img.save(f'{tmp_slides_folderpath}/00007.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00007.png')

def slide_step_3_gen(style, slide_num=-1):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    ### get content from script
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    title = ''
    for line in lines:
        if line.startswith('[step_3_title] '): 
            line = line.replace('[step_3_title] ', '').strip()
            title = line
        elif line.startswith('[step_3_content] '): 
            line = line.replace('[step_3_content] ', '').strip()
            content = line
    ### img
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = title
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, 80), line, color, font=font)
    ### content
    draw_slide_content(content, draw, color)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    if slide_num == -1:
        img.save(f'{tmp_slides_folderpath}/00008.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00008.png')
    else:
        i = slide_num
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        img.save(f'{tmp_slides_folderpath}/{i_str}.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')


def slide_recap_gen(style, slide_num=-1):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    ### get section
    with open(script_filepath) as f: script = f.read()
    scripts_split = [x.strip() for x in script.split('---')]
    script = scripts_split[slide_num]
    print(script)
    lines = []
    for line in script.split('\n'):
        line = line.strip()
        if line == '': continue
        if line[0] == '*':
            lines.append(line)
    ### img
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = 'Recap'
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, 50), line, color, font=font)
    ### lines
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    y_cur = 50 + 128 + 80
    print(lines)
    for line in lines:
        line = line.replace('*', '').strip()
        line = line.replace('#', '').strip()
        line = f'* {line}'
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((100, y_cur), line, color, font=font)
        y_cur += line_h * 1.5
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    if slide_num == -1:
        img.save(f'{tmp_slides_folderpath}/00009.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00009.png')
    else:
        i = slide_num
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        img.save(f'{tmp_slides_folderpath}/{i_str}.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')


def slide_action_gen(style, slide_num=-1):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### set font
    line = 'Now It\'s Your Turn!'
    font_size = 64
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, slide_h//2 - line_h//2), line, color, font=font)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    if slide_num == -1:
        img.save(f'{tmp_slides_folderpath}/00010.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00010.png')
    else:
        i = slide_num
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        img.save(f'{tmp_slides_folderpath}/{i_str}.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')


def slide_next_lesson_gen(style, slide_num=-1):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### set font
    line = 'In The Next Lesson...'
    font_size = 64
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, slide_h//2 - line_h//2), line, color, font=font)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    if slide_num == -1:
        img.save(f'{tmp_slides_folderpath}/00011.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00011.png')
    else:
        i = slide_num
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        img.save(f'{tmp_slides_folderpath}/{i_str}.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')


def slides_gen():
    color = g.color_linen
    bg_color = g.color_carbon_powder
    ### clear
    try: os.mkdir(tmp_slides_folderpath)
    except: pass
    try: os.mkdir(f'{tmp_slides_folderpath}/{src_module_foldername}')
    except: pass
    try: os.mkdir(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}')
    except: pass
    ### placeholder slides
    with open(script_filepath) as f: script = f.read()
    scripts_split = [x.strip() for x in script.split('---')]
    scripts_num = len(scripts_split)
    for i in range(scripts_num):
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
        img.save(f'{tmp_slides_folderpath}/{i_str}.png')
    ### copy src slides
    for src_slide_filepath in src_slides_filepaths:
        src_slide_filename = src_slide_filepath.split('/')[-1]
        tmp_slide_filepath = f'{tmp_slides_folderpath}/{src_slide_filename}'
        shutil.copy2(src_slide_filepath, tmp_slide_filepath)
    ### gen auto slides
    slide_num = 0
    slide_intro_gen(style='default', slide_num=slide_num)
    slide_num += 1
    # slide_why_gen(style='invert')
    # slide_what_gen(style='default')
    # slide_steps_1_gen(style='invert')
    slide_step_1_gen(style='default', slide_num=slide_num)
    slide_num += 1
    # slide_steps_2_gen(style='invert')
    slide_step_2_gen(style='default', slide_num=slide_num)
    slide_num += 1
    # slide_steps_3_gen(style='invert')
    slide_step_3_gen(style='default', slide_num=slide_num)
    slide_num += 1
    slide_recap_gen(style='invert', slide_num=slide_num)
    slide_num += 1
    slide_action_gen(style='default', slide_num=slide_num)
    slide_num += 1
    slide_next_lesson_gen(style='invert', slide_num=slide_num)
    slide_num += 1
    # quit()

def slides_base_general(section_i, section):
    section = section.replace('*', '').strip()
    section = section.replace('#', '').strip()
    lines = [x.strip() for x in section.split('\n') if x.strip() != '']
    heading = ''
    content = ''
    for line in lines:
        if line.startswith('[heading] '): 
            line = line.replace('[heading] ', '').strip()
            heading = line
        elif line.startswith('[content] '): 
            line = line.replace('[content] ', '').strip()
            content = line
    print(f'HEADING: {heading}')
    print(f'CONTENT: {content}')
    ### img
    color = g.color_linen
    bg_color = g.color_carbon_powder
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### heading
    line = heading
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, 80), line, color, font=font)
    ### content
    draw_slide_content(content, draw, color)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
    i = section_i
    i_str = ''
    if i >= 10000: i_str = f'{i}'
    elif i >= 1000: i_str = f'0{i}'
    elif i >= 100: i_str = f'00{i}'
    elif i >= 10: i_str = f'000{i}'
    else: i_str = f'0000{i}'
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')

def create_slides_general(regen=False):
    color = g.color_linen
    bg_color = g.color_carbon_powder
    ### clean
    if regen: 
        try: shutil.rmtree(f'{tmp_slides_folderpath}')
        except: pass
    try: os.mkdir(f'{tmp_slides_folderpath}')
    except: pass
    try: os.mkdir(f'{tmp_slides_folderpath}/{src_module_foldername}')
    except: pass
    try: os.mkdir(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}')
    except: pass
    with open(script_filepath) as f: script = f.read()
    sections = [x.strip() for x in script.split('---')]
    scripts_num = len(sections)
    ###
    slide_i = 0
    ###
    for section in sections:
        if slide_i == 0:
            slide_intro_gen(style='default', slide_num=slide_i, course_name=course_name)
        else:
            slides_base_general(slide_i, section)
        slide_i += 1

def tmp_script_split_gen(regen=False):
    tmp_script_split_folderpath = f'{tmp_folderpath}/script-split'
    ### clean
    if regen: 
        try: shutil.rmtree(tmp_script_split_folderpath)
        except: pass
    try: os.mkdir(tmp_script_split_folderpath)
    except: pass
    ### gen
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = []
    for line in script.split('\n'):
        line = line.strip()
        if line == '': continue
        if line.startswith('[what] '): continue
        elif line.startswith('[what] '): continue
        elif line.startswith('[step_1_title] '): continue
        elif line.startswith('[step_1_content] '): continue
        elif line.startswith('[step_2_title] '): continue
        elif line.startswith('[step_2_content] '): continue
        elif line.startswith('[step_3_title] '): continue
        elif line.startswith('[step_3_content] '): continue
        elif line.startswith('[title_1] '): continue
        elif line.startswith('[title_2] '): continue
        elif line.startswith('[title_3] '): continue
        elif line.startswith('[title_4] '): continue
        elif line.startswith('[title_5] '): continue
        elif line.startswith('[title_6] '): continue
        elif line.startswith('[title_7] '): continue
        elif line.startswith('[title_8] '): continue
        elif line.startswith('[title_9] '): continue
        elif line.startswith('[title_10] '): continue
        elif line.startswith('[title_11] '): continue
        elif line.startswith('[title_12] '): continue
        elif line.startswith('[title_13] '): continue
        elif line.startswith('[title_14] '): continue
        elif line.startswith('[disclaimer] '): continue
        elif line.startswith('[case_study_1_title] '): continue
        elif line.startswith('[case_study_1_content] '): continue
        elif line.startswith('[case_study_2_title] '): continue
        elif line.startswith('[case_study_2_content] '): continue
        elif line.startswith('[case_study_3_title] '): continue
        elif line.startswith('[case_study_3_content] '): continue
        elif line.startswith('[case_study_4_title] '): continue
        elif line.startswith('[case_study_4_content] '): continue
        elif line.startswith('[case_study_5_title] '): continue
        elif line.startswith('[case_study_5_content] '): continue
        elif line.startswith('[heading] '): continue
        elif line.startswith('[content] '): continue
        lines.append(line)
    script = '\n\n'.join(lines)
    scripts_split = [x.strip() for x in script.split('---')]
    for i, script_split in enumerate(scripts_split):
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        tmp_script_split_filepath = f'{tmp_script_split_folderpath}/{i_str}.txt'
        with open(tmp_script_split_filepath, 'w') as f: f.write(script_split)

def tmp_script_split_clips_gen(regen=False):
    tmp_script_split_folderpath = f'{tmp_folderpath}/script-split'
    tmp_script_split_clips_folderpath = f'{tmp_folderpath}/script-split-clips'
    ### clean
    if regen: 
        try: shutil.rmtree(tmp_script_split_clips_folderpath)
        except: pass
    try: os.mkdir(tmp_script_split_clips_folderpath)
    except: pass
    ### gen
    tmp_scripts_split_filenames = sorted(os.listdir(tmp_script_split_folderpath))
    for i, tmp_script_split_filename in enumerate(tmp_scripts_split_filenames):
        ## mk folder
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        try: os.mkdir(f'{tmp_script_split_clips_folderpath}/{i_str}')
        except: pass
        ## mk clips
        tmp_script_filepath = f'{tmp_script_split_folderpath}/{tmp_script_split_filename}'
        with open(tmp_script_filepath) as f: text = f.read()
        text = polish.text_format(text)
        pipeline = KPipeline(lang_code='a')
        generator = pipeline(text, voice='af_heart')
        j = 0
        for (gs, ps, audio) in generator:
            print(j, gs, ps)
            j_str = ''
            if j >= 10000: j_str = f'{j}'
            elif j >= 1000: j_str = f'0{j}'
            elif j >= 100: j_str = f'00{j}'
            elif j >= 10: j_str = f'000{j}'
            else: j_str = f'0000{j}'
            sf.write(f'{tmp_script_split_clips_folderpath}/{i_str}/{j_str}.wav', audio, 24000)
            j += 1

def tmp_audio_clips_gen(regen=False):
    import subprocess
    tmp_concat_filepath = f'{tmp_folderpath}/concat.txt'
    tmp_script_split_clips_folderpath = f'{tmp_folderpath}/script-split-clips'
    tmp_clips_folderpath = f'{tmp_folderpath}/clips'
    ### clean
    if regen: 
        try: shutil.rmtree(tmp_clips_folderpath)
        except: pass
    try: os.mkdir(tmp_clips_folderpath)
    except: pass
    ### gen
    tmp_script_split_clips_foldernames = sorted(os.listdir(tmp_script_split_clips_folderpath))
    for tmp_script_split_clips_foldername in tmp_script_split_clips_foldernames:
        _tmp_script_split_clips_folderpath = f'{tmp_script_split_clips_folderpath}/{tmp_script_split_clips_foldername}'
        print('##########################################')
        print(tmp_script_split_clips_foldername)
        print(_tmp_script_split_clips_folderpath)
        print('##########################################')
        tmp_script_split_clips_filenames = sorted(os.listdir(_tmp_script_split_clips_folderpath))
        tmp_script_split_clips_filepaths = [
            f'{_tmp_script_split_clips_folderpath}/{filename}' 
            for filename in tmp_script_split_clips_filenames
        ]
        ###
        with open(tmp_concat_filepath, 'w') as f:
            for tmp_script_split_clips_filepath in tmp_script_split_clips_filepaths:
                tmp_script_split_clips_filepath = os.path.abspath(
                    os.path.join(_tmp_script_split_clips_folderpath, tmp_script_split_clips_filepath)
                )
                f.write(f"file '{tmp_script_split_clips_filepath}'\n")
        tmp_clip_filepath = f'{tmp_clips_folderpath}/{tmp_script_split_clips_foldername}.wav'
        subprocess.run([
            f'ffmpeg',
            f'-f', f'concat',
            f'-safe', f'0',
            f'-i', f'{tmp_concat_filepath}', 
            f'-acodec', f'pcm_s16le', 
            f'{tmp_clip_filepath}', 
            f'-y',
        ])

def tmp_video_clips_gen(regen=False):
    import subprocess
    ### clean
    if regen:
        try: shutil.rmtree(tmp_video_clips_folderpath)
        except: pass
    try: os.mkdir(tmp_video_clips_folderpath)
    except: pass
    ### gen
    audio_filenames = sorted(os.listdir(tmp_audio_clips_folderpath))
    for i, audio_filename in enumerate(audio_filenames):
        audio_filepath = f'{tmp_audio_clips_folderpath}/{audio_filename}'
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        slide_filepath = f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png'
        video_filepath = f'{tmp_video_clips_folderpath}/{i_str}.mp4'
        subprocess.run([
            f'ffmpeg',
            f'-loop', f'1',
            f'-i', f'{slide_filepath}',
            f'-i', f'{audio_filepath}',
            f'-c:v', f'libx264',
            f'-tune', f'stillimage',
            f'-c:a', f'aac',
            f'-b:a', f'192k',
            f'-shortest',
            f'-pix_fmt', f'yuv420p',
            f'{video_filepath}',
            f'-y',
        ])

def dst_video_clip_gen(regen=False):
    import subprocess
    tmp_concat_filepath = f'{tmp_folderpath}/concat.txt'
    tmp_video_clips_folderpath = f'{tmp_folderpath}/video-clips'
    dst_lesson_folderpath = f'{dst_module_folderpath}/{src_lesson_foldername}'
    ### clean
    if regen:
        try: os.mkdir(dst_video_clips_folderpath)
        except: pass
    try: os.mkdir(dst_module_folderpath)
    except: pass
    # try: os.mkdir(dst_lesson_folderpath)
    # except: pass
    ### gen
    tmp_video_clips_filenames = sorted(os.listdir(tmp_video_clips_folderpath))
    # print(tmp_video_clips_filenames)
    # quit()
    with open(tmp_concat_filepath, 'w') as f:
        for i, tmp_video_clip_filename in enumerate(tmp_video_clips_filenames):
            tmp_video_clip_filepath = f'{tmp_video_clips_folderpath}/{tmp_video_clip_filename}'
            f.write(f"file '{tmp_video_clip_filepath}'\n")
    dst_video_clip_filepath = f'{dst_module_folderpath}/{lesson_filename}.mp4'
    if 1:
        subprocess.run([
            f'ffmpeg',
            f'-f', f'concat',
            f'-safe', f'0',
            f'-i', f'{tmp_concat_filepath}',
            f'-c', f'copy',
            f'{dst_video_clip_filepath}',
            f'-y', 
        ])

def demo():
    course_filename = 'make-your-first-tincture'
    course_folderpath = f'/home/ubuntu/vault/terrawhisper/database/shop/courses/{course_filename}'
    src_folderpath = f'{course_folderpath}/src'
    tmp_folderpath = f'{course_folderpath}/tmp'
    dst_folderpath = f'{course_folderpath}/dst'
    for script_filename in sorted(os.listdir(src_folderpath)):
        script_filepath = f'{src_folderpath}/{script_filename}'
        if 0:
            ### tmp clips
            for filename in os.listdir(tmp_folderpath):
                os.remove(f'{tmp_folderpath}/{filename}')
            with open(script_filepath) as f: text = f.read()
            text = polish.text_format(text)
            pipeline = KPipeline(lang_code='a')
            generator = pipeline(text, voice='af_heart')
            j = 0
            for (gs, ps, audio) in generator:
                print(j, gs, ps)
                j_str = ''
                if j >= 10000: j_str = f'{j}'
                elif j >= 1000: j_str = f'0{j}'
                elif j >= 100: j_str = f'00{j}'
                elif j >= 10: j_str = f'000{j}'
                else: j_str = f'0000{j}'
                sf.write(f'{tmp_folderpath}/{j_str}.wav', audio, 24000)
                j += 1
        if 0:
            ### audio clips
            import subprocess
            audio_clips_filenames = [f'{tmp_folderpath}/{filename}' for filename in sorted(os.listdir(tmp_folderpath))]
            with open(f'{tmp_folderpath}/concat.txt', 'w') as f:
                for filepath in audio_clips_filenames:
                    f.write(f"file '{filepath}'\n")
            script_filename_base = script_filename.split('.')[0]
            dst_clip_filepath = f'{dst_folderpath}/{script_filename_base}.wav'
            subprocess.run([
                f'ffmpeg',
                f'-f', f'concat',
                f'-safe', f'0',
                f'-i', f'{tmp_folderpath}/concat.txt', 
                f'-acodec', f'pcm_s16le', 
                f'{dst_clip_filepath}', 
                f'-y',
            ])
    ### full audio
    import subprocess
    audio_clips_folderpath = f'{dst_folderpath}'
    audio_output_filepath = f'{course_folderpath}/course-audio.wav'
    tmp_concat_filepath = f'{tmp_folderpath}/concat.txt'
    with open(tmp_concat_filepath, 'w') as f:
        for audio_clip_filename in sorted(os.listdir(audio_clips_folderpath)):
            audio_clip_filepath = f'{audio_clips_folderpath}/{audio_clip_filename}'
            f.write(f"file '{audio_clip_filepath}'\n")
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{tmp_concat_filepath}',
        f'-c', f'copy',
        f'{audio_output_filepath}',
        f'-y', 
    ])


# demo()
# quit()


course_name = 'Healing Drops System'
target_module = 4
target_lesson = 0
###
for module_i, src_module_foldername in enumerate(src_modules_foldernames):
    src_module_folderpath = f'{src_folderpath}/{src_module_foldername}'
    src_lessons_foldernames = sorted(os.listdir(src_module_folderpath))
    for lesson_i, src_lesson_foldername in enumerate(src_lessons_foldernames):
        src_lesson_folderpath = f'{src_folderpath}/{src_module_foldername}/{src_lesson_foldername}'
        lesson_filename = src_lesson_foldername
        script_filepath = f'{src_lesson_folderpath}/script.txt'
        src_slides_filepaths = [
            f'{src_lesson_folderpath}/{filename}' for filename in 
            sorted(os.listdir(src_lesson_folderpath))
            if '.png' in filename
        ]
        if target_module != -1:
            if module_i != target_module: continue
        if target_lesson != -1:
            if lesson_i != target_lesson: continue
        if not os.path.exists(script_filepath): continue
        print(f'MODULE: {module_i} - LESSON: {lesson_i}')
        ###
        dst_module_folderpath = f'{dst_video_clips_folderpath}/{src_module_foldername}'
        print(f'{dst_module_folderpath}/{lesson_filename}.mp4')
        # if os.path.exists(f'{dst_module_folderpath}/{lesson_filename}.mp4'): continue
        try: shutil.rmtree(tmp_folderpath)
        except: pass
        os.mkdir(tmp_folderpath)
        ###
        # if target_module == 0 and target_lesson == 0:
            # create_slides_general()
            # tmp_script_split_gen()
            # tmp_script_split_clips_gen()
            # tmp_clips_gen()
            # tmp_video_clips_gen()
            # dst_video_clip_gen()
        if target_module == 0 and target_lesson == 1:
            create_slides_general()
            tmp_script_split_gen()
            tmp_script_split_clips_gen()
            tmp_clips_gen()
            tmp_video_clips_gen()
            dst_video_clip_gen()
        if target_module == 0 and target_lesson == 2:
            create_slides_general()
            tmp_script_split_gen()
            tmp_script_split_clips_gen()
            tmp_clips_gen()
            tmp_video_clips_gen()
            dst_video_clip_gen()
        else:
            pass
            create_slides_general(regen=True)
            tmp_script_split_gen(regen=True)
            tmp_script_split_clips_gen(regen=True)
            tmp_audio_clips_gen(regen=True)
            tmp_video_clips_gen(regen=True)
            dst_video_clip_gen(regen=True)


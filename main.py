import os
import shutil

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

from kokoro import KPipeline
import soundfile as sf 

from pydub import AudioSegment

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import polish

def clips():
    book = epub.read_epub('/home/ubuntu/books/the-green-witch.epub')

    pipeline = KPipeline(lang_code='a')

    i = 0
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            '''
            print('========================================')
            name = item.get_name()
            print(f'NAME: {name}')
            print('----------------------------------------')
            if name == 'xhtml/copy.xhtml':
                print(item.get_content())
            print('========================================')
            '''
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text()
            print(text)
            generator = pipeline(text, voice='af_heart')
            for (gs, ps, audio) in generator:
                print(i, gs, ps)
                i_str = ''
                if i >= 10000: i_str = f'{i}'
                elif i >= 1000: i_str = f'0{i}'
                elif i >= 100: i_str = f'00{i}'
                elif i >= 10: i_str = f'000{i}'
                else: i_str = f'0000{i}'
                sf.write(f'output/{i_str}.wav', audio, 24000)
                i += 1
            # break
        '''
        if item.get_type() == ebooklib.epub.EpubHtml:
            print(item)
        '''

def clips_txt(filepath):
    folderpath = f'output'
    for filename in os.listdir(folderpath):
        _filepath = f'{folderpath}/{filename}'
        try: os.remove(_filepath)
        except: pass
    with open(filepath) as f: text = f.read()
    text = polish.text_format(text)
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(text, voice='af_heart')
    i = 0
    for (gs, ps, audio) in generator:
        print(i, gs, ps)
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        sf.write(f'output/{i_str}.wav', audio, 24000)
        i += 1

def concatenate_file():
    folder = 'output'
    with open('filelist.txt', 'w') as f:
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.wav'):
                filepath = os.path.abspath(os.path.join(folder, filename))
                f.write(f"file '{filepath}'\n")
    '''ffmpeg -f concat -safe 0 -i filelist.txt -acodec pcm_s16le combined.wav'''

def clips_gen(script_filepath, tmp_output_folderpath):
    for filename in os.listdir(tmp_output_folderpath):
        _filepath = f'{tmp_output_folderpath}/{filename}'
        try: os.remove(_filepath)
        except: pass
    with open(script_filepath) as f: text = f.read()
    text = polish.text_format(text)
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(text, voice='af_heart')
    i = 0
    for (gs, ps, audio) in generator:
        print(i, gs, ps)
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        sf.write(f'{tmp_output_folderpath}/{i_str}.wav', audio, 24000)
        i += 1

def concat_file_gen(concat_filepath, clips_folderpath):
    with open(concat_filepath, 'w') as f:
        for filename in sorted(os.listdir(clips_folderpath)):
            if filename.endswith('.wav'):
                filepath = os.path.abspath(os.path.join(clips_folderpath, filename))
                f.write(f"file '{filepath}'\n")

def slideshow_concat_gen(concat_filepath, slides_folderpath):
    with open(concat_filepath, 'w') as f:
        for filename in sorted(os.listdir(slides_folderpath)):
            if filename.endswith('.png'):
                filepath = os.path.abspath(os.path.join(slides_folderpath, filename))
                f.write(f"file '{filepath}'\n")
                f.write(f"duration 3\n")

def audio_gen(clip_filepath, concat_filepath):
    import subprocess
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{concat_filepath}', 
        f'-acodec', f'pcm_s16le', 
        f'{clip_filepath}', 
        f'-y',
    ])

def slideshow_gen(images_filepaths, audio_filepath, output_filepath):
    import subprocess
    cmd = [
        'ffmpeg',
        '-loop', '1', '-t', '3', '-i', f'{images_filepaths[0]}',
        '-loop', '1', '-t', '5', '-i', f'{images_filepaths[1]}',
        '-loop', '1', '-t', '9999', '-i', f'{images_filepaths[2]}',
        '-i', f'{audio_filepath}',
        '-filter_complex', '[0:v][1:v][2:v]concat=n=3:v=1:a=0,format=yuv420p[v]',
        '-map', '[v]', '-map', '3:a',
        '-c:v', 'libx264', '-c:a', 'aac',
        '-shortest',
        f'{output_filepath}',
        f'-y',
    ]
    print(cmd)
    subprocess.run(cmd)


def video_gen(image_filepath, audio_filepath, output_filepath):
    import subprocess
    subprocess.run([
        f'ffmpeg',
        f'-loop', f'1',
        f'-i', f'{image_filepath}',
        f'-i', f'{audio_filepath}',
        f'-c:v', f'libx264',
        f'-tune', f'stillimage',
        f'-c:a', f'aac',
        f'-b:a', f'192k',
        f'-shortest',
        f'-pix_fmt', f'yuv420p',
        f'{output_filepath}',
    ])



# clips_txt('email.txt')
# concatenate_file()
# audio_gen()

if 0:
    scripts_folderpath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/scripts'
    for script_filename in os.listdir(scripts_folderpath):
        script_filename_base = script_filename.replace('.txt', '')
        ### gen tmp clips
        script_filepath = f'{scripts_folderpath}/{script_filename_base}.txt'
        tmp_output_folderpath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/clips-tmp'
        # clips_gen(script_filepath, tmp_output_folderpath)
        ### gen concat file
        clips_folderpath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/clips-tmp'
        concat_filepath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/concat.txt'
        # concat_file_gen(concat_filepath, clips_folderpath)
        ### gen audio
        clip_filepath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/course/{script_filename_base}.wav'
        concat_filepath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/concat.txt'
        # audio_gen(clip_filepath, concat_filepath)

        ### gen slideshow
        # concat_filepath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/slideshow-images.txt'
        # slides_folderpath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/slides'
        # slideshow_concat_gen(concat_filepath, slides_folderpath)
        images_filepaths = [
            f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/slides/image1.png',
            f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/slides/image2.png',
            f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/slides/image1.png',
        ]
        output_filepath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/slideshow.mp4'
        audio_filepath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/course/{script_filename_base}.wav'
        slideshow_gen(images_filepaths, audio_filepath, output_filepath)
        ### gen video
        audio_filepath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/course/{script_filename_base}.wav'
        image_filepath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/slide-test.png'
        output_filepath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/video-test.mp4'
        # video_gen(image_filepath, audio_filepath, output_filepath)


def script_split_gen():
    script_filepath = f'{course_folderpath}/scripts/{script_filename_base}.txt'
    script_split_folderpath = f'{course_folderpath}/script-split'
    with open(script_filepath) as f: script = f.read()
    scripts_split = [x.strip() for x in script.split('---')]
    for i, script_split in enumerate(scripts_split):
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        script_split_filepath = f'{script_split_folderpath}/{i_str}.txt'
        with open(script_split_filepath, 'w') as f: f.write(script_split)
        
def script_split_clips_gen():
    script_split_folderpath = f'{course_folderpath}/script-split'
    script_split_clips_tmp_folderpath = f'{course_folderpath}/script-split-clips-tmp'
    ### clean
    for filename in os.listdir(script_split_clips_tmp_folderpath):
        _filepath = f'{script_split_clips_tmp_folderpath}/{filename}'
        try: os.remove(_filepath)
        except: pass
    ### gen
    scripts_split_filenames = os.listdir(script_split_folderpath)
    scripts_split_filenames = sorted(scripts_split_filenames)
    for i, script_split_filename in enumerate(scripts_split_filenames):
        ## mk folder
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        try: os.mkdir(f'{script_split_clips_tmp_folderpath}/{i_str}')
        except: pass
        ## mk clips
        script_filepath = f'{script_split_folderpath}/{script_split_filename}'
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
            sf.write(f'{script_split_clips_tmp_folderpath}/{i_str}/{j_str}.wav', audio, 24000)
            j += 1

def audio_clips_gen():
    import subprocess
    concat_filepath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety/concat.txt'
    script_split_audio_clips_tmp_folderpath = f'{course_folderpath}/script-split-clips-tmp'
    audio_clips_tmp_folderpath = f'{course_folderpath}/audio-clips-tmp'
    ### clean
    try: shutil.rmtree(audio_clips_tmp_folderpath)
    except: pass
    try: os.mkdir(audio_clips_tmp_folderpath)
    except: pass
    ### gen
    foldernames = os.listdir(script_split_clips_tmp_folderpath)
    foldernames = sorted(foldernames)
    for foldername in foldernames:
        folderpath = f'{script_split_clips_tmp_folderpath}/{foldername}'
        print(folderpath)
        filenames = os.listdir(folderpath)
        filenames = sorted(filenames)
        filepaths = [f'{folderpath}/{filename}' for filename in filenames]
        with open(concat_filepath, 'w') as f:
            for filepath in filepaths:
                filepath = os.path.abspath(os.path.join(script_split_clips_tmp_folderpath, filepath))
                f.write(f"file '{filepath}'\n")
        clip_tmp_filepath = f'{audio_clips_tmp_folderpath}/{foldername}.wav'
        subprocess.run([
            f'ffmpeg',
            f'-f', f'concat',
            f'-safe', f'0',
            f'-i', f'{concat_filepath}', 
            f'-acodec', f'pcm_s16le', 
            f'{clip_tmp_filepath}', 
            f'-y',
        ])

def video_clips_tmp_gen():
    import subprocess
    audio_clips_tmp_folderpath = f'{course_folderpath}/audio-clips-tmp'
    video_clips_tmp_folderpath = f'{course_folderpath}/video-clips-tmp'
    slides_folderpath = f'{course_folderpath}/slides'
    ### clean
    try: shutil.rmtree(video_clips_tmp_folderpath)
    except: pass
    try: os.mkdir(video_clips_tmp_folderpath)
    except: pass
    ### gen
    audio_filenames = os.listdir(audio_clips_tmp_folderpath)
    audio_filenames = sorted(audio_filenames)
    src_slides_filepaths = [f'{slides_folderpath}/{filename}' for filename in sorted(os.listdir(slides_folderpath))]
    for i, audio_filename in enumerate(audio_filenames):
        audio_filepath = f'{audio_clips_tmp_folderpath}/{audio_filename}'
        slide_filepath = src_slides_filepaths[i]
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        video_filepath = f'{video_clips_tmp_folderpath}/{i_str}.mp4'
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
        ])

def video_clip_gen():
    import subprocess
    video_clips_tmp_folderpath = f'{course_folderpath}/video-clips-tmp'
    video_clips_folderpath = f'{course_folderpath}/video-clips'
    video_clip_concat_filepath = f'{course_folderpath}/video-clip-concat.txt'
    ### clean
    try: shutil.rmtree(video_clips_folderpath)
    except: pass
    try: os.mkdir(video_clips_folderpath)
    except: pass
    ### gen
    video_clips_tmp_filenames = sorted(os.listdir(video_clips_tmp_folderpath))
    with open(video_clip_concat_filepath, 'w') as f:
        for i, video_clip_tmp_filename in enumerate(video_clips_tmp_filenames):
            video_clip_tmp_filepath = f'{video_clips_tmp_folderpath}/{video_clip_tmp_filename}'
            f.write(f"file '{video_clip_tmp_filepath}'\n")
    video_clip_filepath = f'{video_clips_folderpath}/test.mp4'
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{video_clip_concat_filepath}',
        f'-c', f'copy',
        f'{video_clip_filepath}',
    ])

if 0:
    course_folderpath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/tincture-dosage-safety'
    scripts_folderpath = f'{course_folderpath}/scripts'
    for script_filename in os.listdir(scripts_folderpath):
        script_filename_base = script_filename.replace('.txt', '')
        # script_split_gen()
        # script_split_clips_gen()
        # audio_clips_gen()
        video_clip_gen()
        break


###########################################################################
# SLIDES............................................................[SLD]
###########################################################################
slide_w = 1280
slide_h = 720

def slide_footer_draw(draw, color):
    line = f'SafeDrop System | Copyright TerraWhisper.com'
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

def slide_intro_gen(style, slide_num=-1):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = 'SafeDrop System'
    font_size = 128
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
    if slide_num == -1:
        img.save(f'{tmp_slides_folderpath}/00000.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00000.png')
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

def slide_step_1_gen(style):
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
    img.save(f'{tmp_slides_folderpath}/00004.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00004.png')

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

def slide_step_2_gen(style):
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
    img.save(f'{tmp_slides_folderpath}/00006.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00006.png')

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

def slide_step_3_gen(style):
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
    img.save(f'{tmp_slides_folderpath}/00008.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00008.png')

def slide_recap_gen(style):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    ### get section
    with open(script_filepath) as f: script = f.read()
    scripts_split = [x.strip() for x in script.split('---')]
    script = scripts_split[9]
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
    img.save(f'{tmp_slides_folderpath}/00009.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00009.png')

def slide_action_gen(style):
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
    img.save(f'{tmp_slides_folderpath}/00010.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00010.png')

def slide_next_lesson_gen(style):
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
    img.save(f'{tmp_slides_folderpath}/00011.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00011.png')

def slide_title_center_gen(style, title_tag, slide_num=-1):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### script
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    text = ''
    for line in lines:
        if line.startswith(f'{title_tag} '): 
            line = line.replace(f'{title_tag} ', '')
            text = line
            break
    ### set font
    line = text
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
        img.save(f'{tmp_slides_folderpath}/00000.png')
        img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/00001.png')
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

def slides_disclaimer_gen():
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
    slide_intro_gen(style='default', slide_num=0)
    slide_title_center_gen(style='invert', title_tag='[title_1]', slide_num=1)
    slide_title_center_gen(style='default', title_tag='[title_2]', slide_num=2)
    slide_title_content_gen(style='invert', title_tag='[title_3]', content_tag='[disclaimer]', slide_num=3)
    slide_title_center_gen(style='default', title_tag='[title_4]', slide_num=4)
    # quit()

def slides_overview_gen():
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
    slide_intro_gen(style='default', slide_num=0)
    slide_title_center_gen(style='invert', title_tag='[title_1]', slide_num=1)
    slide_title_center_gen(style='default', title_tag='[title_2]', slide_num=2)
    slide_title_center_gen(style='invert', title_tag='[title_3]', slide_num=3)
    slide_title_center_gen(style='default', title_tag='[title_4]', slide_num=4)
    slide_title_center_gen(style='invert', title_tag='[title_5]', slide_num=5)
    slide_title_center_gen(style='default', title_tag='[title_6]', slide_num=6)
    slide_title_center_gen(style='invert', title_tag='[title_7]', slide_num=7)
    slide_title_center_gen(style='default', title_tag='[title_8]', slide_num=8)
    slide_title_center_gen(style='invert', title_tag='[title_9]', slide_num=9)
    slide_title_center_gen(style='default', title_tag='[title_10]', slide_num=10)
    slide_title_center_gen(style='invert', title_tag='[title_11]', slide_num=11)
    slide_title_center_gen(style='default', title_tag='[title_12]', slide_num=12)
    slide_title_center_gen(style='invert', title_tag='[title_13]', slide_num=13)
    slide_title_center_gen(style='default', title_tag='[title_14]', slide_num=14)
    # quit()

def slides_case_studies_gen():
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
    slide_intro_gen(style='default', slide_num=0)
    slide_title_center_gen(style='invert', title_tag='[title_1]', slide_num=1)
    slide_title_center_gen(style='default', title_tag='[title_2]', slide_num=2)
    slide_case_study_gen(style='invert', title_tag='[case_study_1_title]', content_tag='[case_study_1_content]', slide_num=3)
    slide_case_study_gen(style='default', title_tag='[case_study_2_title]', content_tag='[case_study_2_content]', slide_num=4)
    slide_case_study_gen(style='invert', title_tag='[case_study_3_title]', content_tag='[case_study_3_content]', slide_num=5)
    slide_case_study_gen(style='default', title_tag='[case_study_4_title]', content_tag='[case_study_4_content]', slide_num=6)
    slide_case_study_gen(style='invert', title_tag='[case_study_5_title]', content_tag='[case_study_5_content]', slide_num=7)
    slide_title_center_gen(style='default', title_tag='[title_3]', slide_num=8)
    slide_title_center_gen(style='invert', title_tag='[title_4]', slide_num=9)

def slides_closing_gen():
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
    slide_intro_gen(style='default', slide_num=0)
    slide_title_center_gen(style='invert', title_tag='[title_1]', slide_num=1)
    slide_title_center_gen(style='default', title_tag='[title_2]', slide_num=2)
    slide_steps_1_gen(style='invert')
    slide_step_1_gen(style='default')
    slide_steps_2_gen(style='invert')
    slide_step_2_gen(style='default')
    slide_steps_3_gen(style='invert')
    slide_step_3_gen(style='default')
    slide_recap_gen(style='invert')
    slide_title_center_gen(style='default', title_tag='[title_3]', slide_num=10)
    slide_title_center_gen(style='invert', title_tag='[title_4]', slide_num=11)


def slide_case_study_gen(style, title_tag, content_tag, slide_num):
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
        if line.startswith(title_tag): 
            line = line.replace(title_tag, '').strip()
            title = line
        elif line.startswith(content_tag): 
            line = line.replace(content_tag, '').strip()
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
    i = slide_num
    i_str = ''
    if i >= 10000: i_str = f'{i}'
    elif i >= 1000: i_str = f'0{i}'
    elif i >= 100: i_str = f'00{i}'
    elif i >= 10: i_str = f'000{i}'
    else: i_str = f'0000{i}'
    img.save(f'{tmp_slides_folderpath}/{i_str}.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')

def slide_title_content_gen(style, title_tag, content_tag, slide_num):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### script
    with open(script_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = [x.strip() for x in script.split('\n') if x.strip() != '']
    title = ''
    content = ''
    for line in lines:
        if line.startswith(f'{title_tag} '): 
            line = line.replace(f'{title_tag} ', '')
            title = line
        elif line.startswith(f'{content_tag} '): 
            line = line.replace(f'{content_tag} ', '')
            content = line
    ### title
    line = title
    font_size = 64
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((slide_w//2 - line_w//2, 80), line, color, font=font)
    ### content
    font_size = 18
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    ### lines
    p_w = 1000
    lines = content_to_lines(content, draw, color, font, p_w)
    ### calc content height
    content_h = 0
    line_spacing = 1.2
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        content_h += font_size * line_spacing
    ### draw lines centered
    y_cur = slide_h//2 - content_h//2
    for line_i, line in enumerate(lines):
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((slide_w//2 - line_w//2, y_cur), line, color, font=font)
        y_cur += line_h * line_spacing
    ### 
    slide_footer_draw(draw, color)
    i = slide_num
    i_str = ''
    if i >= 10000: i_str = f'{i}'
    elif i >= 1000: i_str = f'0{i}'
    elif i >= 100: i_str = f'00{i}'
    elif i >= 10: i_str = f'000{i}'
    else: i_str = f'0000{i}'
    img.save(f'{tmp_slides_folderpath}/{i_str}.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')

def slides_intro_gen():
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
    slide_intro_gen(style='default', slide_num=0)
    slide_title_center_gen(style='invert', title_tag='[title_1]', slide_num=1)
    slide_title_center_gen(style='default', title_tag='[title_2]', slide_num=2)
    slide_title_center_gen(style='invert', title_tag='[title_3]', slide_num=3)
    slide_intro_steps_1_gen(style='invert', slide_num=4)
    slide_intro_steps_2_gen(style='invert', slide_num=5)
    slide_intro_steps_3_gen(style='invert', slide_num=6)
    slide_title_center_gen(style='default', title_tag='[title_4]', slide_num=7)
    slide_title_center_gen(style='invert', title_tag='[title_5]', slide_num=8)
    slide_title_center_gen(style='default', title_tag='[title_6]', slide_num=9)
    # quit()

def slide_intro_steps_1_gen(style, slide_num):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = '3 reasons why safe dosing is critical:'
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
        if line.startswith('Reason '): steps.append(line)
    step_1_x = int(slide_w*0.20)
    step_2_x = int(slide_w*0.50)
    step_3_x = int(slide_w*0.80)
    ### 1
    step = steps[0].replace('Reason ', '').strip()
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
    ### 2
    step = steps[1].replace('Reason ', '').strip()
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
    ### 3
    step = steps[2].replace('Reason ', '').strip()
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
    i = slide_num
    i_str = ''
    if i >= 10000: i_str = f'{i}'
    elif i >= 1000: i_str = f'0{i}'
    elif i >= 100: i_str = f'00{i}'
    elif i >= 10: i_str = f'000{i}'
    else: i_str = f'0000{i}'
    img.save(f'{tmp_slides_folderpath}/{i_str}.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')

def slide_intro_steps_2_gen(style, slide_num):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = '3 reasons why safe dosing is critical:'
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
        if line.startswith('Reason '): steps.append(line)
    step_1_x = int(slide_w*0.20)
    step_2_x = int(slide_w*0.50)
    step_3_x = int(slide_w*0.80)
    ### 1
    step = steps[0].replace('Reason ', '').strip()
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
    ### 2
    step = steps[1].replace('Reason ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_2_x - line_w//2, int(slide_h*0.33)), step_num, color, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_2_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, color, font=font)
    ### 3
    step = steps[2].replace('Reason ', '').strip()
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
    i = slide_num
    i_str = ''
    if i >= 10000: i_str = f'{i}'
    elif i >= 1000: i_str = f'0{i}'
    elif i >= 100: i_str = f'00{i}'
    elif i >= 10: i_str = f'000{i}'
    else: i_str = f'0000{i}'
    img.save(f'{tmp_slides_folderpath}/{i_str}.png')
    img.save(f'{tmp_slides_folderpath}/{src_module_foldername}/{src_lesson_foldername}/{i_str}.png')

def slide_intro_steps_3_gen(style, slide_num):
    if style == 'default':
        bg_color = g.color_linen
        color = g.color_carbon_powder
    else:
        bg_color = g.color_carbon_powder
        color = g.color_linen
    img = Image.new('RGB', (slide_w, slide_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    ### title
    line = '3 reasons why safe dosing is critical:'
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
        if line.startswith('Reason '): steps.append(line)
    step_1_x = int(slide_w*0.20)
    step_2_x = int(slide_w*0.50)
    step_3_x = int(slide_w*0.80)
    ### 1
    step = steps[0].replace('Reason ', '').strip()
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
    ### 2
    step = steps[1].replace('Reason ', '').strip()
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
    ### 3
    step = steps[2].replace('Reason ', '').strip()
    step_num, step_txt = step.split(': ')
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_num)
    draw.text((step_3_x - line_w//2, int(slide_h*0.33)), step_num, color, font=font)
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(step_txt)
    draw.text((step_3_x - line_w//2, int(slide_h*0.33) + 128 + 16), step_txt, color, font=font)
    ### slide footer
    slide_footer_draw(draw, color)
    ###
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
    slide_intro_gen(style='default')
    slide_why_gen(style='invert')
    slide_what_gen(style='default')
    slide_steps_1_gen(style='invert')
    slide_step_1_gen(style='default')
    slide_steps_2_gen(style='invert')
    slide_step_2_gen(style='default')
    slide_steps_3_gen(style='invert')
    slide_step_3_gen(style='default')
    slide_recap_gen(style='invert')
    slide_action_gen(style='default')
    slide_next_lesson_gen(style='invert')
    # quit()

def tmp_script_split_gen():
    tmp_script_split_folderpath = f'{tmp_folderpath}/script-split'
    ### clean
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

def tmp_script_split_clips_gen():
    tmp_script_split_folderpath = f'{tmp_folderpath}/script-split'
    tmp_script_split_clips_folderpath = f'{tmp_folderpath}/script-split-clips'
    ### clean
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

def tmp_clips_gen():
    import subprocess
    tmp_concat_filepath = f'{tmp_folderpath}/concat.txt'
    tmp_script_split_clips_folderpath = f'{tmp_folderpath}/script-split-clips'
    tmp_clips_folderpath = f'{tmp_folderpath}/clips'
    ### clean
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

def tmp_video_clips_gen():
    import subprocess
    ### clean
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
        slide_filepath = f'{tmp_slides_folderpath}/{i_str}.png'
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
        ])

def dst_video_clip_gen():
    import subprocess
    tmp_concat_filepath = f'{tmp_folderpath}/concat.txt'
    tmp_video_clips_folderpath = f'{tmp_folderpath}/video-clips'
    dst_lesson_folderpath = f'{dst_module_folderpath}/{src_lesson_foldername}'
    ### clean
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
        ])

def dst_full_clip_gen():
    import subprocess
    tmp_concat_filepath = f'{tmp_folderpath}/concat.txt'
    dst_video_clips_folderpath = f'{dst_folderpath}/video-clips'
    dst_full_course_folderpath = f'{dst_folderpath}'
    ### init
    try: os.mkdir(dst_video_clips_folderpath)
    except: pass
    try: os.mkdir(dst_full_course_folderpath)
    except: pass
    ### gen
    with open(tmp_concat_filepath, 'w') as f:
        for _module_foldername in sorted(os.listdir(dst_video_clips_folderpath)):
            _module_folderpath = f'{dst_video_clips_folderpath}/{_module_foldername}'
            for _lesson_filename in sorted(os.listdir(_module_folderpath)):
                _lesson_filepath = f'{_module_folderpath}/{_lesson_filename}'
                f.write(f"file '{_lesson_filepath}'\n")
    ###
    dst_video_clip_filepath = f'{dst_full_course_folderpath}/full-course.mp4'
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

def dst_full_audio_gen():
    import subprocess
    dst_video_clip_filepath = f'{dst_folderpath}/full-course.mp4'
    dst_full_audio_filepath = f'{dst_folderpath}/full-audio-version.mp3'
    if 1:
        subprocess.run([
            f'ffmpeg',
            f'-i', f'{dst_video_clip_filepath}',
            f'-q:a', f'0',
            f'-map', f'a', f'{dst_full_audio_filepath}',
            f'-y',
        ])


course_slug = 'tincture-dosage-safety'
course_folderpath = f'/home/ubuntu/vault/terrawhisper/database/assets/shop/courses/{course_slug}'
src_folderpath = f'{course_folderpath}/src'
###
tmp_folderpath = f'{course_folderpath}/tmp'
tmp_slides_folderpath = f'{course_folderpath}/tmp/slides'
tmp_audio_clips_folderpath = f'{tmp_folderpath}/clips'
tmp_video_clips_folderpath = f'{tmp_folderpath}/video-clips'
###
dst_folderpath = f'{course_folderpath}/dst'
dst_video_clips_folderpath = f'{dst_folderpath}/video-clips'
# try: shutil.rmtree(dst_video_clips_folderpath)
# except: pass
src_modules_foldernames = sorted(os.listdir(src_folderpath))
target_module = 3 
target_lesson = 2 
if 0:
    for module_i, src_module_foldername in enumerate(src_modules_foldernames):
        src_module_folderpath = f'{src_folderpath}/{src_module_foldername}'
        src_lessons_foldernames = sorted(os.listdir(src_module_folderpath))
        for lesson_i, src_lesson_foldername in enumerate(src_lessons_foldernames):
            src_lesson_folderpath = f'{src_folderpath}/{src_module_foldername}/{src_lesson_foldername}'
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
            print(module_i)
            print(lesson_i)
            if 1:
                lesson_filename = src_lesson_foldername
                if module_i == 0 and lesson_i == 0:
                    slides_intro_gen()
                elif module_i == 0 and lesson_i == 1:
                    slides_disclaimer_gen()
                elif module_i == 0 and lesson_i == 2:
                    slides_overview_gen()
                elif module_i == 4 and lesson_i == 0:
                    slides_case_studies_gen()
                elif module_i == 4 and lesson_i == 2:
                    slides_closing_gen()
                else:
                    slides_gen()
                # continue
                if os.path.exists(f'{dst_module_folderpath}/{lesson_filename}.mp4'): continue
                ###
            if 1:
                tmp_script_split_gen()
                tmp_script_split_clips_gen()
                tmp_clips_gen()
                tmp_video_clips_gen()
                dst_video_clip_gen()
# dst_full_clip_gen()
dst_full_audio_gen()


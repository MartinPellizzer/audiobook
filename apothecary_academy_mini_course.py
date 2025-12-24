# apothecary academy
    # teas (course)
        # materials (module)
            # ingredients (lesson)
                # lemon balm (section)
                    # constituents (block)
                        # splitted sentences (chunks)

import os
import shutil
import subprocess

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import media
from lib import zimage

apothecary_academy_folderpath = f'/home/ubuntu/vault/terrawhisper/database/shop/apothecary-academy'
hub_folderpath = f'{apothecary_academy_folderpath}/teas'
course_folderpath = f'{hub_folderpath}/mini-course'

def audio_clips_chunks_gen_old(regen=False):
    tmp_audio_clips_folderpath = f'{tmp_lesson_folderpath}/audio-clips-chunks'
    ### clean
    if regen: 
        try: shutil.rmtree(tmp_audio_clips_folderpath)
        except: pass
    try: os.mkdir(tmp_audio_clips_folderpath)
    except: pass
    if os.listdir(tmp_audio_clips_folderpath) != []: return
    ### gen
    from kokoro import KPipeline
    import soundfile as sf 
    with open(src_script_filepath) as f: text = f.read()
    text = text.replace('*', '')
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(
        text, 
        voice='af_heart',
        speed = 0.9,
    )
    j = 0
    for (gs, ps, audio) in generator:
        print(j, gs, ps)
        j_str = ''
        if j >= 10000: j_str = f'{j}'
        elif j >= 1000: j_str = f'0{j}'
        elif j >= 100: j_str = f'00{j}'
        elif j >= 10: j_str = f'000{j}'
        else: j_str = f'0000{j}'
        output_filepath = f'{tmp_audio_clips_folderpath}/{j_str}.wav'
        print('##################################################')
        print(output_filepath)
        print('##################################################')
        sf.write(output_filepath, audio, 24000)
        j += 1

def audio_clips_chunks_gen(lesson_section_index, script_chunk_index, script_chunk, regen=False, dispel=False):
    tmp_section_folderpath = f'{tmp_lesson_folderpath}/{lesson_section_index}'
    tmp_script_chunk_folderpath = f'{tmp_section_folderpath}/{script_chunk_index}'
    tmp_audio_clips_folderpath = f'{tmp_script_chunk_folderpath}/audio-clips-chunks'
    ### clean
    try: os.mkdir(tmp_section_folderpath)
    except: pass
    try: os.mkdir(tmp_script_chunk_folderpath)
    except: pass
    try: os.mkdir(tmp_audio_clips_folderpath)
    except: pass
    if dispel: 
        for filename in os.listdir(tmp_audio_clips_folderpath):
            os.remove(f'{tmp_audio_clips_folderpath}/{filename}')
    if not regen:
        if os.listdir(tmp_audio_clips_folderpath) != []: return
    if os.listdir(tmp_audio_clips_folderpath) != []: return
    ### gen
    from kokoro import KPipeline
    import soundfile as sf 
    # with open(src_script_filepath) as f: text = f.read()
    text = script_chunk
    text = text.replace('*', '')
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line == '': continue
        if line.startswith('['): continue
        lines.append(line)
    text = '\n'.join(lines)
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(
        text, 
        voice='af_heart',
        speed = 0.9,
    )
    j = 0
    for (gs, ps, audio) in generator:
        print(j, gs, ps)
        j_str = ''
        if j >= 10000: j_str = f'{j}'
        elif j >= 1000: j_str = f'0{j}'
        elif j >= 100: j_str = f'00{j}'
        elif j >= 10: j_str = f'000{j}'
        else: j_str = f'0000{j}'
        output_filepath = f'{tmp_audio_clips_folderpath}/{j_str}.wav'
        print('##################################################')
        print(output_filepath)
        print('##################################################')
        sf.write(output_filepath, audio, 24000)
        j += 1

def audio_clips_gen_old(regen=False):
    tmp_concat_filepath = f'{tmp_lesson_folderpath}/concat.txt'
    tmp_audio_clips_chunks_folderpath = f'{tmp_lesson_folderpath}/audio-clips-chunks'
    tmp_audio_clips_folderpath = f'{tmp_lesson_folderpath}/audio-clips'
    ### clean
    if regen: 
        try: shutil.rmtree(tmp_audio_clips_folderpath)
        except: pass
    try: os.mkdir(tmp_audio_clips_folderpath)
    except: pass
    if os.listdir(tmp_audio_clips_folderpath) != []: return
    ### gen
    tmp_audio_clips_chunks_filepaths = [
        f'{tmp_audio_clips_chunks_folderpath}/{filename}' 
        for filename in sorted(os.listdir(tmp_audio_clips_chunks_folderpath))
    ]
    with open(tmp_concat_filepath, 'w') as f:
        for tmp_audio_clips_chunks_filepath in tmp_audio_clips_chunks_filepaths:
            f.write(f"file '{tmp_audio_clips_chunks_filepath}'\n")
    ###
    tmp_audio_clip_filepath = f'{tmp_audio_clips_folderpath}/0000.wav'
    import subprocess
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{tmp_concat_filepath}', 
        f'-acodec', f'pcm_s16le', 
        f'{tmp_audio_clip_filepath}', 
        f'-y',
    ])

def audio_clips_gen(lesson_section_index, script_chunk_index, script_chunk, regen=False, dispel=False):
    tmp_section_folderpath = f'{tmp_lesson_folderpath}/{lesson_section_index}'
    tmp_script_chunk_folderpath = f'{tmp_section_folderpath}/{script_chunk_index}'
    tmp_concat_filepath = f'{tmp_script_chunk_folderpath}/concat.txt'
    tmp_audio_clips_chunks_folderpath = f'{tmp_script_chunk_folderpath}/audio-clips-chunks'
    tmp_audio_clips_folderpath = f'{tmp_script_chunk_folderpath}/audio-clips'
    ### clean
    try: os.mkdir(tmp_script_chunk_folderpath)
    except: pass
    try: os.mkdir(tmp_audio_clips_folderpath)
    except: pass
    if dispel: 
        for filename in os.listdir(tmp_audio_clips_folderpath):
            os.remove(f'{tmp_audio_clips_folderpath}/{filename}')
    if not regen:
        if os.listdir(tmp_audio_clips_folderpath) != []: return
    if os.listdir(tmp_audio_clips_folderpath) != []: return
    ### gen
    tmp_audio_clips_chunks_filepaths = [
        f'{tmp_audio_clips_chunks_folderpath}/{filename}' 
        for filename in sorted(os.listdir(tmp_audio_clips_chunks_folderpath))
    ]
    with open(tmp_concat_filepath, 'w') as f:
        for tmp_audio_clips_chunks_filepath in tmp_audio_clips_chunks_filepaths:
            f.write(f"file '{tmp_audio_clips_chunks_filepath}'\n")
    ###
    tmp_audio_clip_filepath = f'{tmp_audio_clips_folderpath}/audio-clip.wav'
    import subprocess
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{tmp_concat_filepath}', 
        f'-acodec', f'pcm_s16le', 
        f'{tmp_audio_clip_filepath}', 
        f'-y',
    ])

def images_gen(regen=False):
    with open(src_script_filepath) as f: script = f.read()
    tmp_images_folderpath = f'{tmp_lesson_folderpath}/images'
    ###
    if regen: 
        try: shutil.rmtree(tmp_images_folderpath)
        except: pass
    try: os.mkdir(tmp_images_folderpath)
    except: pass
    if os.listdir(tmp_images_folderpath) != []: return
    ###
    prompt = f'''
        dry melissa officinalis herb on a wooden table surrounded by medicinal herbs,
        rustic, vintage, boho,
    '''.replace('  ', ' ')
    tmp_images_filepath = f'{tmp_images_folderpath}/0000.jpg'
    image = zimage.image_create(tmp_images_filepath, prompt, width=768, height=1024, seed=-1)

def slide_template_ingredient_1_gen(script_instructions, tmp_section_folderpath, tmp_slides_folderpath):
    title = ''
    subtitle = ''
    constituents = ''
    benefits = ''
    alternatives = ''
    content = []
    for script_instruction in script_instructions:
        if script_instruction.startswith('title: '):
            title = script_instruction.replace('title: ', '')
        if script_instruction.startswith('subtitle: '):
            subtitle = script_instruction.replace('subtitle: ', '')
        if script_instruction.startswith('constituents: '):
            constituents = script_instruction.replace('constituents: ', '')
        if script_instruction.startswith('benefits: '):
            benefits = script_instruction.replace('benefits: ', '')
        if script_instruction.startswith('alternatives: '):
            alternatives = script_instruction.replace('alternatives: ', '')
        if script_instruction.startswith('content: '):
            content.append(script_instruction.replace('content: ', ''))
    slide_w = 1920
    slide_h = 1080
    color_white_whisper = '#f7f6f2'
    img = Image.new(mode="RGB", size=(slide_w, slide_h), color=color_white_whisper)
    draw = ImageDraw.Draw(img)
    ###
    img_0000_w = int(slide_w*(2/5))
    img_0000_h = int(slide_h/1)
    img_0000_x = slide_w - img_0000_w
    img_0000_y = 0
    # img_0000 = Image.open(f'{tmp_section_folderpath}/images/0000.jpg')
    img_0000 = Image.open(f'{course_folderpath}/placeholders/image.jpg')
    img_0000 = media.resize(img_0000, img_0000_w, img_0000_h)
    img.paste(img_0000, (img_0000_x, img_0000_y))
    ###
    x_cur = 96
    y_cur = 96
    ###
    text = f'''{title}'''.upper()
    font_size = 80
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    # lines = text_to_lines(text, font, 800)
    lines = [text]
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((x_cur, y_cur), line, '#000000', font=font)
    y_cur += 96
    ###
    text = f'''{subtitle}'''
    font_size = 24
    font_family, font_weight = 'Lato', 'Italic'
    font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = [text]
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((x_cur, y_cur), line, '#000000', font=font)
    y_cur += 96
    ###
    y_start = y_cur
    font_size = 36
    line_height = 1.3
    bottom_margin = 96
    ### CONSTITUENTS
    if constituents != '':
        content_block_lines = constituents.split('|')
        content_block_height = (font_size * len(content_block_lines)+1) * line_height
        if y_cur + content_block_height + bottom_margin > 1080: 
            y_cur = y_start
            x_cur = 512 + 128
        text = f'''Constituents'''
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        lines = [text]
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((x_cur, y_cur), line, '#000000', font=font)
            y_cur += font_size*line_height
        for content_line_i, content_line in enumerate(content_block_lines):
            if content_line_i == -1:
                pass
            else:
                content_line = content_line.strip()
                text = f'''- {content_line}'''
                font_family, font_weight = 'Lato', 'Regular'
                font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                font = ImageFont.truetype(font_path, font_size)
                _, _, text_w, text_h = font.getbbox(text)
                lines = [text]
                for line in lines:
                    _, _, line_w, line_h = font.getbbox(line)
                    draw.text((x_cur + 32, y_cur), line, '#000000', font=font)
                    y_cur += font_size*line_height
        y_cur += font_size*line_height
    ### BENEFITS
    if benefits != '':
        content_block_lines = benefits.split('|')
        content_block_height = (font_size * len(content_block_lines)+1) * line_height
        if y_cur + content_block_height + bottom_margin > 1080: 
            y_cur = y_start
            x_cur = 512 + 128
        text = f'''Benefits'''
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        lines = [text]
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((x_cur, y_cur), line, '#000000', font=font)
            y_cur += font_size*line_height
        for content_line_i, content_line in enumerate(content_block_lines):
            if content_line_i == -1:
                pass
            else:
                content_line = content_line.strip()
                text = f'''- {content_line}'''
                font_family, font_weight = 'Lato', 'Regular'
                font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                font = ImageFont.truetype(font_path, font_size)
                _, _, text_w, text_h = font.getbbox(text)
                lines = [text]
                for line in lines:
                    _, _, line_w, line_h = font.getbbox(line)
                    draw.text((x_cur + 32, y_cur), line, '#000000', font=font)
                    y_cur += font_size*line_height
        y_cur += font_size*line_height
    ### ALTERNATIVES
    if alternatives != '':
        content_block_lines = alternatives.split('|')
        content_block_height = (font_size * len(content_block_lines)+1) * line_height
        if y_cur + content_block_height + bottom_margin > 1080: 
            y_cur = y_start
            x_cur = 512 + 128
        text = f'''Alternatives'''
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        lines = [text]
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((x_cur, y_cur), line, '#000000', font=font)
            y_cur += font_size*line_height
        for content_line_i, content_line in enumerate(content_block_lines):
            if content_line_i == -1:
                pass
            else:
                content_line = content_line.strip()
                text = f'''- {content_line}'''
                font_family, font_weight = 'Lato', 'Regular'
                font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                font = ImageFont.truetype(font_path, font_size)
                _, _, text_w, text_h = font.getbbox(text)
                lines = [text]
                for line in lines:
                    _, _, line_w, line_h = font.getbbox(line)
                    draw.text((x_cur + 32, y_cur), line, '#000000', font=font)
                    y_cur += font_size*line_height
        y_cur += font_size*line_height
    ### CONTENT
    if content != []:
        for content_block in content:
            content_block_lines = content_block.split('|')
            content_block_height = (font_size * len(content_block_lines)+1) * line_height
            if y_cur + content_block_height + bottom_margin > 1080: 
                y_cur = y_start
                x_cur = 512 + 128
            if 0:
                text = f'''Content'''
                font_family, font_weight = 'Lato', 'Bold'
                font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                font = ImageFont.truetype(font_path, font_size)
                _, _, text_w, text_h = font.getbbox(text)
                lines = [text]
                for line in lines:
                    _, _, line_w, line_h = font.getbbox(line)
                    draw.text((x_cur, y_cur), line, '#000000', font=font)
                    y_cur += font_size*line_height
            for content_line_i, content_line in enumerate(content_block_lines):
                content_line = content_line.strip()
                if content_line.startswith('*') and content_line.endswith('*'):
                    content_line = content_line.replace('*', '')
                    text = f'''{content_line}'''
                    font_family, font_weight = 'Lato', 'Bold'
                    font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                    _, _, text_w, text_h = font.getbbox(text)
                    lines = [text]
                    for line in lines:
                        _, _, line_w, line_h = font.getbbox(line)
                        draw.text((x_cur + 32, y_cur), line, '#000000', font=font)
                        y_cur += font_size*line_height
                else:
                    text = f'''- {content_line}'''
                    font_family, font_weight = 'Lato', 'Regular'
                    font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                    _, _, text_w, text_h = font.getbbox(text)
                    lines = [text]
                    for line in lines:
                        _, _, line_w, line_h = font.getbbox(line)
                        draw.text((x_cur + 32, y_cur), line, '#000000', font=font)
                        y_cur += font_size*line_height
            y_cur += font_size*line_height
    ###
    tmp_slides_filepath = f'{tmp_slides_folderpath}/slide.jpg'
    img.save(tmp_slides_filepath, format='JPEG', subsampling=0, quality=100)

def slide_template_ingredient_2_gen(script_instructions, tmp_section_folderpath, tmp_slides_folderpath):
    title = ''
    subtitle = ''
    constituents = ''
    benefits = ''
    alternatives = ''
    content = []
    for script_instruction in script_instructions:
        if script_instruction.startswith('title: '):
            title = script_instruction.replace('title: ', '')
        if script_instruction.startswith('subtitle: '):
            subtitle = script_instruction.replace('subtitle: ', '')
        if script_instruction.startswith('constituents: '):
            constituents = script_instruction.replace('constituents: ', '')
        if script_instruction.startswith('benefits: '):
            benefits = script_instruction.replace('benefits: ', '')
        if script_instruction.startswith('alternatives: '):
            alternatives = script_instruction.replace('alternatives: ', '')
        if script_instruction.startswith('content: '):
            content.append(script_instruction.replace('content: ', ''))
    slide_w = 1920
    slide_h = 1080
    color_white_whisper = '#f7f6f2'
    img = Image.new(mode="RGB", size=(slide_w, slide_h), color=color_white_whisper)
    draw = ImageDraw.Draw(img)
    ###
    img_0000_w = int(slide_w*(2/5))
    img_0000_h = int(slide_h/1)
    img_0000_x = 0
    img_0000_y = 0
    img_0000 = Image.open(f'{course_folderpath}/placeholders/image.jpg')
    # img_0000 = Image.open(f'{tmp_section_folderpath}/images/0000.jpg')
    img_0000 = media.resize(img_0000, img_0000_w, img_0000_h)
    img.paste(img_0000, (img_0000_x, img_0000_y))
    content_x = img_0000_w + 96
    ###
    x_cur = content_x
    y_cur = 96
    ###
    text = f'''{title}'''.upper()
    font_size = 80
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    # lines = text_to_lines(text, font, 800)
    lines = [text]
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((x_cur, y_cur), line, '#000000', font=font)
    y_cur += 96
    ###
    text = f'''{subtitle}'''
    font_size = 24
    font_family, font_weight = 'Lato', 'Italic'
    font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = [text]
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((x_cur, y_cur), line, '#000000', font=font)
    y_cur += 96
    ###
    y_start = y_cur
    font_size = 36
    line_height = 1.3
    bottom_margin = 96
    ### CONTENT
    if content != []:
        for content_block in content:
            content_block_lines = content_block.split('|')
            content_block_height = (font_size * len(content_block_lines)+1) * line_height
            if y_cur + content_block_height + bottom_margin > 1080: 
                y_cur = y_start
                x_cur += 512
            if 0:
                text = f'''Content'''
                font_family, font_weight = 'Lato', 'Bold'
                font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                font = ImageFont.truetype(font_path, font_size)
                _, _, text_w, text_h = font.getbbox(text)
                lines = [text]
                for line in lines:
                    _, _, line_w, line_h = font.getbbox(line)
                    draw.text((x_cur, y_cur), line, '#000000', font=font)
                    y_cur += font_size*line_height
            for content_line_i, content_line in enumerate(content_block_lines):
                content_line = content_line.strip()
                if content_line.startswith('*') and content_line.endswith('*'):
                    content_line = content_line.replace('*', '')
                    text = f'''{content_line}'''
                    font_family, font_weight = 'Lato', 'Bold'
                    font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                    _, _, text_w, text_h = font.getbbox(text)
                    lines = [text]
                    for line in lines:
                        _, _, line_w, line_h = font.getbbox(line)
                        draw.text((x_cur + 32, y_cur), line, '#000000', font=font)
                        y_cur += font_size*line_height
                else:
                    text = f'''- {content_line}'''
                    font_family, font_weight = 'Lato', 'Regular'
                    font_path = f"{g.VAULT_FOLDERPATH}/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                    _, _, text_w, text_h = font.getbbox(text)
                    lines = [text]
                    for line in lines:
                        _, _, line_w, line_h = font.getbbox(line)
                        draw.text((x_cur + 32, y_cur), line, '#000000', font=font)
                        y_cur += font_size*line_height
            y_cur += font_size*line_height
    ###
    tmp_slides_filepath = f'{tmp_slides_folderpath}/slide.jpg'
    img.save(tmp_slides_filepath, format='JPEG', subsampling=0, quality=100)

# text = f'''Limbic Downshift Protocol'''.upper()
def slides_gen(lesson_section_index, script_chunk_index, lesson_section_i, script_chunk_i, regen=False, dispel=False):
    tmp_section_folderpath = f'{tmp_lesson_folderpath}/{lesson_section_index}'
    tmp_script_chunk_folderpath = f'{tmp_section_folderpath}/{script_chunk_index}'
    tmp_slides_folderpath = f'{tmp_script_chunk_folderpath}/slides'
    ### clean
    try: os.mkdir(tmp_script_chunk_folderpath)
    except: pass
    try: os.mkdir(tmp_slides_folderpath)
    except: pass
    if dispel: 
        for filename in os.listdir(tmp_slides_folderpath):
            os.remove(f'{tmp_slides_folderpath}/{filename}')
    if not regen:
        if os.listdir(tmp_slides_folderpath) != []: return
    if os.listdir(tmp_slides_folderpath) != []: return
    with open(src_script_filepath) as f: script_text = f.read()
    lesson_section = script_text.split('===')[lesson_section_i]
    script_chunks = lesson_section.split('---')[:script_chunk_i+1]
    ###
    script_instructions = []
    for script_chunk in script_chunks:
        for line in script_chunk.split('\n'):
            line = line.strip()
            if line == '': continue
            if not line.startswith('['): continue
            if not line.endswith(']'): continue
            line = line.replace('[', '')
            line = line.replace(']', '')
            script_instructions.append(line)
    ###
    if 'template: ingredient_1' in script_instructions:
        slide_template_ingredient_1_gen(script_instructions, tmp_section_folderpath, tmp_slides_folderpath)
    elif 'template: ingredient_2' in script_instructions:
        slide_template_ingredient_2_gen(script_instructions, tmp_section_folderpath, tmp_slides_folderpath)

def video_clips_gen_old(script_chunk_index, regen=False, dispel=False):
    tmp_script_chunk_folderpath = f'{tmp_lesson_folderpath}/{script_chunk_index}'
    tmp_slides_folderpath = f'{tmp_script_chunk_folderpath}/slides'
    tmp_audio_clips_folderpath = f'{tmp_script_chunk_folderpath}/audio-clips'
    tmp_video_clips_folderpath = f'{tmp_script_chunk_folderpath}/video-clips'
    ### clean
    try: os.mkdir(tmp_script_chunk_folderpath)
    except: pass
    try: os.mkdir(tmp_video_clips_folderpath)
    except: pass
    if dispel: 
        for filename in os.listdir(tmp_audio_clips_folderpath):
            os.remove(f'{tmp_audio_clips_folderpath}/{filename}')
    if not regen:
        if os.listdir(tmp_audio_clips_folderpath) != []: return
    if os.listdir(tmp_audio_clips_folderpath) != []: return
    ### gen
    tmp_audio_clips_filenames = sorted(os.listdir(tmp_audio_clips_folderpath))
    tmp_slides_filenames = sorted(os.listdir(tmp_slides_folderpath))
    ###
    for i, tmp_audio_clip_filename in enumerate(tmp_audio_clips_filenames):
        tmp_audio_filepath = f'{tmp_audio_clips_folderpath}/{tmp_audio_clip_filename}'
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        tmp_slide_filepath = f'{tmp_slides_folderpath}/{tmp_slides_filenames[i]}'
        tmp_video_filepath = f'{tmp_video_clips_folderpath}/{i_str}.mp4'
        ###
        import subprocess
        subprocess.run([
            f'ffmpeg',
            f'-loop', f'1',
            f'-i', f'{tmp_slide_filepath}',
            f'-i', f'{tmp_audio_filepath}',
            f'-c:v', f'libx264',
            f'-tune', f'stillimage',
            f'-c:a', f'aac',
            f'-b:a', f'192k',
            f'-shortest',
            f'-pix_fmt', f'yuv420p',
            f'{tmp_video_filepath}',
            f'-y',
        ])

def video_clips_gen_old(script_chunk_index, regen=False, dispel=False):
    tmp_script_chunk_folderpath = f'{tmp_lesson_folderpath}/{script_chunk_index}'
    tmp_slide_folderpath = f'{tmp_script_chunk_folderpath}/slides'
    tmp_audio_clips_folderpath = f'{tmp_script_chunk_folderpath}/audio-clips'
    tmp_video_clips_folderpath = f'{tmp_script_chunk_folderpath}/video-clips'
    ### clean
    try: os.mkdir(tmp_script_chunk_folderpath)
    except: pass
    try: os.mkdir(tmp_video_clips_folderpath)
    except: pass
    if dispel: 
        for filename in os.listdir(tmp_video_clips_folderpath):
            os.remove(f'{tmp_video_clips_folderpath}/{filename}')
    if not regen:
        if os.listdir(tmp_video_clips_folderpath) != []: return
    if os.listdir(tmp_video_clips_folderpath) != []: return
    ### gen
    tmp_slide_filepath = f'{tmp_slide_folderpath}/slide.jpg'
    tmp_audio_clip_filepath = f'{tmp_audio_clips_folderpath}/0000.wav'
    tmp_video_clip_filepath = f'{tmp_video_clips_folderpath}/video_clip.mp4'
    import subprocess
    subprocess.run([
        f'ffmpeg',
        f'-loop', f'1',
        f'-i', f'{tmp_slide_filepath}',
        f'-i', f'{tmp_audio_clip_filepath}',
        f'-c:v', f'libx264',
        f'-tune', f'stillimage',
        f'-c:a', f'aac',
        f'-b:a', f'192k',
        f'-shortest',
        f'-pix_fmt', f'yuv420p',
        f'{tmp_video_clip_filepath}',
        f'-y',
    ])

def video_clips_gen(lesson_section_index, script_chunk_index, regen=False, dispel=False):
    tmp_section_folderpath = f'{tmp_lesson_folderpath}/{lesson_section_index}'
    tmp_script_chunk_folderpath = f'{tmp_section_folderpath}/{script_chunk_index}'
    tmp_slide_folderpath = f'{tmp_script_chunk_folderpath}/slides'
    tmp_audio_clips_folderpath = f'{tmp_script_chunk_folderpath}/audio-clips'
    tmp_video_clips_folderpath = f'{tmp_script_chunk_folderpath}/video-clips'
    ### clean
    try: os.mkdir(tmp_script_chunk_folderpath)
    except: pass
    try: os.mkdir(tmp_video_clips_folderpath)
    except: pass
    if dispel: 
        for filename in os.listdir(tmp_video_clips_folderpath):
            os.remove(f'{tmp_video_clips_folderpath}/{filename}')
    if not regen:
        if os.listdir(tmp_video_clips_folderpath) != []: return
    if os.listdir(tmp_video_clips_folderpath) != []: return
    ### gen
    tmp_slide_filepath = f'{tmp_slide_folderpath}/slide.jpg'
    tmp_audio_clip_filepath = f'{tmp_audio_clips_folderpath}/audio-clip.wav'
    tmp_video_clip_filepath = f'{tmp_video_clips_folderpath}/video-clip.mp4'
    import subprocess
    subprocess.run([
        f'ffmpeg',
        f'-loop', f'1',
        f'-i', f'{tmp_slide_filepath}',
        f'-i', f'{tmp_audio_clip_filepath}',
        f'-c:v', f'libx264',
        f'-tune', f'stillimage',
        f'-c:a', f'aac',
        f'-b:a', f'192k',
        f'-shortest',
        f'-pix_fmt', f'yuv420p',
        f'{tmp_video_clip_filepath}',
        f'-y',
    ])

def section_video_gen(lesson_section_index, script_chunks_indices, regen=False, dispel=False):
    tmp_section_folderpath = f'{tmp_lesson_folderpath}/{lesson_section_index}'
    tmp_video_clips_folderpath = f'{tmp_section_folderpath}/video-clip'
    tmp_concat_filepath = f'{tmp_video_clips_folderpath}/concat.txt'
    ### clean
    try: os.mkdir(tmp_video_clips_folderpath)
    except: pass
    if dispel: 
        for filename in os.listdir(tmp_video_clips_folderpath):
            os.remove(f'{tmp_video_clips_folderpath}/{filename}')
    if not regen:
        if os.listdir(tmp_video_clips_folderpath) != []: return
    if os.listdir(tmp_video_clips_folderpath) != []: return
    ### gen
    with open(tmp_concat_filepath, 'w') as f:
        for script_chunk_index in script_chunks_indices:
            tmp_video_clip_filepath = f'{tmp_section_folderpath}/{script_chunk_index}/video-clips/video-clip.mp4'
            f.write(f"file '{tmp_video_clip_filepath}'\n")
            # subprocess.Popen(['vlc', '--play-and-exit', f'{tmp_video_clip_filepath}'])
            # quit()
    ###
    tmp_video_clips_filepath = f'{tmp_video_clips_folderpath}/video-clip.mp4'
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{tmp_concat_filepath}',
        f'-c', f'copy',
        f'{tmp_video_clips_filepath}',
        f'-y', 
    ])

def lesson_video_gen(lesson_sections_indices, regen=False, dispel=False):
    tmp_video_clip_folderpath = f'{tmp_lesson_folderpath}/video-clip'
    tmp_concat_filepath = f'{tmp_video_clip_folderpath}/concat.txt'
    ### clean
    try: os.mkdir(tmp_video_clip_folderpath)
    except: pass
    if dispel: 
        for filename in os.listdir(tmp_video_clip_folderpath):
            os.remove(f'{tmp_video_clip_folderpath}/{filename}')
    if not regen:
        if os.listdir(tmp_video_clip_folderpath) != []: return
    if os.listdir(tmp_video_clip_folderpath) != []: return
    ### gen
    with open(tmp_concat_filepath, 'w') as f:
        for lesson_section_index in lesson_sections_indices:
            tmp_video_clip_filepath = f'{tmp_lesson_folderpath}/{lesson_section_index}/video-clip/video-clip.mp4'
            f.write(f"file '{tmp_video_clip_filepath}'\n")
    ###
    tmp_video_clip_filepath = f'{tmp_video_clip_folderpath}/video-clip.mp4'
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{tmp_concat_filepath}',
        f'-c', f'copy',
        f'{tmp_video_clip_filepath}',
        f'-y', 
    ])

def course_video_gen(lessons_slugs, regen=False, dispel=False):
    dst_concat_filepath = f'{dst_folderpath}/concat.txt'
    ### clean
    if dispel: 
        for filename in os.listdir(dst_folderpath):
            os.remove(f'{dst_folderpath}/{filename}')
    if not regen:
        if os.listdir(dst_folderpath) != []: return
    ### gen
    with open(dst_concat_filepath, 'w') as f:
        for lesson_slug in lessons_slugs:
            tmp_course_video_filepath = f'{tmp_folderpath}/{lesson_slug}/video-clip/video-clip.mp4'
            f.write(f"file '{tmp_course_video_filepath}'\n")
    ###
    dst_course_video_filepath = f'{dst_folderpath}/course-video.mp4'
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{dst_concat_filepath}',
        f'-c', f'copy',
        f'{dst_course_video_filepath}',
        f'-y', 
    ])

### OUTLINE
outline = {
    'modules': [
        {
            'name': '02-materials',
            'lessons': [
                 {'name': '01-ingredients',},
                 {'name': '02-equipment',},
            ],
        },
        {
            'name': '03-preparation',
            'lessons': [
                 {'name': '01-step-1',},
                 {'name': '02-step-2',},
                 {'name': '03-step-3',},
            ],
        },
    ],
}

lessons_slugs = []
for module in outline['modules']:
    module_name = module['name']
    for lesson in module['lessons']:
        lesson_name = lesson['name']
        lessons_slugs.append(f'{module_name}/{lesson_name}')

# for lesson_slug in lessons_slugs:
    # print(lesson_slug)

dst_folderpath = f'{course_folderpath}/dst'
tmp_folderpath = f'{course_folderpath}/tmp'
### LESSONS
for lesson_slug in lessons_slugs:
    module_foldername, lesson_foldername = lesson_slug.split('/')
    ### TODO: remove line
    if lesson_foldername != '02-equipment': continue
    ### LESSON
    src_module_folderpath = f'{course_folderpath}/src/{module_foldername}'
    tmp_module_folderpath = f'{course_folderpath}/tmp/{module_foldername}'
    src_lesson_folderpath = f'{src_module_folderpath}/{lesson_foldername}'
    tmp_lesson_folderpath = f'{tmp_module_folderpath}/{lesson_foldername}'
    src_script_filepath = f'{src_lesson_folderpath}/script.txt'
    try: os.mkdir(tmp_module_folderpath)
    except: pass
    try: os.mkdir(tmp_lesson_folderpath)
    except: pass
    with open(src_script_filepath) as f: script_text = f.read()
    ### LESSON SECTION
    lesson_sections = script_text.split('===')
    lesson_sections_indices = []
    for lesson_section_i, lesson_section in enumerate(lesson_sections):
        lesson_section = lesson_sections[lesson_section_i]
        if lesson_section_i >= 10000: lesson_section_index = f'section-{lesson_section_i}'
        elif lesson_section_i >= 1000: lesson_section_index = f'section-0{lesson_section_i}'
        elif lesson_section_i >= 100: lesson_section_index = f'section-00{lesson_section_i}'
        elif lesson_section_i >= 10: lesson_section_index = f'section-000{lesson_section_i}'
        else: lesson_section_index = f'section-0000{lesson_section_i}'
        lesson_sections_indices.append(lesson_section_index)
        ### LESSON CHUNKS
        lesson_section_chunks = lesson_section.split('---')
        lesson_section_chunks_indices = []
        for lesson_section_chunk_i, lesson_section_chunk in enumerate(lesson_section_chunks):
            lesson_section_chunk_index = ''
            if lesson_section_chunk_i >= 10000: lesson_section_chunk_index = f'chunk-{lesson_section_chunk_i}'
            elif lesson_section_chunk_i >= 1000: lesson_section_chunk_index = f'chunk-0{lesson_section_chunk_i}'
            elif lesson_section_chunk_i >= 100: lesson_section_chunk_index = f'chunk-00{lesson_section_chunk_i}'
            elif lesson_section_chunk_i >= 10: lesson_section_chunk_index = f'chunk-000{lesson_section_chunk_i}'
            else: lesson_section_chunk_index = f'chunk-0000{lesson_section_chunk_i}'
            lesson_section_chunks_indices.append(lesson_section_chunk_index)
            if 1:
                audio_clips_chunks_gen(
                    lesson_section_index, lesson_section_chunk_index, lesson_section_chunk, 
                    regen=True, dispel=True,
                )
            if 1:
                audio_clips_gen(
                    lesson_section_index, lesson_section_chunk_index, lesson_section_chunk, 
                    regen=True, dispel=True,
                )
            if 1:
                slides_gen(
                    lesson_section_index, lesson_section_chunk_index, lesson_section_i, lesson_section_chunk_i, 
                    regen=True, dispel=True,
            )
            if 1:
                video_clips_gen(
                    lesson_section_index, lesson_section_chunk_index, 
                    regen=True, dispel=True,
            )
            # video_clips_gen(lesson_section_chunk_index, regen=True, dispel=True)
            # quit()
        if 1:
            section_video_gen(lesson_section_index, lesson_section_chunks_indices, regen=True, dispel=True)
        # quit()
    if 1:
        lesson_video_gen(lesson_sections_indices, regen=True, dispel=True)

course_video_gen(lessons_slugs, regen=True, dispel=True)

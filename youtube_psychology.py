import os
import re
import sys
import time
import random
import shutil

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
from lib import g
from lib import llm
from lib import media
from lib import zimage

hub_folderpath = f'/home/ubuntu/vault/audiobook/psychology'

with open(f'{hub_folderpath}/ideas.txt') as f: ideas = f.read().strip().split('\n')

def index_to_string(i):
    i_str = ''
    if i >= 1000: i_str = f'{i}'
    elif i >= 100: i_str = f'0{i}'
    elif i >= 10: i_str = f'00{i}'
    else: i_str = f'000{i}'
    return i_str

def sluggify(text):
    slug = text.strip().lower().replace(' ', '-').replace("'", '')
    return slug

def lines_get(final_filepath):
    with open(final_filepath) as f: final_content = f.read()
    if final_content.strip() == '': 
        print('ERR: No content in final.txt')
        quit()
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
    return image_lines, text_lines

def audio_clips_gen(regen=False):
    from kokoro import KPipeline
    import soundfile as sf 
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-').replace("'", '')
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        print(final_filepath)
        if not os.path.exists(f'{video_folderpath}'):
            os.makedirs(f'{video_folderpath}')
        if not os.path.exists(f'{video_folderpath}/tmp'):
            os.makedirs(f'{video_folderpath}/tmp')
        if not os.path.exists(f'{video_folderpath}/tmp/audio-clips'):
            os.makedirs(f'{video_folderpath}/tmp/audio-clips')
        for filename in os.listdir(f'{video_folderpath}/tmp/audio-clips'):
            os.remove(f'{video_folderpath}/tmp/audio-clips/{filename}')
        image_lines, text_lines = lines_get(final_filepath)
        for line in text_lines:
            print(line)
        print(len(text_lines))
        # quit()
        j = 0
        pipeline = KPipeline(lang_code='a')
        for scene in text_lines:
            text = scene
            generator = pipeline(
                text, 
                voice='am_michael',
                speed = 1.1,
            )
            for (gs, ps, audio) in generator:
                print(j, gs, ps)
                j_str = ''
                if j >= 1000: j_str = f'{j}'
                elif j >= 100: j_str = f'0{j}'
                elif j >= 10: j_str = f'00{j}'
                else: j_str = f'000{j}'
                sf.write(f'{video_folderpath}/tmp/audio-clips/audio-{j_str}.wav', audio, 24000)
                j += 1

def video_clips_gen(regen=False):
    import subprocess
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-').replace("'", '')
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        print(final_filepath)
        if not os.path.exists(f'{video_folderpath}'):
            os.makedirs(f'{video_folderpath}')
        if not os.path.exists(f'{video_folderpath}/tmp'):
            os.makedirs(f'{video_folderpath}/tmp')
        if not os.path.exists(f'{video_folderpath}/tmp/video-clips'):
            os.makedirs(f'{video_folderpath}/tmp/video-clips')
        for filename in os.listdir(f'{video_folderpath}/tmp/video-clips'):
            os.remove(f'{video_folderpath}/tmp/video-clips/{filename}')
        ### gen
        audio_filenames = sorted(os.listdir(f'{video_folderpath}/tmp/audio-clips'))
        for i, audio_filename in enumerate(audio_filenames):
            audio_filepath = f'{video_folderpath}/tmp/audio-clips/{audio_filename}'
            i_str = ''
            if i >= 1000: i_str = f'{i}'
            elif i >= 100: i_str = f'0{i}'
            elif i >= 10: i_str = f'00{i}'
            else: i_str = f'000{i}'
            slide_filepath = f'{video_folderpath}/tmp/images-formatted/img-{i_str}.jpg'
            video_filepath = f'{video_folderpath}/tmp/video-clips/video-{i_str}.mp4'
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

def video_final_gen(regen=False):
    import subprocess
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-').replace("'", '')
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        print(final_filepath)
        ###
        if not os.path.exists(f'{video_folderpath}'):
            os.makedirs(f'{video_folderpath}')
        if not os.path.exists(f'{video_folderpath}/tmp'):
            os.makedirs(f'{video_folderpath}/tmp')
        if not os.path.exists(f'{video_folderpath}/tmp/video-final'):
            os.makedirs(f'{video_folderpath}/tmp/video-final')
        if regen: 
            for filename in os.listdir(f'{video_folderpath}/tmp/video-final'):
                if filename.endswith('.mp4'):
                    os.remove(f'{video_folderpath}/tmp/video-final/{filename}')
        video_clips_filenames = sorted(os.listdir(f'{video_folderpath}/tmp/video-clips'))
        concat_filepath = f'{video_folderpath}/tmp/video-concat.txt'
        with open(concat_filepath, 'w') as f:
            for i, video_clip_filename in enumerate(video_clips_filenames):
                video_clip_filepath = f'{video_folderpath}/tmp/video-clips/{video_clip_filename}'
                f.write(f"file '{video_clip_filepath}'\n")
        with open(f'{video_folderpath}/tmp/video-final/title.txt') as f: title = f.read().strip().lower().replace(' ', '-')
        video_final_filepath = f'{video_folderpath}/tmp/video-final/{title}.mp4'
        subprocess.run([
            f'ffmpeg',
            f'-f', f'concat',
            f'-safe', f'0',
            f'-i', f'{concat_filepath}',
            f'-c', f'copy',
            f'{video_final_filepath}',
            f'-y', 
        ])
        print(video_folderpath)
        print(concat_filepath)
        print(video_final_filepath)
        # quit()

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

def init():
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        print(final_filepath)
        ###
        try: os.makedirs(f'{video_folderpath}')
        except: pass
        try: os.makedirs(f'{video_folderpath}/tmp')
        except: pass
        try: os.makedirs(f'{video_folderpath}/tmp/texts')
        except: pass
        if not os.path.exists(final_filepath):
            with open(final_filepath, 'w') as f: f.write('')
        try: os.makedirs(f'{video_folderpath}/tmp/images')
        except: pass

def images_gen_test():
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        running = True
        while running:
            i_str = index_to_string(idea_i)
            idea_slug = sluggify(idea)
            ###
            video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
            script_filepath = f'{video_folderpath}/tmp/texts/final.txt'
            output_folderpath = f'{hub_folderpath}/test-images'
            ###
            # for filename in os.listdir(f'{output_folderpath}'):
                # os.remove(f'{output_folderpath}/{filename}')
            ###
            image_lines, text_lines = lines_get(script_filepath)
            for line_i, line in enumerate(image_lines):
                line = line.strip().replace('.', '')
                i_str = index_to_string(line_i)
                ###
                output_filepath = f'{output_folderpath}/{i_str}.jpg'
                # if os.path.exists(output_filepath): continue
                with open(f'{hub_folderpath}/prompt.txt') as f: prompt = f.read()
                prompt = prompt.replace('[line]', line)
                if 0:
                    prompt = f'''
                        {line},
                        cartoon,
                        line art,
                        black and white,
                        clean white background,
                        illustration,
                        sketch,
                        hand drawn,
                        doodle,
                        imperfect lines,
                        minimalist,
                    '''
                print(prompt)
                print()
                image = zimage.image_create(output_filepath=output_filepath, prompt=prompt, width=768, height=768, seed=-1)
                print(image_lines)
                print(output_filepath)
            ###
            command = input('>> ')
            if command.strip() != '':
                running = False
        return

def images_gen(regen=False):
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        print(final_filepath)
        ###
        if regen: 
            for filename in os.listdir(f'{video_folderpath}/tmp/images'):
                os.remove(f'{video_folderpath}/tmp/images/{filename}')
        ###
        image_lines, text_lines = lines_get(final_filepath)
        line_i = 0
        for line in image_lines[:999]:
            line = line.strip().replace('.', '')
            i_str = index_to_string(line_i)
            line_i += 1
            output_filepath = f'{video_folderpath}/tmp/images/{i_str}.jpg'
            if os.path.exists(output_filepath): continue
            # with open(f'{video_folderpath}/tmp/prompts/prompt.txt') as f: prompt = f.read()
            with open(f'{hub_folderpath}/prompt.txt') as f: prompt = f.read()
            prompt = prompt.replace('[line]', line)
            if 0:
                prompt = f'''
                    {line},
                    cartoon,
                    line art,
                    black and white,
                    clean white background,
                    illustration,
                    sketch,
                    hand drawn,
                    doodle,
                    imperfect lines,
                    minimalist,
                '''
            print(prompt)
            print()
            image = zimage.image_create(output_filepath=output_filepath, prompt=prompt, width=1024, height=1024, seed=-1)
            print(image_lines)
            print(output_filepath)
        # return

def text_to_lines(text, font, max_w):
    lines = []
    line = ''
    for word in text.split():
        _, _, word_w, word_h = font.getbbox(word)
        _, _, line_w, line_h = font.getbbox(line.strip())
        if  line_w + word_w < max_w:
            line += f'{word} '
        else:
            lines.append(line.strip())
            line = f'{word} '
    if line.strip() != '':
        lines.append(line.strip())
    return lines

def images_formatted_gen(regen=False):
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-').replace("'", '')
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        print(final_filepath)
        ###
        try: os.makedirs(f'{video_folderpath}/tmp/images-formatted')
        except: pass
        if regen: 
            for filename in os.listdir(f'{video_folderpath}/tmp/images-formatted'):
                os.remove(f'{video_folderpath}/tmp/images-formatted/{filename}')
        ###
        image_lines, text_lines = lines_get(final_filepath)
        for image_line_i, image_line in enumerate(image_lines[:999]):
            image_line = image_line.strip().replace('.', '')
            i_str = ''
            if image_line_i >= 1000: i_str = f'{image_line_i}'
            elif image_line_i >= 100: i_str = f'0{image_line_i}'
            elif image_line_i >= 10: i_str = f'00{image_line_i}'
            else: i_str = f'000{image_line_i}'
            img = Image.new(mode="RGB", size=(1080, 1920), color='#ffffff')
            draw = ImageDraw.Draw(img)
            img_0000 = Image.open(f'{video_folderpath}/tmp/images/img-{i_str}.jpg')
            img_0000 = media.resize(img_0000, 1080, 1080)
            img.paste(img_0000, (0, int(1920*0.66)-(1080//2)))
            caption_content = text_lines[image_line_i]
            caption_content = caption_content.replace('—', ', ')
            caption_content = caption_content.replace('’', "'")
            font_size = 80
            font_family, font_weight = 'Lato', 'Bold'
            font_path = f"{g.VAULT_FOLDERPATH}/terrawhisper/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
            font = ImageFont.truetype(font_path, font_size)
            caption_lines = text_to_lines(caption_content, font, 1000)
            # caption_lines = caption_content.split()
            for caption_line_i, caption_line in enumerate(caption_lines):
                _, _, caption_line_w, caption_line_h = font.getbbox(caption_line)
                draw.text((1080//2 - caption_line_w//2, int(1920*0.20)-((font_size*len(caption_lines))//2) + font_size*caption_line_i), caption_line, '#000000', font=font)
            img_filepath = f'{video_folderpath}/tmp/images-formatted/img-{i_str}.jpg'
            img.save(img_filepath, format='JPEG', subsampling=0, quality=100)

def video_final_title_gen(regen=False):
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        print(idea_i, ideas_num_min)
        print(idea_i, ideas_num_max)
        print()
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-').replace("'", '')
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        output_filepath = f'{video_folderpath}/tmp/video-final/title.txt'
        ###
        if not os.path.exists(f'{video_folderpath}'):
            os.makedirs(f'{video_folderpath}')
        if not os.path.exists(f'{video_folderpath}/tmp'):
            os.makedirs(f'{video_folderpath}/tmp')
        if not os.path.exists(f'{video_folderpath}/tmp/video-final'):
            os.makedirs(f'{video_folderpath}/tmp/video-final')
        if regen: 
            if os.path.exists(output_filepath):
                os.remove(output_filepath)
        if not os.path.exists(output_filepath):
            prompt = f'''
                Write a title for a youtube video short about the following idea: {idea}.
                Start with the following words: "Psychology of People Who ".
                Never use the character colon.
                Write less than 10 words.
                /no_think
            '''
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            print('#################################################')
            print(reply)
            print(output_filepath)
            print('#################################################')
            with open(output_filepath, 'w') as f: f.write(reply)

def video_final_description_gen(regen=False):
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-').replace("'", '')
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        output_filepath = f'{video_folderpath}/tmp/video-final/description.txt'
        script_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        ###
        if not os.path.exists(f'{video_folderpath}'):
            os.makedirs(f'{video_folderpath}')
        if not os.path.exists(f'{video_folderpath}/tmp'):
            os.makedirs(f'{video_folderpath}/tmp')
        if not os.path.exists(f'{video_folderpath}/tmp/video-final'):
            os.makedirs(f'{video_folderpath}/tmp/video-final')
        if regen: 
            if os.path.exists(output_filepath):
                os.remove(output_filepath)
        # with open(f'{video_folderpath}/tmp/video-final/title.txt') as f: title = f.read()
        title = idea
        image_lines, text_lines = lines_get(script_filepath)
        content = '\n'.join(text_lines)
        if not os.path.exists(output_filepath):
            prompt = f'''
                Write a description for a youtube video short about the following title: 
                {title}.
                Here's the content of the video:
                {content}
                Reply with a paragraph.
                Start the reply with these words: "Based on psychology, "
                /no_think
            '''
            print(prompt)
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            print('#################################################')
            print(reply)
            print(output_filepath)
            print('#################################################')
            with open(output_filepath, 'w') as f: f.write(reply)

def video_final_tags_gen(regen=False):
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-').replace("'", '')
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        script_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        output_filepath = f'{video_folderpath}/tmp/video-final/tags.txt'
        ###
        if not os.path.exists(f'{video_folderpath}'):
            os.makedirs(f'{video_folderpath}')
        if not os.path.exists(f'{video_folderpath}/tmp'):
            os.makedirs(f'{video_folderpath}/tmp')
        if not os.path.exists(f'{video_folderpath}/tmp/video-final'):
            os.makedirs(f'{video_folderpath}/tmp/video-final')
        if regen: 
            if os.path.exists(output_filepath):
                os.remove(output_filepath)
        # with open(f'{video_folderpath}/tmp/video-final/title.txt') as f: title = f.read()
        title = idea
        image_lines, text_lines = lines_get(script_filepath)
        content = '\n'.join(text_lines)
        if not os.path.exists(output_filepath):
            prompt = f'''
                Write a list of tags for a youtube video short about the following title: 
                {title}.
                Here's the content of the video:
                {content}
                Reply in less than 500 characters.
                Reply only with the list of tags separated by commas.
                /no_think
            '''
            print(prompt)
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            print('#################################################')
            print(reply)
            print(output_filepath)
            print('#################################################')
            with open(output_filepath, 'w') as f: f.write(reply)

def video_final_preview():
    import subprocess
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        # with open(f'{video_folderpath}/tmp/video-final/title.txt') as f: title = f.read().strip().lower().replace(' ', '-')
        title = sluggify(idea)
        # video_filepath = f'{video_folderpath}/tmp/video-final/{title}.mp4'
        # video_prev_filepath = f'{hub_folderpath}/video-preview/{i_str}-{idea_slug}.mp4'
        # shutil.copy2(f'{video_filepath}', f'{video_prev_filepath}')
        video_filepath = f'{video_folderpath}/tmp/video-animated/{title}.mp4'
        video_preview_filepath = f'{hub_folderpath}/video-preview/{i_str}-{idea_slug}.mp4'
        shutil.copy2(f'{video_filepath}', f'{video_preview_filepath}')

def version_animated_image_background_text(regen=False):
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_script_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        output_folderpath = f'{video_folderpath}/tmp/images-animated-backgrounds-texts'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        ###
        image_lines, text_lines = lines_get(input_script_filepath)
        for image_line_i, image_line in enumerate(image_lines[:999]):
            image_line = image_line.strip().replace('.', '')
            i_str = index_to_string(image_line_i)
            img = Image.new(mode="RGB", size=(1080, 1920), color='#ffffff')
            draw = ImageDraw.Draw(img)
            # img_0000 = Image.open(f'{video_folderpath}/tmp/images/img-{i_str}.jpg')
            # img_0000 = media.resize(img_0000, 1080, 1080)
            # img.paste(img_0000, (0, int(1920*0.66)-(1080//2)))
            caption_content = text_lines[image_line_i]
            caption_content = caption_content.replace('—', ', ')
            caption_content = caption_content.replace('’', "'")
            font_size = 80
            font_family, font_weight = 'Lato', 'Bold'
            font_path = f"{g.VAULT_FOLDERPATH}/terrawhisper/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
            font = ImageFont.truetype(font_path, font_size)
            caption_lines = text_to_lines(caption_content, font, 1000)
            # caption_lines = caption_content.split()
            for caption_line_i, caption_line in enumerate(caption_lines):
                _, _, caption_line_w, caption_line_h = font.getbbox(caption_line)
                draw.text((1080//2 - caption_line_w//2, int(1920*0.20)-((font_size*len(caption_lines))//2) + font_size*caption_line_i), caption_line, '#000000', font=font)
            img_filepath = f'{output_folderpath}/{i_str}.jpg'
            img.save(img_filepath, format='JPEG', subsampling=0, quality=100)

def video_clips_animated_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_images_folderpath = f'{video_folderpath}/tmp/images-animated-backgrounds-texts'
        input_audios_folderpath = f'{video_folderpath}/tmp/audio-clips'
        # input_videos_folderpath = f'{video_folderpath}/tmp/images-animated'
        input_videos_folderpath = f'{video_folderpath}/tmp/images-animated-selected'
        output_folderpath = f'{video_folderpath}/tmp/video-clips-animated'
        ###
        if not os.path.exists(f'{output_folderpath}'):
            os.makedirs(f'{output_folderpath}')
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                if filename.endswith('.mp4'):
                    os.remove(f'{output_folderpath}/{filename}')
        ### gen
        audio_filenames = sorted(os.listdir(input_audios_folderpath))
        for i, audio_filename in enumerate(audio_filenames):
            i_str = index_to_string(i)
            input_image_filepath = f'{input_images_folderpath}/{i_str}.jpg'
            input_video_filename = sorted(os.listdir(input_videos_folderpath))[i]
            # input_video_filepath = f'{input_videos_folderpath}/{i_str}.mp4'
            input_video_filepath = f'{input_videos_folderpath}/{input_video_filename}'
            input_audio_filepath = f'{input_audios_folderpath}/{audio_filename}'
            output_video_filepath = f'{output_folderpath}/{i_str}.mp4'
            import subprocess
            subprocess.run([
                f'ffmpeg',
                f'-loop', f'1', f'-i', f'{input_image_filepath}',
                f'-stream_loop', f'-1', f'-i', f'{input_video_filepath}',
                f'-i', f'{input_audio_filepath}',
                f'-filter_complex', f'[1:v]scale=1080:1080[vid];[0:v][vid]overlay=0:840',
                f'-map', f'2:a',
                f'-shortest',
                f'-c:v', f'libx264',
                f'-pix_fmt', f'yuv420p',
                f'-c:a', f'aac',
                f'{output_video_filepath}',
                f'-y',
            ])
            '''
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
            '''

def video_animated_final_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_videos_folderpath = f'{video_folderpath}/tmp/video-clips-animated'
        output_folderpath = f'{video_folderpath}/tmp/video-animated'
        concat_filepath = f'{video_folderpath}/tmp/video-concat.txt'
        ###
        if not os.path.exists(f'{output_folderpath}'):
            os.makedirs(f'{output_folderpath}')
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                if filename.endswith('.mp4'):
                    os.remove(f'{output_folderpath}/{filename}')
        input_videos_filenames = sorted(os.listdir(f'{input_videos_folderpath}'))
        with open(concat_filepath, 'w') as f:
            for i, input_video_filename in enumerate(input_videos_filenames):
                input_video_filepath = f'{input_videos_folderpath}/{input_video_filename}'
                f.write(f"file '{input_video_filepath}'\n")
        # with open(f'{video_folderpath}/tmp/video-final/title.txt') as f: title = f.read().strip().lower().replace(' ', '-')
        output_filepath = f'{output_folderpath}/{idea_slug}.mp4'
        import subprocess
        subprocess.run([
            f'ffmpeg',
            f'-f', f'concat',
            f'-safe', f'0',
            f'-i', f'{concat_filepath}',
            f'-c', f'copy',
            f'{output_filepath}',
            f'-y', 
        ])

def video_clips_gradio_gen(regen=False, dispel=False):
    import pyautogui
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/home/ubuntu/.config/google-chrome/SeleniumProfile")
    chrome_options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com")
    driver.maximize_window()
    ### reload page
    # driver.get("http://localhost:7860/")
    # time.sleep(5)
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        idea_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_images_folderpath = f'{idea_folderpath}/tmp/images'
        input_script_folderpath = f'{idea_folderpath}/tmp/texts'
        output_folderpath = f'{idea_folderpath}/tmp/images-animated'
        ###
        if not os.path.exists(f'{output_folderpath}'):
            os.makedirs(f'{output_folderpath}')
        if dispel: 
            for filename in os.listdir(f'{output_folderpath}'):
                if filename.endswith('.mp4'):
                    os.remove(f'{output_folderpath}/{filename}')
        ###
        input_script_filepath = f'{input_script_folderpath}/final.txt'
        image_lines, text_lines = lines_get(input_script_filepath)
        for clip_i in range(len(image_lines)):
            ### adjust number of tries, and name the output files progressively (0000-0000, 0000-0001)
            for i in range(4):
                clip_i_str = index_to_string(clip_i)
                output_filepath = f'{idea_folderpath}/tmp/images-animated/{clip_i_str}-{i}.mp4'
                if os.path.exists(output_filepath): continue
                # input(f'>> PRESS ANY KEY FOR NEXT GENERATION (clip {clip_i})')
                image_line = image_lines[clip_i]
                image_line = image_line.replace('.', ',') + ' live wallpaper style'
                print(image_line)
                ###
                input_image_filepath = f'{input_images_folderpath}/{sorted(os.listdir(input_images_folderpath))[clip_i]}'
                print(input_image_filepath)
                ### reload page
                driver.get("http://localhost:7860/")
                time.sleep(5)
                ### prompt image
                e = driver.find_element(By.XPATH, '//input[@type="file"]')
                img_filepath = input_image_filepath
                e.send_keys(f'{img_filepath}') 
                time.sleep(1)
                ### prompt text
                pyautogui.moveTo(500, 1100)
                pyautogui.click()
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('delete')
                time.sleep(1)
                prompt = image_line
                e = driver.find_element(By.XPATH, "//span[contains(text(), 'Prompts')]/following-sibling::div//textarea")
                driver.execute_script("arguments[0].focus();", e)
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
                actions.send_keys(prompt)
                actions.perform()
                ### gen video
                e = driver.find_element(By.XPATH, '//button[text()="Generate"]')
                e.click()
                ### save video
                for _ in range(60):
                    try:
                        video = driver.find_element(By.XPATH, "//video[@data-testid='detailed-video']")
                    except:
                        time.sleep(5)
                        continue
                    video_url = video.get_attribute("src")
                    import requests
                    video_url = video.get_attribute("src")
                    # Download the video
                    response = requests.get(video_url, stream=True)
                    response.raise_for_status()  # make sure the request worked
                    with open(output_filepath, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    print(f"Video saved")
                time.sleep(5)

def video_clips_wan2gp_manual_gen(regen=False, dispel=False):
    import pyautogui
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/home/ubuntu/.config/google-chrome/SeleniumProfile")
    chrome_options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com")
    driver.maximize_window()
    ### reload page
    # driver.get("http://localhost:7860/")
    # time.sleep(5)
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        idea_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_images_folderpath = f'{idea_folderpath}/tmp/images'
        input_script_folderpath = f'{idea_folderpath}/tmp/texts'
        output_folderpath = f'{idea_folderpath}/tmp/images-animated'
        ###
        if not os.path.exists(f'{output_folderpath}'):
            os.makedirs(f'{output_folderpath}')
        if dispel: 
            for filename in os.listdir(f'{output_folderpath}'):
                if filename.endswith('.mp4'):
                    os.remove(f'{output_folderpath}/{filename}')
        ###
        input_script_filepath = f'{input_script_folderpath}/final.txt'
        image_lines_for, _ = lines_get(input_script_filepath)
        for clip_i in range(len(image_lines_for)):
            image_lines, _ = lines_get(input_script_filepath)
            i = 0
            ### adjust number of tries, and name the output files progressively (0000-0000, 0000-0001)
            clip_i_str = index_to_string(clip_i)
            output_filepath = f'{idea_folderpath}/tmp/images-animated/{clip_i_str}-{i}.mp4'
            print(output_filepath)
            if os.path.exists(output_filepath): continue
            repeat = True
            while repeat:
                # input(f'>> PRESS ANY KEY FOR NEXT GENERATION (clip {clip_i})')
                image_line = image_lines[clip_i]
                image_line = image_line.replace('.', ',') + ' live wallpaper style'
                print(image_line)
                ###
                input_image_filepath = f'{input_images_folderpath}/{sorted(os.listdir(input_images_folderpath))[clip_i]}'
                print(input_image_filepath)
                ### reload page
                driver.get("http://localhost:7860/")
                time.sleep(5)
                ### prompt image
                e = driver.find_element(By.XPATH, '//input[@type="file"]')
                img_filepath = input_image_filepath
                e.send_keys(f'{img_filepath}') 
                time.sleep(1)
                ### prompt text
                pyautogui.moveTo(500, 1100)
                pyautogui.click()
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('delete')
                time.sleep(1)
                prompt = image_line
                e = driver.find_element(By.XPATH, "//span[contains(text(), 'Prompts')]/following-sibling::div//textarea")
                driver.execute_script("arguments[0].focus();", e)
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
                actions.send_keys(prompt)
                actions.perform()
                ### gen video
                e = driver.find_element(By.XPATH, '//button[text()="Generate"]')
                e.click()
                ### save video
                for _ in range(60):
                    try:
                        video = driver.find_element(By.XPATH, "//video[@data-testid='detailed-video']")
                    except:
                        time.sleep(5)
                        continue
                    video_url = video.get_attribute("src")
                    import requests
                    video_url = video.get_attribute("src")
                    # Download the video
                    response = requests.get(video_url, stream=True)
                    response.raise_for_status()  # make sure the request worked
                    with open(output_filepath, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    print(f"Video saved")
                time.sleep(5)
                cmd = input('>> ').strip()
                if cmd == '':
                    repeat = False

def video_clips_wan2gp_auto_gen(regen=False, dispel=False):
    import pyautogui
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/home/ubuntu/.config/google-chrome/SeleniumProfile")
    chrome_options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com")
    driver.maximize_window()
    ### reload page
    # driver.get("http://localhost:7860/")
    # time.sleep(5)
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        idea_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_images_folderpath = f'{idea_folderpath}/tmp/images'
        input_script_folderpath = f'{idea_folderpath}/tmp/texts'
        output_folderpath = f'{idea_folderpath}/tmp/images-animated'
        ###
        if not os.path.exists(f'{output_folderpath}'):
            os.makedirs(f'{output_folderpath}')
        if dispel: 
            for filename in os.listdir(f'{output_folderpath}'):
                if filename.endswith('.mp4'):
                    os.remove(f'{output_folderpath}/{filename}')
        ###
        input_script_filepath = f'{input_script_folderpath}/final.txt'
        image_lines_for, _ = lines_get(input_script_filepath)
        for clip_i in range(len(image_lines_for)):
            image_lines, _ = lines_get(input_script_filepath)
            # i = 0
            ### adjust number of tries, and name the output files progressively (0000-0000, 0000-0001)
            clip_i_str = index_to_string(clip_i)
            for i in range(4):
                output_filepath = f'{idea_folderpath}/tmp/images-animated/{clip_i_str}-{i}.mp4'
                print(output_filepath)
                if os.path.exists(output_filepath): continue
                # input(f'>> PRESS ANY KEY FOR NEXT GENERATION (clip {clip_i})')
                image_line = image_lines[clip_i]
                image_line = image_line.replace('.', ',') + ' live wallpaper style'
                print(image_line)
                ###
                input_image_filepath = f'{input_images_folderpath}/{sorted(os.listdir(input_images_folderpath))[clip_i]}'
                print(input_image_filepath)
                ### reload page
                driver.get("http://localhost:7860/")
                time.sleep(5)
                ### prompt image
                e = driver.find_element(By.XPATH, '//input[@type="file"]')
                img_filepath = input_image_filepath
                e.send_keys(f'{img_filepath}') 
                time.sleep(1)
                ### prompt text
                pyautogui.moveTo(500, 1100)
                pyautogui.click()
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('delete')
                time.sleep(1)
                prompt = image_line
                e = driver.find_element(By.XPATH, "//span[contains(text(), 'Prompts')]/following-sibling::div//textarea")
                driver.execute_script("arguments[0].focus();", e)
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
                actions.send_keys(prompt)
                actions.perform()
                ### gen video
                e = driver.find_element(By.XPATH, '//button[text()="Generate"]')
                e.click()
                ### save video
                for _ in range(60):
                    try:
                        video = driver.find_element(By.XPATH, "//video[@data-testid='detailed-video']")
                    except:
                        time.sleep(5)
                        continue
                    video_url = video.get_attribute("src")
                    import requests
                    video_url = video.get_attribute("src")
                    # Download the video
                    response = requests.get(video_url, stream=True)
                    response.raise_for_status()  # make sure the request worked
                    with open(output_filepath, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    print(f"Video saved")
                time.sleep(5)

ideas_num_min = 60
ideas_num_max = 69
if 0:
    init()
    quit()
if 0:
    # images_gen_test()
    images_gen(regen=False)
    quit()
### generate videos with static images
if 0:
    images_formatted_gen(regen=False)
    video_final_title_gen(regen=False)
    video_final_description_gen(regen=False)
    video_final_tags_gen(regen=False)
    audio_clips_gen(regen=False)
    video_clips_gen(regen=False)
    video_final_gen(regen=False)
    video_final_preview()
### generate videos with animated images
if 0:
    video_clips_gradio_gen(regen=False, dispel=False)
if 0:
    video_clips_wan2gp_manual_gen(regen=False, dispel=False)
    quit()
if 1:
    video_clips_wan2gp_auto_gen(regen=False, dispel=False)
    quit()
if 1:
    # version_animated_image_background_text(regen=False)
    # images_formatted_gen(regen=False)
    # video_final_title_gen(regen=False)
    # video_final_description_gen(regen=False)
    # video_final_tags_gen(regen=False)
    # audio_clips_gen(regen=False)
    # video_clips_animated_gen(regen=False)
    # video_animated_final_gen(regen=False)
    video_final_preview()

# import subprocess
# subprocess.Popen(['vlc', '--play-and-exit', f'{video_folderpath}/tmp/video-final/video.mp4'])


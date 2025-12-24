import os
import re
import sys
import random
import shutil

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import llm
from lib import media
from lib import zimage

hub_folderpath = f'psychology'

def audio_clips_gen(regen=False):
    from kokoro import KPipeline
    import soundfile as sf 
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-')
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
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-')
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
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-')
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        print(final_filepath)
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
        else:
            return
        video_clips_filenames = sorted(os.listdir(f'{video_folderpath}/tmp/video-clips'))
        concat_filepath = f'{video_folderpath}/tmp/video-concat.txt'
        with open(concat_filepath, 'w') as f:
            for i, video_clip_filename in enumerate(video_clips_filenames):
                video_clip_filepath = f'/home/ubuntu/proj/audiobook/{video_folderpath}/tmp/video-clips/{video_clip_filename}'
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
    for i, idea in enumerate(ideas):
        if i < ideas_num_min or i >= ideas_num_max: continue
        print(idea)
        i_str = ''
        if i >= 1000: i_str = f'{i}'
        elif i >= 100: i_str = f'0{i}'
        elif i >= 10: i_str = f'00{i}'
        else: i_str = f'000{i}'
        idea_slug = idea.strip().lower().replace(' ', '-')
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        try: os.makedirs(f'{video_folderpath}')
        except: pass
        try: os.makedirs(f'{video_folderpath}/images')
        except: pass
        try: os.makedirs(f'{video_folderpath}/images-formatted')
        except: pass
        try: os.makedirs(f'{video_folderpath}/tmp')
        except: pass
        try: os.makedirs(f'{video_folderpath}/tmp/texts')
        except: pass
        if not os.path.exists(final_filepath):
            with open(final_filepath, 'w') as f: f.write('')
        try: os.makedirs(f'{video_folderpath}/tmp/images')
        except: pass
        # return  

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

def images_gen(regen=False):
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-')
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
            i_str = ''
            if line_i >= 1000: i_str = f'{line_i}'
            elif line_i >= 100: i_str = f'0{line_i}'
            elif line_i >= 10: i_str = f'00{line_i}'
            else: i_str = f'000{line_i}'
            line_i += 1
            output_filepath = f'{video_folderpath}/tmp/images/img-{i_str}.jpg'
            if os.path.exists(output_filepath): continue
            # with open(f'{video_folderpath}/tmp/prompts/prompt.txt') as f: prompt = f.read()
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
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-')
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
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-')
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
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-')
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
        with open(f'{video_folderpath}/tmp/video-final/title.txt') as f: title = f.read()
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
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-')
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
        with open(f'{video_folderpath}/tmp/video-final/title.txt') as f: title = f.read()
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
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = ''
        if idea_i >= 1000: i_str = f'{idea_i}'
        elif idea_i >= 100: i_str = f'0{idea_i}'
        elif idea_i >= 10: i_str = f'00{idea_i}'
        else: i_str = f'000{idea_i}'
        idea_slug = idea.strip().lower().replace(' ', '-')
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        with open(f'{video_folderpath}/tmp/video-final/title.txt') as f: title = f.read().strip().lower().replace(' ', '-')
        video_filepath = f'{video_folderpath}/tmp/video-final/{title}.mp4'
        video_prev_filepath = f'{hub_folderpath}/video-preview/{i_str}-{idea_slug}.mp4'
        shutil.copy2(f'{video_filepath}', f'{video_prev_filepath}')

ideas_num_min = 20
ideas_num_max = 30
if 0:
    init()
if 0:
    images_gen(regen=False)
if 1:
    images_formatted_gen(regen=False)
    video_final_title_gen(regen=False)
    video_final_description_gen(regen=False)
    video_final_tags_gen(regen=False)
    audio_clips_gen(regen=False)
    video_clips_gen(regen=False)
    video_final_gen(regen=False)
    video_final_preview()

# import subprocess
# subprocess.Popen(['vlc', '--play-and-exit', f'{video_folderpath}/tmp/video-final/video.mp4'])


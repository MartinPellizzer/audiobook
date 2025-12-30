import os
import json
import shutil
import subprocess

from lib import llm
from lib import zimage

hub_folderpath = f'/home/ubuntu/vault/audiobook/herbalism'

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

def lines_get(filepath):
    with open(filepath) as f: content = f.read()
    if content.strip() == '': 
        print(f'ERR: No content in {filepath}')
        return
    lines = []
    for line in content.split('\n'):
        line = line.strip()
        if line == '': continue
        line = line.replace('*', '')
        line = line.replace('[', '')
        line = line.replace(']', '')
        lines.append(line)
    return lines

def init():
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        print(idea)
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        try: os.makedirs(f'{video_folderpath}')
        except: pass
        try: os.makedirs(f'{video_folderpath}/tmp')
        except: pass
        try: os.makedirs(f'{video_folderpath}/tmp/texts')
        except: pass
        if not os.path.exists(final_filepath):
            with open(final_filepath, 'w') as f: f.write('')
        # return  

def images_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        script_text_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        script_images_filepath = f'{video_folderpath}/tmp/texts/images.txt'
        ###
        try: os.makedirs(f'{video_folderpath}/tmp/images')
        except: pass
        if regen: 
            for filename in os.listdir(f'{video_folderpath}/tmp/images'):
                os.remove(f'{video_folderpath}/tmp/images/{filename}')
        ###
        image_lines = lines_get(script_images_filepath)
        line_i = 0
        for line in image_lines[:999]:
            i_str = index_to_string(line_i)
            line = line.strip().replace('.', '')
            line_i += 1
            output_filepath = f'{video_folderpath}/tmp/images/{i_str}.jpg'
            if os.path.exists(output_filepath): continue
            prompt = f'''
                {line}
            '''
            print(prompt)
            image = zimage.image_create(output_filepath=output_filepath, prompt=prompt, width=768, height=1024, seed=-1)

def images_auto_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        script_text_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        script_images_filepath = f'{video_folderpath}/tmp/texts/images.txt'
        ###
        try: os.makedirs(f'{video_folderpath}/tmp/images')
        except: pass
        if regen: 
            for filename in os.listdir(f'{video_folderpath}/tmp/images'):
                os.remove(f'{video_folderpath}/tmp/images/{filename}')
        ###
        for image_i in range(10):
            i_str = index_to_string(image_i)
            output_filepath = f'{video_folderpath}/tmp/images/{i_str}.jpg'
            if os.path.exists(output_filepath): continue
            prompt = f'''
                close-up of {idea} herb
            '''
            print(prompt)
            image = zimage.image_create(output_filepath=output_filepath, prompt=prompt, width=768, height=1024, seed=-1)

def images_prompts_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        output_filepath = f'{video_folderpath}/tmp/texts/images.txt'
        ###
        prompt = f'''
            write a list of 10 prompts for me to generate images with ai about the following herb: {idea}.
            each prompt is a detailed sentence made of comma-separated tags.
            use the following JSON structure to reply:
            [
                {{"prompt": "write prompt 1 here"}},
                {{"prompt": "write prompt 2 here"}},
                {{"prompt": "write prompt 3 here"}},
                {{"prompt": "write prompt 4 here"}},
                {{"prompt": "write prompt 5 here"}},
                {{"prompt": "write prompt 6 here"}},
                {{"prompt": "write prompt 7 here"}},
                {{"prompt": "write prompt 8 here"}},
                {{"prompt": "write prompt 9 here"}},
                {{"prompt": "write prompt 10 here"}}
            ]
            reply only with the paragraps.
        '''
        prompt += '/no_think'
        reply = llm.reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        try: json_data = json.loads(reply)
        except: pass 
        content = []
        if json_data != {}:
            for json_obj in json_data:
                prompt = json_obj['prompt']
                found = False
                content.append(prompt)
        content = '\n'.join(content)
        with open(output_filepath, 'w') as f: f.write(content)

def video_clips_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_images_folderpath = f'{video_folderpath}/tmp/images'
        output_video_clips_folderpath = f'{video_folderpath}/tmp/video-clips'
        output_video_clips_zoom_folderpath = f'{video_folderpath}/tmp/video-clips-zoom'
        ###
        if not os.path.exists(f'{output_video_clips_folderpath}'):
            os.makedirs(f'{output_video_clips_folderpath}')
        '''
        if regen: 
            for filename in os.listdir(f'{output_video_clips_folderpath}'):
                if filename.endswith('.mp4'):
                    os.remove(f'{output_video_clips_folderpath}/{filename}')
        '''
        if not os.path.exists(f'{output_video_clips_zoom_folderpath}'):
            os.makedirs(f'{output_video_clips_zoom_folderpath}')
        if regen: 
            for filename in os.listdir(f'{output_video_clips_zoom_folderpath}'):
                if filename.endswith('.mp4'):
                    os.remove(f'{output_video_clips_zoom_folderpath}/{filename}')
        ###
        input_images_filenames = sorted(os.listdir(f'{input_images_folderpath}'))
        for input_image_i, input_image_filename in enumerate(input_images_filenames):
            i_str = index_to_string(input_image_i)
            input_image_filepath = f'{input_images_folderpath}/{input_image_filename}'
            output_video_clip_filepath = f'{output_video_clips_folderpath}/{i_str}.mp4'
            output_video_clip_zoom_filepath = f'{output_video_clips_zoom_folderpath}/{i_str}.mp4'
            subprocess.run([
                'ffmpeg', '-y',
                '-i', input_image_filepath,
                '-vf',
                "scale=10000:-1,format=yuv420p,zoompan=z='min(max(zoom,pzoom)+0.01,2.0)':d=150:x='floor(iw/2-(iw/zoom/2))':y='floor(ih/2-(ih/zoom/2))':s=768x1024", 
                '-t', '5',
                '-r', '30',
                output_video_clip_zoom_filepath,
            ])

def video_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i >= ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_video_clips_zoom_folderpath = f'{video_folderpath}/tmp/video-clips-zoom'
        output_video_clips_concat_transitions_folderpath = f'{video_folderpath}/tmp/video-clips-concat-transitions'
        output_video_folderpath = f'{video_folderpath}/tmp/video'
        concat_filepath = f'{video_folderpath}/tmp/video-concat.txt'
        ###
        if not os.path.exists(f'{output_video_folderpath}'):
            os.makedirs(f'{output_video_folderpath}')
        if regen: 
            for filename in os.listdir(f'{output_video_folderpath}'):
                if filename.endswith('.mp4'):
                    os.remove(f'{output_video_folderpath}/{filename}')
        filenames = sorted(os.listdir(f'{input_video_clips_zoom_folderpath}'))
        clips_filepaths = []
        with open(concat_filepath, 'w') as f:
            for i, filename in enumerate(filenames):
                filepath = f'{input_video_clips_zoom_folderpath}/{filename}'
                f.write(f"file '{filepath}'\n")
                clips_filepaths.append(filepath)
        # with open(f'{video_folderpath}/tmp/video-final/title.txt') as f: 
            # title = f.read().strip().lower().replace(' ', '-')
        title = idea

        for clip_i in range(len(clips_filepaths)):
            transitions = ['slideleft', 'slidedown', 'slideright', 'slideup']
            transition = transitions[clip_i%4]
            i_str_cur = index_to_string(clip_i)
            if clip_i == 0:
                shutil.copy2(
                    f'{input_video_clips_zoom_folderpath}/{i_str_cur}.mp4', 
                    f'{output_video_clips_concat_transitions_folderpath}/{i_str_cur}.mp4'
                )
                continue
            i_str_old = index_to_string(clip_i-1)
            clip_cur_filepath = f'{input_video_clips_zoom_folderpath}/{i_str_cur}.mp4'
            clip_old_filepath = f'{output_video_clips_concat_transitions_folderpath}/{i_str_old}.mp4'
            clip_out_filepath = f'{output_video_clips_concat_transitions_folderpath}/{i_str_cur}.mp4'
            print(clip_cur_filepath)
            print(clip_old_filepath)
            print()
            duration_clip1 = (2*clip_i) + 0.5   # duration of first clip before transition
            duration_clip2 = 2.5   # duration of second clip after transition
            transition_duration = 0.5  # duration of xfade transition
            xfade_offset = duration_clip1 - transition_duration
            subprocess.run([
                'ffmpeg',
                '-y',
                '-i', clip_old_filepath,
                '-i', clip_cur_filepath,
                '-filter_complex',
                (
                    f"[0:v]trim=duration={duration_clip1},setpts=PTS-STARTPTS,"
                    "scale=1280:720,fps=30,format=yuv420p[v0];"
                    f"[1:v]trim=duration={duration_clip2},setpts=PTS-STARTPTS,"
                    "scale=1280:720,fps=30,format=yuv420p[v1];"
                    f"[v0][v1]xfade=transition={transition}:duration={transition_duration}:offset={xfade_offset}[v]"
                ),
                '-map', '[v]',
                '-an',
                '-pix_fmt', 'yuv420p',
                clip_out_filepath,
            ], check=True)

ideas_num_min = 0
ideas_num_max = 1
if 0:
    init()

### nope
# images_auto_gen(regen=True)

if 1:
    # images_prompts_gen(regen=False)
    # images_gen(regen=True)
    # video_clips_gen(regen=True)
    video_gen(regen=True)

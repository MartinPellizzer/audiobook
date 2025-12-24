import os
import re
import sys
import random

from kokoro import KPipeline
import soundfile as sf 

from PIL import Image

from lib import g
from lib import llm
from lib import media

video_folderpath = 'archaeology-0000'
# final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
narration_filepath = f'archaeology-video-narration.txt'
narration_split_filepath = f'archaeology-video-narration_split.txt'
script_filepath = f'archaeology-video-script.txt'
artifact_filepath = f'archaeology-video-artifact.txt'

try: os.makedirs(f'{video_folderpath}')
except: pass
try: os.makedirs(f'{video_folderpath}/images')
except: pass
try: os.makedirs(f'{video_folderpath}/tmp')
except: pass
try: os.makedirs(f'{video_folderpath}/tmp/texts')
except: pass
try: os.makedirs(f'{video_folderpath}/tmp/images')
except: pass

def script_gen():
        # Give me a list of 50 artifact ideas.
        # That said, can you please help me come up with 15 big broad categories to start with?
    context = f'''
        I'm creating a youtube channel with the following name:
        "The Museum of Lost Objects"
        Each video showcases an ancient object with a mysterious history that is discovered in an archaeological excavation.

        The angle is mystery with a touch of eeriness.
        The tone sits right between mysterious, beautiful, and slightly unsettling.
        It has that "this feels like it shouldn't exist" quality that makes people want to share it.
        This angle should provoke curiosity, make people comment theories, encourages rewatches, works perfectly with static images.
        It must be 30% mystery + 30% wonder + 20% eeriness + 10% blank-space ambiguity + 10% soft dark humor.
        Each video will be a youtube short of about 30 seconds.
    '''
    ## ideas
    prompt = f'''
        {context}
        I will create different series, so I'm going to create different categories.
        The category I want to focus now is the following:
        1. Forgotten Civilizations  
        Objects from lost or little-known ancient cultures, like the Indus Valley, Maya, or lost cities in the Amazon. 
        These can spark questions about their disappearance and purpose.

        Give me a list of 50 clickbait artifact ideas about this category. 
        Make each one cover a slightly different topic, get as micro as you'd like.

        Reply only with the list.
    '''
    title = 'The 3,000-Year-Old Goddess of the Amazon Statue Found in the Jungle'
    ## structure
    prompt = f'''
        {context}
        Give me the script for the video short with the following TITLE:
        {title}
        STRUCTURE:
        Each video must start with the words: "Archaeologists discovered ".
        Start with a one sentence hook.
        
        Each video must end with a question or mystery to encourage engagement.
    '''
    prompt = f'''
        {context}
        Let's say that one of my video has the TITLE:
        {title}
        Give me a general structure template for making this types of video shorts that has the best chance of them going viral.
        Start with the words "Archaeologists discovered" a 3-second opening hook to grab attention immediately.
        Then build intrigue by revealing what it is and where it was discovered to set mystery and wonder, but don't include the time when it was discovered.
        Then the twist or eerie moment, where you introduce something unsettling or ambiguous, something that shouldn't be possible and make this object like it shouldn't exists.
        Then tell what archaeologists hypothesis are on why this ackward thing is.
        Then end with a ending hook, leaving the audience with a open loop wondering about it and sparking conspiration theories.
    '''

    ## video narration
    if 0:
        prompt = f'''
            {context}
            I have to make a video short with the following TITLE: 
            {title}
            Give me the narrated text for this types video short that has the best chance of them going viral.
            Follow this STRUCTURE:
            - Start with the words "Archaeologists discovered" and a 3-second opening hook to grab attention immediately.
            - Then build intrigue by revealing where it was discovered to set mystery and wonder, but don't include the time when it was discovered.
            - Then include a twist or eerie moment, where you introduce something unsettling or ambiguous, something that shouldn't be possible and make this object like it shouldn't exists. To do this, don't be generic, pick a concrete detail about the artifact and discuss why it shouldn't have it, or why that artifact shouldn't be discovered in that location.
            - Then tell what are the archaeologists' hypothesis on why this ackward thing is.
            - Then end with ONE single question hook, leaving the audience with a open loop wondering about how is this artifact possible.
            Reply only with the asked content.
            Reply with a paragraph. 
            The text must not have formatting, no bold or other styles.
            Reply using simple language.
            Reply in 60 words.
        '''
        prompt += '/no_think'
        reply = llm.reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        with open(narration_filepath, 'w') as f: f.write(reply)

    ## scenes generation
    if 1:
        with open(narration_filepath) as f: narration_text = f.read()
        prompt = f'''
            {context}
            I have to make a video short with the following TITLE: 
            {title}
            The video has this narrated text:
            {narration_text}
            Split this text in multiple scenes. Make each scene about the right length to be narrated in 3 seconds.
            Reply only with the asked content.
        '''
        prompt += '/no_think'
        reply = llm.reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        with open(narration_split_filepath, 'w') as f: f.write(reply)
        print('boom')
        quit()

    ## narrated sentences split
    if 0:
        with open(narration_filepath) as f: narration_text = f.read()
        prompt = f'''
            {context}
            I have to make a video short with the following title: 
            The 3,000-Year-Old Goddess of the Amazon Statue Found in the Jungle  
            The narrated content is the following:
            {narration_text}
            I want you to split this narrated content in several lines, each line must be the right length to be narrated in 3 seconds.
            Try to respect punctuation when splitting, to try to make the sentences have natural pausings for me to narrate.
            Reply only with the asked content.
        '''
        prompt += '/no_think'
        reply = llm.reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        with open(narration_split_filepath, 'w') as f: f.write(reply)
        print('boom')
        quit()

    ## artifact description
    with open(narration_filepath) as f: narration_text = f.read()
    if 0:
        prompt = f'''
            {context}
            I have to make a video short with the following narrated part: 
            {narration_text}
            Give me a detailed paragraph that describe the artifact discussed in the narrated part.
            Give me the description in form of a prompt I can use to generate a photorealistic image of this artifact using a Generative AI.
        '''
        prompt += '/no_think'
        reply = llm.reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        with open(artifact_filepath, 'w') as f: f.write(reply)

    ## images prompts
    with open(narration_split_filepath) as f: narration_split_text = f.read()
    if 1:
        prompt = f'''
            {context}
            I have to make a video short with the following title: 
            The 3,000-Year-Old Goddess of the Amazon Statue Found in the Jungle  
            The narrated content is made by the following sentences:
            {narration_split_text}
            I want you to give me 10 prompts I can use to generate relevant images with Generative AI that best represent the scenes for this video.
            Each prompt must be a detailed paragraph.
            The style of the images must be coherent throughout the video, and it must be primarily photorealistic, eerie, and believable, almost amateur. It must look like it's from a real archaeological photo.
            Only the first prompt must portray the artifact discussed in the video.
            Reply only with the asked content.
            Reply in a numbered list.
        '''
        prompt += '/no_think'
        reply = llm.reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        with open(script_filepath, 'w') as f: f.write(reply)

script_gen()
quit()

with open(script_filepath) as f: script_content = f.read()

image_lines = []
text_lines = []
for line in script_content.split('\n'):
    line = line.strip()
    if line == '': continue
    if '---' in line: continue
    if '###' in line: continue
    if line.startswith('**'): continue
    line = line.replace('*', '')
    if line.startswith('Voiceover: '):
        line = line.replace('Voiceover: ', '')
        text_lines.append(line)

print(text_lines)
# print(text_lines)

def audio_clips_gen(scenes, regen=False):
    if not os.path.exists(f'{video_folderpath}'):
        os.makedirs(f'{video_folderpath}')
    if not os.path.exists(f'{video_folderpath}/tmp'):
        os.makedirs(f'{video_folderpath}/tmp')
    if not os.path.exists(f'{video_folderpath}/tmp/audio-clips'):
        os.makedirs(f'{video_folderpath}/tmp/audio-clips')
    if regen: 
        for filename in os.listdir(f'{video_folderpath}/tmp/audio-clips'):
            os.remove(f'{video_folderpath}/tmp/audio-clips/{filename}')
    else:
        return
    j = 0
    pipeline = KPipeline(lang_code='a')
    for scene in scenes:
        text = scene
        generator = pipeline(
            text, 
            voice='am_michael',
            speed = 1.3,
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
    if not os.path.exists(f'{video_folderpath}'):
        os.makedirs(f'{video_folderpath}')
    if not os.path.exists(f'{video_folderpath}/tmp'):
        os.makedirs(f'{video_folderpath}/tmp')
    if not os.path.exists(f'{video_folderpath}/tmp/video-clips'):
        os.makedirs(f'{video_folderpath}/tmp/video-clips')
    if regen: 
        for filename in os.listdir(f'{video_folderpath}/tmp/video-clips'):
            os.remove(f'{video_folderpath}/tmp/video-clips/{filename}')
    else:
        return
    ### gen
    audio_filenames = sorted(os.listdir(f'{video_folderpath}/tmp/audio-clips'))
    for i, audio_filename in enumerate(audio_filenames):
        audio_filepath = f'{video_folderpath}/tmp/audio-clips/{audio_filename}'
        i_str = ''
        if i >= 1000: i_str = f'{i}'
        elif i >= 100: i_str = f'0{i}'
        elif i >= 10: i_str = f'00{i}'
        else: i_str = f'000{i}'
        slide_filepath = f'{video_folderpath}/tmp/images/img-{i_str}.jpg'
        slide_filepath = f'{video_folderpath}/tmp/images/{i}.jpg'
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
    if not os.path.exists(f'{video_folderpath}'):
        os.makedirs(f'{video_folderpath}')
    if not os.path.exists(f'{video_folderpath}/tmp'):
        os.makedirs(f'{video_folderpath}/tmp')
    if not os.path.exists(f'{video_folderpath}/tmp/video-final'):
        os.makedirs(f'{video_folderpath}/tmp/video-final')
    if regen: 
        for filename in os.listdir(f'{video_folderpath}/tmp/video-final'):
            os.remove(f'{video_folderpath}/tmp/video-final/{filename}')
    else:
        return
    video_clips_filenames = sorted(os.listdir(f'{video_folderpath}/tmp/video-clips'))
    concat_filepath = f'{video_folderpath}/tmp/video-concat.txt'
    with open(concat_filepath, 'w') as f:
        for i, video_clip_filename in enumerate(video_clips_filenames):
            video_clip_filepath = f'/home/ubuntu/proj/audiobook/{video_folderpath}/tmp/video-clips/{video_clip_filename}'
            f.write(f"file '{video_clip_filepath}'\n")
    video_final_filepath = f'{video_folderpath}/tmp/video-final/video.mp4'
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

scene_num = 9999
scenes = text_lines
audio_clips_gen(scenes[:scene_num], regen=True)
video_clips_gen(regen=True)
video_final_gen(regen=True)

import subprocess
subprocess.Popen(['vlc', '--play-and-exit', f'{video_folderpath}/tmp/video-final/video.mp4'])


quit()

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

regen = False
if regen:
    for filename in os.listdir(f'{video_folderpath}/tmp/images'):
        os.remove(f'{video_folderpath}/tmp/images/{filename}')
if 1:
    if len(sys.argv) > 1:
        if sys.argv[1] == 'image':
            running = True
            while running:
                i = 0
                for line in image_lines:
                    i_str = ''
                    if i >= 1000: i_str = f'{i}'
                    elif i >= 100: i_str = f'0{i}'
                    elif i >= 10: i_str = f'00{i}'
                    else: i_str = f'000{i}'
                    i += 1
                    output_filepath = f'{video_folderpath}/tmp/images/img-{i_str}.jpg'
                    print(output_filepath)
                    if os.path.exists(output_filepath): continue
                    image_prompt = f'{line}, illustrative, botanical, figurative, dry brush, splatter effect, salt texture, paper texture, pastel tones'
                    # image = media.image_gen(image_prompt, 768, 512, steps=20, cfg=6.0)
                    image = media.image_gen(image_prompt, 1216, 832, steps=20, cfg=6.0)

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
                    image = image_resize_ratio(image)
                    image.save(output_filepath)
                    print('############################################################')
                    print(image_prompt)
                    print('############################################################')
                print('enter "done" to quit')
                done = input('>> ')
                if done == 'done': running = True
    else:
        i = 0
        for line in image_lines:
            i_str = ''
            if i >= 1000: i_str = f'{i}'
            elif i >= 100: i_str = f'0{i}'
            elif i >= 10: i_str = f'00{i}'
            else: i_str = f'000{i}'
            i += 1
            output_filepath = f'{video_folderpath}/tmp/images/img-{i_str}.jpg'
            print(output_filepath)
            if os.path.exists(output_filepath): 
                image = Image.open(output_filepath)
                width, height = image.size
                if width != 1280 or height != 720:
                    image = image_resize_ratio(image)
                    image.save(output_filepath)
                continue
            image_prompt = f'{line}, illustrative, botanical, figurative, dry brush, splatter effect, salt texture, paper texture, pastel tones'
            # image = media.image_gen(image_prompt, 768, 512, steps=20, cfg=6.0)
            image = media.image_gen(image_prompt, 1216, 832, steps=20, cfg=6.0)
            image = image_resize_ratio(image)
            image.save(output_filepath)
            print('############################################################')
            print(image_prompt)
            print('############################################################')


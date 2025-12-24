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

tmp_folderpath = '/home/ubuntu/proj/audiobook/tmp'
video_title = 'The ONE Herb That Can Calm Anxiety Naturally (Lemon Balm)'
outline_filepath = f'{g.base_folderpath}/tmp/texts/outline.txt'

anecdote_filepath = f'{g.base_folderpath}/tmp/texts/anecdote.txt'
story_filepath = f'{g.base_folderpath}/tmp/texts/anecdote.txt'
hook_filepath = f'{g.base_folderpath}/tmp/texts/hook.txt'
what_filepath = f'{g.base_folderpath}/tmp/texts/what.txt'
why_filepath = f'{g.base_folderpath}/tmp/texts/why.txt'
how_filepath = f'{g.base_folderpath}/tmp/texts/how.txt'

final_filepath = f'{g.base_folderpath}/tmp/texts/final.txt'

try: os.makedirs(f'{g.base_folderpath}')
except: pass
try: os.makedirs(f'{g.base_folderpath}/images')
except: pass
try: os.makedirs(f'{g.base_folderpath}/tmp')
except: pass
try: os.makedirs(f'{g.base_folderpath}/tmp/texts')
except: pass
if not os.path.exists(final_filepath):
    with open(final_filepath, 'w') as f: f.write('')
try: os.makedirs(f'{g.base_folderpath}/tmp/images')
except: pass

def script_outline_gen(regen=False):
    if not regen: return
    prompt = f'''
        Write an outline for a 5-minute YouTube video about the following TOPIC, using the following TEMPLATE and GUIDELINES:
        TOPIC:
        {video_title}
        TEMPLATE:
        - Hook (15 seconds)
        - Historical Anecdote (1 minute)
        - What Is This Herb (45 seconds)
        - Why It Works (1 minute)
        - How To Use It (1 minute)
        - Conclusion (30 seconds)
        GUIDELINES:
        Include the titles of the template starting with "###".
        Write a detailed description for each template item, indicating what to speak about in that section.
        Separate each section with the characters "---".
        Reply only with the outline.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    with open(f'{g.base_folderpath}/tmp/texts/outline.txt', 'w') as f: f.write(reply)

def anecdote_gen(regen=False):
    if not regen: return
    prompt = f'''
        Write a list of 10 real anecdotes (based on ancient history, folklore, and spirituality) about the following topic so I can make a short documentary:
        The ONE herb that can calm anxiety naturally (lemon balm).
        GUIDELINES:
        Don't reveal the herb.
        The goal of thes anecdotes are to build curiosity.
        The anecdotes must be about real events, so name a real place, popular historical character, or age period.
        Separate each anecdote with the characters "---".
        Include a title "###" for each anecdote.
        Reply only with the anecdotes.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    anecdotes = reply.split('---')
    anecdote_random = random.choice(anecdotes)
    print("########################################")
    print("ANECDOTES")
    print("########################################")
    print(anecdote_random)
    prompt = f'''
        Format the following text by separating in a new line each sentence.
        {anecdote_random}
        Reply only with the lines.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    with open(f'{g.base_folderpath}/tmp/texts/anecdote.txt', 'w') as f: f.write(reply)

def anecdote_story_gen(anecdote):
    prompt = f'''
        I have to make a youtube video with the following TITLE:
        {video_title}
        This video contains the following ANECDOTE.
        So I want you to turn this anecdote into a fully cinematic 45-60 second story for a documentary trailer.
        Also, for reference the context TOPIC is below too.
        ANECDOTE:
        {anecdote}
        GUIDELINES:
        Don't reveal the herb.
        The goal of this story is to build curiosity.
        The story must be engaging and have a "wow factor".
        Make the story about 10-sentence long, so I can narrate it for 45-60 seconds.
        End with a one sentence cliffhanger, that will be used as transition to reveal the herb.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    return reply

def hook_gen(regen=False):
    if not regen: return
    story_filepath = f'{g.base_folderpath}/tmp/texts/anecdote.txt'
    with open(story_filepath) as f: story = f.read()
    examples_filepath = f'{g.base_folderpath}/assets/hooks-examples.txt'
    with open(examples_filepath) as f: examples = f.read()
    prompt = f'''
        I have to make a youtube video with the following TITLE:
        {video_title}
        The video contains the following STORY:
        {story}
        Write a list of engaging and viral hooks I can use to open the video before the story.
        GUIDELINES:
        Don't reveal the herb in the hooks.
        The goal of these hooks is to build curiosity.
        Separate each hook with the characters "---".
        Reply only with the hooks.
    '''
    prompt = f'''
        Write a list of 10 hooks for a YouTube video with the following TOPIC and STORY.
        TOPIC: 
        {video_title}
        STORY: 
        {story}
        EXAMPLES:
        Here's a list of hooks I like from another video you can take inspiration from.
        {examples}
        GUIDELINES:
        The hooks must be 1-3 sentences.
        The hooks must transition naturally to the story.
        Separate each hook with the characters "---".
        Reply only with the hooks.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    hooks = reply.split('---')
    hook_random = random.choice(hooks)
    print("########################################")
    print("HOOK")
    print("########################################")
    print(hook_random)
    with open(f'{g.base_folderpath}/tmp/texts/hook.txt', 'w') as f: f.write(hook_random)

def script_what_gen(regen=False):
    if not regen: return
    with open(outline_filepath) as f: outline = f.read()
    with open('prompts/section-what.txt') as f: prompt = f.read()
    topic = outline.split('---')[2].strip()
    prompt = prompt.replace('[topic]', topic)
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    with open(f'{g.base_folderpath}/tmp/texts/what.txt', 'w') as f: f.write(reply)
    print(len(reply.split(' ')))

def script_why_gen(regen=False):
    if not regen: return
    with open(outline_filepath) as f: outline = f.read()
    with open('prompts/section-what.txt') as f: prompt = f.read()
    topic = outline.split('---')[3].strip()
    prompt = prompt.replace('[topic]', topic)
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    with open(f'{g.base_folderpath}/tmp/texts/why.txt', 'w') as f: f.write(reply)
    print(len(reply.split(' ')))

def script_how_gen(regen=False):
    if not regen: return
    with open(outline_filepath) as f: outline = f.read()
    with open('prompts/section-what.txt') as f: prompt = f.read()
    topic = outline.split('---')[4].strip()
    prompt = prompt.replace('[topic]', topic)
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    with open(f'{g.base_folderpath}/tmp/texts/how.txt', 'w') as f: f.write(reply)
    print(len(reply.split(' ')))

# script_outline_gen(regen=True)
# script_what_gen(regen=True)
# quit()

# anecdote_gen(regen=False)
# hook_gen(regen=False)

# script_what_gen(regen=True)
# script_why_gen(regen=True)
# script_how_gen(regen=True)

# body_gen(regen=False)
# quit()

def images_from_script_gen(line, line_i):
    ### get image subject from script line
    prompt = f'''
        I have to make a youtube video with the following TITLE:
        {video_title}
        The video starts with the following ANECDOTE (in the style of a cinematic story for a documentary trailer). 
        I want to create an image for the below indicated narrated SENTENCE. 
        Please give me the best subject for this image based on the specific sentence.
        ANECDOTE:
        {anecdote}
        SENTENCE:
        {line}
        GUIDELINES:
        Reply with a list of tags, separated by commas.
        For context, these tags will be used for stable diffusion to generate the image.
        In the tags, include the main subject, background scenery, camera position, lighting, etc.
        The style is watercolor illustration for storybooks.
        Write less that 60 words.
        Start the reply with: a watercolor illustration of.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    prompt = f'''
        {reply},
    '''.replace('  ', ' ')
    image = media.image_gen(prompt, 768, 512, steps=20, cfg=6.0)
    i = line_i
    i_str = ''
    if i >= 1000: i_str = f'{i}'
    elif i >= 100: i_str = f'0{i}'
    elif i >= 10: i_str = f'00{i}'
    else: i_str = f'000{i}'
    image.save(f'video-0000/tmp/images/img-{i_str}.jpg')

def images_body_from_script_gen(line, line_i):
    ### get image subject from script line
    prompt = f'''
        I have to make a youtube video with the following TITLE:
        {video_title}
        I want to create an image for the below indicated narrated SENTENCE. 
        SENTENCE:
        {line}
        GUIDELINES:
        Reply with a list of tags, separated by commas.
        For context, these tags will be used for stable diffusion to generate the image.
        In the tags, include the main subject, background scenery, camera position, lighting, etc.
        The style is watercolor illustration for storybooks.
        Write less that 60 words.
        Start the reply with: a watercolor illustration of.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    prompt = f'''
        {reply},
    '''.replace('  ', ' ')
    image = media.image_gen(prompt, 768, 512, steps=20, cfg=6.0)
    i = line_i
    i_str = ''
    if i >= 1000: i_str = f'{i}'
    elif i >= 100: i_str = f'0{i}'
    elif i >= 10: i_str = f'00{i}'
    else: i_str = f'000{i}'
    image.save(f'video-0000/tmp/images/img-{i_str}.jpg')

def images_body_from_script_gen_2(line, line_i):
    ### get image subject from script line
    prompt = f'''
        I have the following CONTENT to narrate for a video, and I want to create an image that best represent it.
        CONTENT:
        {line}
        GUIDELINES:
        Reply with a list of tags, separated by commas.
        For context, these tags will be used for stable diffusion to generate the image.
        In the tags, include the main subject and background scenery in less than 10 words.
        The style is watercolor illustration for storybooks.
        Write less that 40 words.
        Start the reply with: watercolor illustration, .
        End the reply with: soft brush texture, pastel palette, natural paper texture, calm and minimal composition, cinematic lighting
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    prompt = f'''
        {reply},
    '''.replace('  ', ' ')
    image = media.image_gen(prompt, 768, 512, steps=20, cfg=6.0)
    i = line_i
    i_str = ''
    if i >= 1000: i_str = f'{i}'
    elif i >= 100: i_str = f'0{i}'
    elif i >= 10: i_str = f'00{i}'
    else: i_str = f'000{i}'
    image.save(f'video-0000/tmp/images/img-{i_str}.jpg')

if 0:
    with open(hook_filepath) as f: hook = f.read().strip().replace('\n', ' ')
    with open(anecdote_filepath) as f: anecdote = f.read().strip()
    with open(what_filepath) as f: what = f.read().strip()
    with open(why_filepath) as f: why = f.read().strip()
    with open(how_filepath) as f: how = f.read().strip()
    scene_i = 0
    images_body_from_script_gen_2(hook, scene_i)
    scene_i += 1
    lines = anecdote.split('\n')
    for line in lines:
        images_body_from_script_gen_2(line, scene_i)
        scene_i += 1
    lines = what.split('\n')
    for line in lines:
        images_body_from_script_gen_2(line, scene_i)
        scene_i += 1
    lines = why.split('\n')
    for line in lines:
        images_body_from_script_gen_2(line, scene_i)
        scene_i += 1
    lines = how.split('\n')
    for line in lines:
        images_body_from_script_gen_2(line, scene_i)
        scene_i += 1

def audio_clips_gen(scenes, regen=False):
    if not os.path.exists(f'{g.base_folderpath}'):
        os.makedirs(f'{g.base_folderpath}')
    if not os.path.exists(f'{g.base_folderpath}/tmp'):
        os.makedirs(f'{g.base_folderpath}/tmp')
    if not os.path.exists(f'{g.base_folderpath}/tmp/audio-clips'):
        os.makedirs(f'{g.base_folderpath}/tmp/audio-clips')
    if regen: 
        for filename in os.listdir(f'{g.base_folderpath}/tmp/audio-clips'):
            os.remove(f'{g.base_folderpath}/tmp/audio-clips/{filename}')
    else:
        return
    j = 0
    pipeline = KPipeline(lang_code='a')
    for scene in scenes:
        text = scene
        generator = pipeline(text, voice='af_heart')
        for (gs, ps, audio) in generator:
            print(j, gs, ps)
            j_str = ''
            if j >= 1000: j_str = f'{j}'
            elif j >= 100: j_str = f'0{j}'
            elif j >= 10: j_str = f'00{j}'
            else: j_str = f'000{j}'
            sf.write(f'{g.base_folderpath}/tmp/audio-clips/audio-{j_str}.wav', audio, 24000)
            j += 1

def audio_gen(regen=False):
    import subprocess
    audio_clips_filenames = sorted(os.listdir(f'{tmp_folderpath}/audio-clips'))
    concat_filepath = f'{tmp_folderpath}/audio-concat.txt'
    with open(concat_filepath, 'w') as f:
        for i, audio_clip_filename in enumerate(audio_clips_filenames):
            audio_clip_filepath = f'{tmp_folderpath}/audio-clips/{audio_clip_filename}'
            f.write(f"file '{audio_clip_filepath}'\n")
    audio_final_filepath = f'{tmp_folderpath}/audio-final/audio.wav'
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{concat_filepath}', 
        f'-acodec', f'pcm_s16le', 
        f'{audio_final_filepath}', 
        f'-y',
    ])

def video_clips_gen(regen=False):
    import subprocess
    if not os.path.exists(f'{g.base_folderpath}'):
        os.makedirs(f'{g.base_folderpath}')
    if not os.path.exists(f'{g.base_folderpath}/tmp'):
        os.makedirs(f'{g.base_folderpath}/tmp')
    if not os.path.exists(f'{g.base_folderpath}/tmp/video-clips'):
        os.makedirs(f'{g.base_folderpath}/tmp/video-clips')
    if regen: 
        for filename in os.listdir(f'{g.base_folderpath}/tmp/video-clips'):
            os.remove(f'{g.base_folderpath}/tmp/video-clips/{filename}')
    else:
        return
    ### gen
    audio_filenames = sorted(os.listdir(f'{g.base_folderpath}/tmp/audio-clips'))
    for i, audio_filename in enumerate(audio_filenames):
        audio_filepath = f'{g.base_folderpath}/tmp/audio-clips/{audio_filename}'
        i_str = ''
        if i >= 1000: i_str = f'{i}'
        elif i >= 100: i_str = f'0{i}'
        elif i >= 10: i_str = f'00{i}'
        else: i_str = f'000{i}'
        slide_filepath = f'{g.base_folderpath}/tmp/images/img-{i_str}.jpg'
        video_filepath = f'{g.base_folderpath}/tmp/video-clips/video-{i_str}.mp4'
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
    if not os.path.exists(f'{g.base_folderpath}'):
        os.makedirs(f'{g.base_folderpath}')
    if not os.path.exists(f'{g.base_folderpath}/tmp'):
        os.makedirs(f'{g.base_folderpath}/tmp')
    if not os.path.exists(f'{g.base_folderpath}/tmp/video-final'):
        os.makedirs(f'{g.base_folderpath}/tmp/video-final')
    if regen: 
        for filename in os.listdir(f'{g.base_folderpath}/tmp/video-final'):
            os.remove(f'{g.base_folderpath}/tmp/video-final/{filename}')
    else:
        return
    video_clips_filenames = sorted(os.listdir(f'{g.base_folderpath}/tmp/video-clips'))
    concat_filepath = f'{g.base_folderpath}/tmp/video-concat.txt'
    with open(concat_filepath, 'w') as f:
        for i, video_clip_filename in enumerate(video_clips_filenames):
            video_clip_filepath = f'/home/ubuntu/proj/audiobook/{g.base_folderpath}/tmp/video-clips/{video_clip_filename}'
            f.write(f"file '{video_clip_filepath}'\n")
    video_final_filepath = f'{g.base_folderpath}/tmp/video-final/video.mp4'
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{concat_filepath}',
        f'-c', f'copy',
        f'{video_final_filepath}',
        f'-y', 
    ])
    print(g.base_folderpath)
    print(concat_filepath)
    print(video_final_filepath)
    # quit()

def video_clips_manual_with_audio():
    import subprocess
    # for filename in os.listdir(f'{tmp_folderpath}/video-clips-manual'):
        # os.remove(f'{tmp_folderpath}/video-clips-manual/{filename}')
    ### gen
    audio_filenames = sorted(os.listdir(f'{tmp_folderpath}/audio-clips'))
    for i, audio_filename in enumerate(audio_filenames):
        i_str = ''
        if i >= 1000: i_str = f'{i}'
        elif i >= 100: i_str = f'0{i}'
        elif i >= 10: i_str = f'00{i}'
        else: i_str = f'000{i}'
        input_video_filepath = f'{tmp_folderpath}/video-clips-manual/scene-{i_str}.mp4'
        input_audio_filepath = f'{tmp_folderpath}/audio-clips/{audio_filename}'
        output_video_filepath = f'{tmp_folderpath}/video-clips/video-{i_str}.mp4'
        subprocess.run([
            f'ffmpeg',
            f'-stream_loop', f'-1',
            f'-i', f'{input_video_filepath}',
            f'-i', f'{input_audio_filepath}',
            f'-c:v', f'libx264',
            f'-c:a', f'aac',
            f'-shortest',
            f'{output_video_filepath}',
            f'-y',
        ])

# quit()

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
    for filename in os.listdir(f'{g.base_folderpath}/tmp/images'):
        os.remove(f'{g.base_folderpath}/tmp/images/{filename}')
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
                    output_filepath = f'{g.base_folderpath}/tmp/images/img-{i_str}.jpg'
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
            output_filepath = f'{g.base_folderpath}/tmp/images/img-{i_str}.jpg'
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

if 0:
    # scenes = content.split('---')
    scenes = content.split('.')
    separators = ['.', '?']
    pattern = '(' + '|'.join(map( re.escape, separators)) + ')'
    scenes = re.split(pattern, content)
    scenes = [''.join(pair) for pair in zip(scenes[::2], scenes[1::2] + [''])]
    scenes = [scene.strip() for scene in scenes if scene.strip() != '']
    print(scenes)
    # quit()
    i = 0
    scene_num = 999
    for scene_text in scenes[:scene_num]:
        i_str = ''
        if i >= 1000: i_str = f'{i}'
        elif i >= 100: i_str = f'0{i}'
        elif i >= 10: i_str = f'00{i}'
        else: i_str = f'000{i}'
        i += 1
        output_filepath = f'video-0000/tmp/images/img-{i_str}.jpg'
        print(output_filepath)
        if os.path.exists(output_filepath): continue
        prompt = f'''
            I'm making a viral youtube video with the following title: 
            The one herb that can calm anxiety naturally (melissa officinalis).
            Give me 2 tags I can use for stable diffusion create an image for the following scene:
            {scene_text}
            GUIDELINES:
            The tags must be comma separated.
            The first tag describes the central subject of the image.
            The second tag describes the background scenery of the image.
            Reply only with the tags.
            Start with the following words: A watercolor painting of 
        '''
        # The first tag describes the central subject of the image. The central subject must be people, animals, or objects.
        prompt += f'/no_think'
        print(prompt)
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        image_prompt = f'{reply}, soft brush texture, pastel palette, natural paper texture, calm and minimal composition, cinematic lighting'
        image_prompt = f'{reply}, illustrative, botanical, figurative, dry brush, splatter effect, salt texture, paper texture, pastel tones'
        image = media.image_gen(image_prompt, 768, 512, steps=20, cfg=6.0)
        image.save(output_filepath)
        print('############################################################')
        print(image_prompt)
        print('############################################################')

# quit()
scene_num = 9999
scenes = text_lines
audio_clips_gen(scenes[:scene_num], regen=True)
video_clips_gen(regen=True)
video_final_gen(regen=True)

import subprocess
subprocess.Popen(['vlc', '--play-and-exit', f'{g.base_folderpath}/tmp/video-final/video.mp4'])


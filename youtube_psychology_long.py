import os
import re
import sys
import time
import random
import shutil
import subprocess

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import io
from lib import llm
from lib import media
from lib import zimage

hub_folderpath = f'/home/ubuntu/vault/audiobook/psychology-long'

ideas = ['Psychology of People Who Are Lazy but Ambitious']

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
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}'
        input_script_filepath = f'{video_folderpath}/script.txt'
        output_folderpath = f'{video_folderpath}/audio-clips'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(output_folderpath):
                os.remove(f'{output_folderpath}/{filename}')
        image_lines, text_lines = lines_get(input_script_filepath)
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
                j_str = index_to_string(j)
                sf.write(f'{output_folderpath}/{j_str}.wav', audio, 24000)
                j += 1

def audio_full_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        ###
        video_folderpath = f'{hub_folderpath}'
        input_audio_clips_folderpath = f'{video_folderpath}/audio-clips'
        output_folderpath = f'{video_folderpath}/audio-full'
        output_filepath = f'{output_folderpath}/0000.wav'
        concat_filepath = f'{video_folderpath}/concat.txt'
        ###
        if not os.path.exists(output_folderpath):
            os.makedirs(output_folderpath)
        if regen: 
            for filename in os.listdir(output_filepath):
                os.remove(output_filepath)
        ###
        with open(concat_filepath, 'w') as f:
            for i, filename in enumerate(sorted(os.listdir(f'{input_audio_clips_folderpath}'))):
                filepath = f'{input_audio_clips_folderpath}/{filename}'
                f.write(f"file '{filepath}'\n")
        ###
        subprocess.run([
            f'ffmpeg',
            f'-f', f'concat',
            f'-safe', f'0',
            f'-i', f'{concat_filepath}',
            f'-c', f'copy',
            f'{output_filepath}',
            f'-y', 
        ])

def images_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}'
        input_script_lines_images_filepath = f'{video_folderpath}/script-lines-images/0000.txt'
        output_folderpath = f'{video_folderpath}/images'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        ###
        image_lines, text_lines = lines_get(input_script_lines_images_filepath)
        line_i = 0
        for line in image_lines[:999]:
            line = line.strip().replace('.', '')
            i_str = index_to_string(line_i)
            line_i += 1
            output_filepath = f'{video_folderpath}/tmp/images/{i_str}.jpg'
            output_filepath = f'{output_folderpath}/{i_str}.jpg'
            if os.path.exists(output_filepath): continue
            # with open(f'{video_folderpath}/tmp/prompts/prompt.txt') as f: prompt = f.read()
            # with open(f'{hub_folderpath}/prompt.txt') as f: prompt = f.read()
            # prompt = prompt.replace('[line]', line)
            if 1:
                prompt = f'''
                    {line},
                    cartoon,
                    doodle,
                    illustration,
                '''
            print(prompt)
            image = zimage.image_create(output_filepath=output_filepath, prompt=prompt, width=1024, height=768, seed=-1)
        # return

def video_clips_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        ###
        video_folderpath = f'{hub_folderpath}'
        input_script_filepath = f'{video_folderpath}/script.txt'
        input_audio_clips_folderpath = f'{video_folderpath}/audio-clips'
        input_images_folderpath = f'{video_folderpath}/images'
        output_folderpath = f'{video_folderpath}/video-clips'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        ### gen
        audio_filenames = sorted(os.listdir(f'{input_audio_clips_folderpath}'))
        for i, audio_filename in enumerate(audio_filenames):
            i_str = index_to_string(i)
            audio_filepath = f'{input_audio_clips_folderpath}/{audio_filename}'
            image_filepath = f'{input_images_folderpath}/{i_str}.jpg'
            video_filepath = f'{output_folderpath}/{i_str}.mp4'
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
                f'{video_filepath}',
                f'-y',
            ])

def video_full_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        ###
        video_folderpath = f'{hub_folderpath}'
        input_script_filepath = f'{video_folderpath}/script.txt'
        input_video_clips_folderpath = f'{video_folderpath}/video-clips'
        output_folderpath = f'{video_folderpath}/video-full'
        output_filepath = f'{output_folderpath}/0000.mp4'
        concat_filepath = f'{video_folderpath}/concat.txt'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        ###
        with open(concat_filepath, 'w') as f:
            for i, filename in enumerate(sorted(os.listdir(f'{input_video_clips_folderpath}'))):
                filepath = f'{input_video_clips_folderpath}/{filename}'
                f.write(f"file '{filepath}'\n")
        ###
        subprocess.run([
            f'ffmpeg',
            f'-f', f'concat',
            f'-safe', f'0',
            f'-i', f'{concat_filepath}',
            f'-c', f'copy',
            f'{output_filepath}',
            f'-y', 
        ])

def script_lines(regen=False):
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        ###
        video_folderpath = f'{hub_folderpath}'
        input_script_filepath = f'{video_folderpath}/script.txt'
        output_folderpath = f'{video_folderpath}/script-lines'
        output_filepath = f'{output_folderpath}/0000.txt'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        ###
        with open(f'{input_script_filepath}') as f: text = f.read()
        text = text.replace('’', "'")
        text = text.replace('”', '"')
        text = text.replace('“', '"')
        text = text.replace('—', ', ')
        text = text.replace('…', ',')
        text = text.replace('."', '".')
        import re
        # Characters to split by
        delimiters = [".", ";", "?"]
        # Create a regex pattern with capturing group for the delimiters
        pattern = "([{}])".format(re.escape("".join(delimiters)))
        # Use re.split
        parts = re.split(pattern, text)
        # Combine each part with its delimiter
        result = [parts[i] + parts[i+1] for i in range(0, len(parts)-1, 2)]
        # If there’s a leftover piece without a delimiter at the end, append it
        if len(parts) % 2 != 0:
            result.append(parts[-1])
        for line in result:
            print(line.strip())
        lines = '\n'.join(result)
        with open(output_filepath, 'w') as f: f.write(lines)
        # quit()

def script_lines_images(regen=False):
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        ###
        video_folderpath = f'{hub_folderpath}'
        input_script_lines_filepath = f'{video_folderpath}/script-lines/0000.txt'
        output_folderpath = f'{video_folderpath}/script-lines-images'
        output_filepath = f'{output_folderpath}/0000.txt'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        with open(input_script_lines_filepath) as f: lines = '\n'.join(f.read().split('\n')[:10])
        ###
        prompt = f'''
            I'm going to give some NARRATED SENTENCES from a youtube video about the topic: The Psychology of People Who Are Lazy but Ambitious. 
            These sentences are one per line, and I want you to write a detailed prompt in one paragraph below each narrated sentence, describing the scene for me to use it for stable diffusion to generate the corresponding visual.
            These prompts must include the subject, the action performed, and the environment, in this order.
            The subject is always a young cartoon man. 
            Write these prompts for images inside squared brackets.
            Here's the NARRATED SENTENCES:
            {lines}
            /no_think
        '''

            # Start each image prompt with the words: "a cartoon young man".

        '''
        write the full script for: Psychology of People Who Stop Competing With Others

        to write the script:
        - write the full narrated sentences, structured like you suggested before to make a 60 seconds video.
        - below each narrated sentence, write a prompt in one detailed paragraph describing the scene for me to use it for stable diffusion to generate the corresponding visual. 
        - this prompt must include the subject, the action performed, and the environment. 
        - the subject is always a young man. 
        - the action must always be a stationary action, like standing, sit, reading, etc., never a dynamic action like walking or running. 
        - don't include other info like lighting and style because i'll add them myself. 
        - write the prompts for images inside squared brackets. 
        - each image prompt must be standalone, not a continuation of the previous ones. start each image prompt with "a cartoon young man".

        reply only with the content. 
        don't include titles.
        update the structure of the script based on the suggestion you gave me from the analytics.
        don't miss last sentence image prompt.
        '''
        print(prompt)
        reply = llm.reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        reply = reply.replace('*', '')
        print('#################################################')
        print(reply)
        print(output_filepath)
        print('#################################################')
        with open(output_filepath, 'w') as f: f.write(reply)

def audio_timing_gen(regen=False):
    import whisperx
    import torch
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        ###
        video_folderpath = f'{hub_folderpath}'
        input_audio_clips_folderpath = f'{video_folderpath}/audio-clips'
        input_audio_clip_filepath = f'{input_audio_clips_folderpath}/0000.wav'
        # input_script_lines_filepath = f'{video_folderpath}/script-lines/0000.txt'
        output_folderpath = f'{video_folderpath}/script-timing'
        output_filepath = f'{output_folderpath}/0000.json'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        # with open(input_script_lines_filepath) as f: lines = '\n'.join(f.read().split('\n')[:10])
        ###
        audio_file = input_audio_clip_filepath
        ##
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print("Using device:", device)
        model = whisperx.load_model(
            "medium",
            device="cpu",
            compute_type="float32",
            vad_method="silero"
        )
        result = model.transcribe(audio_file)
        align_model, metadata = whisperx.load_align_model(
            language_code=result["language"],
            device=device
        )
        aligned = whisperx.align(
            result["segments"],
            align_model,
            metadata,
            audio_file,
            device=device
        )
        print("\nWord-level timestamps:\n")
        output_text = ''
        words_timestamps = []
        for w in aligned["word_segments"]:
            start = w["start"]
            end = w["end"]
            word = w["word"]
            print(f"{start:6.2f}s → {end:6.2f}s  {word}")
            words_timestamps.append({
                'word': w['word'].strip(),
                'start': f"{w['start']:6.2f}".strip(),
                'end': f"{w['end']:6.2f}".strip(),
            })
        io.json_write(output_filepath, words_timestamps)

def audio_timing_fix_words_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        ###
        video_folderpath = f'{hub_folderpath}'
        input_script_timing_filepath = f'{video_folderpath}/script-timing/0000.json'
        input_script_lines_filepath = f'{video_folderpath}/script-lines/0000.txt'
        output_folderpath = f'{video_folderpath}/script-timing-fix-words'
        output_filepath = f'{output_folderpath}/0000.json'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        ###
        script_content = io.file_read(input_script_lines_filepath)
        script_lines = script_content.split('\n')
        script_words = []
        for script_line in script_lines:
            _script_words = script_line.split()
            for script_word in _script_words:
                script_words.append(script_word)
        ###
        script_timing_data = io.json_read(input_script_timing_filepath)
        script_timing_data_len = len(script_timing_data)
        script_words_len = len(script_words)
        print(script_timing_data_len )
        print(script_words_len )
        if script_timing_data_len != script_words_len:
            print(f'ERR: words not matching in num')
            # quit()
        words_fixed = []
        for item_i, item in enumerate(script_timing_data):
            word = item['word']
            start = item['start']
            end = item['end']
            if ',' in word and '.' in script_words[item_i]:
                item['word'] = script_words[item_i]
                words_fixed.append(item)
            else:
                words_fixed.append(item)
        io.json_write(output_filepath, words_fixed)

def audio_timing_sentences_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        ###
        video_folderpath = f'{hub_folderpath}'
        input_script_timing_fix_words_filepath = f'{video_folderpath}/script-timing-fix-words/0000.json'
        output_folderpath = f'{video_folderpath}/script-timing-sentences'
        output_filepath = f'{output_folderpath}/0000.txt'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        ###
        durations = []
        start_cur = 0
        end_cur = 0
        update_start = False
        script_timing_fix_words_data = io.json_read(input_script_timing_fix_words_filepath)
        i = 0
        for _ in range(len(script_timing_fix_words_data)):
            word = script_timing_fix_words_data[i]['word'].strip()
            start = float(script_timing_fix_words_data[i]['start'].strip())
            end = float(script_timing_fix_words_data[i]['end'].strip())
            if word.endswith('.') or word.endswith('?'):
                end_cur = end
                duration = end_cur - start_cur
                # start_cur = start
                if 1:
                    try: 
                        start_next = float(script_timing_fix_words_data[i+1]['start'].strip())
                        start_cur = (start_next + start)/2
                    except: 
                        pass
                duration = f'{duration:6.2f}'.strip()
                durations.append(duration)
            i += 1
        durations = '\n'.join(durations)
        io.file_write(output_filepath, durations)

def slideshow_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        ###
        video_folderpath = f'{hub_folderpath}'
        # input_script_filepath = f'{video_folderpath}/script.txt'
        input_images_folderpath = f'{video_folderpath}/images'
        input_audio_clip_filepath = f'{video_folderpath}/audio-clips/0000.wav'
        input_script_timing_sentences_filepath = f'{video_folderpath}/script-timing-sentences/0000.txt'
        output_folderpath = f'{video_folderpath}/slideshow'
        output_filepath = f'{output_folderpath}/0000.mp4'
        concat_filepath = f'{video_folderpath}/concat.txt'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        ###
        durations = io.file_read(input_script_timing_sentences_filepath).split('\n')
        images_filenames = sorted(os.listdir(input_images_folderpath))
        slides = []
        for i in range(len(durations)):
            slides.append((f"{input_images_folderpath}/{images_filenames[i]}", durations[i]))

        HUGE_DURATION = 10 * 60 * 60  # 10 hours (effectively infinite)

        ffmpeg_cmd = ["ffmpeg", "-y"]

        for i, (image_path, duration) in enumerate(slides):
            if i == len(slides) - 1:
                duration = HUGE_DURATION   # extend last image
            ffmpeg_cmd.extend([
                "-loop", "1",
                "-t", str(duration),
                "-i", image_path,
            ])

        # 2. Add audio
        ffmpeg_cmd.extend([
            "-i", input_audio_clip_filepath,
        ])

        # 3. Build filter_complex concat string
        video_inputs = "".join(f"[{i}:v]" for i in range(len(slides)))
        filter_complex = f"{video_inputs}concat=n={len(slides)}:v=1:a=0"

        # 4. Finish command
        ffmpeg_cmd.extend([
            "-filter_complex", filter_complex,
            "-pix_fmt", "yuv420p",
            "-c:v", "libx264",
            "-shortest",
            output_filepath,
        ])

        # 5. Run
        subprocess.run(ffmpeg_cmd, check=True)


'''
ffmpeg -f concat -safe 0 -i slideshow.txt \
       -i audio.mp3 \
       -vsync vfr \
       -pix_fmt yuv420p \
       -c:v libx264 \
       -shortest \
       output.mp4
'''


if 0:
    ### script
    # script_lines(regen=True)
    script_lines_images(regen=True)
    quit()

if 0:
    # images_gen_test()
    images_gen(regen=True)
    quit()

if 1:
    # audio_clips_gen(regen=True)
    # audio_timing_gen(regen=True)
    # audio_timing_fix_words_gen(regen=True)
    audio_timing_sentences_gen(regen=True)
    # audio_full_gen(regen=False)
    # quit()

if 1:
    slideshow_gen(regen=True)
    # video_clips_gen(regen=True)
    # video_full_gen(regen=True)

import os
import json
import shutil
import subprocess

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
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

def init():
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
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
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
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
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
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
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
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
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
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
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
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

def audio_clips_gen(regen=False):
    from kokoro import KPipeline
    import soundfile as sf 
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
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
        text_lines = lines_get(final_filepath)
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

def video_audio_gen(regen=False):
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        final_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        output_folderpath = f'{video_folderpath}/tmp/video-audio'
        output_filepath = f'{output_folderpath}/0000.mp4'
        print(final_filepath)
        if not os.path.exists(f'{video_folderpath}'):
            os.makedirs(f'{video_folderpath}')
        if not os.path.exists(f'{video_folderpath}/tmp'):
            os.makedirs(f'{video_folderpath}/tmp')
        if not os.path.exists(f'{video_folderpath}/tmp/video-clips'):
            os.makedirs(f'{video_folderpath}/tmp/video-clips')
        for filename in os.listdir(f'{video_folderpath}/tmp/video-clips'):
            os.remove(f'{video_folderpath}/tmp/video-clips/{filename}')
        ###
        if not os.path.exists(f'{output_folderpath}'):
            os.makedirs(f'{output_folderpath}')
        for filename in os.listdir(f'{output_folderpath}'):
            os.remove(f'{output_folderpath}/{filename}')
        ### gen
        audio_filename = sorted(os.listdir(f'{video_folderpath}/tmp/audio-clips'))[-1]
        audio_filepath = f'{video_folderpath}/tmp/audio-clips/{audio_filename}'
        video_filename = sorted(os.listdir(f'{video_folderpath}/tmp/video-clips-concat-transitions'))[-1]
        video_filepath = f'{video_folderpath}/tmp/video-clips-concat-transitions/{video_filename}'
        subprocess.run([
            f'ffmpeg',
            f'-i', f'{video_filepath}',
            f'-i', f'{audio_filepath}',
            f'-c:v', f'copy',
            f'-c:a', f'aac',
            f'-map', f'0:v:0',
            f'-map', f'1:a:0',
            f'-shortest',
            f'{output_filepath}',
            f'-y',
        ])

def images_texts_gen(regen=False):
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_script_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        output_folderpath = f'{video_folderpath}/tmp/images-texts'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        ###
        text_lines = lines_get(input_script_filepath)
        fg_color = '#ffffff'
        bg_color = '#000000'
        for text_line_i, text_line in enumerate(text_lines):
            i_str = index_to_string(text_line_i)
            ###
            font_size = 80
            font_family, font_weight = 'Lato', 'Bold'
            font_path = f"{g.VAULT_FOLDERPATH}/terrawhisper/database/assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
            font = ImageFont.truetype(font_path, font_size)
            caption_lines = text_to_lines(text_line, font, 1000)
            lines_num = len(caption_lines)
            img_h = lines_num * (font_size)
            ###
            img = Image.new(mode="RGB", size=(1080, img_h), color=bg_color)
            text_line = text_line.replace('—', ', ')
            text_line = text_line.replace('’', "'")
            draw = ImageDraw.Draw(img)
            ###
            for caption_line_i, caption_line in enumerate(caption_lines):
                _, _, caption_line_w, caption_line_h = font.getbbox(caption_line)
                draw.text((1080//2 - caption_line_w//2, font_size*caption_line_i), caption_line, fg_color, font=font)
            img_filepath = f'{output_folderpath}/{i_str}.jpg'
            img.save(img_filepath, format='JPEG', subsampling=0, quality=100)

def audio_timing_gen(regen=False):
    import whisperx
    import torch
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_audio_filepath = f'{video_folderpath}/tmp/audio-clips/audio-0000.wav'
        input_text_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        output_text_filepath = f'{video_folderpath}/tmp/texts/timing.txt'
        audio_file = input_audio_filepath
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
        for w in aligned["word_segments"]:
            start = w["start"]
            end = w["end"]
            word = w["word"]
            print(f"{start:6.2f}s → {end:6.2f}s  {word}")
            output_text += f"{start:6.2f}s → {end:6.2f}s  {word}" + '\n'
        with open(output_text_filepath, 'w') as f: f.write(output_text)
        print(output_text_filepath)

        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        output_folderpath = f'{video_folderpath}/tmp/ass'
        output = f'{video_folderpath}/tmp/ass/karaoke.ass'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')
        header = """[Script Info]
    Title: Karaoke
    ScriptType: v4.00+
    PlayResX: 1920
    PlayResY: 1080

    [V4+ Styles]
    Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
    Style: Karaoke,Arial,48,&H0000FFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,3,1,2,60,60,80,1

    [Events]
    Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
    """
        lines = []
        current_words = []
        line_start = None
        for w in aligned['word_segments']:
            if line_start is None:
                line_start = w["start"]
            duration_cs = max(1, int((w["end"] - w["start"]) * 100))
            text = w["word"]
            current_words.append(f"{{\\k{duration_cs}}}{text}")

            ###
            '''
            prev_end = None
            for w in aligned["word_segments"]:
                if line_start is None:
                    line_start = w["start"]
                if prev_end and w["start"] - prev_end > 0.7:
                    # new sentence after pause
                    lines.append((line_start, prev_end, " ".join(current_words)))
                    current_words = []
                    line_start = w["start"]
                duration_cs = max(1, int((w["end"] - w["start"]) * 100))
                current_words.append(f"{{\\k{duration_cs}}}{w['word']}")
                prev_end = w["end"]
            # flush last line
            if current_words:
                lines.append((line_start, prev_end, " ".join(current_words)))
            '''
            ###
            if text.endswith((".", "?", "!")):
                line_end = w["end"]
                lines.append((line_start, line_end, " ".join(current_words)))
                current_words = []
                line_start = None
            ###
        with open(output, "w", encoding="utf-8") as f:
            f.write(header)
            for start, end, text in lines:
                f.write(
                    f"Dialogue: 0,{sec_to_ass_time(start)},{sec_to_ass_time(end)},Karaoke,,0,0,0,,{text}\n"
                )
        print(f"Written {output}")


def sec_to_ass_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def video_karaoke_gen(regen=False):
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_ass_folderpath = f'{video_folderpath}/tmp/ass'
        input_ass_filepath = f'{input_ass_folderpath}/karaoke.ass'
        input_video_folderpath = f'{video_folderpath}/tmp/video-audio'
        input_video_filepath = f'{input_video_folderpath}/0000.mp4'
        output_folderpath = f'{video_folderpath}/tmp/video-karaoke'
        output_filepath = f'{output_folderpath}/0000.mp4'
        print(output_filepath)
        ###
        if not os.path.exists(f'{output_folderpath}'):
            os.makedirs(f'{output_folderpath}')
        for filename in os.listdir(f'{output_folderpath}'):
            os.remove(f'{output_folderpath}/{filename}')
        ### gen
        # ffmpeg -i input.mp4 -vf "subtitles=karaoke.ass" -c:a copy output_karaoke.mp4
        subprocess.run([
            f'ffmpeg',
            f'-i', f'{input_video_filepath}',
            f'-vf', f'subtitles={input_ass_filepath}',
            f'-c:a', f'copy',
            f'{output_filepath}',
            f'-y',
        ])

def audio_timing_gen_2(regen=False):
    import whisperx
    import torch
    for idea_i, idea in enumerate(ideas):
        if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
        i_str = index_to_string(idea_i)
        idea_slug = sluggify(idea)
        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        input_audio_filepath = f'{video_folderpath}/tmp/audio-clips/audio-0000.wav'
        input_text_filepath = f'{video_folderpath}/tmp/texts/final.txt'
        output_text_filepath = f'{video_folderpath}/tmp/texts/timing.txt'
        audio_file = input_audio_filepath
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
        for w in aligned["word_segments"]:
            start = w["start"]
            end = w["end"]
            word = w["word"]
            print(f"{start:6.2f}s → {end:6.2f}s  {word}")
            output_text += f"{start:6.2f}s → {end:6.2f}s  {word}" + '\n'
        with open(output_text_filepath, 'w') as f: f.write(output_text)
        print(output_text_filepath)

        video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
        output_folderpath = f'{video_folderpath}/tmp/ass'
        output = f'{video_folderpath}/tmp/ass/karaoke.ass'
        ###
        try: os.makedirs(output_folderpath)
        except: pass
        if regen: 
            for filename in os.listdir(f'{output_folderpath}'):
                os.remove(f'{output_folderpath}/{filename}')

        def ass_time(t):
            h = int(t // 3600)
            m = int((t % 3600) // 60)
            s = t % 60
            return f"{h}:{m:02d}:{s:05.2f}"

        header = """[Script Info]
        ScriptType: v4.00+
        PlayResX: 1080
        PlayResY: 1920

        [V4+ Styles]
        Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        Style: Word,Arial,256,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,120,100,0,0,3,20,0,5,0,0,0,1

        [Events]
        Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        """

        with open(output, "w", encoding="utf-8") as f:
            f.write(header)

            for w in aligned["word_segments"]:
                start = ass_time(w["start"])
                end = ass_time(w["end"])
                word = w["word"]

                f.write(
                    f"Dialogue: 0,{start},{end},Word,,0,0,0,,{word}\n"
                )

        print(f"Written {output}")

ideas_num_min = 0
ideas_num_max = 9
if 0:
    init()

### nope
# images_auto_gen(regen=True)

if 1:
    # images_prompts_gen(regen=False)
    # images_gen(regen=True)
    video_clips_gen(regen=True)
    # images_texts_gen(regen=True)
    # video_gen(regen=True)
    # audio_clips_gen(regen=False)
    # video_audio_gen(regen=False)

    # audio_timing_gen_2(regen=True)
    # video_karaoke_gen()


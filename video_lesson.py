import os
import subprocess

lesson_folderpath = f'lesson'

def script_split_gen(regen=False):
    input_filepath = f'test.txt'
    output_folderpath = f'{lesson_folderpath}/script-split'
    ### clean
    if regen: 
        try: shutil.rmtree(output_folderpath)
        except: pass
    try: os.mkdir(output_folderpath)
    except: pass
    ### gen
    with open(input_filepath) as f: script = f.read()
    script = script.replace('*', '').strip()
    script = script.replace('#', '').strip()
    lines = []
    for line in script.split('\n'): line = line.strip()
        if line == '': continue
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
        output_filepath = f'{output_folderpath}/{i_str}.txt'
        with open(output_filepath, 'w') as f: f.write(script_split)

def audio_clips_chunks_gen(regen=False):
    from kokoro import KPipeline
    import soundfile as sf 
    script_split_folderpath = f'{lesson_folderpath}/script-split'
    audio_clips_folderpath = f'{lesson_folderpath}/audio-clips-chunks'
    ### clean
    if regen: 
        try: shutil.rmtree(audio_clips_folderpath)
        except: pass
    try: os.mkdir(audio_clips_folderpath)
    except: pass
    ### gen
    scripts_split_filenames = sorted(os.listdir(script_split_folderpath))
    for i, script_split_filename in enumerate(scripts_split_filenames):
        ## mk folder
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        try: os.mkdir(f'{audio_clips_folderpath}/{i_str}')
        except: pass
        ## mk clips
        script_split_filepath = f'{script_split_folderpath}/{script_split_filename}'
        with open(script_split_filepath) as f: text = f.read()
        # text = polish.text_format(text)
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
            output_filepath = f'{audio_clips_folderpath}/{i_str}/{j_str}.wav'
            print('##################################################')
            print(output_filepath)
            print('##################################################')
            sf.write(output_filepath, audio, 24000)
            j += 1

def audio_clips_gen(regen=False):
    import subprocess
    concat_filepath = f'{lesson_folderpath}/concat.txt'
    audio_clips_chunks_folderpath = f'{lesson_folderpath}/audio-clips-chunks'
    audio_clips_folderpath = f'{lesson_folderpath}/audio-clips'
    ### clean
    if regen: 
        try: shutil.rmtree(audio_clips_folderpath)
        except: pass
    try: os.mkdir(audio_clips_folderpath)
    except: pass
    ### gen
    audio_clips_chunks_foldernames = sorted(os.listdir(audio_clips_chunks_folderpath))
    for audio_clip_chunk_foldername in audio_clips_chunks_foldernames:
        _tmp_script_split_clips_folderpath = f'{audio_clips_chunks_folderpath}/{audio_clip_chunk_foldername}'
        tmp_script_split_clips_filenames = sorted(os.listdir(_tmp_script_split_clips_folderpath))
        tmp_script_split_clips_filepaths = [
            f'{_tmp_script_split_clips_folderpath}/{filename}' 
            for filename in tmp_script_split_clips_filenames
        ]
        ###
        with open(concat_filepath, 'w') as f:
            for tmp_script_split_clips_filepath in tmp_script_split_clips_filepaths:
                tmp_script_split_clips_filepath = os.path.abspath(
                    os.path.join(f'./', tmp_script_split_clips_filepath)
                )
                # print(tmp_script_split_clips_filepath)
                # quit()
                f.write(f"file '{tmp_script_split_clips_filepath}'\n")
        audio_clip_filepath = f'{audio_clips_folderpath}/{audio_clip_chunk_foldername}.wav'
        print(audio_clip_filepath)
        # quit()
        subprocess.run([
            f'ffmpeg',
            f'-f', f'concat',
            f'-safe', f'0',
            f'-i', f'{concat_filepath}', 
            f'-acodec', f'pcm_s16le', 
            f'{audio_clip_filepath}', 
            f'-y',
        ])

def video_clips_gen(regen=False):
    import subprocess
    slides_folderpath = f'{lesson_folderpath}/slides'
    audio_clips_folderpath = f'{lesson_folderpath}/audio-clips'
    video_clips_folderpath = f'{lesson_folderpath}/video-clips'
    ### clean
    if regen:
        try: shutil.rmtree(video_clips_folderpath)
        except: pass
    try: os.mkdir(video_clips_folderpath)
    except: pass
    ### gen
    audio_filenames = sorted(os.listdir(audio_clips_folderpath))
    slides_filenames = sorted(os.listdir(slides_folderpath))
    for i, audio_filename in enumerate(audio_filenames):
        audio_filepath = f'{audio_clips_folderpath}/{audio_filename}'
        i_str = ''
        if i >= 10000: i_str = f'{i}'
        elif i >= 1000: i_str = f'0{i}'
        elif i >= 100: i_str = f'00{i}'
        elif i >= 10: i_str = f'000{i}'
        else: i_str = f'0000{i}'
        slide_filepath = f'{slides_folderpath}/{slides_filenames[i]}'
        video_filepath = f'{video_clips_folderpath}/{i_str}.mp4'
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
    concat_filepath = f'{lesson_folderpath}/concat.txt'
    video_clips_folderpath = f'{lesson_folderpath}/video-clips'
    video_final_folderpath = f'{lesson_folderpath}/video-final'
    ### clean
    if regen:
        try: os.mkdir(video_final_folderpath)
        except: pass
    try: os.mkdir(video_final_folderpath)
    except: pass
    ### gen
    video_clips_filenames = sorted(os.listdir(video_clips_folderpath))
    with open(concat_filepath, 'w') as f:
        for i, video_clip_filename in enumerate(video_clips_filenames):
            video_clip_filepath = os.path.abspath(os.path.join(f'./', f'{video_clips_folderpath}/{video_clip_filename}'))
            # video_clip_filepath = f'{video_clips_folderpath}/{video_clip_filename}'
            f.write(f"file '{video_clip_filepath}'\n")
    video_final_filepath = f'{video_final_folderpath}/final.mp4'
    subprocess.run([
        f'ffmpeg',
        f'-f', f'concat',
        f'-safe', f'0',
        f'-i', f'{concat_filepath}',
        f'-c', f'copy',
        f'{video_final_filepath}',
        f'-y', 
    ])

script_split_gen(regen=True)
audio_clips_chunks_gen(regen=True)
audio_clips_gen(regen=True)
video_clips_gen(regen=True)
video_final_gen(regen=True)
quit()

def clips_gen():
    ### clear clips
    for filename in os.listdir(f'test/clips'):
        os.remove(f'test/clips/{filename}')

    ### generate clips
    pipeline = KPipeline(lang_code='a')
    with open('test.txt') as f: text = f.read()
    generator = pipeline(text, voice='af_heart')
    for i, (gs, ps, audio) in enumerate(generator):
        print(i, gs, ps)
        i_str = ''
        if i >= 1000: i_str = f'{i}'
        elif i >= 100: i_str = f'0{i}'
        elif i >= 10: i_str = f'00{i}'
        else: i_str = f'000{i}'
        sf.write(f'test/clips/{i_str}.wav', audio, 24000)

clips_gen()

### gen final clip
test_clips_filenames = sorted(os.listdir(f'test/clips'))
concat_filepath = f'test/concat.txt'
with open(concat_filepath, 'w') as f:
    for i, test_clip_filename in enumerate(test_clips_filenames):
        test_clip_filepath = f'/home/ubuntu/proj/audiobook/test/clips/{test_clip_filename}'
        f.write(f"file '{test_clip_filepath}'\n")

subprocess.run([
    f'ffmpeg',
    f'-f', f'concat',
    f'-safe', f'0',
    f'-i', f'{concat_filepath}',
    f'-c', f'copy',
    f'test/final/output.wav',
    f'-y', 
])

subprocess.Popen(['vlc', '--play-and-exit', f'test/final/output.wav'])


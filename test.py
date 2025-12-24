import os
import subprocess

from kokoro import KPipeline
import soundfile as sf 

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


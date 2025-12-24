import os
import tkinter as tk

from kokoro import KPipeline
import soundfile as sf 

from lib import llm

tmp_folderpath = '/home/ubuntu/proj/audiobook/prompt-crafter/tmp'

def generate_reply(event=None):
    content = prompt_textarea.get('1.0', tk.END).strip()
    prompt = f'''
        {content}
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    content = reply
    content = content.replace('…', ',')
    content = content.replace('*', '')
    content = content.replace('(', '')
    content = content.replace(')', '')
    content = content.replace('—', '. ')
    reply_textarea.delete('1.0', tk.END)
    reply_textarea.insert(tk.END, content)

def save_text(event=None):
    content = prompt_textarea.get('1.0', tk.END).strip()
    with open('prompt-crafter-current.txt', 'w') as f: f.write(content)

def load_text(event=None):
    try: 
        with open('prompt-crafter-current.txt') as f: content = f.read()
    except: return
    prompt_textarea.delete('1.0', tk.END)
    prompt_textarea.insert(tk.END, content)

def play_text(event=None):
    for filename in os.listdir(f'{tmp_folderpath}/audio-clips'):
        os.remove(f'{tmp_folderpath}/audio-clips/{filename}')
    content = reply_textarea.get('1.0', tk.END).strip()
    content = content.replace('…', ',')
    content = content.replace('*', '')
    content = content.replace('(', '')
    content = content.replace(')', '')
    content = content.replace('—', '. ')
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(content, voice='af_heart')
    j = 0
    for (gs, ps, audio) in generator:
        print(j, gs, ps)
        j_str = ''
        if j >= 1000: j_str = f'{j}'
        elif j >= 100: j_str = f'0{j}'
        elif j >= 10: j_str = f'00{j}'
        else: j_str = f'000{j}'
        sf.write(f'{tmp_folderpath}/audio-clips/audio-{j_str}.wav', audio, 24000)
        j += 1
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
    subprocess.Popen(['vlc', '--play-and-exit', f'{tmp_folderpath}/audio-final/audio.wav'])

root = tk.Tk()
root.title('Prompt Crafter')
root.geometry('800x600')

frame1 = tk.Frame(root)
frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

prompt_textarea = tk.Text(frame1, wrap=tk.WORD, font=('Arial', 12), height=30, width=40)
prompt_textarea.pack()
prompt_textarea.focus_set()
prompt_textarea.bind('<Control-Return>', generate_reply)
prompt_textarea.bind('<Control-s>', save_text)
prompt_textarea.bind('<Control-l>', load_text)
prompt_textarea.bind('<Control-p>', play_text)

button = tk.Button(frame1, text='Generate Reply', command=generate_reply)
button.pack()

frame2 = tk.Frame(root)
frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

reply_textarea = tk.Text(frame2, wrap=tk.WORD, font=('Arial', 12), height=30, width=40)
reply_textarea.pack()


root.mainloop()

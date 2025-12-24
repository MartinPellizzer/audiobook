from kokoro import KPipeline
import soundfile as sf 

pipeline = KPipeline(lang_code='a')

text = f'''
    this is a sample sentence.
'''

generator = pipeline(text, voice='af_heart')
for i, (gs, ps, audio) in enumerate(generator):
    print(i, gs, ps)
    sf.write(f'{i}.wav', audio, 24000)

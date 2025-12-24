from lib import zimage

script_filepath = f'archaeology-video-script.txt'

with open(script_filepath) as f: script_content = f.read()

visuals = [line.replace('Visuals: ', '') for line in script_content.split('\n') if line.startswith('Visuals: ')]

if 0:
    visuals = [
        'Photorealistic image of a 3,000-year-old stone statue of a serene, enigmatic goddess, carved from a single block of smooth, polished stone, standing tall in the Amazon jungle. The statue has lifelike eyes with a deep, mysterious gaze, hands raised in a peaceful, blessing-like gesture, with intricately detailed fingers. The stone is smooth and finely worked, showing advanced craftsmanship for its age. The statue is set in a dense, overgrown jungle clearing, with ancient roots and foliage surrounding it. The atmosphere is mysterious, slightly eerie, with soft natural lighting filtering through the canopy, casting long shadows. The scene feels untouched by modern hands, as if the statue has been hidden for millennia, exuding a sense of wonder, ambiguity, and the feeling that it shouldn’t exist. Style: photorealistic, high detail, cinematic lighting, subtle eerie ambiance, soft dark humor in the untouched nature of the artifact.',
    ]

for line_i, line in enumerate(visuals):
    print(line)
    zimage.image_create(f'archaeology-0000/tmp/images/{line_i}.jpg', prompt=line, seed=-1)

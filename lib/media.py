from PIL import Image

from lib import g

pipe = None
checkpoint_filepath = f'{g.vault_tmp_folderpath}/stable-diffusion/juggernautXL_ragnarokBy.safetensors'
# lora_filepath = f'{g.vault_tmp_folderpath}/stable-diffusion/lora/watercolor.safetensors'
lora_folderpath = f'{g.vault_tmp_folderpath}/stable-diffusion/lora'

def resize(img, target_w, target_h):
    original_w, original_h = img.size
    scale = max(target_w / original_w, target_h / original_h)
    new_size = (int(original_w * scale), int(original_h * scale))

    resized_img = img.resize(new_size, Image.LANCZOS)
    
    left = (resized_img.width - target_w) // 2
    top = (resized_img.height - target_h) // 2
    right = left + target_w
    bottom = left + target_h

    cropped_img = resized_img.crop((left, top, right, bottom))

    return cropped_img

def image_gen(prompt, width, height, steps=30, cfg=7.0, lora_filename='', lora_keywords=''):
    import torch
    from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
    from diffusers import DPMSolverMultistepScheduler
    global pipe
    if not pipe:
        pipe = StableDiffusionXLPipeline.from_single_file(
            checkpoint_filepath, 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        if lora_filename.strip() != '':
            pipe.load_lora_weights(f'{lora_folderpath}/{lora_filename}.safetensors')
            pipe.fuse_lora(lora_scale=1.0)
            prompt = f'{lora_keywords}, ' + prompt
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(prompt)
    negative_prompt = f'''
        text, watermark,
    '''
    image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=width, height=height, num_inference_steps=steps, guidance_scale=cfg).images[0]
    return image


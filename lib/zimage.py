
pipe = None

# prompt = "Young Chinese woman in red Hanfu, intricate embroidery. Impeccable makeup, red floral forehead pattern. Elaborate high bun, golden phoenix headdress, red flowers, beads. Holds round folding fan with lady, trees, bird. Neon lightning-bolt lamp (⚡️), bright yellow glow, above extended left palm. Soft-lit outdoor night background, silhouetted tiered pagoda (西安大雁塔), blurred colorful distant lights."

def image_create(output_filepath='', prompt='', width=1024, height=1024, seed=-1):
    import torch
    import random
    from diffusers import ZImagePipeline
    global pipe
    if not pipe:
        pipe = ZImagePipeline.from_pretrained(
            "/home/ubuntu/vault-tmp/zimage",
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=False,
        )
        pipe.to("cuda")

    if seed == -1:
        image = pipe(
            prompt=prompt,
            height=height,
            width=width,
            num_inference_steps=9,  # This actually results in 8 DiT forwards
            guidance_scale=0.0,     # Guidance should be 0 for the Turbo models
            generator=torch.Generator("cuda").manual_seed(random.randint(0, 2**32 - 1)),
        ).images[0]
    else:
        image = pipe(
            prompt=prompt,
            height=height,
            width=width,
            num_inference_steps=9,  # This actually results in 8 DiT forwards
            guidance_scale=0.0,     # Guidance should be 0 for the Turbo models
            generator=torch.Generator("cuda").manual_seed(seed),
        ).images[0]
    image.save(output_filepath)
    return image

# image_create(prompt)

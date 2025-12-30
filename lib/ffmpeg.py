
if 0:
    # FADE TRANSITION
    subprocess.run([
        'ffmpeg',
        '-y',
        '-i', clip1,
        '-i', clip2,
        '-filter_complex',
        (
            "[0:v]trim=duration=2,setpts=PTS-STARTPTS,"
            "scale=1280:720,fps=30,format=yuv420p[v0];"
            "[1:v]trim=duration=2,setpts=PTS-STARTPTS,"
            "scale=1280:720,fps=30,format=yuv420p[v1];"
            "[v0][v1]xfade=transition=fade:duration=0.5:offset=1.5[v]"
        ),
        '-map', '[v]',
        '-an',
        '-pix_fmt', 'yuv420p',
        output_filepath
    ], check=True)

        '''
        subprocess.run([
            'ffmpeg',
            '-y',
            '-i', clip_cur_filepath,
            '-i', clip_new_filepath,
            '-filter_complex',
            (
                "[0:v]trim=duration=2.5,setpts=PTS-STARTPTS,"
                "scale=1280:720,fps=30,format=yuv420p[v0];"
                "[1:v]trim=duration=2,setpts=PTS-STARTPTS,"
                "scale=1280:720,fps=30,format=yuv420p[v1];"
                "[v0][v1]xfade=transition=slideleft:duration=0.5:offset=2[v]"
            ),
            '-map', '[v]',
            '-an',
            '-pix_fmt', 'yuv420p',
            clip_out_filepath,
        ], check=True)
        '''

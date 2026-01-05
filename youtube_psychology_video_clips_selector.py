import os
import math
import cv2
import pygame
import numpy as np
from pathlib import Path
import shutil

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

# ideas_num_min = 60
# ideas_num_max = 60

ideas_num = 69

hub_folderpath = f'/home/ubuntu/vault/audiobook/psychology'
with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
ideas = content.strip().split('\n')
video_folderpath = ''
for idea_i, idea in enumerate(ideas):
    # if idea_i < ideas_num_min or idea_i > ideas_num_max: continue
    if idea_i != ideas_num: continue
    i_str = index_to_string(idea_i)
    idea_slug = sluggify(idea)
    video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
    break

# ---------------- CONFIG ---------------- #

VIDEO_DIR = f"{video_folderpath}/tmp/images-animated"
SAVED_DIR = f"{video_folderpath}/tmp/images-animated-selected"

try: os.makedirs(SAVED_DIR)
except: pass

print(VIDEO_DIR)
# quit()
# SAVED_DIR = "saved_videos"

THUMB_SIZE = 512
VIDEO_FPS = 24

GRID_SIZE = 2                  # 2x2 grid
VIDEOS_PER_CLUSTER = 4

THUMB_MARGIN = 20
UI_MARGIN = 30
BUTTON_SIZE = (120, 40)

WINDOW_BG = (18, 18, 18)
HIGHLIGHT_COLOR = (255, 215, 0)
BUTTON_BG = (60, 60, 60)
BUTTON_HOVER = (90, 90, 90)
BUTTON_TEXT = (230, 230, 230)

# ---------------- INIT ---------------- #

pygame.init()
pygame.display.set_caption("Paged Video Viewer")
FONT = pygame.font.SysFont(None, 28)

# ---------------- VIDEO LOADING ---------------- #

def load_video_frames(path, size, fps):
    cap = cv2.VideoCapture(str(path))
    frames = []

    src_fps = cap.get(cv2.CAP_PROP_FPS) or fps
    frame_skip = max(1, int(src_fps // fps))

    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if i % frame_skip == 0:
            frame = cv2.resize(frame, (size, size))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frames.append(surf)

        i += 1

    cap.release()
    return frames

def load_all_videos(video_dir):
    videos = []
    for path in sorted(Path(video_dir).glob("*")):
        frames = load_video_frames(path, THUMB_SIZE, VIDEO_FPS)
        if frames:
            videos.append({
                "path": path,
                "frames": frames,
                "index": 0,
                "timer": 0.0,
                "liked": False,
                "rect": None,
            })
    return videos

# ---------------- PAGING ---------------- #

def get_clusters(videos):
    return [
        videos[i:i + VIDEOS_PER_CLUSTER]
        for i in range(0, len(videos), VIDEOS_PER_CLUSTER)
    ]

# ---------------- LAYOUT ---------------- #

def layout_cluster(cluster, screen_w):
    grid_w = GRID_SIZE * THUMB_SIZE + (GRID_SIZE - 1) * THUMB_MARGIN
    start_x = (screen_w - grid_w) // 2
    start_y = UI_MARGIN * 2

    for i, v in enumerate(cluster):
        r = i // GRID_SIZE
        c = i % GRID_SIZE

        x = start_x + c * (THUMB_SIZE + THUMB_MARGIN)
        y = start_y + r * (THUMB_SIZE + THUMB_MARGIN)

        v["rect"] = pygame.Rect(x, y, THUMB_SIZE, THUMB_SIZE)

# ---------------- UPDATE ---------------- #

def update_videos(cluster, dt):
    for v in cluster:
        v["timer"] += dt
        if v["timer"] >= 1 / VIDEO_FPS:
            v["timer"] = 0
            v["index"] = (v["index"] + 1) % len(v["frames"])

# ---------------- DRAW ---------------- #

def draw_cluster(screen, cluster):
    for v in cluster:
        screen.blit(v["frames"][v["index"]], v["rect"].topleft)
        if v["liked"]:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, v["rect"], 4)
        if any(v["liked"] for v in cluster) and not v["liked"]:
            overlay = pygame.Surface(v["rect"].size)
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, v["rect"].topleft)

def draw_button(screen, rect, text, hover):
    color = BUTTON_HOVER if hover else BUTTON_BG
    pygame.draw.rect(screen, color, rect, border_radius=6)
    label = FONT.render(text, True, BUTTON_TEXT)
    screen.blit(
        label,
        label.get_rect(center=rect.center)
    )

def draw_header(screen, page, total):
    label = FONT.render(
        f"Cluster {page + 1} / {total}",
        True,
        (200, 200, 200),
    )
    screen.blit(label, (UI_MARGIN, UI_MARGIN))

# ---------------- INPUT ---------------- #

'''
def handle_video_click(cluster, pos):
    for v in cluster:
        if v["rect"].collidepoint(pos):
            v["liked"] = not v["liked"]
            print(
                "Liked:" if v["liked"] else "Unliked:",
                v["path"].name
            )
            return None
    return None
'''

def handle_video_click(cluster, pos):
    clicked = None

    for v in cluster:
        if v["rect"].collidepoint(pos):
            clicked = v
            break

    if clicked is None:
        return False

    was_selected = clicked["liked"]

    # Clear cluster
    for v in cluster:
        v["liked"] = False

    # Toggle behavior
    if not was_selected:
        clicked["liked"] = True
        print("Selected:", clicked["path"].name)
    else:
        print("Deselected all")

    return True

def handle_button_click(pos, prev_rect, next_rect, page, total):
    if prev_rect.collidepoint(pos) and page > 0:
        return page - 1
    if next_rect.collidepoint(pos) and page < total - 1:
        return page + 1
    return page

def save_selected(clusters, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    saved = []
    for cluster in clusters:
        for v in cluster:
            if v["liked"]:
                dst = Path(output_dir) / v["path"].name
                shutil.copy2(v["path"], dst)
                saved.append(v["path"].name)

    print(f"Saved {len(saved)} video(s):")
    for name in saved:
        print("  ", name)

# ---------------- MAIN ---------------- #

def main():
    videos = load_all_videos(VIDEO_DIR)
    if not videos:
        raise SystemExit("No videos found.")

    clusters = get_clusters(videos)
    page = 0

    screen_w = 1280
    screen_h = (
        UI_MARGIN * 4
        + GRID_SIZE * THUMB_SIZE
        + (GRID_SIZE - 1) * THUMB_MARGIN
        + BUTTON_SIZE[1]
    )

    screen = pygame.display.set_mode((screen_w, screen_h))
    clock = pygame.time.Clock()

    btn_y = screen_h - BUTTON_SIZE[1] - UI_MARGIN

    prev_btn = pygame.Rect(
        UI_MARGIN,
        btn_y,
        *BUTTON_SIZE
    )

    save_btn = pygame.Rect(
        (screen_w - BUTTON_SIZE[0]) // 2,
        btn_y,
        *BUTTON_SIZE
    )

    next_btn = pygame.Rect(
        screen_w - BUTTON_SIZE[0] - UI_MARGIN,
        btn_y,
        *BUTTON_SIZE
    )

    running = True
    while running:
        dt = clock.tick(60) / 1000
        cluster = clusters[page]
        layout_cluster(cluster, screen_w)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if handle_video_click(cluster, event.pos):
                    pass

                elif prev_btn.collidepoint(event.pos) and page > 0:
                    page -= 1

                elif next_btn.collidepoint(event.pos) and page < len(clusters) - 1:
                    page += 1

                elif save_btn.collidepoint(event.pos):
                    save_selected(clusters, SAVED_DIR)

        update_videos(cluster, dt)

        screen.fill(WINDOW_BG)
        draw_header(screen, page, len(clusters))
        draw_cluster(screen, cluster)

        mouse_pos = pygame.mouse.get_pos()
        draw_button(screen, prev_btn, "PREV", prev_btn.collidepoint(mouse_pos))
        draw_button(screen, save_btn, "SAVE", save_btn.collidepoint(mouse_pos))
        draw_button(screen, next_btn, "NEXT", next_btn.collidepoint(mouse_pos))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

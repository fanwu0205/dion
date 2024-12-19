import pygame
import random
from PIL import Image

# pygame 初始化
pygame.init()

# 畫布大小
screen = pygame.display.set_mode((1280, 400))
pygame.display.set_caption("小恐龍跳躍遊戲")

# 使用 Pillow 加載 GIF 動畫
def load_gif_frames(gif_path):
    # 打開 GIF 動畫文件
    img = Image.open(gif_path)
    frames = []
    try:
        while True:
            # 將每一幀轉換為 pygame 可用的格式
            frame = pygame.image.fromstring(img.convert('RGBA').tobytes(), img.size, 'RGBA')
            frames.append(frame)
            img.seek(img.tell() + 1)
    except EOFError:
        pass  # GIF 動畫結束
    return frames

# 載入恐龍的 GIF 動畫（同一張 GIF）
dino_gif = load_gif_frames("dino.gif")  # 站立和跳躍動作的 GIF（同一張）

# 設置其他遊戲參數
img_cactus = pygame.image.load("monster1.png")
img_cactus = pygame.transform.scale(img_cactus, (70, 70))  # 縮小障礙物尺寸

# 初始化恐龍位置
dino_rect = dino_gif[0].get_rect()
dino_rect.x = 50
dino_rect.y = 300

# 設定障礙物
cactus_list = []
cactus_speed = 10

# 遊戲時鐘
clock = pygame.time.Clock()

# 跳躍設定
is_jumping = False
jump_speed = -20  # 調整初速度讓跳躍弧度更大
gravity = 1.2
velocity_y = 0

# 分數
score = 0

# 遊戲狀態
running = True
game_over = False

# 按鈕
font = pygame.font.SysFont("Arial", 40)
button_rect = pygame.Rect(540, 200, 200, 60)

# 動畫控制變數
frame = 0  # 用來控制恐龍的幀數
lasttime = pygame.time.get_ticks()  # 上次切換幀的時間

def reset_game():
    global cactus_list, dino_rect, score, is_jumping, velocity_y, game_over, frame
    cactus_list = []
    dino_rect.y = 300
    score = 0
    is_jumping = False
    velocity_y = 0
    game_over = False
    frame = 0

while running:
    clock.tick(60)  # 每秒60幀

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                reset_game()

    if not game_over:
        # 檢查按鍵
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not is_jumping:
            is_jumping = True
            velocity_y = jump_speed

        # 跳躍邏輯
        if is_jumping:
            dino_rect.y += velocity_y
            velocity_y += gravity
            if dino_rect.y >= 300:  # 恢復到地面
                dino_rect.y = 300
                is_jumping = False

        # 更新幀數，根據時間切換 GIF 幀
        nowtime = pygame.time.get_ticks()
        if nowtime - lasttime > 100:  # 每100毫秒切換一次
            frame = (frame + 1) % len(dino_gif)  # 循環顯示幀
            lasttime = nowtime

        # 根據跳躍狀態選擇顯示的 GIF 幀
        if is_jumping:
            # 假設 GIF 中的跳躍動畫位於後半部分
            jump_frame = len(dino_gif) // 2
            dino_image = dino_gif[frame + jump_frame]  # 使用 GIF 後半部分幀來顯示跳躍動畫
        else:
            dino_image = dino_gif[frame]  # 站立動畫

        # 障礙物生成
        if random.randint(1, 100) == 1:
            cactus_rect = img_cactus.get_rect()
            cactus_rect.x = 1280
            cactus_rect.y = 330  # 調整障礙物底部位置
            cactus_list.append(cactus_rect)

        # 障礙物移動
        for cactus_rect in cactus_list:
            cactus_rect.x -= cactus_speed
            if cactus_rect.x + cactus_rect.width < 0:
                cactus_list.remove(cactus_rect)
                score += 1

        # 碰撞檢測
        for cactus_rect in cactus_list:
            if dino_rect.colliderect(cactus_rect):
                game_over = True

        # 畫面更新
        screen.fill((255, 255, 255))  # 白色背景
        screen.blit(dino_image, dino_rect)  # 根據幀數畫出恐龍
        for cactus_rect in cactus_list:
            screen.blit(img_cactus, cactus_rect)

        # 顯示分數
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
    else:
        # 顯示遊戲結束畫面
        screen.fill((255, 255, 255))
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, (520, 100))

        # 繪製重新開始按鈕
        pygame.draw.rect(screen, (0, 128, 255), button_rect)
        button_text = font.render("Restart", True, (255, 255, 255))
        screen.blit(button_text, (button_rect.x + 50, button_rect.y + 10))

    # 更新畫面
    pygame.display.flip()

pygame.quit()
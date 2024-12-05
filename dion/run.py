import pygame
import random

# pygame 初始化
pygame.init()

# 畫布大小
screen = pygame.display.set_mode((1280, 400))
pygame.display.set_caption("小恐龍跳躍遊戲")

# 載入圖像
img_dino = pygame.image.load("ss8.png")
img_cactus = pygame.image.load("monster1.png")

# 縮放圖片
img_dino = pygame.transform.scale(img_dino, (100, 100))
img_cactus = pygame.transform.scale(img_cactus, (70, 70))  # 縮小障礙物尺寸

# 初始化恐龍位置
dino_rect = img_dino.get_rect()
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

def reset_game():
    global cactus_list, dino_rect, score, is_jumping, velocity_y, game_over
    cactus_list = []
    dino_rect.y = 300
    score = 0
    is_jumping = False
    velocity_y = 0
    game_over = False

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

        # 障礙物生成
        if random.randint(1, 100) == 1:
            cactus_rect = img_cactus.get_rect()
            cactus_rect.x = 1280
            cactus_rect.y = 330  # 調整障礙物底部位置
            cactus_list.append(cactus_rect)

        # 障礙物移動
        for cactus_rect in cactus_list[:]:
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
        screen.blit(img_dino, dino_rect)  # 畫出恐龍
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
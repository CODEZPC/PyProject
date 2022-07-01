import pygame
import random
import os
from pygame import mixer
from spritesheet import SpriteSheet
from enemy import Enemy

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 10
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_panel(screen, score, font_small):
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text(screen, '得分: ' + str(score), font_small, WHITE, 0, 0)

def draw_bg(screen, bg_image, bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))

class Player(object):
    def __init__(self, x, y, player_image):
        self.image = pygame.transform.scale(player_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self, platform_group, jump_fx):
        scroll = 0
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False
        self.vel_y += GRAVITY
        dy += self.vel_y
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        jump_fx.play()
        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                scroll = -dy
        self.rect.x += dx
        self.rect.y += dy + scroll
        return scroll
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving, platform_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self, scroll):
        if self.moving is True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def main():
    pygame.init()
    mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('跳一跳')
    pygame.mixer.music.load('assets/music.mp3')
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1, 0.0)
    jump_fx = pygame.mixer.Sound('assets/jump.mp3')
    jump_fx.set_volume(0.5)
    death_fx = pygame.mixer.Sound('assets/death.mp3')
    death_fx.set_volume(0.5)
    bg_scroll = 0
    game_over = False
    score = 0
    fade_counter = 0
    if os.path.exists('score.txt'):
        with open('score.txt', 'r') as file:
            high_score = int(file.read())
    else:
        high_score = 0
    font_small = pygame.font.Font('yh.ttf', 20)
    font_big = pygame.font.Font('yh.ttf', 24)
    player_image = pygame.image.load('assets/jump.png').convert_alpha()
    bg_image = pygame.image.load('assets/bg.png').convert_alpha()
    platform_image = pygame.image.load('assets/wood.png').convert_alpha()
    bird_sheet_img = pygame.image.load('assets/bird.png').convert_alpha()
    bird_sheet = SpriteSheet(bird_sheet_img)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, player_image)
    platform_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, platform_image)
    platform_group.add(platform)
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 更新高分数
                if score > high_score:
                    high_score = score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                run = False
        if game_over is False:
            scroll = player.move(platform_group, jump_fx)
            bg_scroll += scroll
            if bg_scroll >= 600:
                bg_scroll = 0
            draw_bg(screen, bg_image, bg_scroll)
            if len(platform_group) < MAX_PLATFORMS:
                p_w = random.randint(40, 60)
                p_x = random.randint(0, SCREEN_WIDTH - p_w)
                p_y = platform.rect.y - random.randint(80, 120)
                p_type = random.randint(1, 2)
                if p_type == 1 and score > 500:
                    p_moving = True
                else:
                    p_moving = False
                platform = Platform(p_x, p_y, p_w, p_moving, platform_image)
                platform_group.add(platform)
            platform_group.update(scroll)
            if len(enemy_group) == 0 and score > 1500:
                enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
                enemy_group.add(enemy)
            enemy_group.update(scroll, SCREEN_WIDTH)
            if scroll > 0:
                score += scroll
            pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 3)
            draw_text(screen, '历史最高分', font_small, WHITE, SCREEN_WIDTH - 130, score - high_score + SCROLL_THRESH)
            platform_group.draw(screen)
            enemy_group.draw(screen)
            player.draw(screen)
            draw_panel(screen, score, font_small)
            if player.rect.top > SCREEN_HEIGHT:
                game_over = True
                death_fx.play()
            if pygame.sprite.spritecollide(player, enemy_group, False):
                if pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_mask):
                    game_over = True
                    death_fx.play()
        else:
            if fade_counter < SCREEN_WIDTH:
                fade_counter += 5
                for y in range(0, 6, 2):
                    pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, 100))
                    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
            else:
                draw_text(screen, 'GAME OVER!', font_big, WHITE, 130, 200)
                draw_text(screen, 'SCORE: ' + str(score), font_big, WHITE, 160, 250)
                draw_text(screen, 'Press the SPACEBAR again', font_big, WHITE, 110, 300)
                if score > high_score:
                    high_score = score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    game_over = False
                    score = 0
                    scroll = 0
                    fade_counter = 0
                    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                    enemy_group.empty()
                    platform_group.empty()
                    platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, platform_image)
                    platform_group.add(platform)
        clock.tick(FPS)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()

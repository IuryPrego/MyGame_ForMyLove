from random import randint
from sys import exit
import pygame
import os
import sys
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

pygame.init()


# funções
def display_text(surface, text, pos, font, color):
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x, y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= surface.get_size()[0]:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height


def fade_img(v, img):
    img.set_alpha(img.get_alpha() - v)


def enemy_move(enemys, surface, enemy_surf):
    if enemys:
        for i in range(len(enemys)):
            enemys[i].x += 16

            surface.blit(enemy_surf, enemys[i])
        enemys = [enemy for enemy in enemys if enemy.x < 900]

        return enemys
    else:
        return []


def collision(player, enemys):
    if enemys:
        for enemy in enemys:
            if (player.colliderect(enemy)):
                return True
            else:
                return False


# Fixos
start_time = 0
temp_surf = []
vdown = 0
vup = 0
user_text = ''
display_control = [False, False]
active = False
scene_number = 0
fade = False
fade_control = 0
screen_size = (700, 680)
background = pygame.Surface(screen_size)
clock = pygame.time.Clock()
game_font = pygame.font.Font('data/fonts/Birds of Paradise.ttf', 40)
janela = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Uma aventura natalina! (vlw natalina)')
with open('data/Cenas/textos.txt', 'r') as arq:
    texts = arq.readlines()
    for i in range(len(texts)):
        texts[i] = texts[i].replace('\\n', '\n')

# Variáveis de construção de cena
scenes_infos = [[0, 'data/Cenas/Cena1.jpg', (180, 40, 35), (20, 520)],
                [0, 'data/Cenas/cena2_def.png', (255, 255, 255), (20, 500)],
                [0, 'data/Cenas/rena lacada.jpg', (180, 40, 35), (280, 550)],
                [0, 'data/Cenas/cena4.jpg', (180, 40, 35), (280, 580)],
                [0, 'data/Cenas/pegada floresta.jpg', (0, 0, 0), (0, 100)],
                [1, 'data/Cenas/tronco.jpg', (0, 0, 0), (0, 148), (0, 534)],
                [2, 'data/Cenas/trenó2.png', (0, 0, 0), (0, 148), (320, 0)],
                [3, 'data/Cenas/cena perder.png',
                    (255, 255, 255), (150, 520), (0, 0)],
                [0, 'data/Cenas/cena final.jpg', (255, 255, 255), (20, 500), (0, 0)]]

# game_state 2
# player sec
player_path = scenes_infos[6][1]
player_surf = pygame.image.load(player_path).convert_alpha()
player_rect = player_surf.get_rect(midright=(680, 350))
# enemy sec
enemy_surf = pygame.image.load('data/Cenas/bitmap.png').convert_alpha()
enemy_rect_list = []
# Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 500)

while True:
    game_state = scenes_infos[scene_number][0]

    # variables definition
    if game_state != 2:
        scene_path = scenes_infos[scene_number][1]
        text = texts[scene_number]
        color_text = scenes_infos[scene_number][2]
        text_position = scenes_infos[scene_number][3]
        scene_img = pygame.image.load(scene_path).convert_alpha()
        if game_state == 1:
            input_rect = pygame.Rect(
                scenes_infos[scene_number][4][0], scenes_infos[scene_number][4][1], screen_size[0], screen_size[1] - 534)
            input_surf = pygame.Surface(input_rect.size)
            input_surf.fill((255, 0, 0))
        background.fill((0, 0, 0))
        if game_state == 3:
            background.fill((120, 0, 0))
    else:
        background.fill((255, 255, 255))

    # teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == 1:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if game_state == 1 and active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
            if event.key == pygame.K_RETURN and game_state == 1:
                display_control[1] = False
                if user_text.strip().lower() == 'sexta':
                    fade_control = 0
                    fade = True
                elif user_text.strip().lower() == 'estou na mesa da cozinha':
                    display_control[0] = True
                else:
                    display_control[1] = True
                user_text = ''
            elif event.key == pygame.K_RETURN and (game_state == 0 or game_state == 3):
                fade_control = 0
                fade = True
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and game_state == 2:
                vup = 10
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and game_state == 2:
                vdown = 10
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and game_state == 2:
                vup = 0
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and game_state == 2:
                vdown = 0
        if event.type == enemy_timer and game_state == 2:
            rand = randint(0, 680-96)
            enemy_rect_list.append(enemy_surf.get_rect(
                topright=(0, rand)))
    # run

    if game_state != 2:
        if fade and scene_number < 8:
            fade_img(fade_control, scene_img)
            fade_control += 10
        elif fade and scene_number == 8:
            pygame.quit()
            exit()
        if scene_img.get_alpha() <= 0 and fade == True:
            fade = False
            if game_state == 0 or game_state == 1:
                scene_number += 1
            elif game_state == 3:
                scene_number -= 1

    janela.blit(background, (0, 0))

    if game_state == 0 or game_state == 1:
        janela.blit(scene_img, (0, 0))
        display_text(janela, text, text_position, game_font, color_text)

    if game_state == 1:
        font_temp = pygame.font.Font(None, 40)
        display_text(janela, 'PesPtou Pna PmePsa Pda PcoPziPnha',
                     (0, 450), font_temp, color_text)

        display_text(janela, 'clique no retangulo\npara digitar\nvale pesquisar no google',
                     (0, 0), font_temp, (0, 0, 0))
        if display_control[0] == True:
            display_text(
                janela, 'voce descobriu o enigma\nMas interpretou errado\nvai la procurar!!!', (350, 300), game_font, (0, 0, 0))
        if display_control[1] == True:
            display_text(
                janela, 'errou! tenta de novo!', (450, 100), game_font, (0, 0, 0))

        if active:
            color = (100, 100, 100)
        else:
            color = (0, 0, 0)
        pygame.draw.rect(janela, color, input_rect)
        display_text(janela, user_text, (0, 534),
                     game_font, (255, 255, 255))

    if game_state == 2:
        if start_time == 0:
            start_time = pygame.time.get_ticks()

        time_now = pygame.time.get_ticks()

        player_rect.top -= vup - vdown
        if player_rect.top <= 0:
            player_rect.top = 0
        if player_rect.bottom >= screen_size[1]:
            player_rect.bottom = screen_size[1]
        enemy_rect_list = enemy_move(
            enemy_rect_list, janela, enemy_surf)
        janela.blit(player_surf, player_rect)
        if collision(player_rect, enemy_rect_list):
            scene_number += 1
        time_game = 21000 - (time_now - start_time)
        timer_pos = scenes_infos[scene_number][4]
        if time_game >= 10000:
            time_str = f'{time_game}'[:2]
        else:
            time_str = '0'+f'{time_game}'[:1]
        display_text(janela, time_str, timer_pos,
                     pygame.font.Font(None, 60), (0, 0, 0))
        if scene_number == 6 and time_game <= 1000:
            scene_number += 2

    if game_state == 3:
        janela.blit(scene_img, ((700 - 512)/2, 20))
        display_text(janela, text, text_position,
                     game_font, color_text)
        player_rect.midright = (680, 350)
        vup = 0
        vdown = 0
        enemy_rect_list = []
        start_time = 0

    pygame.display.update()
    clock.tick(30)

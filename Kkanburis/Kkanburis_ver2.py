# -*-coding:utf-8-*-
# PYTRIS Copyright (c) 2017 Jason Kim All Rights Reserved.

import pygame
import operator
import datetime
from mino import *
from random import *
import random as rand
from pygame.locals import *
from database import *

# Define values
color_active = pygame.Color('lightskyblue3')
color_inactive = pygame.Color('blue')
color = color_inactive
text=''
FONT = pygame.font.FONT(None, 32)

block_size = 17  # Height, width of single block
width = 10  # Board width
height = 20  # Board height
board_x = 10
board_y = 20

board_width = 800   # 가로 크기
board_height = 450   # 세로 크기
board_rate = 0.5625
block_size = int(board_height * 0.045)
mino_matrix_x = 4   # mino는 4*4 배열 -> for문에서 변수로 사용
mino_matrix_y = 4

speed_incre = 2   # 레벨 별 블록 하강 속도의 상승 정도

min_width = 400   # 최소 화면 너비
min_height = 225   # 최소 화면 높이
mid_width = 1200

framerate = 30  # Bigger -> Slower

set_300 = 300   # 0.3초

pygame.init()   # 게임 초가화

clock = pygame.time.Clock()   # FPS - 화면을 초당 몇 번 출력하는가? -> clock.tick() 가 높을수록 CPU를 많이 사용 
# pygame.RESIZABLE : 마우스 커서로 screen 화면 조절 가능
screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)   # 스크린 화면을 설정하는 변수 (board_width, board_height)

# pygame.time.set_timer(eventid, milliseconds, once) : 이벤트 큐에서 이벤트를 반복적으로 생성
# once = true -> 타이머를 한 번만
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("Kkanburis")   # 화면 타이틀 설정 - 게임 이름 표시

# 변수 클래스 -> 변수 파일 따로 생성할지 결정
class ui_variables:
    # Fonts
    font_path = "./assets/fonts/OpenSans-Light.ttf"
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"
    font_path_i = "./assets/fonts/Inconsolata/Inconsolata.otf"

    h1 = pygame.font.Font(font_path_b, 80)
    h2 = pygame.font.Font(font_path_b, 30)
    h4 = pygame.font.Font(font_path_b, 20)
    h5 = pygame.font.Font(font_path_b, 13)
    h6 = pygame.font.Font(font_path_b, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds

    pygame.mixer.music.load("assets/sounds/SFX_BattleMusic.wav")
    pygame.mixer.music.set_volume(0.3)

    intro_sound = pygame.mixer.Sound("assets/sounds/SFX_Intro.wav")   # 시작 화면 배경음악 - 끊기지 않게 
    fall_sound = pygame.mixer.Sound("assets/sounds/SFX_Fall.wav")   # 
    break_sound = pygame.mixer.Sound("assets/sounds/SFX_Break.wav")   # 블럭 사라질 때 소리 - 콤보로 한 줄 사라질 때?
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav")   # 설정이나 기타 버튼 누를 때 소리
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")   # 블럭 이동 시 소리
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")   # 블럭 하드드롭 시 소리
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav")
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")
    LevelUp_sound = pygame.mixer.Sound("assets/sounds/SFX_LevelUp.wav")   # 레벨 업 시 소리
    GameOver_sound = pygame.mixer.Sound("assets/sounds/SFX_GameOver.wav")   # 게임 종료 시 소리

    # Combo graphic
    combos = []
    large_combos = []
    combo_ring = pygame.image.load("assets/Combo/4combo ring.png")  # 4블록 동시제거 그래픽
    combo_4ring = pygame.transform.smoothscale(combo_ring, (200, 100))   # 이미지를 특정 크기로 불러옴 -> 가로 200, 세로 100
    for i in range(1, 11):   # Max Combo를 10으로 지정
        combos.append(pygame.image.load("assets/Combo/" + str(i) + "combo.png"))   #combos: 각 콤보 이미지를 추가한 리스트
        # pygame.transform.smoothscale() : 표면을 임의의 크기로 부드럽게 조정
        large_combos.append(pygame.transform.smoothscale(combos[i - 1], (150, 200)))   # large_combo: combo 이미지 조정해서 리스트에 추가

    combos_sound = []   # 10가지 combo 사운드 한 번에 조절하기 위해
    for i in range(1, 10):
        combos_sound.append(pygame.mixer.Sound("assets/sounds/SFX_" + str(i + 2) + "Combo.wav"))

    # Background colors
    black = (10, 10, 10)  # rgb(10, 10, 10)
    white = (0, 153, 153)  # rgb(255, 255, 255) # 청록색으로 변경
    real_white = (255, 255, 255)  # rgb(255, 255, 255) # 청록색으로 변경

    grey_1 = (70, 130, 180)  # rgb(26, 26, 26) 테두리 파랑색
    grey_2 = (221, 221, 221)  # rgb(35, 35, 35)
    grey_3 = (000, 000, 139)  # rgb(55, 55, 55)  # 남색
    bright_yellow = (255, 217, 102)  # 밝은 노랑

    # Tetrimino colors
    cyan = (10, 255, 226)  # rgb(69, 206, 204) # I
    blue = (64, 105, 255)  # rgb(64, 111, 249) # J
    orange = (245, 144, 12)  # rgb(253, 189, 53) # L
    yellow = (225, 242, 41)  # rgb(246, 227, 90) # O
    green = (22, 181, 64)  # rgb(98, 190, 68) # S
    pink = (242, 41, 195)  # rgb(242, 64, 235) # T
    red = (204, 22, 22)  # rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]
    cyan_image = 'assets/block_images/cyan.png'
    blue_image = 'assets/block_images/blue.png'
    orange_image = 'assets/block_images/orange.png'
    yellow_image = 'assets/block_images/yellow.png'
    green_image = 'assets/block_images/green.png'
    pink_image = 'assets/block_images/purple.png'
    red_image = 'assets/block_images/red.png'
    ghost_image = 'assets/block_images/ghost.png'
    table_image = 'assets/block_images/background.png'
    linessent_image = 'assets/block_images/linessent.png'
    t_block = [table_image, cyan_image, blue_image, orange_image, yellow_image, green_image, pink_image, red_image,
               ghost_image, linessent_image]

class button():   # 버튼 객체
    # def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, id, img=''):   # 버튼 생성
    def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, id, img=''):   # 버튼 생성
        self.x = board_width * x_rate   # 버튼 x 좌표
        self.y = board_height * y_rate   # 버튼 y 좌표
        self.width = int(board_width * width_rate)   # 버튼의 너비
        self.height = int(board_height * height_rate)   # 버튼의 높이
        self.x_rate = x_rate   
        self.y_rate = y_rate
        self.width_rate = width_rate
        self.height_rate = height_rate
        # self.id = id
        self.image = img

    def change(self, board_width, board_height):   # 버튼 위치, 크기 바꾸기
        self.x = board_width * self.x_rate   # x 좌표
        self.y = board_height * self.y_rate   # y 좌표
        self.width = int(board_width * self.width_rate)   # 너비
        self.height = int(board_height * self.height_rate)   # 높이


    def draw(self, win, outline=None):   # 버튼 보이게 만들기 
        if outline:
            draw_image(screen, self.image, self.x, self.y, self.width, self.height)

    def isOver(self, pos):   # 마우스의 위치에 따라 버튼 누르기 -> pos[0]: 마우스의 x 좌표 / pos[1]: 마우스의 y 좌표
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):   # 좌측 화면/우측 화면 넘어가기 전, 
            if pos[1] > self.y - (self.height / 2) and pos[1] < self.y + (self.height / 2):   # 상/하단 화면 넘어가기 전, 
                return True
        return False

# InoutBox 초기 설정
class InputBox:
    def __init__(self, x, y, w, h, text = ''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the user clicked on the inpur_box rect
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable
                self.active = not self.active
            else:
                self.active = False
            # Change the currnet of input box
            self.color = color_active if self.active else color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text
                self.text_surface = FONT.render(text, True, self.color)

    def update(self):
        # Resize the box if the txt is too long
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the text
        screen.draw.rect(screen, self.color, self.rect, 2)

# InputBox 설정
# Sign up에서 box
input_box1 = InputBox(int(board_width * 322 / 800), int(board_height * 155.5/450), 156, 32)
input_box2 = InputBox(int(board_width * 322 / 800), int(board_height * 242.5/450), 156, 32)
input_boxes_signup = [input_box1, input_box2]
# Sign in에서 box
input_box3 = InputBox(int(board_width * 322 / 800), int(board_height * 155.5/450), 156, 32)
input_box4 = InputBox(int(board_width * 322 / 800), int(board_height * 242.5/450), 156, 32)
input_boxes_signin = [input_box3, input_box4]

# start_image = 'assets/images/start.png'
# help_image = 'assets/images/help.png'
# start_button = button(board_width * 0.5, board_height * 0.5, 146, 43, 1, start_image)

background_image = 'assets/vector/Background.png'   # 배경 보드 이미지 

single_button_image = 'assets/vector/single_button.png'   # 싱글 모드 버튼 이미지
clicked_single_button_image = 'assets/vector/clicked_single_button.png'   # 싱글 모드 버튼 클릭 시 이미지

pvp_button_image = 'assets/vector/pvp_button.png'   # PVP 모드 버튼 이미지
clicked_pvp_button_image = 'assets/vector/clicked_pvp_button.png'   # PVP 모드 버튼 클릭 시 이미지

help_button_image = 'assets/vector/help_button.png'   # HELP 버튼 이미지
clicked_help_button_image = 'assets/vector/clicked_help_button.png'   # HELP 버튼 클릭 시 이미지

quit_button_image = 'assets/vector/quit_button.png'   # 종료 버튼 이미지
clicked_quit_button_image = 'assets/vector/clicked_quit_button.png'   # 종료 버튼 클릭 시 이미지

leaderboard_vector = 'assets/vector/leaderboard_vector.png'   # 리더보드 버튼(아이콘) 이미지 
clicked_leaderboard_vector = 'assets/vector/clicked_leader_vector.png'   # 리더보드 버튼(아이콘) 클릭 시 이미지  

setting_vector = 'assets/vector/setting_vector.png'
clicked_setting_vector = 'assets/vector/clicked_setting_vector.png'

pause_board_image = 'assets/vector/pause_board.png'   # 정지 보드 이미지
leader_board_image = 'assets/vector/leader_board.png'   # 리더보드 판 이미지
setting_board_image = 'assets/vector/setting_board.png'   # 설정 보드 판 이미지
gameover_board_image = 'assets/vector/gameover_board.png'   # 게임 종료 보드 이미지

smallsize_board = 'assets/vector/screensize1.png'   # 설정 - 스크린 화면 조절 버튼(사이즈별)
midiumsize_board = 'assets/vector/screensize2.png'
bigsize_board = 'assets/vector/screensize3.png'

mute_button_image = 'assets/vector/mute_button.png'   # 음소거 버튼
##clicked_mute_button_image = 'assets/vector/clicked_mute_button.png'

number_board = 'assets/vector/number_board.png'   # ?

resume_button_image = 'assets/vector/resume_button.png'   # 재개 버튼
clicked_resume_button_image = 'assets/vector/clicked_resume_button.png'

restart_button_image = 'assets/vector/restart_button.png'   # 재시작 버튼
clicked_restart_button_image = 'assets/vector/clicked_restart_button.png'

setting_button_image = 'assets/vector/setting_button.png'   # 설정 버튼
clicked_setting_button_image = 'assets/vector/clicked_setting_button.png'

back_button_image = 'assets/vector/back_button.png'   # 뒤로 가기 버튼
clicked_back_button_image = 'assets/vector/clicked_back_button.png'

volume_vector = 'assets/vector/volume_vector.png'   # 볼륨 조절 버튼
clicked_volume_vector = 'assets/vector/clicked_volume_vector.png'

keyboard_vector = 'assets/vector/keyboard_vector.png'   # 키보드 버튼
clicked_keyboard_vector = 'assets/vector/clicked_keyboard_vector.png'

screen_vector = 'assets/vector/screen_vector.png'   # 화면 버튼
clicked_screen_vector = 'assets/vector/clicked_screen_vector.png'

menu_button_image = 'assets/vector/menu_button.png'   # 메뉴 버튼
clicked_menu_button_image = 'assets/vector/clicked_menu_button.png'

ok_button_image = 'assets/vector/ok_button.png'   # OK(확인) 버튼
clicked_ok_button_image = 'assets/vector/clicked_ok_button.png'

plus_button_image = 'assets/vector/plus_button.png'   # + 조절 버튼
clicked_plus_button_image = 'assets/vector/clicked_plus_button.png'

minus_button_image = 'assets/vector/minus_button.png'   # - 조절 버튼
clicked_minus_button_image = 'assets/vector/clicked_minus_button.png'

check_button_image = 'assets/vector/checkbox_button.png'   # 체크박스 버튼
clicked_check_button_image = 'assets/vector/clicked_checkbox_button.png'

# 아이템 이미지
bomb_image = 'item/bomb_powerup.png'
explosion_image = 'item/explosion.png'

# 회원가입/로그인 이미지
signup_board = 'assets/vector/signup.png'
signin_board = 'assets/vector/signin.png'
login_bg = 'assets/vector/Background_login.png'
log_board = 'assets/vector/log_or_sign_board.png'

button_log_back = 'assets/vector/button_l_back.png'   # 이거 추가
button_log_back_clicked = 'assets/vector/button_l_back_clicked.png'   # 이거 추가
button_sign_up = 'assets/vector/button_sign_up.png'
button_sign_up_clicked = 'assets/vector/button_sign_up_clicked.png'
button_sign_in = 'assets/vector/button_sign_in.png'
button_sign_in_clicked = 'assets/vector/button_sign_in_clicked.png'
button_quit = 'assets/vector/button_quit.png'
button_quit_clicked = 'assets/vector/button_quit_clicked.png'

# 버튼 객체 생성 - class button()에서 확인
# def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img = '')
# (현재 보드 너비, 현재 보드 높이, 버튼의 x 좌표 위치 비율, 버튼의 y좌표 위치 비율, 버튼의 너비 길이 비율, 버튼의 높이 길이 비율) - 전체 화면 크기에 대한 비율

# 변경된 버튼 클래스에 따라 크기 다시
mute_button = button(board_width, board_height, 0.5, 0.23, 0.18, 0.14, 1, mute_button_image)   

single_button = button(board_width, board_height, 0.78, 0.23, 0.37, 0.17, 1, single_button_image)
pvp_button = button(board_width, board_height, 0.78, 0.43, 0.37, 0.17, 2, pvp_button_image)
help_button = button(board_width, board_height, 0.78, 0.63, 0.37, 0.17, 3, help_button_image)
quit_button = button(board_width, board_height, 0.78, 0.83, 0.37, 0.17, 4, quit_button_image)
setting_icon = button(board_width, board_height, 0.1, 0.85, 0.15, 0.15, 5, setting_vector)
leaderboard_icon = button(board_width, board_height, 0.1, 0.6, 0.15, 0.15, 6, leaderboard_vector)

resume_button = button(board_width, board_height, 0.5, 0.23, 0.37, 0.17, 1, resume_button_image)
restart_button = button(board_width, board_height, 0.5, 0.43, 0.37, 0.17, 1, restart_button_image)
restart_button_pvp1 = button(board_width, board_height, 0.25, 0.43, 0.37, 0.17, 1, restart_button_image)
restart_button_pvp2 = button(board_width, board_height, 0.75, 0.43, 0.37, 0.17, 1, restart_button_image)
setting_button = button(board_width, board_height, 0.5, 0.63, 0.37, 0.17, 1, setting_button_image)
pause_quit_button = button(board_width, board_height, 0.5, 0.83, 0.37, 0.17, 1, quit_button_image)

back_button = button(board_width, board_height, 0.5, 0.9, 0.37, 0.17, 1, back_button_image)
volume_icon = button(board_width, board_height, 0.4, 0.5, 0.15, 0.15, 5, volume_vector)
screen_icon = button(board_width, board_height, 0.6, 0.5, 0.15, 0.15, 6, screen_vector)
ok_button = button(board_width, board_height, 0.5, 0.83, 0.37, 0.17, 1, ok_button_image)
ok_button_pvp1 = button(board_width, board_height, 0.25, 0.83, 0.37, 0.17, 1, ok_button_image)
ok_button_pvp2 = button(board_width, board_height, 0.75, 0.83, 0.37, 0.17, 1, ok_button_image)

menu_button = button(board_width, board_height, 0.5, 0.23, 0.37, 0.17, 1, menu_button_image)
menu_button_pvp1 = button(board_width, board_height, 0.25, 0.23, 0.37, 0.17, 1, menu_button_image)
menu_button_pvp2 = button(board_width, board_height, 0.75, 0.23, 0.37, 0.17, 1, menu_button_image)
gameover_quit_button = button(board_width, board_height, 0.5, 0.43, 0.37, 0.17, 1, quit_button_image)

volume = 1.0

effect_plus_button = button(board_width, board_height, 0.43, 0.43, 0.06, 0.11, 1, plus_button_image)
effect_minus_button = button(board_width, board_height, 0.57, 0.43, 0.06, 0.11, 1, minus_button_image)

sound_plus_button = button(board_width, board_height, 0.43, 0.63, 0.06, 0.11, 1, plus_button_image)
sound_minus_button = button(board_width, board_height, 0.57, 0.63, 0.06, 0.11, 1, minus_button_image)

mute_check_button = button(board_width, board_height, 0.2, 0.4, 0.06, 0.11, 1, check_button_image)
smallsize_check_button = button(board_width, board_height, 0.5, 0.25, 0.18, 0.14, 1, smallsize_board)
midiumsize_check_button = button(board_width, board_height, 0.5, 0.45, 0.18, 0.14, 1, midiumsize_board)
bigsize_check_button = button(board_width, board_height, 0.5, 0.65, 0.18, 0.14, 1, bigsize_board)

# 회원가입/로그인 버튼
sign_up_button1 = button(board_width, board_height, 0.415, 0.5, 12/80, 4/45, button_sign_up)
sign_in_button1 = button(board_width, board_height, 0.585, 0.5, 12/80, 4/45, button_sign_in)
log_quit = button(board_width, board_height, 0.5, 0.9, 0.16, 0.084, button_quit)
# log_quit = button(board_width, board_height, 0.5, 0.9, 0.16, 0.084, quit_button_image)

# login page 2) sign up / sign in
sign_up_button2 = button(board_width, board_height, 0.415, 0.7, 12/80, 4/45, button_sign_up)
sign_in_button2 = button(board_width, board_height, 0.415, 0.7, 12/80, 4/45, button_sign_in)
log_back = button(board_width, board_height, 0.585, 0.7, 12/80, 4/45, button_log_back)

# 아이템을 버튼 클래스 객체로 생성 - 비율은 테트리스 블럭 하나 사이즈 -> block_size = int(board_height * 0.045) 만큼으로
# bomb = button()
# exlosion = button()

tetris3 = pygame.image.load("assets/images/tetris3.png")
tetris4 = pygame.transform.smoothscale(tetris3, (200, 150))

# 게임 중 버튼을 생성하기 위한 버튼 객체 리스트(버튼 전체)
button_list = [mute_button, single_button, pvp_button, help_button, quit_button, setting_icon, leaderboard_icon, 
        resume_button, restart_button, restart_button_pvp1, restart_button_pvp2, setting_button, pause_quit_button, back_button, volume_icon, screen_icon, 
        ok_button, ok_button_pvp1, ok_button_pvp2, menu_button, menu_button_pvp1, menu_button_pvp2, gameover_quit_button, effect_plus_button, effect_minus_button, sound_plus_button, 
        sound_minus_button, mute_check_button, smallsize_check_button, midiumsize_check_button, bigsize_check_button,
        # 회원가입/로그인 관련
        sign_up_button1, sign_up_button2 ,sign_in_button1, sign_in_button2, log_back, log_quit]


def set_volume():
    ui_variables.fall_sound.set_volume(effect_volume / 10)   # effect_volume = 10 으로 초기화
    ui_variables.click_sound.set_volume(effect_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10)
    ui_variables.move_sound.set_volume(effect_volume / 10)
    ui_variables.drop_sound.set_volume(effect_volume / 10)
    ui_variables.single_sound.set_volume(effect_volume / 10)
    ui_variables.double_sound.set_volume(effect_volume / 10)
    ui_variables.triple_sound.set_volume(effect_volume / 10)
    ui_variables.tetris_sound.set_volume(effect_volume / 10)
    ui_variables.LevelUp_sound.set_volume(effect_volume / 10)
    ui_variables.GameOver_sound.set_volume(music_volume / 10)   # music_volume = 10 으로 초기화
    ui_variables.intro_sound.set_volume(music_volume / 10)   
    pygame.mixer.music.set_volume(music_volume / 10)   # pygame.mixer.music.set_volume(1~0.1 값): 배경 사운드 로드
                                                       # set_volume의 argument는 0.0 ~ 1.0으로 이루어져야 함 -> 소수로 만들기 위해 /10
                                                       # pygame.mixer.music.play(n) : n회 반복 -> 음수 값은 종료 시까지 반복
    for i in range(1, 10):
        ui_variables.combos_sound[i - 1].set_volume(effect_volume / 10)   # 10가지의 combo 사운드 한 번에 조절


def draw_image(window, img_path, x, y, width, height):
    x = x - (width / 2)   # 이미지 그리는 위치: 좌측 상단 기준 -> 2로 나누기
    y = y - (height / 2)
    image = pygame.image.load(img_path)
    image = pygame.transform.smoothscale(image, (width, height))
    window.blit(image, (x, y))


# Draw block
# pygame.draw.rect(Surface, color, Rect, Width=0)에서 Surface: pygame 실행 시 화면 변수, 사각형 색깔(R,G,B) 형태, 사각형의 [x축,y축,가로,세로], Width: 사각형의 선 크기(default=0)
def draw_block(x, y, color):
    pygame.draw.rect(   
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )

def draw_block_image(x, y, image):
    draw_image(screen, image, x, y, block_size, block_size)   # (screen, image path, x좌표, y좌표, 너비, 높이)

# grid[i][j] = 0 / matrix[tx+j][ty+i] = 0에서
# 0은 빈 칸
# 1~7: 테트리스 블록 종류
# 8: ghost
# 9: 장애물(벽돌)에 해당  -> t_block 참고
# 10: 아이템(폭탄)

# Draw game screen
def draw_board(next1, next2, hold, score, level, goal):
    sidebar_width = int(board_width * 0.5312)   # 크기 비율 고정 -> 해당 비율 변수화하기

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height)   # 크기 비율 고정
    )

    # Draw next mino   # 다음 블록의 모양
    grid_n1 = tetrimino.mino_map[next1 - 1][0]   # 배열 인덱스 -> -1처리 
    grid_n2 = tetrimino.mino_map[next2 - 1][0]

    for i in range(mino_matrix_y):   # 다음 블록    # 4 = mino_matrix_y
        for j in range(mino_matrix_x):   # 4 = mino_matrix_x 변수화
            dx1 = int(board_width * 0.025) + sidebar_width + block_size * j   # 위치 비율 고정 / 전체 가로 길이 * 비율
            dy1 = int(board_height * 0.3743) + block_size * i   # 위치 비율 고정 / 전체 세로 길이 * 비율
            if grid_n1[i][j] != 0:   # 해당 부분에 블록이 존재하면 -> 0 = mino_zero 로 바꾸기
                ##draw_block(dx,dy,ui_variables.t_color[grid_n[i][j]])
                draw_block_image(dx1, dy1, ui_variables.t_block[grid_n1[i][j]])     # t_block: 테트리스 블록 이미지 리스트
                                                                                    # 블록 이미지 출력

    for i in range(mino_matrix_y):   # 다음 다음 블록
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + block_size * j
            dy2 = int(board_height * 0.3743) + block_size * i
            if grid_n2[i][j] != 0:
                ##draw_block(dx,dy,ui_variables.t_color[grid_n[i][j]])
                draw_block_image(dx2, dy2, ui_variables.t_block[grid_n2[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0] 

    if hold_mino != -1:   # hold_mino = -1  # Holded mino   # hold가 존재하지 않으면, 
        for i in range(mino_matrix_y):   # mino_matrix_y
            for j in range(mino_matrix_x):   # mino_matrix_x
                dx = int(board_width * 0.045) + sidebar_width + block_size * j   # 위치 비율 고정 / 전체 가로 길이 * 비율
                dy = int(board_height * 0.1336) + block_size * i   # 위치 비율 고정 / 전체 세로 길이 * 비율
                if grid_h[i][j] != 0:   # 해당 부분에 블록이 존재하면, 
                    ##draw_block(dx,dy,ui_variables.t_color[grid_h[i][j]])
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]])   # hold 블록 모양 출력

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    # render("텍스트 내용", 안티에일리언싱 적용 여부(1), 색깔)
    if textsize == False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.real_white)
        text_item = ui_variables.h5.render("ITEM", 1, ui_variables.real_white)

    if textsize == True:
        text_hold = ui_variables.h3.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h3.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h3.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h2.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h3.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h2.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h3.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h2.render(str(combo_count), 1, ui_variables.real_white)
        text_item = ui_variables.h3.render("ITEM", 1, ui_variables.real_white)
    
    # Place texts
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.6791)))
    screen.blit(level_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_combo, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.8395)))
    screen.blit(combo_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.8823)))
    screen.blit(text_item, (int(board_width * 0.15) + sidebar_width, int(board_height * 0.6791)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * x   # 위치 비율 고정 / board 가로 길이 * 비율
            dy = int(board_height * 0.055) + block_size * y   # 위치 비율 고정 / board 세로 길이 * 비율
            ## draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])
    
    # 아이템/인벤토리 그리기
    if len(inventory_list) >= 0:   # 아이템이 있어도, 없어도 상자는 그대로 존재 
        pygame.draw.rect(screen, ui_variables.real_white, (dx_inventory[0] - item_size/2, dy_inventory - item_size/2, item_size, item_size), 1)
        pygame.draw.rect(screen, ui_variables.real_white, (dx_inventory[1] - item_size/2, dy_inventory - item_size/2, item_size, item_size), 1)
        pygame.draw.rect(screen, ui_variables.real_white, (dx_inventory[2] - item_size/2, dy_inventory - item_size/2, item_size, item_size), 1)

        show_item()

    # 타이머를 위한 시간 초기화

def draw_1Pboard(next, hold, score, level, goal):
    sidebar_width = int(board_width * 0.2867)   # 위치 비율 고정 / board 가로 길이 * 비율 ( -> 0.31 )

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height)   # 크기 비율 고정 / board 가로 길이 * 비율
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]   # 다음 블록 모양

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.045) + sidebar_width + block_size * j    # 위치 비율 고정 / board 가로 길이 * 비율
            dy = int(board_height * 0.3743) + block_size * i    # 위치 비율 고정 / board 세로 길이 * 비율
            if grid_n[i][j] != 0:
                ## draw_block(dx,dy,ui_variables.t_color[grid_n[i][j]])
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:   # hold_mino의 default 값 = -1 -> 즉, hold 블록이 존재하지 때
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j    # 위치 비율 고정 / board 가로 길이 * 비율
                dy = int(board_height * 0.1336) + block_size * i    # 위치 비율 고정 / board 세로 길이 * 비율
                if grid_h[i][j] != 0:
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]])

    # Set max score
    if score > 999999:
        score = 999999   # 최대 점수 999,999로 설정

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
    text_score = ui_variables.h5.render("ATTACK", 1, ui_variables.real_white)
    score_value = ui_variables.h4.render(str(attack_point), 1, ui_variables.real_white)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
    text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
    combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.real_white)


    # Place texts
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))    # board 가로/세로 길이 * 비율
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) + sidebar_width, int(board_height*0.6791)))
    screen.blit(level_value, (int(board_width * 0.055) + sidebar_width , int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width * 0.045) + sidebar_width , int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width * 0.055) + sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_height * 0.055) + block_size * x    # 위치 비율 고정 / board 가로 길이 * 비율
            dy = int(board_height * 0.055) + block_size * y    # 위치 비율 고정 / board 세로 길이 * 비율
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])

# 여기까지

def draw_2Pboard(next, hold, score, level, goal):
    sidebar_width = int(board_width * 0.7867)    # 위치 비율 고정 / board 가로 길이 * 비율

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height)   # 크기 비율 고정 / board 가로 길이 * 비율
                                                                          # Rect(x축, y축, 가로길이, 세로길이)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(mino_matrix_y):  # 16개의 그리드 칸에서 true인 값만 뽑아서 draw.rect
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.045) + sidebar_width + block_size * j    # 위치 비율 고정 / board 가로 길이 * 비율
            dy = int(board_height * 0.3743) + block_size * i    # 위치 비율 고정 / board 세로 길이 * 비율
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j    # 위치 비율 고정 / board 가로 길이 * 비율
                dy = int(board_height * 0.1336) + block_size * i    # 위치 비율 고정 / board 세로 길이 * 비율
                if grid_h[i][j] != 0:
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]])

    # Set max score
    if score > 999999:
        score = 999999   # 최대 점수 설정

    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
    text_score = ui_variables.h5.render("ATTACK", 1, ui_variables.real_white)
    score_value = ui_variables.h4.render(str(attack_point_2P), 1, ui_variables.real_white)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
    text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
    combo_value = ui_variables.h4.render(str(combo_count_2P), 1, ui_variables.real_white)

    # Place texts
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) + sidebar_width, int(board_height*0.6791)))
    screen.blit(level_value, (int(board_width * 0.055) + sidebar_width , int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width * 0.045) + sidebar_width , int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width * 0.055) + sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.5) + block_size * x    # 위치 비율 고정 
            dy = int(board_height * 0.055) + block_size * y    # 위치 비율 고정 
            draw_block_image(dx, dy, ui_variables.t_block[matrix_2P[x][y + 1]])


# Draw a tetrimino
def draw_mino(x, y, mino, r):   # mino: 블록 모양 - r: 회전된 모양 중 하나
    grid = tetrimino.mino_map[mino - 1][r]   # grid: 출력할 테트리스

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r):   # 테트리스가 바닥에 존재하는 경우: true -> not: 바닥에 존재하지 않는 상태
        ty += 1   # 한 칸 밑으로 하강

    # Draw ghost
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:   # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면 
                matrix[tx + j][ty + i] = 8   # 테트리스가 쌓일 위치에 8이라는 ghost 만들기

    # Draw mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:    # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면 
                matrix[x + j][y + i] = grid[i][j]   # 해당 위치에 블록 만들기


def draw_mino_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom_2P(tx, ty, mino, r):
        ty += 1

    # Draw ghost
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:
                matrix_2P[tx + j][ty + i] = 8

    # Draw mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:   # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면, 
                matrix_2P[x + j][y + i] = grid[i][j]   # 해당 위치에 블록 만들기


# Erase a tetrimino
def erase_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(21):
        for i in range(10):
            if matrix[i][j] == 8:   # 테트리스 블록에서 해당 행렬 위치에 ghost 블록이 존재하면,
                matrix[i][j] = 0   # 없애서 빈 곳으로 만들기
 
    # Erase mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:   # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면, 
                matrix[x + j][y + i] = 0   # 해당 위치에 블록을 없애 빈 곳으로 만들기
                


def erase_mino_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(21):
        for i in range(10):
            if matrix_2P[i][j] == 8:    # 테트리스 블록에서 해당 행렬 위치에 ghost 블록이 존재하면,
                matrix_2P[i][j] = 0   # 없애서 빈 곳으로 만들기

    # Erase mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:   # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면,
                matrix_2P[x + j][y + i] = 0   # 해당 위치에 블록을 없애 빈 곳으로 만들기


# Returns true if mino is at bottom
def is_bottom(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]   # grid: 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    return True

    return False


def is_bottom_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:
                    return True
                elif matrix_2P[x + j][y + i + 1] != 0 and matrix_2P[x + j][y + i + 1] != 8:
                    return True

    return False


# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]   # grid: 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:   # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면, 
                if (x + j - 1) < 0:   # 가장 왼쪽에 위치
                    return True
                elif matrix[x + j - 1][y + i] != 0:   # 그 위치의 왼쪽에 이미 무엇인가가 존재하면, 
                    return True

    return False


def is_leftedge_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]   # grid: 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:   # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면, 
                if (x + j - 1) < 0: 
                    return True
                elif matrix_2P[x + j - 1][y + i] != 0:
                    return True

    return False


# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:   # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면, 
                if (x + j + 1) > 9:   # 가장 오른쪽에 위치 
                    return True
                elif matrix[x + j + 1][y + i] != 0:   # 그 위치의 오른쪽에 이미 무엇인가가 존재함.
                    return True

    return False


def is_rightedge_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:
                if (x + j + 1) > 9:
                    return True
                elif matrix_2P[x + j + 1][y + i] != 0:
                    return True

    return False


# Returns true if turning right is possible
def is_turnable_r(x, y, mino, r):
    # 회전 모양은 0, 1, 2, 3 -> 총 4가지
    if r != 3:   
        grid = tetrimino.mino_map[mino - 1][r + 1]   # 3이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][0]   # 3이면 0번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:   # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면, 
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:   # 테트리스 matrix 크기를 벗어나면 회전 X  /  20 = board_y
                    return False
                elif matrix[x + j][y + i] != 0:   # 해당 자리에 이미 블록이 있으면 회전 X
                    return False

    return True


def is_turnable_r_2P(x, y, mino, r):
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:   
                    return False
                elif matrix_2P[x + j][y + i] != 0:
                    return False

    return True


# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r):
    # 회전 모양은 0, 1, 2, 3 -> 총 4가지
    if r != 0:   
        grid = tetrimino.mino_map[mino - 1][r - 1]   # 0이 아니면 -> 그 다음 모양
    else:   
        grid = tetrimino.mino_map[mino - 1][3]   # 0이면 -> 3번째 모양으로 

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:   # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면, 
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:   # 테트리스 matrix 크기를 벗어나면 회전 X  /  20 = board_y
                    return False
                elif matrix[x + j][y + i] != 0:   # 해당 자리에 이미 블록이 있으면 돌리지 못 함.
                    return False

    return True


def is_turnable_l(x, y, mino, r):   # is_turnable_l_2P ?
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]   # grid: 출력할 테트리스
    else:
        grid = tetrimino.mino_map[mino - 1][3]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True


# Returns true if new block is drawable
def is_stackable(mino):
    grid = tetrimino.mino_map[mino - 1][0]   # grid: 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            # print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True


def is_stackable_2P(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            # print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix_2P[3 + j][i] != 0:
                return False

    return True

def draw_multiboard(next_1P, hold_1P, next_2P, hold_2P, score, score_2P, level, level_2P, goal, goal_2P):
    screen.fill(ui_variables.real_white)
    draw_1Pboard(next_1P, hold_1P, score, level, goal)   
    draw_2Pboard(next_2P, hold_2P, score_2P, level_2P, goal_2P)


def set_vol(val):
    volume = int(val) / 100   # set_volume의 인자로 소수점 만들기 위해 -> 100으로 나누어줌.
    print(volume)
    ui_variables.click_sound.set_volume(volume)

# # Erase a tetrimino
# def erase_mino(x, y, mino, r):
#     grid = tetrimino.mino_map[mino - 1][r]

#     # Erase ghost
#     for j in range(21):
#         for i in range(10):
#             if matrix[i][j] == 8:   # 테트리스 블록에서 해당 행렬 위치에 ghost 블록이 존재하면,
#                 matrix[i][j] = 0   # 없애서 빈 곳으로 만들기
 
#     # Erase mino
#     for i in range(mino_matrix_y):
#         for j in range(mino_matrix_x):
#             if grid[i][j] != 0:   # 테트리스 블록에서 해당 행렬 위치에 블록이 존재하면, 
#                 matrix[x + j][y + i] = 0   # 해당 위치에 블록을 없애 빈 곳으로 만들기

# 아이템 획득 - 콤보 11 달성 시 item_list 중 랜덤으로 
def get_item():    # inventory_list에 아이템 생성
    if len(inventory_list) < 3:
        # inventory_list.append(item_list[random.randrange(0,2)])
        # inventory_list.append(item_list[rand.randrange(0,2)])
        inventory_list.append(item_list[0])

def show_item():
    for i in range(len(inventory_list)):
        item = inventory_list[i]
        screen.blit(item, item.get_rect(center = (dx_inventory[i], dy_inventory)))

def use_item():
    if len(inventory_list) > 0:
        item = inventory_list[0]
        inventory_list.pop(0)

        if item == item_bomb:
            use_bomb(dx, dy, mino, rotation)
        # elif item == item_explosion:
        #     use_erase_attack(dx, dy, mino, rotation)

    return item

# 아이템 사용 함수 - 아이템 사용 시 잠깐 멈추거나 딜레이 하는 순간 필요(이미지, 사운드 출력)
def use_bomb(x, y, mino, r):   # 행 삭제 폭탄
    grid = tetrimino.mino_map[mino - 1][r]

    k = height   # 마지막 행 제거

    while k > 0:
        for i in range(width):
            matrix[i][k] = matrix[i][k-1]   # 지워진 블록 윗 줄을 한 줄 아래로 내리기
        k -= 1

    # for i in range(3):
    #     k = height 
    #     while k > 0:
    #         for i in range(width):
    #             matrix[i][k] = matrix[i][k-1]
    #         k -= 1

# def use_bomb(x, y, mino, r):   # 3*3, 5*5 삭제 폭탄
#     grid = tetrimino.mino_map[mino - 1][r]

#     for j in range(21):
#         for i in range(10):
#             if matrix[j][i] == 10:
#                 x = i - 1
#                 y = j - 1
                
#                 for m in range(bomb_size):
#                     for n in range(bomb_size):
#                         if x + m >= 0 and y + n >= 0   # 블록이 있든 없든
#                             matrix[x+m][y+n] = 0   # 3 * 3 크기만큼 지워줌

# 장애물 제거
def use_erase_attack(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for j in range(21):
        for i in range(10):
            matrix[i][j] = matrix[i][j-1]

    # for j in range(21):
    #     is_full = True
    #     for i in range(10):
    #         if matrix[i][j] == 0:
    #             is_full = False

    #  while k > 0:
    #     for i in range(10):
    #         matrix[i][k] = matrix[i][k - 1]

    #         k -= 1

# Initial values   # 변수 초기화 부분 -> 정리하기 
blink = False
start = False
pause = False
done = False
game_over = False
game_over_pvp = False
leader_board = False
setting = False
pvp = False
help = False
textsize = False
signup = False
signin = False
main = False

combo_count = 0
combo_count_2P = 0   # pvp 모드에서 2P의 콤보 처리를 위해 추가 
score = 0
# score2 = 0   # -> score_2P로 통일
score_2P = 0
level = 1
level_2P = 1
goal = level * 5
goal_2P = level_2P * 5
bottom_count = 0
hard_drop = False
item = False

volume_setting = False
screen_setting = False
keyboard_setting = False

music_volume = 10
effect_volume = 10
attack_point = 0
attack_point_2P = 0

dx, dy = 3, 0  # Minos location status

rotation = 0  # Minos rotation status

mino = randint(1, 7)  # Current mino   # 테트리스 블록 7가지 중 하나

next_mino1 = randint(1, 7)  # Next mino1   # 다음 테트리스 블록 7가지 중 하나
next_mino2 = randint(1, 7)  # Next mino2   # 다음 테트리스 블록 7가지 중 하나

hold = False  # Hold status

hold_mino = -1  # Holded mino   # 현재 hold 하는 것이 없는 상태

hold_mino_2P = -1
bottom_count_2P = 0
hard_drop_2P = False
hold_2P = False
next_mino1_2P = randint(1, 7)
mino_2P = randint(1, 7)
rotation_2P = 0
dx_2P, dy_2P = 3, 0

name_location = 0
name = [65, 65, 65, 65, 65, 65]

# 아이템 변수 - bomb, 행 제거
item_list = []
inventory_list = []   # 인벤토리 리스트
# bomb_size = 20   # 블록 한 칸의 사이즈
bomb_size = 3
item_size = 30

# inventory 출력을 위한 위치 변수
sidebar_width = int(board_width * 0.5312)
# dx = int(board_width * 0.045) + sidebar_width + block_size * j 
dx_inventory1 = int(board_width * 0.135) + sidebar_width
dx_inventory2 = int(board_width * 0.175) + sidebar_width
dx_inventory3 = int(board_width * 0.215) + sidebar_width
dx_inventory = [dx_inventory1, dx_inventory2, dx_inventory3]
 # score value 위치: (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)
 # Level value 위치: int(board_widt * 0.7219)
 # text item 위치: int(board_height * 0.6791)
dy_inventory = int(board_height * 0.75)

# 아이템 이미지 scale
item_bomb = pygame.transform.scale(pygame.image.load('item/bomb_powerup.png'), (item_size,item_size))
# item_explosion = pygame.transform.scale(pygame.image.load('item/explosion.png'), (item_size,item_size))
bomb_num = 10
# explosion_num = 11

item_list.append(item_bomb)
# item_list.append(item_explosion)

# 추가
add_leaders = ['1st', '2nd', '3rd']
r_n = ['n1', 'n2', 'n3']
r_s = ['0', '0', '0']

# 시간 부분
previous_time = pygame.time.get_ticks()
current_time = pygame.time.get_ticks()
pause_time = pygame.time.get_ticks()

# 리더보드 .txt 파일 작성/정렬(내림차순 정렬 -> reverse=True)
with open('leaderboard.txt') as f:
    lines = f.readlines()
lines = [line.rstrip('\n') for line in open('leaderboard.txt')]   # leaderboard.txt 한 줄씩 읽어옴

leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
for i in lines:
    leaders[i.split(' ')[0]] = int(i.split(' ')[1])
leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix

matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix

###########################################################
# Loop Start
###########################################################

volume = 1.0   # 필요없는 코드 -> effect_volume으로 대체 가능

ui_variables.click_sound.set_volume(volume)   # 필요없는 코드 -> 전체 코드에서, click_sound를 effect_volume으로 설정하는 코드만 있으면 됨

pygame.mixer.init()
ui_variables.intro_sound.set_volume(0.1)   # 소리 설정 부분도 
ui_variables.intro_sound.play()
game_status = ''
ui_variables.break_sound.set_volume(0.2)

while not done:

    # Pause screen
    # ui_variables.click_sound.set_volume(volume)
    
    # 볼륨 설정 창 
    if volume_setting:   
        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3),
                   board_height)
        draw_image(screen, number_board, board_width * 0.5, board_height * 0.43, int(board_width * 0.09),
                   int(board_height * 0.1444))
        draw_image(screen, number_board, board_width * 0.5, board_height * 0.63, int(board_width * 0.09),
                   int(board_height * 0.1444))
        mute_button.draw(screen, (0, 0, 0))
        effect_plus_button.draw(screen, (0, 0, 0))
        effect_minus_button.draw(screen, (0, 0, 0))
        sound_plus_button.draw(screen, (0, 0, 0))
        sound_minus_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

        music_volume_text = ui_variables.h5.render('Music Volume', 1, ui_variables.grey_1)
        effect_volume_tex = ui_variables.h5.render('Effect Volume', 1, ui_variables.grey_1)
        screen.blit(music_volume_text, (board_width * 0.44, board_height * 0.3))
        screen.blit(effect_volume_tex, (board_width * 0.44, board_height * 0.5))

        music_volume_size_text = ui_variables.h4.render(str(music_volume), 1, ui_variables.grey_1)
        effect_volume_size_text = ui_variables.h4.render(str(effect_volume), 1, ui_variables.grey_1)
        screen.blit(music_volume_size_text, (board_width * 0.485, board_height * 0.4))
        screen.blit(effect_volume_size_text, (board_width * 0.485, board_height * 0.6))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)   # 0.3초로 설정

                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

                if effect_plus_button.isOver(pos):
                    effect_plus_button.image = clicked_plus_button_image
                else:
                    effect_plus_button.image = plus_button_image

                if effect_minus_button.isOver(pos):
                    effect_minus_button.image = clicked_minus_button_image
                else:
                    effect_minus_button.image = minus_button_image

                if sound_plus_button.isOver(pos):
                    sound_plus_button.image = clicked_plus_button_image
                else:
                    sound_plus_button.image = plus_button_image

                if sound_minus_button.isOver(pos):
                    sound_minus_button.image = clicked_minus_button_image
                else:
                    sound_minus_button.image = minus_button_image

                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    volume_setting = False
                if effect_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume >= 10:   # 음량 최대 크기
                        music_volume = 10
                    else:
                        music_volume += 1
                if effect_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume <= 0:   # 음량 최소 크기
                        music_volume = 0
                    else:
                        music_volume -= 1
                if sound_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume >= 10:   # 음량 최대 크기
                        effect_volume = 10
                    else:
                        effect_volume += 1
                if sound_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume <= 0:   # 음량 최소 크기
                        effect_volume = 0
                    else:
                        effect_volume -= 1
                if mute_button.isOver(pos):
                    ui_variables.click_sound.play()
                    effect_volume = 0 
                    music_volume = 0

                set_volume()

            # elif event.type == VIDEORESIZE: 부분 추가

    # 화면(크기) 설정 창  ->  각 화면 크기 설정 시 화면(board) 크기 설정 후 -> board 사이즈에 비례하게 크기 각각 조절 -> 조절하는 비율 변수화하기 ?
    elif screen_setting:
        screen.fill(ui_variables.white)
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height)
        single_button.draw(screen, (0, 0, 0))
        pvp_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        setting_icon.draw(screen, (0, 0, 0))
        leaderboard_icon.draw(screen, (0, 0, 0))

        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3),
                   board_height)
        smallsize_check_button.draw(screen, (0, 0, 0))
        bigsize_check_button.draw(screen, (0, 0, 0))
        midiumsize_check_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

                # if smallsize_check_button.isOver(pos):
                #    smallsize_check_button.image = clicked_plus_button_image
                # else :
                #    smallsize_check_button.image = plus_button_image

                # if bigsize_check_button.isOver(pos):
                #    bigsize_check_button.image = clicked_minus_button_image
                # else :
                #    bigsize_check_button.image = minus_button_image

                # if midiumsize_check_button.isOver(pos):
                #    midiumsize_check_button.image = clicked_plus_button_image
                # else :
                #    midiumsize_check_button.image = plus_button_image

                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    screen_setting = False

                # 가장 작은 사이즈 화면 크기 버튼 눌렀을 때
                if smallsize_check_button.isOver(pos):
                    ui_variables.click_sound.play()

                    board_width = 800
                    board_height = 450
                    block_size = int(board_height * 0.045)
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize = False

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

                    pygame.display.update()

                # 중간 사이즈 화면 크기 버튼 눌렀을 때
                if midiumsize_check_button.isOver(pos):
                    ui_variables.click_sound.play()

                    board_width = 1200
                    board_height = 675
                    block_size = int(board_height * 0.045)
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize = True
                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)       

                    pygame.display.update()

                # 가장 큰 사이즈 화면 크기 버튼 눌렀을 때
                if bigsize_check_button.isOver(pos):
                    ui_variables.click_sound.play()
                    block_size = int(board_height * 0.045)

                    board_width = 1600
                    board_height = 900
                    block_size = int(board_height * 0.045)
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize = True

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height) 

                    pygame.display.update()

    # 설정 화면 기능 
    elif setting:
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height)
        single_button.draw(screen, (0, 0, 0))
        pvp_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        setting_icon.draw(screen, (0, 0, 0))
        leaderboard_icon.draw(screen, (0, 0, 0))

        if start:
            screen.fill(ui_variables.real_white)

            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
        if pvp:
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3),
                   board_height)

        # keyboard_icon.draw(screen,(0,0,0))
        screen_icon.draw(screen, (0, 0, 0))
        volume_icon.draw(screen, (0, 0, 0))

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)

                pause_text = ui_variables.h2_b.render("PAUSED", 1, ui_variables.real_white)
                pause_start = ui_variables.h5.render("Press esc to continue", 1, ui_variables.real_white)

                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

                if volume_icon.isOver(pos):
                    volume_icon.image = clicked_volume_vector
                else:
                    volume_icon.image = volume_vector

                # if keyboard_icon.isOver(pos):
                # keyboard_icon.image = clicked_keyboard_vector
                # else :
                # keyboard_icon.image = keyboard_vector

                if screen_icon.isOver(pos):
                    screen_icon.image = clicked_screen_vector
                else:
                    screen_icon.image = screen_vector

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = False

                if volume_icon.isOver(pos):
                    ui_variables.click_sound.play()

                    volume_setting = True

                # if keyboard_icon.isOver(pos):
                # ui_variables.click_sound.play()

                if screen_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    screen_setting = True
            elif event.type == VIDEORESIZE:

                board_width = event.w
                board_height = event.h

                # 최소 화면 너비/높이 조건 설정
                if board_width < min_width or board_height < min_height:   # 최소 너비/높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                
                if not ( (board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05) ):   # 높이/너비가 일정 비율을 넘어서게 되면
                    board_width = int(board_height / board_rate)   # 너비를 적정 비율로 바꾸어줌
                    board_height = int(board_width * board_rate)   # 높이를 적정 비율로 바꾸어줌

                if board_width >= mid_width:   # 화면 사이즈가 큰  경우
                    textsize = True   # 큰  글자 
                    
                if board_width <= mid_width:
                    textsize = False

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height) 

    # 정지 화면 기능
    elif pause:
        pygame.mixer.music.pause()
        # screen.fill(ui_variables.real_white)
        # draw_board(next_mino, hold_mino, score, level, goal)
        if start:
            screen.fill(ui_variables.real_white)

            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
        if pvp:
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
        draw_image(screen, pause_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 0.7428),
                   board_height)
        resume_button.draw(screen, (0, 0, 0))
        restart_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        pause_quit_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)

                pause_text = ui_variables.h2_b.render("PAUSED", 1, ui_variables.real_white)
                pause_start = ui_variables.h5.render("Press esc to continue", 1, ui_variables.real_white)

                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.mixer.music.unpause()
                    pygame.time.set_timer(pygame.USEREVENT, 1)
            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver(pos):
                    resume_button.image = clicked_resume_button_image
                else:
                    resume_button.image = resume_button_image

                if restart_button.isOver(pos):
                    restart_button.image = clicked_restart_button_image
                else:
                    restart_button.image = restart_button_image

                if setting_button.isOver(pos):
                    setting_button.image = clicked_setting_button_image
                else:
                    setting_button.image = setting_button_image
                if pause_quit_button.isOver(pos):
                    pause_quit_button.image = clicked_quit_button_image
                else:
                    pause_quit_button.image = quit_button_image
                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_quit_button.isOver(pos):
                    ui_variables.click_sound.play()
                    done = True
                if setting_button.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if restart_button.isOver(pos):   # 다시 시작 버튼을 눌렀을 때 게임 변수 초기화
                    ui_variables.click_sound.play()
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino1 = randint(1, 7)
                    next_mino2 = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score_2P = 0
                    level = 1
                    level_2P = 1
                    combo_count = 0
                    combo_count_2P = 0   # pvp 모드에서 2P의 콤보 처리를 위해 추가
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65, 65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    pause = False
                    start = False

                    hold_mino_2P = -1  #
                    bottom_count_2P = 0  #
                    hard_drop_2P = False  #
                    hold_2P = False  #
                    next_mino1_2P = randint(1, 7)  #
                    mino_2P = randint(1, 7)  #
                    rotation_2P = 0  #
                    dx_2P, dy_2P = 3, 0  #
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix

                    if pvp:
                        pvp = False

                if resume_button.isOver(pos):
                    pygame.mixer.music.unpause()
                    pause = False
                    ui_variables.click_sound.play()  
                    pygame.time.set_timer(pygame.USEREVENT, 1)   # 0.001초

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h

                # 최소 화면 너비/높이 조건 설정
                if board_width < min_width or board_height < min_height:   # 최소 너비/높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                
                if not ( (board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05) ):   # 높이/너비가 일정 비율을 넘어서게 되면
                    board_width = int(board_height / board_rate)   # 너비를 적정 비율로 바꾸어줌
                    board_height = int(board_width * board_rate)   # 높이를 적정 비율로 바꾸어줌
                
                if board_width >= mid_width:   # 화면 사이즈가 큰  경우
                    textsize = True   # 큰  글자 
                    
                if board_width <= mid_width:
                    textsize = False

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height) 

    # HELP 화면 기능                                          
    elif help:
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height)
        single_button.draw(screen, (0, 0, 0))
        pvp_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        setting_icon.draw(screen, (0, 0, 0))
        leaderboard_icon.draw(screen, (0, 0, 0))

        draw_image(screen, 'assets/vector/help_board.png', board_width * 0.5, board_height * 0.5,
                   int(board_height * 1.3), board_height)
        draw_image(screen, 'assets/vector/help_contents.png', board_width * 0.5, board_height * 0.5,
                   int(board_height * 1.1), int(board_height * 0.55))

        # draw_image(screen ,'assets/images/help_image.png', board_width*0.15, 0, int(board_width*0.7), board_height)

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True

            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    help = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h

                # 최소 화면 너비/높이 조건 설정
                if board_width < min_width or board_height < min_height:   # 최소 너비/높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                
                if not ( (board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05) ):   # 높이/너비가 일정 비율을 넘어서게 되면
                    board_width = int(board_height / board_rate)   # 너비를 적정 비율로 바꾸어줌
                    board_height = int(board_width * board_rate)   # 높이를 적정 비율로 바꾸어줌
                
                if board_width >= mid_width:   # 화면 사이즈가 큰  경우
                    textsize = True   # 큰  글자 
                    
                if board_width <= mid_width:
                    textsize = False

                block_size = int(board_height * 0.045)

                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height) 

    # 리더보드 화면 기능
    elif leader_board:
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height)
        single_button.draw(screen, (0, 0, 0))
        pvp_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        setting_icon.draw(screen, (0, 0, 0))
        leaderboard_icon.draw(screen, (0, 0, 0))
        draw_image(screen, leader_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3),
                   board_height)

        back_button.draw(screen, (0, 0, 0))

        leader_1 = ui_variables.h1_b.render('1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1, ui_variables.grey_1)
        leader_2 = ui_variables.h1_b.render('2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1, ui_variables.grey_1)
        leader_3 = ui_variables.h1_b.render('3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1, ui_variables.grey_1)
        screen.blit(leader_1, (board_width * 0.3, board_height * 0.15))
        screen.blit(leader_2, (board_width * 0.3, board_height * 0.35))
        screen.blit(leader_3, (board_width * 0.3, board_height * 0.55))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True

            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)

                pause_text = ui_variables.h2_b.render("PAUSED", 1, ui_variables.real_white)
                pause_start = ui_variables.h5.render("Press esc to continue", 1, ui_variables.real_white)

                pygame.display.update()

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    leader_board = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h

                # 최소 화면 너비/높이 조건 설정
                if board_width < min_width or board_height < min_height:   # 최소 너비/높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                
                if not ( (board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05) ):   # 높이/너비가 일정 비율을 넘어서게 되면
                    board_width = int(board_height / board_rate)   # 너비를 적정 비율로 바꾸어줌
                    board_height = int(board_width * board_rate)   # 높이를 적정 비율로 바꾸어줌    

                if board_width >= mid_width:   # 화면 사이즈가 큰  경우
                    textsize = True   # 큰  글자 
                    
                if board_width <= mid_width:
                    textsize = False

                block_size = int(board_height * 0.045)

                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height) 

   
    # 싱글모드 시작 화면 기능
    elif start:
        # 시간 계산
        if start == False:
            start_ticks = pygame.time.get_ticks()   # 현재 시간을 게임 시작 시간으로
            start = True
            play_time = (pygame.time.get_ticks() + start_ticks)   # 경과시간 계산   ->  formating 하기

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:   # USEREVENT: 사용자가 임의로 설정하는 이벤트
            
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]: #얘가 더 빨라야함
                        if level <1:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 15 - 50) #400
                        elif level < 3:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10 + 50) #350
                        elif level < 6:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10) #300
                        elif level < 10:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 8 + 10) #250
                        else:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 6 + 20) #200 숫자가 클수록 느림
                        
                    else:
                        if level <1:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 15) #450
                        elif level < 3:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 15 - 50) #400
                        elif level < 6:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10 + 50) #350
                        elif level < 10:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10) #300
                        else:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 8 + 10) #250

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)
                screen.fill(ui_variables.real_white)
                draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                
                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1 

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)
                        screen.fill(ui_variables.real_white)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                        if is_stackable(next_mino1):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_status = 'start'
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                combo_value = 0
                attack_stack = 0

                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        attack_stack += 1
                        k = j
                        combo_value += 1
                        combo_count += 1   # N 줄 한 번에 깰 때 N 콤보 작동 -> is_full 확인 시 True일 때마다 combo_count 증가
                        pygame.time.delay(300)
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 10) 

                        if combo_count >= 11:
                            screen.blit(tetris4, (board_width * 0.27, board_height * 0.3))  # blits the combo number
                            pygame.display.update()
                            ui_variables.combos_sound[8].play()
                            pygame.time.delay(300)

                            get_item()
                            show_item()
                            # if item == item_bomb:
                            #     use_bomb(dx, dy, mino, rotation)
                            # elif item == item_explosion:
                            #     use_erase_attack(dx, dy, mino, rotation)

                            combo_value = 0   # combo_value = 0 -> combo_count = 0으로 하면 11이 되는 순간 value 값에 11을 출력하지 않고 바로 0으로 
                            combo_count = 0   # 11이 되는 순간 이미지/사운드 먼저 띄우고 초기화
                        
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1

                # while attack_stack >= 2:
                #     for j in range(20):
                #         for i in range(10):
                #             matrix_2P[i][j] = matrix_2P[i][j + 1]

                #             attack_stack -= 1
                #     for i in range(10):
                #         matrix_2P[i][20] = 9
                #     k = randint(1, 10)
                #     matrix_2P[k][20] = 0
                #     attack_point += 1
                
                while attack_stack >= 2:
                    for j in range(20):
                        for i in range(10):
                            matrix[i][j] = matrix[i][j + 1]

                            attack_stack -= 1
                    for i in range(10):
                        matrix[i][20] = 9
                    k = randint(1, 10)
                    matrix[k][20] = 0
                    attack_point += 1

                if erase_count >= 1:
                    previous_time = current_time
                    # combo_count += 1   -> if is_full: 조건문으로 이동
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        # score += 50 * level * erase_count + combo_count
                        score += (10 * (combo_count * combo_count))   # 동시에 2줄 완성 시 10 + 40 점 추가

                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        # score += 150 * level * erase_count + 2 * combo_count
                        score += (10 * (combo_count * combo_count))

                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        # score += 350 * level * erase_count + 3 * combo_count
                        score += (10 * (combo_count * combo_count))

                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        # score += 1000 * level * erase_count + 4 * combo_count
                        score += (10 * (combo_count * combo_count))
                        screen.blit(ui_variables.combo_4ring, (250, 160))

                    else:
                        score += (10 * (combo_count * combo_count ))

                    for i in range(1, 11):
                        if combo_count == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1],
                                        (board_width * 0.27, board_height * 0.3))  # blits the combo number
                            pygame.display.update()
                            pygame.time.delay(500)
                        elif combo_count > 10:  # 11 이상 콤보 이미지
                            screen.blit(tetris4, (board_width * 0.27, board_height * 0.3))  # blits the combo number
                            pygame.display.update()

                            pygame.time.delay(300)

                    # for i in range(1, 11):
                    #     if combo_count == i:  # 1 ~ 10 콤보 이미지
                    #         screen.blit(ui_variables.large_combos[i - 1], (124, 190))  # blits the combo number
                    #     elif combo_count > 10:  # 11 이상 콤보 이미지  ->  콤보값 초기화
                    #         screen.blit(tetris4, (100, 190))  # blits the combo number
                    #         # combo_count  = 0   # 콤보 11 달성 시 초기화 및 아이템 부여

                    for i in range(1, 9):
                        if combo_count == i + 2:  # 3 ~ 11 콤보 사운드 
                            ui_variables.combos_sound[i - 1].play()
                            pygame.time.delay(800)   # 콤보 작동 사운드 출력 후 delay
                        if combo_count > 11:
                            ui_variables.combos_sound[8].play()

                # if current_time - previous_time > 11000:   # 11초가 지나면
                #     previous_time = current_time   # 현재 시간을 과거 시간으로 하고
                #     combo_count = 0

                # 지운 블록이 없으면 콤보 -1
                #               if is_bottom(dx, dy, mino, rotation) :
                #                   if erase_count == 0 :
                #                       combo_count -= 1
                #                       if combo_count < 0:
                #                           combo_count = 0

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    ui_variables.LevelUp_sound.play()
                    ui_variables.LevelUp_sound.play()
                    goal += level * 5
                    framerate = int(framerate * 0.8)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:   # ESC 버튼을 눌렀을 때 잠시 멈춤
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:   # SPCE 버튼 눌렀을 때 -> Hard Drop
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate*10)
                    draw_mino(dx, dy, mino, rotation)
                    screen.fill(ui_variables.real_white)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                    pygame.display.update()

                # Hold
                elif event.key == K_LSHIFT or event.key == K_q:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    screen.fill(ui_variables.real_white)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                    
                # Turn right
                elif event.key == K_UP or event.key == K_w:
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    screen.fill(ui_variables.real_white)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    screen.fill(ui_variables.real_white)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    screen.fill(ui_variables.real_white)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    screen.fill(ui_variables.real_white)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                # Use bomb
                elif event.key == K_x:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()

                    use_item()

                    if item == item_bomb:
                        use_bomb(dx, dy, mino, rotation)
                        draw_mino(dx, dy, mino, rotation)
                        screen.fill(ui_variables.real_white)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal) 
                    
                    show_item()
                
                # # Use erase attack
                # elif event.key == K_c:
                #     ui_variables.fall_sound.play()
                #     ui_variables.drop_sound.play()

                #     use_item()
                #     if item == item_explosion:
                #         use_erase_attack(dx, dy, mino, rotation)
                #         draw_mino(dx, dy, mino, rotation)
                #         screen.fill(ui_variables.real_white)
                #         draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h

                # 최소 화면 너비/높이 조건 설정
                if board_width < min_width or board_height < min_height:   # 최소 너비/높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                
                if not ( (board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05) ):   # 높이/너비가 일정 비율을 넘어서게 되면
                    board_width = int(board_height / board_rate)   # 너비를 적정 비율로 바꾸어줌
                    board_height = int(board_width * board_rate)   # 높이를 적정 비율로 바꾸어줌    

                if board_width >= mid_width:   # 화면 사이즈가 큰  경우
                    textsize = True   # 큰  글자 
                    
                if board_width <= mid_width:
                    textsize = False

                block_size = int(board_height * 0.045)

                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height) 

        pygame.display.update()

    # PVP 모드 화면 기능     
    elif pvp:
        for event in pygame.event.get():
            # event.key = pygame.key.get_pressed()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over_pvp:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]: 
                        if level <1:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 15 - 50) #400
                        elif level < 3:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10 + 50) #350
                        elif level < 6:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10) #300
                        elif level < 10:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 8 + 10) #250
                        else:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 6 + 20) #200 숫자가 클수록 느림
                        
                    else:
                        if level <1:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 15) #450
                        elif level < 3:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 15 - 50) #400
                        elif level < 6:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10 + 50) #350
                        elif level < 10:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10) #300
                        else:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 8 + 10) #250
                    
                    if keys_pressed[K_s]: 
                        if level_2P <1:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 15 - 50) #400
                        elif level_2P < 3:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10 + 50) #350
                        elif level_2P < 6:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10) #300
                        elif level_2P < 10:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 8 + 10) #250
                        else:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 6 + 20) #200 숫자가 클수록 느림
                        
                    else:
                        if level_2P <1:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 15) #450
                        elif level_2P < 3:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 15 - 50) #400
                        elif level_2P < 6:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10 + 50) #350
                        elif level_2P < 10:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 10) #300
                        else:
                            pygame.time.set_timer(pygame.USEREVENT, framerate * 8 + 10) #250

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)

                draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)

                draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Erase a mino
                if not game_over_pvp:
                    erase_mino(dx, dy, mino, rotation)
                    erase_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):   # 땅에 붙어있는 것이 아니라면 -> 아래로 한 칸씩
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)

                        if is_stackable(next_mino1):
                            mino = next_mino1
                            # next_mino1 = next_mino2
                            next_mino1 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            ui_variables.GameOver_sound.play()
                            pvp = False
                            game_status = 'pvp'
                            game_over_pvp = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # Move mino down
                if not is_bottom_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                    dy_2P += 1

                # Create new mino
                else:
                    if hard_drop_2P or bottom_count_2P == 6:
                        hard_drop_2P = False
                        bottom_count_2P = 0
                        score_2P += 10 * level_2P
                        draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)

                        if is_stackable_2P(next_mino1_2P):
                            mino_2P = next_mino1_2P
                            # next_mino1_2P = next_mino2_2P
                            next_mino1_2P = randint(1, 7)
                            dx_2P, dy_2P = 3, 0
                            rotation_2P = 0
                            hold_2P = False
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            ui_variables.GameOver_sound.play()
                            pvp = False
                            gagame_status = 'pvp'
                            game_over_pvp = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count_2P += 1

                # Erase line
                # 콤보 카운트
                erase_count = 0
                erase_count_2P = 0
                combo_value = 0
                combo_value_2P = 0   # pvp 모드에서 콤보 값 출력 변수 combo_value_2P 생성
                sent = 0

                attack_stack = 0
                attack_stack_2P = 0

                # 1P 플레이어 부분
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        attack_stack += 1
                        # attack_stack += 1
                        k = j
                        combo_value += 1
                        combo_count += 1

                        pygame.time.set_timer(pygame.USEREVENT, framerate * 10) 

                        if combo_count >= 11:
                            screen.blit(tetris4, (100, 190))
                            pygame.display.update()
                            ui_variables.combos_sound[8].play()
                            pygame.time.delay(300)

                            combo_value = 0   # combo_value = 0 -> combo_count = 0으로 하면 11이 되는 순간 value 값에 11을 출력하지 않고 바로 0으로 
                            combo_count = 0   # 11이 되는 순간 이미지/사운드 먼저 띄우고 초기화
                        
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]

                            k -= 1
                # 2P 플레이어 부분            
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix_2P[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count_2P += 1
                        attack_stack_2P += 1
                        k = j
                        combo_value_2P += 1
                        combo_count_2P += 1

                        pygame.time.set_timer(pygame.USEREVENT, framerate * 10) 

                        if combo_count_2P >= 11:
                            screen.blit(tetris4, (100, 190))  # blits the combo number
                            pygame.display.update()
                            ui_variables.combos_sound[8].play()
                            pygame.time.delay(300)

                            combo_value_2P = 0   # combo_value = 0 -> combo_count = 0으로 하면 11이 되는 순간 value 값에 11을 출력하지 않고 바로 0으로 
                            combo_count_2P = 0   # 11이 되는 순간 이미지/사운드 먼저 띄우고 초기화
                
                        while k > 0:
                            for i in range(10):
                                matrix_2P[i][k] = matrix_2P[i][k - 1]
                            k -= 1

                while attack_stack >= 2:
                    for j in range(20):
                        for i in range(10):
                            matrix_2P[i][j] = matrix_2P[i][j + 1]

                            attack_stack -= 1
                    for i in range(10):
                        matrix_2P[i][20] = 9
                    k = randint(1, 10)
                    matrix_2P[k][20] = 0
                    attack_point += 1

                while attack_stack_2P >= 2:
                    for j in range(20):
                        for i in range(10):
                            matrix[i][j] = matrix[i][j + 1]

                            attack_stack_2P -= 1
                    for i in range(10):
                        matrix[i][20] = 9
                    k = randint(1, 10)
                    matrix[k][20] = 0
                    attack_point_2P += 1

                # 지운 블록이 없으면 콤보 -1
                # if erase_count == 0 :
                # combo_count -= 1
                # if combo_count < 0:
                # combo_count = 0
                
                # PVP 모드 1P
                if erase_count >= 1:
                    # combo_count += 1
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        # score += 50 * level * erase_count + combo_count
                        score += (10 * (combo_count * combo_count))
                        sent += 1
                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        # score += 150 * level * erase_count + 2 * combo_count
                        score += (10 * (combo_count * combo_count))
                        sent += 2
                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        # score += 350 * level * erase_count + 3 * combo_count
                        score += (10 * (combo_count * combo_count))
                        sent += 3
                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        # score += 1000 * level * erase_count + 4 * combo_count
                        score += (10 * (combo_count * combo_count))
                        sent += 4
                        screen.blit(ui_variables.combo_4ring, (250, 160))  

                    else:
                        score += (10 * (combo_count * combo_count)) 

                    for i in range(1, 11):
                        if combo_count == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (124, 190))  # blits the combo number
                        elif combo_count > 10:  # 11 이상 콤보 이미지  ->  콤보값 초기화
                            screen.blit(tetris4, (100, 190))  # blits the combo number
                            combo_count  = 0   # 콤보 11 달성 시 초기화 및 아이템 부여

                    for i in range(1, 10):
                        if combo_count == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    ui_variables.LevelUp_sound.play()
                    ui_variables.LevelUp_sound.play()

                    goal += level * 5
                    framerate = int(framerate * 0.8)


                # PVP 모드 2P
                if erase_count_2P >= 1:
                    # erase_count_2P는 해당 if문에서 정적인 상수
                    # 10 * (N * N) 점수 처리
                    # combo_count += 1
                    # for i in range(erase_count_2P):
                    #     score_2P += (10 * (combo_count_2P ** 2))
                    if erase_count_2P == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        # score_2P += 50 * level * erase_count_2P + combo_count_2P
                        score_2P += (10 * (combo_count_2P * combo_count_2P))   

                        sent += 1
                    elif erase_count_2P == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        # score_2P += 150 * level * erase_count_2P + 2 * combo_count_2P
                        score_2P += (10 * (combo_count_2P * combo_count_2P))  

                        sent += 2
                    elif erase_count_2P == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        # score_2P += 350 * level * erase_count_2P + 3 * combo_count_2P
                        score_2P += (10 * (combo_count_2P * combo_count_2P))  

                        sent += 3
                    elif erase_count_2P == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()         
                        # score_2P += 1000 * level * erase_count_2P + 4 * combo_count_2P
                        score_2P += (10 * (combo_count_2P * combo_count_2P))  
                        sent += 4
                        screen.blit(ui_variables.combo_4ring, (250, 160))

                    else:
                        score_2P += (10 * (combo_count_2P * combo_count_2P)) 


                    for i in range(1, 11):
                        if combo_count_2P == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (124, 190))  # blits the combo number
                        elif combo_count_2P > 10:  # 11 이상 콤보 이미지
                            screen.blit(tetris4, (100, 190))  # blits the combo number

                    for i in range(1, 10):
                        if combo_count_2P == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()

                # Increase level
                goal_2P -= erase_count_2P
                if goal_2P < 1 and level_2P < 15:
                    level_2P += 1
                    ui_variables.LevelUp_sound.play()
                    ui_variables.LevelUp_sound.play()

                    goal_2P += level_2P * 5
                    framerate = int(framerate * 0.8)


            elif event.type == KEYDOWN:  ##중요
                erase_mino(dx, dy, mino, rotation)
                erase_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)

                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_g:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate*10)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P,dy_2P,mino_2P,rotation_2P)
                    # draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                    # draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                elif event.key == K_k:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        dy_2P += 1
                    hard_drop_2P = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate*10)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    # draw_mino(dx, dy, mino, rotation)
                    # draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                # Hold
                elif event.key == K_f:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            #next_mino1 = next_mino2
                            next_mino1 = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                elif event.key == K_j:
                    if hold_2P == False:
                        ui_variables.move_sound.play()
                        if hold_mino_2P == -1:
                            hold_mino_2P = mino_2P
                            mino_2P = next_mino1_2P
                            # next_mino1_2P = next_mino2_2P
                            next_mino1_2P = randint(1, 7)
                        else:
                            hold_mino_2P, mino_2P = mino_2P, hold_mino_2P
                        dx_2P, dy_2P = 3, 0
                        rotation_2P = 0
                        hold_2P = True
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_mino(dx, dy, mino, rotation)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                # Turn right
                elif event.key == K_h or event.key == K_w:
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, 
                                    level, level_2P, goal, goal_2P)


                elif event.key == K_UP:

                    if is_turnable_r_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        rotation_2P += 1
                    # Kick
                    elif is_turnable_r_2P(dx_2P, dy_2P - 1, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r_2P(dx_2P + 1, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P += 1
                    elif is_turnable_r_2P(dx_2P - 1, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r_2P(dx_2P, dy_2P - 2, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P += 1
                    elif is_turnable_r_2P(dx_2P + 2, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P += 1
                    elif is_turnable_r_2P(dx_2P - 2, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P += 1
                    if rotation_2P == 4:
                        rotation_2P = 0
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_mino(dx, dy, mino, rotation)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                    
                elif event.key == K_l or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Move left
                elif event.key == K_a:  # key = pygame.key.get_pressed()
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate * 3)
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                elif event.key == K_LEFT:  # key = pygame.key.get_pressed()
                    if not is_leftedge_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate * 3)
                        dx_2P -= 1
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_mino(dx, dy, mino, rotation)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Move right
                elif event.key == K_d:
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate * 3)
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                    # if not is_leftedge_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate * 3)
                        dx_2P += 1
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_mino(dx, dy, mino, rotation)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                elif event.key == K_s:
                    if not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                elif event.key == K_DOWN:
                    if not is_bottom_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        dy_2P += 1
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_mino(dx, dy, mino, rotation)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                    
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h

                # 최소 화면 너비/높이 조건 설정
                if board_width < min_width or board_height < min_height:   # 최소 너비/높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                
                if not ( (board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05) ):   # 높이/너비가 일정 비율을 넘어서게 되면
                    board_width = int(board_height / board_rate)   # 너비를 적정 비율로 바꾸어줌
                    board_height = int(board_width * board_rate)   # 높이를 적정 비율로 바꾸어줌

                if board_width >= mid_width:   # 화면 사이즈가 큰  경우
                    textsize = True   # 큰  글자 
                    
                if board_width <= mid_width:
                    textsize = False

                block_size = int(board_height * 0.045)

                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height) 

        # if any(movement_keys.values()):
        #    movement_keys_timer += clock.tick(50)

        pygame.display.update()

    elif signup:
        draw_image(screen, login_bg, board_width * 0.5, board_height * 0.5, board_width, board_height)
        draw_image(screen, signup_board, board_width * 0.5, board_height * 0.55, int(board_width * 3/8), int(board_height * 24/45))
        
        sign_up_button2.draw(screen, (0, 0, 0))
        log_back.draw(screen, (0, 0, 0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            for box in input_boxes_signup:
                box.handle_event(event)
            for box in input_boxes_signup:
                box.update()
            for box in input_boxes_signup:
                box.draw(screen)
            pygame.display.update()

            if event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300)
            elif event.type == pygame.MOUSEMOTION:
                if sign_up_button2.isOver_2(pos):
                    sign_up_button2.image = button_sign_up_clicked
                else:
                    sign_up_button2.image = button_sign_up
                if log_back.isOver_2(pos):
                    log_back.image = button_log_back_clicked
                else:
                    log_back.image = button_log_back
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sign_up_button2.isOver_2(pos):
                    ui_variables.click_sound.play()
                    id_text = input_box1.text
                    pw_text = input_box2.text
                    add_id(id_text)
                    add_pw(id_text, pw_text)
                    signup = False
                if log_back.isOver_2(pos):
                    ui_variables.click_sound.play()
                    signup = False
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif signin:
        draw_image(screen, login_bg, board_width*0.5, board_height*0.5,
        board_width, board_height)
        draw_image(screen, signin_board, board_width*0.5, board_height*0.55,
        int(board_width*3/8),int(board_height*24/45))
        sign_in_button2.draw(screen,(0,0,0))
        log_back.draw(screen,(0,0,0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            for box in input_boxes_signin:
                box.handle_event(event)
            for box in input_boxes_signin:
                box.update()
            for box in input_boxes_signin:
                box.draw(screen)
            pygame.display.update()
            if event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300)
                pygame.display.update()
            elif event.type == pygame.MOUSEMOTION:
                if sign_in_button2.isOver_2(pos):
                    sign_in_button2.image = button_sign_in_clicked
                else:
                    sign_in_button2.image = button_sign_in
                if log_back.isOver_2(pos):
                    log_back.image = button_log_back_clicked
                else:
                    log_back.image = button_log_back

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sign_in_button2.isOver_2(pos):
                    ui_variables.click_sound.play()
                    id_text = input_box3.text
                    pw_text = input_box4.text
                    if check_info(id_text, pw_text):
                        signin= False
                        main = True
                        # num_earthquake = load_earthquake_data(id_text)
                        # num_light = load_light_data(id_text)
                        # num_tnt = load_tnt_data(id_text)
                        # gold = load_gold_data(id_text)
                        user_id = id_info(id_text)

                if log_back.isOver_2(pos):
                    ui_variables.click_sound.play()
                    signin = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
               

    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.mixer.music.stop()
                pygame.time.set_timer(pygame.USEREVENT, 300)

                draw_image(screen, gameover_board_image, board_width * 0.5, board_height * 0.5,
                           int(board_height * 0.7428), board_height)
                menu_button.draw(screen, (0, 0, 0))
                restart_button.draw(screen, (0, 0, 0))
                ok_button.draw(screen, (0, 0, 0))

                score1 = ui_variables.h1_b.render(str(score), 1, ui_variables.white) #점수를 출력하기 위해 폰트, 글자색 지정
                screen.blit(score1, (int(board_width * 0.440), int(board_height * 0.55))) #글자를 화면에 나타냄(출력할 문구, x좌표, y좌표)

                pygame.display.update()

            elif event.type == KEYDOWN:                
                  

                if event.key == K_RETURN:
                    ui_variables.click_sound.play()
                    '''
                    outfile = open('leaderboard.txt', 'a')
                    outfile.write( text + ' ' + str(score) + '\n')
                    outfile.close()
                    '''

                    game_over = False
                    game_over_pvp = False
                    main = True

                    hold = False  #
                    dx, dy = 3, 0  #
                    rotation = 0  #
                    mino = randint(1, 7)  #
                    next_mino1 = randint(1, 7)  #
                    hold_mino = -1  #
                    framerate = 30
                    score = 0
                    #
                    score_2P = 0

                    combo_count = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0  #
                    hard_drop = False  #
                    name_location = 0
                    name = [65, 65, 65, 65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    hold_mino_2P = -1  #
                    bottom_count_2P = 0  #
                    hard_drop_2P = False  #
                    hold_2P = False  #
                    next_mino1_2P = randint(1, 7)  #
                    mino_2P = randint(1, 7)  #
                    rotation_2P = 0  #
                    dx_2P, dy_2P = 3, 0  #
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix

                    
                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)
                    

                    pygame.time.set_timer(pygame.USEREVENT, 1)
                pygame.display.flip()
                

            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver(pos):
                    menu_button.image = clicked_menu_button_image
                else:
                    menu_button.image = menu_button_image

                if restart_button.isOver(pos):
                    restart_button.image = clicked_restart_button_image
                else:
                    restart_button.image = restart_button_image

                if ok_button.isOver(pos):
                    ok_button.image = clicked_ok_button_image
                else:
                    ok_button.image = ok_button_image

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.isOver(pos):
                    ui_variables.click_sound.play()
                    ui_variables.click_sound.play()
                    '''
                    outfile = open('leaderboard.txt', 'a')
                    outfile.write(text+ ' ' + str(score) + '\n')
                    outfile.close()
                    '''
                    text=''
                    game_over = False
                    game_over_pvp = False
                    main = True
                    hold = False  #
                    dx, dy = 3, 0  #
                    rotation = 0  #
                    mino = randint(1, 7)  #
                    next_mino1 = randint(1, 7)  #
                    hold_mino = -1  #
                    framerate = 30
                    score = 0
                    score_2P = 0
                    combo_count = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0  #
                    hard_drop = False  #
                    name_location = 0
                    name = [65, 65, 65, 65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    hold_mino_2P = -1  #
                    bottom_count_2P = 0  #
                    hard_drop_2P = False  #
                    hold_2P = False  #
                    next_mino1_2P = randint(1, 7)  #
                    mino_2P = randint(1, 7)  #
                    rotation_2P = 0  #
                    dx_2P, dy_2P = 3, 0  #
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
                    attack_point = 0
                    attack_point_2P = 0

                    
                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)
                    
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                if menu_button.isOver(pos):
                    ui_variables.click_sound.play()
                    text=''
                    start = False
                    pvp = False
                    game_over = False
                    game_over_pvp = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino1 = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score_2P = 0
                    combo_count = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65, 65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]
                    hold_mino_2P = -1  #
                    bottom_count_2P = 0  #
                    hard_drop_2P = False  #
                    hold_2P = False  #
                    next_mino1_2P = randint(1, 7)  #
                    mino_2P = randint(1, 7)  #
                    rotation_2P = 0  #
                    dx_2P, dy_2P = 3, 0  #
                    attack_point = 0
                    ttack_point_2P = 0
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
                if restart_button.isOver(pos):
                    if game_status == 'start':
                        start = True
                        pygame.mixer.music.play(-1)
                    if game_status == 'pvp':
                        pvp = True
                        pygame.mixer.music.play(-1)
                    ui_variables.click_sound.play()
                    text=''
                    game_over = False
                    game_over_pvp = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino1 = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score_2P = 0
                    combo_count = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65, 65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]
                    hold_mino_2P = -1  #
                    bottom_count_2P = 0  #
                    hard_drop_2P = False  #
                    hold_2P = False  #
                    next_mino1_2P = randint(1, 7)  #
                    mino_2P = randint(1, 7)  #
                    rotation_2P = 0  #
                    dx_2P, dy_2P = 3, 0  #
                    attack_point = 0
                    ttack_point_2P = 0
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
                    pause = False

                if resume_button.isOver(pos):
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h

                # 최소 화면 너비/높이 조건 설정
                if board_width < min_width or board_height < min_height:   # 최소 너비/높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                
                if not ( (board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05) ):   # 높이/너비가 일정 비율을 넘어서게 되면
                    board_width = int(board_height / board_rate)   # 너비를 적정 비율로 바꾸어줌
                    board_height = int(board_width * board_rate)   # 높이를 적정 비율로 바꾸어줌

                if board_width >= mid_width:   # 화면 사이즈가 큰  경우
                    textsize = True   # 큰  글자 
                    
                if board_width <= mid_width:
                    textsize = False

                block_size = int(board_height * 0.045)

                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height) 


    elif game_over_pvp:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.mixer.music.stop()
                pygame.time.set_timer(pygame.USEREVENT, 300)

                draw_image(screen, gameover_board_image, board_width * 0.5, board_height * 0.5,
                           int(board_height * 0.7428), board_height)
                menu_button.draw(screen, (0, 0, 0))
                restart_button.draw(screen, (0, 0, 0))
                ok_button.draw(screen, (0, 0, 0))

                score1 = ui_variables.h1_b.render(str(score), 1, ui_variables.white) #점수를 출력하기 위해 폰트, 글자색 지정
                player_1 = ui_variables.h2_b.render('1P', 1, ui_variables.grey_1)
                score2 = ui_variables.h1_b.render(str(score_2P), 1, ui_variables.white) #점수를 출력하기 위해 폰트, 글자색 지정
                player_2 = ui_variables.h2_b.render('2P', 1, ui_variables.grey_1)
                winner = ui_variables.h4.render('WIN',1,ui_variables.red)
                if(str(score)>str(score_2P)) :
                    screen.blit(winner,(int(board_width * 0.330), int(board_height * 0.457)))
                else :
                    screen.blit(winner,(int(board_width * 0.600), int(board_height * 0.457)))
                    
                screen.blit(score1, (int(board_width * 0.380), int(board_height * 0.55))) #글자를 화면에 나타냄(출력할 문구, x좌표, y좌표)
                screen.blit(score2, (int(board_width * 0.550), int(board_height * 0.55))) #글자를 화면에 나타냄(출력할 문구, x좌표, y좌표)
                screen.blit(player_1, (int(board_width * 0.390), int(board_height * 0.457)))
                screen.blit(player_2, (int(board_width * 0.560), int(board_height * 0.457)))

                pygame.display.update()

            elif event.type == KEYDOWN:            
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()
                    '''
                    if score > score_2P:
                        outfile = open('leaderboard.txt', 'a')
                        outfile.write( text + ' ' + str(score) + '\n')
                        outfile.close()
                    else:
                        outfile = open('leaderboard.txt', 'a')
                        outfile.write( text + ' ' + str(score_2P) + '\n')
                        outfile.close()
                    '''
                    text=''
                    game_over = False
                    game_over_pvp = False
                    hold = False  #
                    dx, dy = 3, 0  #
                    rotation = 0  #
                    mino = randint(1, 7)  #
                    next_mino1 = randint(1, 7)  #
                    hold_mino = -1  #
                    framerate = 30
                    score = 0
                    score_2P = 0
                    combo_count = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0  #
                    hard_drop = False  #
                    name_location = 0
                    name = [65, 65, 65, 65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    hold_mino_2P = -1  #
                    bottom_count_2P = 0  #
                    hard_drop_2P = False  #
                    hold_2P = False  #
                    next_mino1_2P = randint(1, 7)  #
                    mino_2P = randint(1, 7)  #
                    rotation_2P = 0  #
                    dx_2P, dy_2P = 3, 0  #
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix

                    
                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)
                    

                    pygame.time.set_timer(pygame.USEREVENT, 1)
                pygame.display.flip()
                

            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver(pos):
                    menu_button.image = clicked_menu_button_image
                else:
                    menu_button.image = menu_button_image

                if restart_button.isOver(pos):
                    restart_button.image = clicked_restart_button_image
                else:
                    restart_button.image = restart_button_image

                if ok_button.isOver(pos):
                    ok_button.image = clicked_ok_button_image
                else:
                    ok_button.image = ok_button_image

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.isOver(pos):
                    ui_variables.click_sound.play()
                    ui_variables.click_sound.play()

                    if score > score_2P:
                        outfile = open('leaderboard.txt', 'a')
                        outfile.write( text + ' ' + str(score) + '\n')
                        outfile.close()
                    else:
                        outfile = open('leaderboard.txt', 'a')
                        outfile.write( text + ' ' + str(score_2P) + '\n')
                        outfile.close()
                    
                    text=''
                    game_over = False
                    game_over_pvp = False
                    hold = False  #
                    dx, dy = 3, 0  #
                    rotation = 0  #
                    mino = randint(1, 7)  #
                    next_mino1 = randint(1, 7)  #
                    hold_mino = -1  #
                    framerate = 30
                    score = 0
                    score_2P = 0
                    combo_count = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0  #
                    hard_drop = False  #
                    name_location = 0
                    name = [65, 65, 65, 65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    hold_mino_2P = -1  #
                    bottom_count_2P = 0  #
                    hard_drop_2P = False  #
                    hold_2P = False  #
                    next_mino1_2P = randint(1, 7)  #
                    mino_2P = randint(1, 7)  #
                    rotation_2P = 0  #
                    dx_2P, dy_2P = 3, 0  #
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
                    attack_point = 0
                    ttack_point_2P = 0

                    
                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)
                    
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                if menu_button.isOver(pos):
                    ui_variables.click_sound.play()
                    text=''
                    start = False
                    pvp = False
                    game_over = False
                    game_over_pvp = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino1 = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score_2P = 0
                    combo_count = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65, 65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]
                    hold_mino_2P = -1  #
                    bottom_count_2P = 0  #
                    hard_drop_2P = False  #
                    hold_2P = False  #
                    next_mino1_2P = randint(1, 7)  #
                    mino_2P = randint(1, 7)  #
                    rotation_2P = 0  #
                    dx_2P, dy_2P = 3, 0  #
                    attack_point = 0
                    ttack_point_2P = 0
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
                if restart_button.isOver(pos):
                    if game_status == 'start':
                        start = True
                        pygame.mixer.music.play(-1)
                    if game_status == 'pvp':
                        pvp = True
                        pygame.mixer.music.play(-1)
                    ui_variables.click_sound.play()
                    text=''
                    game_over = False
                    game_over_pvp = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino1 = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score_2P = 0
                    combo_count = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65, 65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]
                    hold_mino_2P = -1  #
                    bottom_count_2P = 0  #
                    hard_drop_2P = False  #
                    hold_2P = False  #
                    next_mino1_2P = randint(1, 7)  #
                    mino_2P = randint(1, 7)  #
                    rotation_2P = 0  #
                    dx_2P, dy_2P = 3, 0  #
                    attack_point = 0
                    ttack_point_2P = 0
                    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
                    pause = False

                if resume_button.isOver(pos):
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h

                # 최소 화면 너비/높이 조건 설정
                if board_width < min_width or board_height < min_height:   # 최소 너비/높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                
                if not ( (board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05) ):   # 높이/너비가 일정 비율을 넘어서게 되면
                    board_width = int(board_height / board_rate)   # 너비를 적정 비율로 바꾸어줌
                    board_height = int(board_width * board_rate)   # 높이를 적정 비율로 바꾸어줌

                if board_width >= mid_width:   # 화면 사이즈가 큰  경우
                    textsize = True   # 큰  글자 
                    
                if board_width <= mid_width:
                    textsize = False

                block_size = int(board_height * 0.045)

                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height) 

    # Start screen  ->  여기가 기존에서는 메인
    elif main:
        main = True

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    ui_variables.click_sound.play()
                    start = True
            elif event.type == pygame.MOUSEMOTION:
                if single_button.isOver(pos):
                    single_button.image = clicked_single_button_image
                else:
                    single_button.image = single_button_image

                if pvp_button.isOver(pos):
                    pvp_button.image = clicked_pvp_button_image
                else:
                    pvp_button.image = pvp_button_image

                if help_button.isOver(pos):
                    help_button.image = clicked_help_button_image
                else:
                    help_button.image = help_button_image

                if quit_button.isOver(pos):
                    quit_button.image = clicked_quit_button_image
                else:
                    quit_button.image = quit_button_image

                if setting_icon.isOver(pos):
                    setting_icon.image = clicked_setting_vector
                else:
                    setting_icon.image = setting_vector

                if leaderboard_icon.isOver(pos):
                    leaderboard_icon.image = clicked_leaderboard_vector
                else:
                    leaderboard_icon.image = leaderboard_vector
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if single_button.isOver(pos):
                    ui_variables.click_sound.play()
                    previous_time = pygame.time.get_ticks()
                    start = True
                    pygame.mixer.music.play(-1)
                if pvp_button.isOver(pos):
                    ui_variables.click_sound.play()
                    pvp = True
                    pygame.mixer.music.play(-1)
                if leaderboard_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    leader_board = True
                if setting_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if quit_button.isOver(pos):
                    ui_variables.click_sound.play()
                    done = True
                if help_button.isOver(pos):
                    ui_variables.click_sound.play()
                    help = True
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h

                # 최소 화면 너비/높이 조건 설정
                if board_width < min_width or board_height < min_height:   # 최소 너비/높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                
                if not ( (board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05) ):   # 높이/너비가 일정 비율을 넘어서게 되면
                    board_width = int(board_height / board_rate)   # 너비를 적정 비율로 바꾸어줌
                    board_height = int(board_width * board_rate)   # 높이를 적정 비율로 바꾸어줌

                if board_width >= mid_width:   # 화면 사이즈가 큰  경우
                    textsize = True   # 큰  글자 
                    
                if board_width <= mid_width:
                    textsize = False
                
                block_size = int(board_height * 0.045)

                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height) 

        screen.fill(ui_variables.white)

        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height)

        single_button.draw(screen, (0, 0, 0))
        pvp_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))

        setting_icon.draw(screen, (0, 0, 0))
        leaderboard_icon.draw(screen, (0, 0, 0))

        if not start:
            pygame.display.update()
            clock.tick(3)

    else:


pygame.quit()
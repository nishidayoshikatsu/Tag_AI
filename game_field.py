import pygame
from pygame.locals import *
import sys

### スクリーンのパラメータ ###
SCREEN_SIZE = (500, 500)        # スクリーンサイズ(幅、高さ)
BACK_COLOR = (255, 255, 255)    # 背景色をRGBで指定
### end ###

### 矩形関連のパラメータ ###
OBSTACLE_COLOR = (0, 0, 0)
RECT_COLOR = (0, 0, 0)          # 矩形の色をRGBで指定
RECT_SIZE = 100                 # 矩形の大きさを指定
LINE_WIDTH = 1                  # 矩形の線の太さを指定
RECT_FIRST_POSITION = 50        # 矩形の初期位置(左上)
### end ###

def field_set():
    ### グローバル変数宣言 ###
    global RECT_COLOR
    global RECT_SIZE
    global LINE_WIDTH
    global RECT_FIRST_POSITION
    ### end ###
    ELEMENT_COORDINATE = []
    for i in range(4):
        imaginary_array = []
        for j in range(4):
            ### 図形の描画に必要なパラメータの計算 ###
            RECT_POSITION_X = RECT_FIRST_POSITION + 100 * j
            RECT_POSITION_Y = RECT_FIRST_POSITION + 100 * i
            ### end ###

            coordinate = (RECT_POSITION_X, RECT_POSITION_Y)
            imaginary_array.append(coordinate)               #二次元のリストにするための仮のリスト
        ELEMENT_COORDINATE.append(imaginary_array)      #二次元のリストで取得

    return ELEMENT_COORDINATE

if __name__ == "__main__":

    pygame.init()               #　初期化
    screen = pygame.display.set_mode(SCREEN_SIZE) # スクリーンの初期化
    pygame.display.set_caption("Pygame Test") # スクリーンのタイトルの設定

    ### エージェント等の設定 ###
    human_agent = pygame.image.load("./image/人.png")                                           # 人の画像を指定
    demon_agent = pygame.image.load("./image/鬼.png")                                           # 鬼の画像を指定
    goal = pygame.image.load("./image/ゴール.png")                                              # ゴールの画像を指定
    demon_agent = pygame.transform.smoothscale(demon_agent, (RECT_SIZE, RECT_SIZE))
    human_agent = pygame.transform.smoothscale(human_agent, (RECT_SIZE, RECT_SIZE))
    goal = pygame.transform.smoothscale(goal, (RECT_SIZE, RECT_SIZE))
    ### end ###

    coordinate = field_set()    # 各マスの左上の座標を生成

    ### 各要素の座標を選択 ###
    HUMAN_AGENT_POSITION = coordinate[0][3]                     # 人の座標を指定(移動可能)
    DEMON_AGENT_POSITION = coordinate[1][2]                     # 鬼の座標を指定(移動可能)
    OBSTACLE_POSITION = (coordinate[2][2][0], coordinate[2][2][1], RECT_SIZE, RECT_SIZE)    # 障害物の座標を指定(固定)
    GOAL_POSITION = coordinate[3][0]                            # ゴールの座標を指定(固定)
    ### end ###

    # ゲームループ
    while True:
        screen.fill(BACK_COLOR)     # surfaceを1色で塗りつぶす

        for i in range(4):
            for j in range(4):
                pygame.draw.rect(screen, RECT_COLOR, Rect(coordinate[i][j][0], coordinate[i][j][1], RECT_SIZE, RECT_SIZE), LINE_WIDTH)

        '''
        ### キーボード入力 ###
        #pygame.event.pump()
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_w]:
            HUMAN_AGENT_POSITION = list(HUMAN_AGENT_POSITION)
            HUMAN_AGENT_POSITION[1] -= RECT_SIZE
            HUMAN_AGENT_POSITION = tuple(HUMAN_AGENT_POSITION)
            #Rect.move_ip(HUMAN_AGENT_POSITION[0], HUMAN_AGENT_POSITION[1] + RECT_SIZE)
        if pressed_key[K_a]:
            HUMAN_AGENT_POSITION = list(HUMAN_AGENT_POSITION)
            HUMAN_AGENT_POSITION[0] -= RECT_SIZE
            HUMAN_AGENT_POSITION = tuple(HUMAN_AGENT_POSITION)
        if pressed_key[K_s]:
            HUMAN_AGENT_POSITION = list(HUMAN_AGENT_POSITION)
            HUMAN_AGENT_POSITION[1] += RECT_SIZE
            HUMAN_AGENT_POSITION = tuple(HUMAN_AGENT_POSITION)
        if pressed_key[K_d]:
            HUMAN_AGENT_POSITION = list(HUMAN_AGENT_POSITION)
            HUMAN_AGENT_POSITION[0] += RECT_SIZE
            HUMAN_AGENT_POSITION = tuple(HUMAN_AGENT_POSITION)
        ### end ###
        '''

        ### 各要素をスクリーンに表示 ###
        screen.blit(human_agent, HUMAN_AGENT_POSITION)                                          # 人の画像を表示
        screen.blit(demon_agent, DEMON_AGENT_POSITION)                                          # 鬼の画像を表示
        screen.fill(OBSTACLE_COLOR, OBSTACLE_POSITION)                                          # 障害物を黒で表示
        screen.blit(goal, GOAL_POSITION)                                                        # ゴールの画像を表示
        ### end ###


        pygame.display.update() # スクリーンの更新

        for event in pygame.event.get(): # イベント処理
            if event.type == QUIT:     # 終了イベント
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT:
                    HUMAN_AGENT_POSITION = list(HUMAN_AGENT_POSITION)
                    HUMAN_AGENT_POSITION[0] -= RECT_SIZE
                    HUMAN_AGENT_POSITION = tuple(HUMAN_AGENT_POSITION)
                    #Rect.move_ip(HUMAN_AGENT_POSITION[0], HUMAN_AGENT_POSITION[1] + RECT_SIZE)
                if event.key == K_RIGHT:
                    HUMAN_AGENT_POSITION = list(HUMAN_AGENT_POSITION)
                    HUMAN_AGENT_POSITION[0] += RECT_SIZE
                    HUMAN_AGENT_POSITION = tuple(HUMAN_AGENT_POSITION)
                if event.key == K_UP:
                    HUMAN_AGENT_POSITION = list(HUMAN_AGENT_POSITION)
                    HUMAN_AGENT_POSITION[1] -= RECT_SIZE
                    HUMAN_AGENT_POSITION = tuple(HUMAN_AGENT_POSITION)
                if event.key == K_DOWN:
                    HUMAN_AGENT_POSITION = list(HUMAN_AGENT_POSITION)
                    HUMAN_AGENT_POSITION[1] += RECT_SIZE
                    HUMAN_AGENT_POSITION = tuple(HUMAN_AGENT_POSITION)
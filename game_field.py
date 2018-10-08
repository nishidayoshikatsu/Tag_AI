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
#ELEMENT_FIRST_POSITION = RECT_FIRST_POSITION + (RECT_SIZE / 2)     #中心座標の計算(無駄無駄無駄ア！)
### end ###

def field_set():
    ### グローバル変数宣言 ###
    global RECT_COLOR
    global RECT_SIZE
    global LINE_WIDTH
    global RECT_FIRST_POSITION
    #global ELEMENT_FIRST_POSITION

    ELEMENT_COORDINATE = []
    for i in range(4):
        imaginary_array = []
        for j in range(4):
            ### 図形の描画に必要なパラメータの計算 ###
            RECT_POSITION_X = RECT_FIRST_POSITION + 100 * j
            RECT_POSITION_Y = RECT_FIRST_POSITION + 100 * i
            #ELEMENT_POSITION_X = ELEMENT_FIRST_POSITION + 100 * j
            #ELEMENT_POSITION_Y = ELEMENT_FIRST_POSITION + 100 * i
            ### end ###

            pygame.draw.rect(screen, RECT_COLOR, Rect(RECT_POSITION_X, RECT_POSITION_Y, RECT_SIZE, RECT_SIZE), LINE_WIDTH)    # surfaceに四角形を描画
            coordinate = (RECT_POSITION_X, RECT_POSITION_Y)
            #pygame.draw.line(screen, RECT_COLOR, pivot, pivot, 2)       #中心の座標が出ているか確認(無駄無駄無駄ア！)
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

    # ゲームループ
    while True:
        screen.fill(BACK_COLOR)     # surfaceを1色で塗りつぶす
        coordinate = field_set()    # ４×4のマスを生成し、各マスの左上の座標を返す

        ### 各要素の座標を選択 ###
        HUMAN_AGENT_POSITION = (coordinate[0][3][0], coordinate[0][3][1])                       # 人の座標を指定
        DEMON_AGENT_POSITION = (coordinate[1][2][0], coordinate[1][2][1])                       # 鬼の座標を指定
        OBSTACLE_POSITION = (coordinate[2][2][0], coordinate[2][2][1], RECT_SIZE, RECT_SIZE)    # 障害物の座標を指定
        GOAL_POSITION = (coordinate[3][0][0], coordinate[3][0][1])                              # ゴールの座標を指定
        ### end ###
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
import pygame
from pygame.locals import *
import sys

### スクリーンのパラメータ ###
SCREEN_SIZE = (500, 500)        # スクリーンサイズ(幅、高さ)
BACK_COLOR = (255, 255, 255)    # 背景色をRGBで指定
### end ###
    
### 矩形関連のパラメータ ###
RECT_COLOR = (0, 0, 0)          # 矩形の色をRGBで指定
RECT_SIZE = 100                 # 矩形の大きさを指定
LINE_WIDTH = 1                  # 矩形の線の太さを指定
RECT_FIRST_POSITION = 50        # 矩形の初期位置(左上)
ELEMENT_FIRST_POSITION = RECT_FIRST_POSITION + (RECT_SIZE / 2)
### end ###

def field_set():
    ### グローバル変数宣言 ###
    global RECT_COLOR
    global RECT_SIZE
    global LINE_WIDTH
    global RECT_FIRST_POSITION
    global ELEMENT_FIRST_POSITION

    ELEMENT_COORDINATE = []
    for i in range(4):
        imaginary_array = []
        for j in range(4):
            ### 図形の描画に必要なパラメータの計算 ###
            RECT_POSITION_X = RECT_FIRST_POSITION + 100 * j
            RECT_POSITION_Y = RECT_FIRST_POSITION + 100 * i
            ELEMENT_POSITION_X = ELEMENT_FIRST_POSITION + 100 * j
            ELEMENT_POSITION_Y = ELEMENT_FIRST_POSITION + 100 * i
            ### end ###

            pygame.draw.rect(screen, RECT_COLOR, Rect(RECT_POSITION_X, RECT_POSITION_Y, RECT_SIZE, RECT_SIZE), LINE_WIDTH)    # surfaceに四角形を描画
            pivot = (ELEMENT_POSITION_X, ELEMENT_POSITION_Y)
            #pygame.draw.line(screen, RECT_COLOR, pivot, pivot, 2)       #中心の座標が出ているか確認
            imaginary_array.append(pivot)               #二次元のリストにするための仮のリスト
        ELEMENT_COORDINATE.append(imaginary_array)      #二次元のリストで取得

    return ELEMENT_COORDINATE

if __name__ == "__main__":

    pygame.init()               #　初期化
    screen = pygame.display.set_mode(SCREEN_SIZE) # スクリーンの初期化
    pygame.display.set_caption("Pygame Test") # スクリーンのタイトルの設定

    # ゲームループ
    while True:
        screen.fill(BACK_COLOR)     # surfaceを1色で塗りつぶす
            
        coordinate = field_set()
        print(coordinate)

        pygame.display.update() # スクリーンの更新

        for event in pygame.event.get(): # イベント処理
            if event.type == QUIT:     # 終了イベント
                pygame.quit()
                sys.exit()
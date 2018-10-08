import pygame
from pygame.locals import *
import sys


if __name__ == "__main__":
    SCREEN_SIZE = (500, 500)        # スクリーンサイズ
    BACK_COLOR = (255, 255, 255)    # 背景色をRGBで指定
    RECT_COLOR = (0, 0, 0)          # 矩形の色をRGBで指定
    RECT_FIRST_POSITION = 50        # 矩形の初期位置
    ELEMENT_FIRST_POSITION = 100

    pygame.init()               #　初期化
    screen = pygame.display.set_mode(SCREEN_SIZE) # スクリーンの初期化
    pygame.display.set_caption("Pygame Test") # スクリーンのタイトルの設定


    # ゲームループ
    while True:
        screen.fill(BACK_COLOR)     # surfaceを1色で塗りつぶす
        ELEMENT_COORDINATE = []
        #cnt = 0
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(screen, RECT_COLOR, Rect(RECT_FIRST_POSITION + 100 * j, RECT_FIRST_POSITION + 100 * i, 100, 100), 1)    # surfaceに四角形を描画
                ELEMENT_COORDINATE.append([ELEMENT_FIRST_POSITION + 100 * j, ELEMENT_FIRST_POSITION + 100 * i])
                pivot = tuple(ELEMENT_COORDINATE[j + 4 * i])
                pygame.draw.line(screen, RECT_COLOR, pivot, pivot, 2)
                #cnt += 1
        


        pygame.display.update() # スクリーンの更新

        for event in pygame.event.get(): # イベント処理
            if event.type == QUIT:     # 終了イベント
                pygame.quit()
                sys.exit()
import pygame
from pygame.locals import *
import sys

#import action                   # action.pyをインポート

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

def field_coordinate_set():
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
            imaginary_array.append(coordinate)          # 二次元のリストにするための仮のリスト
        ELEMENT_COORDINATE.append(imaginary_array)      # 二次元のリストで取得

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

    coordinate = field_coordinate_set()    # 各マスの左上の座標を生成

    ### 各要素の座標を選択 ###
    HUMAN_AGENT_POSITION = coordinate[0][3]                     # 人の座標を指定(移動可能)
    DEMON_AGENT_POSITION = coordinate[1][2]                     # 鬼の座標を指定(移動可能)
    OBSTACLE_POSITION_1 = (coordinate[2][2][0], coordinate[2][2][1], RECT_SIZE, RECT_SIZE)    # 障害物の座標を指定(固定)
    OBSTACLE_POSITION_2 = coordinate[2][2]
    GOAL_POSITION = coordinate[3][0]                            # ゴールの座標を指定(固定)
    ### end ###

    while True:
        agent = input("鬼(0)と人(1)のどちらを操作しますか？> ")
        if agent == '鬼' or agent == '0':
            agent = "demon"
            ally = DEMON_AGENT_POSITION
            enemy = HUMAN_AGENT_POSITION
            #operation_position = DEMON_AGENT_POSITION
            break
        elif agent == '人' or agent == '1':
            agent = "human"
            ally = HUMAN_AGENT_POSITION
            enemy = HUMAN_AGENT_POSITION
            #operation_position = HUMAN_AGENT_POSITION
            break
        else:
            print("ちゃんと選べよおお")

    # ゲームループ
    while True:
        screen.fill(BACK_COLOR)     # surfaceを1色で塗りつぶす

        ### 4×4のフィールドを描画 ###
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(screen, RECT_COLOR, Rect(coordinate[i][j][0], coordinate[i][j][1], RECT_SIZE, RECT_SIZE), LINE_WIDTH)
        ### end ###

        ### 各要素をスクリーンに表示 ###
        screen.blit(human_agent, HUMAN_AGENT_POSITION)                                          # 人の画像を表示
        screen.blit(demon_agent, DEMON_AGENT_POSITION)                                          # 鬼の画像を表示
        screen.fill(OBSTACLE_COLOR, OBSTACLE_POSITION_1)                                        # 障害物を黒で表示
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
                if event.key == K_a:    # 左方向に行く
                    if ally[0] >= coordinate[0][1][0] and (ally[0] - RECT_SIZE, ally[1]) != OBSTACLE_POSITION_2:      # 左端のマスにいない時
                        ally = list(ally)
                        ally[0] -= RECT_SIZE
                        ally = tuple(ally)
                        #Rect.move_ip(HUMAN_AGENT_POSITION[0], HUMAN_AGENT_POSITION[1] + RECT_SIZE)
                    else:
                        print("これ以上左には行けないよ")
                if event.key == K_d:    # 右方向に行く
                    if ally[0] <= coordinate[0][2][0] and (ally[0] + RECT_SIZE, ally[1]) != OBSTACLE_POSITION_2:      # 右端のマスにいない時
                        ally = list(ally)
                        ally[0] += RECT_SIZE
                        ally = tuple(ally)
                    else:
                        print("これ以上右には行けないよ")
                if event.key == K_w:    # 上方向に行く
                    if ally[1] >= coordinate[1][0][1] and (ally[0], ally[1] - RECT_SIZE) != OBSTACLE_POSITION_2:      # 上端のマスにいない時
                        ally = list(ally)
                        ally[1] -= RECT_SIZE
                        ally = tuple(ally)
                    else:
                        print("これ以上上には行けないよ")
                if event.key == K_s:    # 下方向に行く
                    if ally[1] <= coordinate[2][0][1] and (ally[0], ally[1] + RECT_SIZE) != OBSTACLE_POSITION_2:      # 下端のマスにいない時
                        ally = list(ally)
                        ally[1] += RECT_SIZE
                        ally = tuple(ally)
                    else:
                        print("これ以上下には行けないよ")
                if agent == "human":
                    HUMAN_AGENT_POSITION = ally
                else:
                    DEMON_AGENT_POSITION = ally
                if agent == "human" and HUMAN_AGENT_POSITION == GOAL_POSITION:                   # ゴールについた時
                    print("goal!!")
                    print("人の勝ち！！")
                    if event.key == K_KP_ENTER:
                        pygame.quit()
                        sys.exit()
                if HUMAN_AGENT_POSITION == DEMON_AGENT_POSITION:
                    print("鬼の勝ち！！")
                    if event.key == K_KP_ENTER:
                        pygame.quit()
                        sys.exit()
# -*- coding: utf-8 -*-

import numpy as np

import pygame
from pygame.locals import *
import sys

import os

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

# 行は状態0～7、列は移動方向で↑、→、↓、←、stopを表す
theta_0 = np.array([[np.nan, 1, 1, np.nan, 1],  # coordinate[0][0]
                    [np.nan, 1, 1, 1, 1],  # coordinate[0][1]
                    [np.nan, 1, 1, 1, 1],  # coordinate[0][2]
                    [np.nan, np.nan, 1, 1, 1],  # coordinate[0][3]
                    [1, 1, 1, np.nan, 1],  # coordinate[1][0]
                    [1, 1, 1, 1, 1],  # coordinate[1][1]
                    [1, 1, np.nan, 1, 1],  # coordinate[1][2]
                    [1, np.nan, 1, 1, 1],  # coordinate[1][3]
                    [1, np.nan, 1, np.nan, 1],  # coordinate[2][0] ※coordinate[2][1]は障害物だから方策なし
                    [np.nan, np.nan, np.nan, np.nan, np.nan],  # coordinate[2][1]は障害物
                    [1, 1, 1, np.nan, 1],   # coordinate[2][2]
                    [1, np.nan, 1, 1, 1],  # coordinate[2][3]
                    [1, 1, np.nan, np.nan, 1],  # coordinate[3][0]
                    [1, 1, np.nan, 1, 1],  # coordinate[3][1]
                    [1, 1, np.nan, 1, 1],  # coordinate[3][2] ※coordinate[3][3]はゴールだから方策なし
                    ])

goal_state = 15       #ゴールの状態s

def simple_convert_into_pi_from_theta(theta):
    '''単純に割合を計算する'''

    [m, n] = theta.shape  # thetaの行列サイズを取得
    pi = np.zeros((m, n))
    for i in range(0, m):
        pi[i, :] = theta[i, :] / np.nansum(theta[i, :])  # 割合の計算

    pi = np.nan_to_num(pi)  # nanを0に変換

    return pi

# ランダム行動方策pi_0を求める
pi_0 = simple_convert_into_pi_from_theta(theta_0)

# ε-greedy法を実装


def get_action(s, Q, epsilon, pi_0):
    direction = ["up", "right", "down", "left", "stop"]

    while True:
        r = np.random.rand()

        # 行動を決める
        if r < epsilon:
            # εの確率でランダムに動く
            next_direction = np.random.choice(direction, p=pi_0[s, :])

        else:
            # Qの最大値の行動を採用する
            next_direction = direction[np.nanargmax(Q[s, :])]
        

        # 行動をindexに
        if next_direction == "up":
            action = 0
        elif next_direction == "right":
            action = 1
        elif next_direction == "down":
            action = 2
        elif next_direction == "left":
            action = 3
        else:
            action = 4

        if next_direction == "up" and (s-4) != 9 and action >= 0 and action <= 4:
            print("完了")
            break
        elif next_direction == "right" and (s+1) != 9 and action >= 0 and action <= 4:
            print("完了")
            break
        elif next_direction == "down" and (s+4) != 9 and action >= 0 and action <= 4:
            print("完了")
            break
        elif next_direction == "left" and (s-1) != 9 and action >= 0 and action <= 4:
            print("完了")
            break
        elif next_direction == "stop" and action >= 0 and action <= 4:
            print("完了")
            break

    return action       #なんかよくわからんけどここでnp.nanが入ることがあった(action != np.nanを入れてない時)


def get_s_next(s, a, Q, epsilon, pi_0):
    direction = ["up", "right", "down", "left", "stop"]
    next_direction = direction[a]  # 行動aの方向
    print("---------------------")
    print("next_direction: " + str(next_direction))
    print("s: " + str(s))

    # 行動から次の状態を決める
    if next_direction == "up":
        s_next = s - 4  # 上に移動するときは状態の数字が3小さくなる
    elif next_direction == "right":
        s_next = s + 1  # 右に移動するときは状態の数字が1大きくなる
    elif next_direction == "down":
        s_next = s + 4  # 下に移動するときは状態の数字が3大きくなる
    elif next_direction == "left":
        s_next = s - 1  # 左に移動するときは状態の数字が1小さくなる
    else:
        s_next = s

    print("s_next: " + str(s_next))
    print("---------------------")

    return s_next

def Q_learning(s, a, r, s_next, Q, eta, gamma):

    global goal_state

    if s_next == goal_state:  # ゴールした場合
        Q[s, a] = Q[s, a] + eta * (r - Q[s, a])

    else:
        Q[s, a] = Q[s, a] + eta * (r + gamma * np.nanmax(Q[s_next,: ]) - Q[s, a])

    return Q

# Q学習で迷路を解く関数の定義、状態と行動の履歴および更新したQを出力


def human_Q(Q, epsilon, eta, gamma, pi):

    global goal_state

    s = 0  # スタート地点
    a = a_next = get_action(s, Q, epsilon, pi)  # 初期の行動        #エラーの原因(np.nanが入ることがある)
    s_a_history = [[0, np.nan]]  # エージェントの移動を記録するリスト

    while True:  # ゴールするまでループ
        a = a_next  # 行動更新

        s_a_history[-1][1] = a
        # 現在の状態（つまり一番最後なのでindex=-1）に行動を代入
        #print("s_a_history: " + str(s_a_history))

        s_next = get_s_next(s, a, Q, epsilon, pi)
        # 次の状態を格納

        s_a_history.append([s_next, np.nan])
        # 次の状態を代入。行動はまだ分からないのでnanにしておく

        # 報酬を与え,　次の行動を求めます
        if s_next == goal_state:
            r = 100  # ゴールにたどり着いたなら報酬を与える
            a_next = np.nan
        else:
            r = 0
            a_next = get_action(s_next, Q, epsilon, pi)
            # 次の行動a_nextを求めます。

        # 価値関数を更新
        Q = Q_learning(s, a, r, s_next, Q, eta, gamma)

        # 終了判定
        if s_next == goal_state:  # ゴール地点なら終了
            break
        else:
            s = s_next

    #print("s_next: " + str(s_next))
    #print("s_a_history: " + str(s_a_history))

    return [s_a_history, Q]

# 未実装
'''
def demon_Q(Q, epsilon, eta, gamma, pi):


    s = 6  # スタート地点
    a = a_next = get_action(s, Q, epsilon, pi)  # 初期の行動
    s_a_history = [[0, np.nan]]  # エージェントの移動を記録するリスト

    while True:  # ゴールするまでループ
        a = a_next  # 行動更新

        s_a_history[-1][1] = a
        # 現在の状態（つまり一番最後なのでindex=-1）に行動を代入

        s_next = get_s_next(s, a, Q, epsilon, pi)
        # 次の状態を格納

        s_a_history.append([s_next, np.nan])
        # 次の状態を代入。行動はまだ分からないのでnanにしておく

        # 報酬を与え,　次の行動を求めます
        if s_next == goal_state:
            r = 100  # ゴールにたどり着いたなら報酬を与える
            a_next = np.nan
        else:
            r = 0
            a_next = get_action(s_next, Q, epsilon, pi)
            # 次の行動a_nextを求めます。

        # 価値関数を更新
        Q = Q_learning(s, a, r, s_next, Q, eta, gamma)

        # 終了判定
        if s_next == 15:  # ゴール地点なら終了
            break
        else:
            s = s_next

    return [s_a_history, Q]
'''

def Q_learning_exe(Q, agent):
    global pi_0

    # Q学習で迷路を解く

    eta = 0.1  # 学習率
    gamma = 0.9  # 時間割引率
    epsilon = 0.5  # ε-greedy法の初期値
    v = np.nanmax(Q, axis=1)  # 状態ごとに価値の最大値を求める
    is_continue = True
    episode = 1

    V = []  # エピソードごとの状態価値を格納する
    V.append(np.nanmax(Q, axis=1))  # 状態ごとに行動価値の最大値を求める

    os.makedirs("./result", exist_ok=True)

    while is_continue:  # is_continueがFalseになるまで繰り返す
        print("エピソード:" + str(episode))

        # ε-greedyの値を少しずつ小さくする
        epsilon = epsilon / 2

        # Q学習で迷路を解き、移動した履歴と更新したQを求める
        if agent == "demon":
            [s_a_history, Q] = human_Q(Q, epsilon, eta, gamma, pi_0)
        else:
            [s_a_history, Q] = demon_Q(Q, epsilon, eta, gamma, pi_0)
        #print("[s_a_history, Q]: " + str([s_a_history, Q]))

        # 状態価値の変化
        new_v = np.nanmax(Q, axis=1)  # 状態ごとに行動価値の最大値を求める
        #print(np.sum(np.abs(new_v - v)))  # 状態価値関数の変化を出力
        #print("new_v: " + str(new_v))
        #print("v: " + str(v))
        #print("np.abs(new.v-v): " + str(np.abs(new_v-v)))
        #print("np.sum(np.abs(new_v - v)): " + str(np.sum(np.abs(new_v - v))))
        v = new_v
        V.append(v)  # このエピソード終了時の状態価値関数を追加

        print("迷路を解くのにかかったステップ数は" + str(len(s_a_history) - 1) + "です")


        # 100エピソード繰り返す
        episode += 1
        if episode > 100:
            break

    with open("./result/state_value.txt", mode='w') as f:
        f.write(str(V))
        
    return Q

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

def coordinate_to_state_change(now_coordinate, corrdinate):
    s = 0

    for i in range(4):
        for j in range(4):
            if now_coordinate == coordinate[i][j]:
                return s
            s += 1

def state_to_coordinate_change(s, corrdinate):
    cnt = 0

    for i in range(4):
        for j in range(4):
            if s == cnt:
                return coordinate[i][j]
            cnt += 1

def human_AI(Q, s):
    direction = ["up", "right", "down", "left", "stop"]

    next_direction = direction[np.nanargmax(Q[s, :])]
    print("next_direction: " + str(next_direction))

    # 行動から次の状態を決める
    if next_direction == "up":
        s_next = s - 4  # 上に移動するときは状態の数字が3小さくなる
    elif next_direction == "right":
        s_next = s + 1  # 右に移動するときは状態の数字が1大きくなる
    elif next_direction == "down":
        s_next = s + 4  # 下に移動するときは状態の数字が3大きくなる
    elif next_direction == "left":
        s_next = s - 1  # 左に移動するときは状態の数字が1小さくなる
    else:
        s_next = s

    return s_next

def demon_AI(Q, s):
    print("s: " + str(s))
    #next_direction = direction[np.nanargmax(Q[s, :])]
    print("Q_value: " + str(Q_value))


if __name__ == "__main__":

    pygame.init()               #　初期化
    screen = pygame.display.set_mode(SCREEN_SIZE) # スクリーンの初期化
    pygame.display.set_caption("鬼ごっこAI") # スクリーンのタイトルの設定

    ### エージェント等の設定 ###
    human_agent = pygame.image.load("./image/人.png")                                           # 人の画像を指定
    demon_agent = pygame.image.load("./image/鬼.png")                                           # 鬼の画像を指定
    goal = pygame.image.load("./image/ゴール.png")                                              # ゴールの画像を指定
    demon_agent = pygame.transform.smoothscale(demon_agent, (RECT_SIZE, RECT_SIZE))
    human_agent = pygame.transform.smoothscale(human_agent, (RECT_SIZE, RECT_SIZE))
    goal = pygame.transform.smoothscale(goal, (RECT_SIZE, RECT_SIZE))
    ### end ###

    coordinate = field_coordinate_set()    # 各マスの左上の座標を生成
    #state_value = coordinate_change(coordinate)

    ### 各要素の座標を選択 ###
    HUMAN_AGENT_POSITION = coordinate[0][0]                     # 人の座標を指定(移動可能)
    DEMON_AGENT_POSITION = coordinate[1][1]                     # 鬼の座標を指定(移動可能)
    OBSTACLE_POSITION_1 = (coordinate[2][1][0], coordinate[2][1][1], RECT_SIZE, RECT_SIZE)    # 障害物の座標を指定(固定)
    OBSTACLE_POSITION_2 = coordinate[2][1]
    GOAL_POSITION = coordinate[3][3]                            # ゴールの座標を指定(固定)
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
            enemy = DEMON_AGENT_POSITION
            #operation_position = HUMAN_AGENT_POSITION
            break
        else:
            print("ちゃんと選べよおお")
    

    # 初期の行動価値関数Qを設定

    [a, b] = theta_0.shape  # 行と列の数をa, bに格納
    Q = np.random.rand(a, b) * theta_0 * 0.1
    # *theta0をすることで要素ごとに掛け算をし、Qの壁方向の値がnanになる

    q_value = Q_learning_exe(Q, agent)
    print("q_value: " + str(q_value))

    
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
                    state = coordinate_to_state_change(DEMON_AGENT_POSITION, coordinate)
                    print("now_state: " + str(state))
                    enemy = demon_AI(q_value, state)      #ここで敵の行動を選出
                    enemy = state_to_coordinate_change(enemy, coordinate)

                    HUMAN_AGENT_POSITION = ally         #実際にはここで代入することで動かせるよ
                    DEMON_AGENT_POSITION = enemy        #実際にはここで代入することで動かせるよ
                else:
                    state = coordinate_to_state_change(HUMAN_AGENT_POSITION, coordinate)
                    print("now_state: " + str(state))
                    enemy = human_AI(q_value, state)      #ここで敵の行動を選出
                    enemy = state_to_coordinate_change(enemy, coordinate)
                    print("enemy: " + str(enemy))

                    DEMON_AGENT_POSITION = ally         #実際にはここで代入することで動かせるよ
                    HUMAN_AGENT_POSITION = enemy        #実際にはここで代入することで動かせるよ


                if agent == "human" and HUMAN_AGENT_POSITION == GOAL_POSITION:                   # ゴールについた時
                    print("goal!!")
                    print("人の勝ち！！")
                    if event.key == K_KP_ENTER:     #なんかここ処理できてなくね
                        pygame.quit()
                        sys.exit()
                if HUMAN_AGENT_POSITION == DEMON_AGENT_POSITION:
                    print("鬼の勝ち！！")
                    if event.key == K_KP_ENTER:     #なんかここ処理できてなくね
                        pygame.quit()
                        sys.exit()
# -*- coding: utf-8 -*-
import codecs
import os
import random
import tools
from config import (DOWN, LEFT, RIGHT, UP)
from config import GS

STOP, MOVE = 0, 1  # 移動タイプ
PROB_MOVE = 0.005  # 移動確率


def load_charachips(dir, file):
    file = os.path.join(dir, file)
    fp = open(file, 'r')
    for line in fp:
        line = line.rstrip()
        data = line.split(',')
        # chara_id = int(data[0])
        chara_name = data[1]
        Character._images[chara_name] = \
            tools.split_image(tools.load_image('charachip', '%s.png' % chara_name))  # noqa
    fp.close()


def load_chara_status():
    return tools.load_parameter(os.path.join('data', 'initial_chara_status.dat'))


class Character(object):
    """一般キャラクタークラス"""
    speed = 4  # 1フレームの移動ピクセル数
    animcycle = 24  # アニメーション速度
    frame = 0
    # キャラクターイメージ（mainで初期化）
    # キャラクター名 -> 分割画像リストの辞書
    _images = {}
    _statuses = {}

    def __init__(self, name, pos, dir, movetype, message):
        self.name = name  # キャラクター名（ファイル名と同じ）
        self.image = self._images[name][0]  # 描画中のイメージ
        self.status = self._statuses.get(name)
        print('Character : name = {}, status = {}'.format(name, self.status))
        self.x, self.y = pos[0], pos[1]  # 座標（単位：マス）
        self.rect = self.image.get_rect(topleft=(self.x * GS, self.y * GS))
        self.vx, self.vy = 0, 0  # 移動速度
        self.moving = False  # 移動中か？
        self.direction = dir  # 向き
        self.movetype = movetype  # 移動タイプ
        self.message = message  # メッセージ

    def update(self, map):
        """キャラクター状態を更新する。
        mapは移動可能かの判定に必要。"""
        # プレイヤーの移動処理
        if self.moving:
            # ピクセル移動中ならマスにきっちり収まるまで移動を続ける
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left % GS == 0 and self.rect.top % GS == 0:  # マスにおさまったら移動完了  # noqa
                self.moving = False
                self.x = int(self.rect.left / GS)
                self.y = int(self.rect.top / GS)
        elif self.movetype == MOVE and random.random() < PROB_MOVE:
            # 移動中でないならPROB_MOVEの確率でランダム移動開始
            self.direction = random.randint(0, 3)  # 0-3のいずれか
            if self.direction == DOWN:
                if map.is_movable(self.x, self.y + 1):
                    self.vx, self.vy = 0, self.speed
                    self.moving = True
            elif self.direction == LEFT:
                if map.is_movable(self.x - 1, self.y):
                    self.vx, self.vy = -self.speed, 0
                    self.moving = True
            elif self.direction == RIGHT:
                if map.is_movable(self.x + 1, self.y):
                    self.vx, self.vy = self.speed, 0
                    self.moving = True
            elif self.direction == UP:
                if map.is_movable(self.x, self.y - 1):
                    self.vx, self.vy = 0, -self.speed
                    self.moving = True
        # キャラクターアニメーション（frameに応じて描画イメージを切り替える）
        self.frame += 1
        self.image = self._images[self.name][self.direction * 4 + int(self.frame / self.animcycle) % 4]  # noqa

    def draw(self, screen, offset):
        """オフセットを考慮してプレイヤーを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px - offsetx, py - offsety))

    def set_pos(self, x, y, dir):
        """キャラクターの位置と向きをセット"""
        self.x, self.y = x, y
        self.rect = self.image.get_rect(topleft=(self.x * GS, self.y * GS))
        self.direction = dir

    def __str__(self):
        return "CHARA,%s,%d,%d,%d,%d,%s" % (self.name,self.x,self.y,self.direction,self.movetype,self.message)  # noqa

# -*- coding: utf-8 -*-
import pygame
from pygame.locals import (
    K_LEFT, K_RIGHT, K_DOWN, K_UP)
from config import (DOWN, LEFT, RIGHT, UP)


class Party(object):
    def __init__(self):
        # Partyのメンバーリスト
        self.member = []
        self.is_visible = False
        self.locked = False

    def add(self, player):
        """Partyにplayerを追加"""
        self.member.append(player)

    def statuses(self):
        statuses = []
        for chara in self.member:
            statuses.append(chara.status)
        return statuses

    def show(self):
        self.is_visible = True

    def hide(self):
        self.is_visible = False

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def update(self, map, battle):
        if not self.is_visible:
            return
        # Party全員を更新
        for player in self.member:
            player.update(map, battle)
        # 移動中でないときにキー入力があったらParty全員を移動開始
        if self.locked:
            # print('ロックされているので移動はしない')
            return
        if not self.member[0].moving:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_DOWN]:
                # 先頭キャラは移動できなくても向きは変える
                self.member[0].direction = DOWN
                # 先頭キャラが移動できれば
                if map.is_movable(self.member[0].x, self.member[0].y + 1):
                    # 後ろにいる仲間から1つ前の仲間の位置へ移動開始
                    for i in range(len(self.member) - 1, 0, -1):
                        self.member[i].move_to(self.member[i - 1].x,self.member[i - 1].y)  # noqa
                    # 先頭キャラを最後に移動開始
                    self.member[0].move_to(self.member[0].x,self.member[0].y + 1)  # noqa
            elif pressed_keys[K_LEFT]:
                self.member[0].direction = LEFT
                if map.is_movable(self.member[0].x - 1, self.member[0].y):
                    for i in range(len(self.member) - 1, 0, -1):
                        self.member[i].move_to(self.member[i - 1].x,self.member[i - 1].y)  # noqa
                    self.member[0].move_to(self.member[0].x - 1,self.member[0].y)  # noqa
            elif pressed_keys[K_RIGHT]:
                self.member[0].direction = RIGHT
                if map.is_movable(self.member[0].x + 1, self.member[0].y):
                    for i in range(len(self.member) - 1, 0, -1):
                        self.member[i].move_to(self.member[i - 1].x,self.member[i - 1].y)  # noqa
                    self.member[0].move_to(self.member[0].x + 1,self.member[0].y)  # noqa
            elif pressed_keys[K_UP]:
                self.member[0].direction = UP
                if map.is_movable(self.member[0].x, self.member[0].y - 1):
                    for i in range(len(self.member) - 1, 0, -1):
                        self.member[i].move_to(self.member[i - 1].x,self.member[i - 1].y)  # noqa
                    self.member[0].move_to(self.member[0].x,self.member[0].y -1)  # noqa

    def draw(self, screen, offset):
        if not self.is_visible:
            return
        # Partyの全員を描画
        # 重なったとき先頭キャラが表示されるように後ろの人から描画
        for player in self.member[::-1]:
            player.draw(screen, offset)

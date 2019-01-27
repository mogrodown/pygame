# -*- coding: utf-8 -*-

import codecs
import os
import struct

import database
import pygame
import tools
from character import Character
from config import (GS, SCR_RECT)
from rpgobject import Door, RpgObject, Treasure, Portal
import sounds
from rpg_keyword import ACT_CMD_WINDOW, ACT_NONE

TRANS_COLOR = (190, 179, 145)  # マップチップの透明色


def load_mapchips(dir, file):
    file = os.path.join(dir, file)
    fp = open(file, 'r')
    for line in fp:
        line = line.rstrip()
        data = line.split(',')
        # mapchip_id = int(data[0])
        mapchip_name = data[1]
        movable = int(data[2])
        transparent = int(data[3])
        if transparent == 0:
            RpgMap.images.append(tools.load_image('mapchip', '%s.png' % mapchip_name))  # noqa
        else:
            RpgMap.images.append(tools.load_image('mapchip', '%s.png' % mapchip_name, TRANS_COLOR))  # noqa
        RpgMap.movable_type.append(movable)
    fp.close()


class RpgMap(object):
    images = []
    movable_type = []

    def __init__(self, name, party):
        self.name = name
        self.row = -1
        self.col = -1
        self.map = []
        self.charas = []
        self.events = []
        self.party = party
        self.load()
        self.load_event()

    def create(self, dest_map):
        self.name = dest_map
        self.charas = []
        self.events = []
        self.load()
        self.load_event()

    def add_chara(self, chara):
        self.charas.append(chara)

    def update(self):
        for chara in self.charas:
            chara.update(self)

    def key_handler(self, event):
        if tools.is_key_cancel(event):
            print('z pressed')
            return ACT_CMD_WINDOW
        return ACT_NONE

    def key_action(self, player):
        sounds.play('pi')
        # player = self.party.member[0]
        chara = player.touch_person(self)
        if chara:
            return database.ACT_TALK_CHARA, chara.message
        else:
            door = player.touch_door(self)
            if door:
                door.open()
                self.remove_event(door)
                return False, None
            else:
                treasure = player.touch_object(self)
                if treasure:
                    treasure.open()
                    self.remove_event(treasure)
                    return database.ACT_GET_TREASURE, treasure.item
        return False, None

    def key_cancel(self):
        sounds.play('pi')
        return False

    def draw(self, screen, offset):
        offsetx, offsety = offset

        startx = int(offsetx / GS)
        endx = startx + int(SCR_RECT.width / GS) + 1
        starty = int(offsety / GS)
        endy = starty + int(SCR_RECT.height / GS) + 1

        for y in range(starty, endy):
            for x in range(startx, endx):
                if x < 0 or y < 0 or x > self.col - 1 or y > self.row - 1:
                    screen.blit(self.images[self.default],
                                (x * GS - offsetx, y * GS - offsety))
                else:
                    screen.blit(self.images[self.map[y][x]],
                                (x * GS - offsetx, y * GS - offsety))

        for event in self.events:
            event.draw(screen, offset)

        for chara in self.charas:
            chara.draw(screen, offset)

    def is_movable(self, x, y):
        if x < 0 or x > self.col - 1 or y < 0 or y > self.row - 1:
            return False

        if self.movable_type[self.map[y][x]] == 0:
            return False

        for chara in self.charas:
            if chara.x == x and chara.y == y:
                return False

        # イベントが発生する座標には移動させない(見た目上)
        for event in self.events:
            if self.movable_type[event.mapchip] == 0:
                if event.x == x and event.y == y:
                    return False

        player = self.party.member[0]
        if player.x == x and player.y == y:
            return False

        return True

    def get_chara(self, x, y):
        for chara in self.charas:
            if chara.x == x and chara.y == y:
                return chara
        return None

    def get_event(self, x, y):
        for event in self.events:
            if event.x == x and event.y == y:
                return event
        return None

    def remove_event(self, event):
        self.events.remove(event)

    def load(self):
        file = os.path.join("data", self.name + ".map")
        fp = open(file, "rb")

        self.row = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
        self.col = struct.unpack("i", fp.read(struct.calcsize("i")))[0]
        self.default = struct.unpack("B", fp.read(struct.calcsize("B")))[0]
        self.map = [[0 for c in range(self.col)] for r in range(self.row)]
        for r in range(self.row):
            for c in range(self.col):
                self.map[r][c] = \
                    struct.unpack("B", fp.read(struct.calcsize("B")))[0]
        fp.close()

    def load_event(self):
        """ファイルからイベントをロード"""
        file = os.path.join("data", self.name + ".evt")
        # テキスト形式のイベントを読み込む
        fp = codecs.open(file, "r", "utf-8")
        for line in fp:
            line = line.rstrip()  # 改行除去
            if line.startswith("#"):
                continue  # コメント行は無視
            if line == "":
                continue  # 空行は無視
            data = line.split(",")
            event_type = data[0]
            if event_type == "BGM":  # BGMイベント
                self.play_bgm(data)
            elif event_type == "CHARA":  # キャラクターイベント
                self.create_chara(data)
            elif event_type == "MOVE":  # 移動イベント
                self.create_move(data)
            elif event_type == "TREASURE":  # 宝箱
                self.create_treasure(data)
            elif event_type == "DOOR":  # とびら
                self.create_door(data)
            elif event_type == "OBJECT":  # 一般オブジェクト（玉座など）
                self.create_obj(data)
        fp.close()

    def play_bgm(self, data=None):
        """BGMを鳴らす"""
        if not data:
            sounds.play_bgm(None)
        else:
            sounds.play_bgm("%s.mp3" % data[1])

    def create_chara(self, data):
        name = data[1]
        x, y = int(data[2]), int(data[3])
        direction = int(data[4])
        movetype = int(data[5])
        message = data[6]
        chara = Character(name, (x, y), direction, movetype, message)
        self.charas.append(chara)

    def create_move(self, data):
        x, y = int(data[1]), int(data[2])
        mapchip = int(data[3])
        dest_map = data[4]
        dest_x, dest_y = int(data[5]), int(data[6])
        move = Portal((x, y), mapchip, RpgMap.images[mapchip], dest_map, (dest_x, dest_y))
        self.events.append(move)

    def create_treasure(self, data):
        """宝箱を作成してeventsに追加する"""
        x, y = int(data[1]), int(data[2])
        item = data[3]
        treasure = Treasure((x, y), item, 46, RpgMap.images[46])
        self.events.append(treasure)

    def create_door(self, data):
        """とびらを作成してeventsに追加する"""
        x, y = int(data[1]), int(data[2])
        door = Door((x, y), 45, RpgMap.images[45])
        self.events.append(door)

    def create_obj(self, data):
        """一般オブジェクトを作成してeventsに追加する"""
        x, y = int(data[1]), int(data[2])
        mapchip = int(data[3])
        obj = RpgObject((x, y), mapchip, RpgMap.images[mapchip])
        self.events.append(obj)

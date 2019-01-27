# -*- coding: utf-8 -*-

from config import GS
import sounds


import database


class Treasure(object):
    """宝箱"""
    def __init__(self, pos, item, mapchip, image):
        self.x, self.y = pos[0], pos[1]  # 宝箱座標
        self.mapchip = mapchip
        # self.image = RpgMap.images[self.mapchip]
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x * GS, self.y * GS))
        self.item = item  # アイテム名

    def open(self):
        """宝箱をあける"""
        sounds.play("treasure")
        # TODO: アイテムを追加する処理

    def draw(self, screen, offset):
        """オフセットを考慮してイベントを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px - offsetx, py - offsety))

    def __str__(self):
        return "TREASURE,%d,%d,%s" % (self.x, self.y, self.item)


class Door:
    """とびら"""
    def __init__(self, pos, mapchip, image):
        self.x, self.y = pos[0], pos[1]
        self.mapchip = mapchip
        # self.image = RpgMap.images[self.mapchip]
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x * GS, self.y * GS))

    def open(self):
        """とびらをあける"""
        sounds.play("door")

    def draw(self, screen, offset):
        """オフセットを考慮してイベントを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px - offsetx, py - offsety))

    def __str__(self):
        return "DOOR,%d,%d" % (self.x, self.y)


class RpgObject:
    """一般オブジェクト"""
    def __init__(self, pos, mapchip, image):
        self.x, self.y = pos[0], pos[1]
        self.mapchip = mapchip
        # self.image = RpgMap.images[self.mapchip]
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x * GS, self.y * GS))

    def draw(self, screen, offset):
        """オフセットを考慮してイベントを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px - offsetx, py - offsety))

    def __str__(self):
        return "OBJECT,%d,%d" % (self.x, self.y)


class Portal(object):
    """移動イベント"""
    def __init__(self, pos, mapchip, image, dest_map, dest_pos):
        self.x, self.y = pos[0], pos[1]  # イベント座標
        self.mapchip = mapchip  # マップチップ
        self.dest_map = dest_map  # 移動先マップ名
        self.dest_x, self.dest_y = dest_pos[0], dest_pos[1]  # 移動先座標
        # self.image = RpgMap.images[self.mapchip]
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x * GS, self.y * GS))

    def draw(self, screen, offset):
        """オフセットを考慮してイベントを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px - offsetx, py - offsety))

    def __str__(self):
        return "MOVE,%d,%d,%d,%s,%d,%d" % (self.x, self.y, self.mapchip, self.dest_map, self.dest_x, self.dest_y)  # noqa

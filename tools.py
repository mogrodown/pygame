# -*- coding: utf-8 -*-

import codecs
import os
import pygame
import yaml
from pygame.locals import RLEACCEL
from config import GS, FONT_WIDTH, FONT_HEIGHT
from pygame.locals import (
    KEYDOWN, K_ESCAPE, K_DOWN, K_UP, KEYUP, K_z, K_x)


def load_image(dir, file, colorkey=None):
    """

    :rtype:
    """
    file = os.path.join(dir, file)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        print('load file error : %s' % file)
        raise SystemExit()
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def split_image(image):
    imageList = []
    for i in range(0, 128, GS):
        for j in range(0, 128, GS):
            surface = pygame.Surface((GS, GS))
            surface.blit(image, (0, 0), (j, i, GS, GS))
            surface.set_colorkey(surface.get_at((0, 0)), RLEACCEL)
            surface.convert()
            imageList.append(surface)
    return imageList


def is_key_action(event):
    return event.type == KEYDOWN and event.key == K_z


def is_key_cancel(event):
    return event.type == KEYDOWN and event.key == K_x


def is_key_upward(event):
    return event.type == KEYUP and event.key == K_UP


def is_key_downward(event):
    return event.type == KEYDOWN and event.key == K_DOWN


def is_key_quit(event):
    return event.type == KEYDOWN and event.key == K_ESCAPE


def calculate_rect(str_count, row_count, column_count):
    LINE_HEIGHT = 8  # 行間の大きさ

    fw = FONT_WIDTH
    fh = FONT_HEIGHT

    one_width = (str_count * fw + fw)  # ▼ + 文字
    w = one_width * row_count
    w += (row_count - 1) * fw
    w += fw * 2
    w += 4 * 2
    h = column_count * (fh + LINE_HEIGHT)
    h += fh * 2
    h += 4 * 2

    print('width = %d, height = %d' % (w, h))


def load_parameter(filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        data = yaml.load(f)
    return data


def save_parameer(filename, data):
    with codecs.open(filename, 'w', 'utf-8') as f:
        yaml.dump(data, f, encoding='utf-8', default_flow_style=False )


if __name__ == '__main__':
    # TOPメニュー
    calculate_rect(6, 1, 6)

    # GAMEINFO
    calculate_rect(12, 1, 3)

    # 終了問い合わせ
    calculate_rect(15, 1, 3)

    # ITEM
    calculate_rect(10, 1, 5)

    # ステータス
    calculate_rect(12, 1, 4)

    # data = {'mano': 99, 'address': 'toyota-city'}
    # data = [{'mano': 99, 'address': 'toyota-city'}, {'takashi': 102, 'address': 'okinawa'}]
    # data = [{'name': '主人公', 'chip_name': 'swordman_female', 'hp': 16, 'mp': 0, 'lavel': 1}]
    # save_parameer('tmp.dat', data)

    # 主人公,swordman_female,16,0,1

    load_parameter('tmp.dat')

# -*- coding: utf-8 -*-
import os

import pygame

sounds = {}  # サウンド
bgm_file = None


def load(dir, file):
    file = os.path.join(dir, file)
    fp = open(file, 'r')
    for line in fp:
        line = line.rstrip()
        data = line.split(',')
        se_name = data[0]
        se_file = os.path.join('se', data[1])
        sounds[se_name] = pygame.mixer.Sound(se_file)
        sounds[se_name].set_volume(0.0)  # TODO  0.1
    fp.close()


def play(name):
    sounds[name].play()


def play_bgm(filename):
    global bgm_file
    vol = 0.0  # TODO 0.1
    if not filename:
        pygame.mixer.music.load(bgm_file)
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(-1)
    else:
        bgm_file = os.path.join("bgm", filename)
        pygame.mixer.music.load(bgm_file)
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(-1)
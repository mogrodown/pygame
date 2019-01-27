# -*- coding: utf-8 -*-
import codecs
import os

import database
import pygame
import tools
from pygame.locals import Rect

from rpg_keyword import ACT_MEDICINAL_PLANTS




class Window(object):
    """ウィンドウの基本クラス"""
    EDGE_WIDTH = 4  # 白枠の幅

    def __init__(self, rect):
        self.rect = rect  # 一番外側の白い矩形
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH * 2, -self.EDGE_WIDTH * 2)  # noqa 内側の黒い矩形
        self._is_visible = False  # ウィンドウを表示中か？

    def draw(self, screen):
        """ウィンドウを描画"""
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.inner_rect, 0)

    def show(self):
        self._is_visible = True

    def hide(self):
        self._is_visible = False


class QueryWindow(Window):
    LINE_HEIGHT = 8  # 行間の大きさ
    def __init__(self, query_action, msg, x, y, msg_engine):
        Window.__init__(self, Rect(x, y, 400, 120))
        self.text_rect = self.inner_rect.inflate(-32, -32)
        self._msg_engine = msg_engine
        self._query_text = msg
        self.cursol_pos = 0
        self.cursor = tools.load_image("data", "cursor2.png", -1)
        self.query_action = query_action

    def draw(self, screen):
        fw = MessageEngine.FONT_WIDTH
        fh = MessageEngine.FONT_HEIGHT

        Window.draw(self, screen)

        self._msg_engine.draw_string(screen, (self.text_rect[0], self.text_rect[1]), self._query_text)

        query = [database.menu_items[database.ACT_YES][0], database.menu_items[database.ACT_NO][0]]
        for index, data in enumerate(query):
            dx = self.text_rect[0] + MessageEngine.FONT_WIDTH
            dy = self.text_rect[1] + (self.LINE_HEIGHT + fh) * (index + 1)
            self._msg_engine.draw_string(screen, (dx, dy), data)

        # 選択中のコマンドの左側に▶を描画
        dx = self.text_rect[0]
        dy = self.text_rect[1] + (self.LINE_HEIGHT + fh) * (self.cursol_pos + 1)
        screen.blit(self.cursor, (dx, dy))

    def key_handler(self, event):
        if tools.is_key_quit(event):
            return database.ACT_BACK

        if tools.is_key_upward(event):
            if self.cursol_pos == 0 or self.cursol_pos == 2:
                return
            self.cursol_pos -= 1
        elif tools.is_key_downward(event):
            if self.cursol_pos == 2 - 1:
                self.cursol_pos = 0
            else:
                self.cursol_pos += 1

    def key_action(self):
        if self.cursol_pos == 0:
            return self.query_action
        else:
            return database.ACT_NONE




class BattleCommandWindow(Window):
    LINE_HEIGHT = 8
    ATTACK, SPELL, ITEM, ESCAPE = range(4)
    COMMAND = [u'たたかう', u'じゅもん', u'どうぐ', u'にげる']

    def __init__(self, rect, msg_engine):
        Window.__init__(self, rect)
        self.text_rect = self.inner_rect.inflate(-32, -16)
        self.command = self.ATTACK
        self.msg_engine = msg_engine
        self.cursor = tools.load_image('data', 'cursor2.png', -1)
        self.frame = 0

    def draw(self, screen):
        Window.draw(self, screen)
        for i in range(0, 4):
            dx = self.text_rect[0] + MessageEngine.FONT_WIDTH
            dy = self.text_rect[1] + (self.LINE_HEIGHT + MessageEngine.FONT_HEIGHT) * (i % 4)  # noqa
            self.msg_engine.draw_string(screen, (dx, dy), self.COMMAND[i])

        dx = self.text_rect[0]
        dy = self.text_rect[1] + (self.LINE_HEIGHT + MessageEngine.FONT_HEIGHT) * (self.command % 4)  # noqa
        screen.blit(self.cursor, (dx, dy))

    def show(self):
        self.command = self.ATTACK


class BattleStatusWindow(Window):
    LINE_HEIGHT = 8

    def __init__(self, rect, status, msg_engine):
        Window.__init__(self, rect)
        self.text_rect = self.inner_rect.inflate(-32, -16)
        self.status = status  # status = ["なまえ", HP, MP, LV]
        self.msg_engine = msg_engine
        self.frame = 0

    def draw(self, screen):
        Window.draw(self, screen)
        if not self.is_visible:
            return
        # ステータスを描画
        status_str = [self.status[0], u"H%3d" % self.status[1], u"M%3d" % self.status[2],  # noqa
                      u"%s%3d" % (self.status[0][0], self.status[3])]  # noqa
        for i in range(0, 4):
            dx = self.text_rect[0]
            dy = self.text_rect[1] + (self.LINE_HEIGHT + MessageEngine.FONT_HEIGHT) * (i % 4)  # noqa
            self.msg_engine.draw_string(screen, (dx, dy), status_str[i])

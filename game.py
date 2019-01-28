# -*- coding: utf-8 -*-

import character
import database
import menu
import pygame
import rpgmap
import title
import tools
import sounds
import sys
from config import SCR_RECT, DOWN
from message import MessageEngine, MessageWindow, MESSAGE_FORM
from party import Party
from player import Player
from popup import PopupManager
from pygame.locals import (
    Rect, QUIT, DOUBLEBUF, HWSURFACE)
import savedata
from window import build_infomations


def main():
    my_rpg = MyRPG()

    clock = pygame.time.Clock()
    while(True):
        clock.tick(60)
        my_rpg.update()
        my_rpg.render()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                my_rpg.quit_game()
            if tools.is_key_action(event):
                my_rpg.key_action()
            elif tools.is_key_cancel(event):
                my_rpg.key_cancel()
                pass
            else:
                my_rpg.key_handler(event)


class MyRPG(object):
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode(
            SCR_RECT.size, DOUBLEBUF | HWSURFACE)  # | FULLSCREEN)
        sounds.load('data', 'sound.dat')
        character.load_charachips('data', 'charachip.dat')
        chara_status = character.load_chara_status()
        rpgmap.load_mapchips('data', 'mapchip.dat')

        # Windows関連
        self._msg_engine = MessageEngine()
        self._msgwnd = MessageWindow(MESSAGE_FORM, self._msg_engine)
        menu.build_menus(self._msg_engine)
        build_infomations(self._msg_engine)
        self._popup = PopupManager()

        # キャラ関連
        status = [status for status in chara_status if status['name'] == 'しゅじんこう']
        self._party = Party()
        self._party.add(Player(status[0], (3, 5), DOWN, True, self._msgwnd))
        self._player = self._party.member[0]
        self._player.add_member(self._party.member)

        # マップ
        self._map = rpgmap.RpgMap('field', self._party)

        # タイトル
        self._title = title.Title(self._msg_engine)
        self._selected_action = None
        self._title.show()
        self._win = self._title

    def update(self):
        self._win.update()
        self._party.update(self._map, 'dumy')
        self._popup.update()

    def render(self):
        offset = self.calc_offset(self._party.member[0])
        self._win.draw(self._screen, offset)
        offset = self.calc_offset(self._player)
        self._party.draw(self._screen, offset)
        self._popup.draw(self._screen)

    def key_handler(self, event):
        if not self._popup.key_handler(event):
            return self._win.key_handler(event)

    def key_action(self):
        if not self._popup.is_empty():
            ret = self._popup.key_action()
            try:
                print('popup key_action = {}'.format(database.menu_items[ret]))
            except KeyError:
                print('とりあえずなにもしない')

            if ret == database.ACT_QUIT:
                self._popup.push(menu.all_menus[menu.QUITMENU])
            elif ret == database.ACT_GAME_QUIT:
                self.quit_game()
            elif ret == database.ACT_CLOSE:
                self._popup.pop()
                if self._popup.is_empty():
                    self._party.unlock()
            elif ret == database.ACT_ITEM:
                print('どうぐめにゅーGo')
                self._popup.push(menu.MenuWindow(
                    menu.ITEMMENU_FORM,
                    [database.ACT_MEDICAL_PLANTS, database.ACT_TNT],
                    msg_engine=self._msg_engine))
            elif ret == database.ACT_STATUS:
                status = self._party.member[0].get_status()
                print('ST = {}'.format(status))
                self._popup.push(menu.InfoWindow(
                    menu.STATEINFO_FORM,
                    [u'なまえ　' + status['name'], u'HP:27', u'MP:00', u'LEVEL:01'],
                    msg_engine=self._msg_engine))

            return  # TODO 大事

        action, param = self._win.key_action(self._party.member[0])
        if action == database.ACT_GAME_START:
            # TITLE => GAME
            self._win.hide()
            self._win = self._map
            self._party.show()
            self._party.unlock()
        elif action == database.ACT_TALK_CHARA:
            self._party.lock()
            self._msgwnd.set(param)
            # self._popup_stack.append(self._msgwnd)
            self._popup.push(self._msgwnd)
        elif action == database.ACT_GET_TREASURE:
            self._party.lock()
            self._msgwnd.set(u'%s　をてにいれた。' % param)
            # self._popup_stack.append(self._msgwnd)
            self._popup.push(self._msgwnd)

    def key_cancel(self):
        # self._popup.push(menu.gameinfo)
        if self._popup.is_empty():
            self._party.lock()
            self._popup.push(menu.all_menus[menu.TOPMENU])
        else:
            self._popup.pop()
            if self._popup.is_empty():
                self._party.unlock()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def calc_offset(self, player):
        offsetx = player.rect.topleft[0] - int(SCR_RECT.width / 2)
        offsety = player.rect.topleft[1] - int(SCR_RECT.height / 2)
        return offsetx, offsety

if __name__ == '__main__':
    main()

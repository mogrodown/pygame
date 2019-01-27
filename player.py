# -*- coding: utf-8 -*-
from config import (DOWN, LEFT, RIGHT, UP)
from rpgobject import RpgObject, Treasure, Door, Portal
from config import GS
import sounds
from character import Character

PROB_ENCOUNT = 0.05  # エンカウント確率


class Player(Character):
    def __init__(self, status, pos, dir, leader, msgwnd):
        Character.__init__(self, status['chip_name'], pos, dir, False, None)
        self.leader = leader
        self.is_visible = False
        self.status = status

    def get_status(self):
        return self.status

    def add_member(self, member):
        self.member = member

    def update(self, map, battle):
        """プレイヤー状態を更新する。
        mapは移動可能かの判定に必要。"""
        # プレイヤーの移動処理
        if self.moving:
            # ピクセル移動中ならマスにきっちり収まるまで移動を続ける
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left % GS == 0 and self.rect.top % GS == 0:  # noqa マスにおさまったら移動完了
                self.moving = False
                self.x = int(self.rect.left / GS)
                self.y = int(self.rect.top / GS)
                # TODO: ここに接触イベントのチェックを入れる
                if not self.leader:
                    return  # リーダーでなければイベントは無視
                event = map.get_event(self.x, self.y)
                if isinstance(event, Portal):  # MoveEventなら
                    sounds.play("step")
                    dest_map = event.dest_map
                    dest_x = event.dest_x
                    dest_y = event.dest_y
                    map.create(dest_map)
                    # パーティの全員を移動先マップへ
                    # for player in self.party.member:
                    for player in self.member:
                        player.set_pos(dest_x, dest_y, DOWN)  # プレイヤーを移動先座標へ
                        player.moving = False
                """
                if map.name == 'field' and random.random() < PROB_ENCOUNT:
                    rpgstate.game_state = rpgstate.BATTLE_INIT
                    battle.start()
                """
        # キャラクターアニメーション（frameに応じて描画イメージを切り替える）
        self.frame += 1
        self.image = self._images[self.name][self.direction * 4 + int(self.frame / self.animcycle) % 4]  # noqa

    def move_to(self, destx, desty):
        """現在位置から(destx,desty)への移動を開始"""
        dx = destx - self.x
        dy = desty - self.y
        # 向きを変える
        if dx == 1:
            self.direction = RIGHT
        elif dx == -1:
            self.direction = LEFT
        elif dy == -1:
            self.direction = UP
        elif dy == 1:
            self.direction = DOWN
        # 速度をセット
        self.vx, self.vy = dx * self.speed, dy * self.speed
        # 移動開始
        self.moving = True

    def touch_person(self, map):
        """キャラクターが向いている方向のとなりにキャラクターがいるか調べる"""
        # 向いている方向のとなりの座標を求める
        nextx, nexty = self.x, self.y
        if self.direction == DOWN:
            nexty = self.y + 1
            event = map.get_event(nextx, nexty)
            if isinstance(event, RpgObject) and event.mapchip == 41:
                nexty += 1  # テーブルがあったらさらに隣
        elif self.direction == LEFT:
            nextx = self.x - 1
            event = map.get_event(nextx, nexty)
            if isinstance(event, RpgObject) and event.mapchip == 41:
                nextx -= 1
        elif self.direction == RIGHT:
            nextx = self.x + 1
            event = map.get_event(nextx, nexty)
            if isinstance(event, RpgObject) and event.mapchip == 41:
                nextx += 1
        elif self.direction == UP:
            nexty = self.y - 1
            event = map.get_event(nextx, nexty)
            if isinstance(event, RpgObject) and event.mapchip == 41:
                nexty -= 1
        # その方向にキャラクターがいるか？
        chara = map.get_chara(nextx, nexty)
        # キャラクターがいればプレイヤーの方向へ向ける
        if chara:
            if self.direction == DOWN:
                chara.direction = UP
            elif self.direction == LEFT:
                chara.direction = RIGHT
            elif self.direction == RIGHT:
                chara.direction = LEFT
            elif self.direction == UP:
                chara.direction = DOWN
            chara.update(map)  # 向きを変えたので更新
        return chara

    def touch_object(self, map):
        """足もとに宝箱があるか調べる"""
        event = map.get_event(self.x, self.y)
        if isinstance(event, Treasure):
            return event
        return None

    def touch_door(self, map):
        """目の前にとびらがあるか調べる"""
        # 向いている方向のとなりの座標を求める
        nextx, nexty = self.x, self.y
        if self.direction == DOWN:
            nexty = self.y + 1
        elif self.direction == LEFT:
            nextx = self.x - 1
        elif self.direction == RIGHT:
            nextx = self.x + 1
        elif self.direction == UP:
            nexty = self.y - 1
        # その場所にとびらがあるか？
        event = map.get_event(nextx, nexty)
        if isinstance(event, Door):
            return event
        return None

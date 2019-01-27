import codecs
import os
from pygame.locals import Rect
import tools
from window import Window
from config import FONT_WIDTH, FONT_HEIGHT
import database


MESSAGE_FORM = (Rect(140, 334, 360, 140), 20, 4)

class MessageEngine(object):
    WHITE, RED, GREEN, BLUE = 0, 160, 320, 480

    def __init__(self):
        self.image = tools.load_image("data", "font.png", -1)
        self.color = self.WHITE
        self.kana2rect = {}
        self.create_hash()

    def set_color(self, color):
        self.color = color
        # 変な値だったらWHITEにする
        if self.color not in [self.WHITE, self.RED, self.GREEN, self.BLUE]:
            self.color = self.WHITE

    def draw_character(self, screen, pos, ch):
        x, y = pos
        try:
            rect = self.kana2rect[ch]
            screen.blit(self.image, (x,y), (rect.x + self.color, rect.y, rect.width, rect.height))  # noqa
        except KeyError:
            print("描画できない文字があります:%s" % ch)
            return

    def draw_string(self, screen, pos, str):
        x, y = pos
        for i, ch in enumerate(str):
            dx = x + FONT_WIDTH * i
            self.draw_character(screen, (dx, y), ch)

    def create_hash(self):
        """文字から座標への辞書を作成"""
        filepath = os.path.join("data", "kana2rect.dat")
        fp = codecs.open(filepath, "r", "utf-8")
        for line in fp.readlines():
            line = line.rstrip()
            d = line.split("\t")
            kana, x, y, w, h = d[0], int(d[1]), int(d[2]), int(d[3]), int(d[4])
            self.kana2rect[kana] = Rect(x, y, w, h)
        fp.close()


class TexTrucker(object):
    MAX_CHARS_PER_PAGE = 20 * 3  # 1ページの最大文字数
    MAX_LINES = 30             # メッセージを格納できる最大行数
    LINE_HEIGHT = 8            # 行間の大きさ
    def __init__(self, max_chars_per_line):
        self.cur_page = 0
        self.cur_pos = 0  # 現在ページで表示した最大文字数
        self.is_wait_action = False
        self.is_text_end = False
        self.max_chars_per_line = max_chars_per_line
        self.text = []

    def next_pos(self, p, unit):
        p += self.max_chars_per_line
        return(int(p / self.max_chars_per_line) * self.max_chars_per_line)

    def set(self, message):
        self.cur_pos = 0
        self.cur_page = 0
        self.is_wait_action = False
        self.is_text_end = False
        self.text = [u'　'] * (self.MAX_LINES * self.max_chars_per_line)

        p = 0
        for i in range(len(message)):
            ch = message[i]
            if ch == "/":  # /は改行文字
                self.text[p] = "/"
                p = self.next_pos(p, self.max_chars_per_line)
            elif ch == "%":  # \fは改ページ文字
                self.text[p] = "%"
                p = self.next_pos(p, self.MAX_CHARS_PER_PAGE)
            else:
                self.text[p] = ch
                p += 1
        self.text[p] = "$"  # 終端文字

    def is_empty(self):
        return not self.text

    def update(self):
        # ユーザ入力待ちならアニメーションSTOP
        if self.is_wait_action:
            return

        self.cur_pos += 1  # 1文字流す
        # テキスト全体から見た現在位置
        p = self.cur_page * self.MAX_CHARS_PER_PAGE + self.cur_pos
        if self.text[p] == "/":  # 改行文字
            self.cur_pos = self.next_pos(self.cur_pos, self.max_chars_per_line)
        elif self.text[p] == "%":  # 改ページ文字
            self.cur_pos = self.next_pos(self.cur_pos, self.MAX_CHARS_PER_PAGE)
        elif self.text[p] == "$":  # 終端文字
            self.is_text_end = True

        # 現在のページ終端に到達していたらユーザ入力待ちへ遷移する。
        if self.cur_pos % self.MAX_CHARS_PER_PAGE == 0:
            self.is_wait_action = True

    def get_ch(self, i):
        ch = self.text[self.cur_page * self.MAX_CHARS_PER_PAGE + i]
        if ch == "/" or ch == "%" or ch == "$":
            return None, 0, 0
        return ch, (i % self.max_chars_per_line), int(i / self.max_chars_per_line)

    def key_action(self):
        # 次アクションが発生し得るならTrue、そうでなければFalse
        if self.is_text_end:
            # テキスト終端に達した状態でアクションキー押下された。
            # 次のアクションは発生しえないのでFalseを返す。
            self.text= []
            return False
        if self.is_wait_action:
            # 次ページが存在するので、次アクションありとしてTrueを返す。
            self.cur_page += 1
            self.cur_pos = 0
            self.is_wait_action = False
            return True
        if not self.text:
            raise ValueError('こないはず')
        return True # TODO おしゃべり中のkey_actonで抜けてしまうのを防ぐ。

    def get_center(self):
        return int(self.max_chars_per_line / 2) * FONT_WIDTH - int(FONT_WIDTH / 2), (self.LINE_HEIGHT + FONT_HEIGHT) * 3


class MessageWindow(Window):
    MAX_CHARS_PER_PAGE = 20 * 3  # 1ページの最大文字数
    MAX_LINES = 30             # メッセージを格納できる最大行数
    LINE_HEIGHT = 8            # 行間の大きさ
    animcycle = 24

    def __init__(self, form, msg_engine):
        Window.__init__(self, form[0])
        self.text_rect = self.inner_rect.inflate(-32, -32)
        self.msg_engine = msg_engine
        self.cursor = tools.load_image("data", "cursor.png", -1)
        self.text_tracker = TexTrucker(form[1])
        self.frame = 0

    def set(self, message):
        self.text_tracker.set(message)

    def key_handler(self, event):
        if tools.is_key_action(event):
            if not self.text_tracker.is_empty():
                return self.text_tracker.key_action()
        return False

    def key_action(self):
        if not self.text_tracker.is_empty():
            if not self.text_tracker.key_action():
                print('くろーずをかえすよ : {}'.format(database.ACT_CLOSE))
                return database.ACT_CLOSE
        return database.ACT_NONE

    def update(self):
        if not self.text_tracker.is_empty():
            self.text_tracker.update()
            self.frame += 1

    def draw(self, screen):
        Window.draw(self, screen)
        for i in range(self.text_tracker.cur_pos):
            ch, char_no, line_no = self.text_tracker.get_ch(i)
            if ch:
                self.msg_engine.draw_character(
                    screen,
                    (self.text_rect[0] + FONT_WIDTH * char_no,
                     self.text_rect[1] + (self.LINE_HEIGHT + FONT_HEIGHT) * line_no), ch)

        if (not self.text_tracker.is_text_end) and self.text_tracker.is_wait_action:
            if int(self.frame / self.animcycle) % 2 == 0:
                center_x, center_y = self.text_tracker.get_center()
                screen.blit(self.cursor, (self.text_rect[0] + center_x,
                                          self.text_rect[1] + center_y))

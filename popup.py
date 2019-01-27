import database


class PopupManager(object):
    def __init__(self):
        self._popup_stack = []

    def push(self, popup):
        popup.show()
        self._popup_stack.append(popup)

    def pop(self):
        self._popup_stack[-1].hide()
        self._popup_stack.pop()

    def is_empty(self):
        return not self._popup_stack

    def update(self):
        if self._popup_stack:
            self._popup_stack[-1].update()

    def draw(self, screen):
        if self._popup_stack:
            self._popup_stack[-1].draw(screen)

    def key_handler(self, event):
        if not self._popup_stack:
            return False
        self._popup_stack[-1].key_handler(event)

    def key_action(self):
        if not self._popup_stack:
            return database.ACT_NONE
        return self._popup_stack[-1].key_action()

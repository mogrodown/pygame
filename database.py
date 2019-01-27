
ACT_NONE, ACT_GAME_START, ACT_GAME_QUIT, ACT_TALK_CHARA, ACT_CMD_WINDOW,\
ACT_STATUS, ACT_EQUIPMENT, ACT_SPELL, ACT_ITEM, ACT_IS_SAVE,\
ACT_ADVENTURE_BOOK1, ACT_ADVENTURE_BOOK2, ACT_BACK, ACT_MEDICAL_PLANTS, ACT_TNT,\
ACT_QUIT, ACT_YES, ACT_NO, ACT_GET_TREASURE, ACT_CLOSE = range(20)

TYPE_SUB, TYPE_QUERY, TYPE_EXEC = range(3)
menu_items = {
    ACT_STATUS: (u'つよさ', TYPE_SUB),
    ACT_EQUIPMENT: (u'そうび',TYPE_SUB),
    ACT_SPELL: (u'じゅもん', TYPE_SUB),
    ACT_ITEM: (u'どうぐ', TYPE_SUB),
    ACT_IS_SAVE: (u'ほぞん', TYPE_SUB),
    ACT_BACK: (u'もどる', TYPE_EXEC),
    ACT_MEDICAL_PLANTS: (u'やくそう', TYPE_EXEC),
    ACT_TNT: (u'ばくやく', TYPE_EXEC),
    ACT_ADVENTURE_BOOK1: (u'ぼうけんのしょ１', TYPE_QUERY),
    ACT_ADVENTURE_BOOK2: ('ぼうけんのしょ２', TYPE_QUERY),
    ACT_QUIT: (u'しゅうりょう', TYPE_QUERY),
    ACT_YES: (u'はい', TYPE_EXEC),
    ACT_NO: (u'いいえ', TYPE_EXEC)}

def is_sub_menu(action):
    return menu_items[action][1] == TYPE_SUB

def is_query_menu(action):
    return menu_items[action][1] == TYPE_QUERY

OBJ_ITEM, OBJ_EQUIPMENT = range(2)

item_database = {OBJ_ITEM:['やくそう', 'どくけし', 'ばくやく'],
                 OBJ_EQUIPMENT:['はがねのつるぎ']}

if __name__ == '__main__':
    if 'やくそう' in item_database[OBJ_ITEM]:
        print('found')
    else:
        print('not found')


    print(type)

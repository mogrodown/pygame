import database

items = {}
equipments = {}

def save_baggage(key):
    if key in database.item_database[database.OBJ_ITEM]:
        if key in items:
            items[key] += 1
        else:
            items[key] = 1
    elif key in database.item_database[database.OBJ_EQUIPMENT]:
        if key in equipments:
            equipments[key] += 1
        else:
            equipments[key] = 1


if __name__ == '__main__':
    save_baggage('やくそう')
    save_baggage('ばくやく')

    dest = sorted(items.items(), key=lambda  x: x[0])
    print(dest)

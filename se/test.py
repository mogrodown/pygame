
class Parent(object):
    def __init__(self):
        pass

    def func(self):
        print('hello')

class Child(Parent):
    def __init__(self):
        pass

    def func(self):
        # Parent.func(self)
        print('world')


if __name__ == '__main__':
    c = Child()
    c.func()
class A(object):
    a = 1
    b = 2


a = A()
a.b = 3
a.c = 4
print(a.__dict__)
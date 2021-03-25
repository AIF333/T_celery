from tasks import test_1

if __name__ == '__main__':
    res = test_1.delay(1, 2)
    print(res)

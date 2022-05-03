
from concurrent.futures import ThreadPoolExecutor

from time import sleep


def test1():
    res = {
        't1-key1': 1,
        't1-key2': 2,
    }
    sleep(5)
    print('done t1 - 2 seconds')
    return res

def test2():
    res = {
        't2-key1': 1,
        't2-key2': 2,
    }
    sleep(4)
    print('done t2 - 7 seconds')
    return res

def test3():
    res = {
        't3-key1': 1,
        't3-key2': 2,
    }
    sleep(3)
    print('done t3 - 6 seconds')
    return res

def test4():
    res = 45
    res1 = 60
    sleep(2)
    print('done t=4 - 1 seconds')
    return res, res1

def runTestWithParallelisation():
    executorList = []
    with ThreadPoolExecutor() as executor:
        f1 = executor.submit(test1)
        f2 = executor.submit(test2)
        f3 = executor.submit(test3)
        f4 = executor.submit(test4)

    res, res1 = f4.result()
    print(f1.result())
    print(f2.result())
    print(f3.result())
    print(f4.result())

runTestWithParallelisation()
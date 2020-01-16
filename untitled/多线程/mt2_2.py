# coding=utf-8
import threading
from time import sleep

zhifu ={
    'tom'    : 12000,
    'limingchen' : 8500,
    'wangye'  : 75000,
    'zhaoyun' : 100000,
}


# 调用 Lock函数，返回一个锁对象
weizhifu_lock = threading.Lock()

def thread1_didi_pay(account,amount):
    # 在代码访问共享对象之前 加锁
    # 当多个线程同时执行lock.acquire()时，
    # 只有一个线程能成功地获取锁，然后继续执行代码
    # 其他线程就继续等待，直到获得锁为止。
    weizhifu_lock.acquire()
    print('* t1: get balance from bank')

    balance = zhifu[account]
    print(balance)
    print('* t1: do something(like discount lookup) for 2 seconds')
    sleep(2)

    print('* t1: deduct')
    zhifu[account] = balance - amount

    # 访问完共享对象 释放锁
    # 访问结束后，一定要调用Lock对象的release方法，进行解锁操作。
    # 否则其它等待锁的线程将永远等待下去，成为死线程。
    weizhifu_lock.release()

def thread2_yuebao_interest(account,amount):
    # 在代码访问共享对象之前 加锁
    # weizhifu_lock.acquire()
    print('$ t2: get balance from bank')

    balance = zhifu[account]
    print(balance)
    print('$ t2: do something2... for 1 seconds')
    sleep(1)

    print('$ t2: add')
    zhifu[account] = balance + amount

    # 访问完共享对象 释放锁
    # weizhifu_lock.release()


t1 = threading.Thread(target=thread1_didi_pay,    args=('tom',100))
t2 = threading.Thread(target=thread2_yuebao_interest, args=('tom',200))
t1.start()
t2.start()
t1.join()
t2.join()
print('finally, tom balance is %s' % zhifu['tom'])

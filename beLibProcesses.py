#!/usr/bin/env python3.6
# coding: utf8
#from __future__ import unicode_literals

from pprint import pprint

from multiprocessing import Process, Lock, Queue, BoundedSemaphore, Semaphore
import multiprocessing as mp
import os
from queue import Empty

from bgp import *
from beLib import *

#==================================================


class ParallelCounter(Counter):
    def __init__(self, stat, date=''):
        Counter.__init__(self, date)
        self.stat = stat

    def line(self):
        self.stat.put((self.date, 'line'))
        Counter.line(self)

    def err_qr(self):
        self.stat.put((self.date, 'err_qr'))
        Counter.err_qr(self)

    def err_ns(self):
        self.stat.put((self.date, 'err_ns'))
        Counter.err_ns(self)

    def ok(self):
        self.stat.put((self.date, 'ok'))
        Counter.ok(self)

    def select(self):
        self.stat.put((self.date, 'select'))
        Counter.select(self)

    def autre(self):
        self.stat.put((self.date, 'autre'))
        Counter.autre(self)

    def union(self):
        self.stat.put((self.date, 'union'))
        Counter.union(self)

    def bgp_not_valid(self):
        self.stat.put((self.date, 'bgp_not_valid'))
        Counter.bgp_not_valid(self)

    def err_tpf(self):
        self.stat.put((self.date, 'err_tpf'))
        Counter.err_tpf(self)

#==================================================


def analyse(in_queue):
    logging.debug('Start analyse worker "%s"', os.getpid())
    while True:
        try:
            mess = in_queue.get()
            if mess is None:
                break
            else:
                logging.debug('Treat mess in %s %s', os.getpid(), mess)
                rankAnalysis(mess)
        except Empty as e:
            print('empty!')
        except Exception as e:
            print(mess, e)
            break
    logging.debug('Stop analyse worker "%s"', os.getpid())


#==================================================


def count_stat(in_queue):
    logging.debug('Start stat worker "%s"', os.getpid())
    nb = 0
    counter_list = dict()
    total = Counter()
    while True:
        try:
            mess = in_queue.get()
            if mess is None:
                break
            else:
                nb += 1
                (date, c) = mess
                #print('recieve ',date,c)
                if not (date in counter_list):
                    counter_list[date] = Counter(date)
                counter_list[date].cpt[c] += 1
        except Empty as e:
            print('empty!')
        except Exception as e:
            print(e)
            break
    for d in counter_list:
        total.join(counter_list[d])
        counter_list[d].print()
    print('=========== total (%d date(s)) =============' % len(counter_list))
    total.print()
    logging.debug('Stop stat worker "%s" with %d', os.getpid(), nb)


class Stat:
    def __init__(self):
        self.stat_queue = mp.Queue()
        self.stat_proc = mp.Process(
            target=count_stat, args=(self.stat_queue, ))
        self.stat_proc.start()

    def put(self, v):
        self.stat_queue.put(v)

    def stop(self):
        self.stat_queue.put(None)
        self.stat_proc.join()


#==================================================
#==================================================
#==================================================

if __name__ == '__main__':
    logging.basicConfig(
        format='%(levelname)s:%(asctime)s:%(message)s',
        filename='scan.log',
        filemode='w',
        level=logging.DEBUG)
    print('main')
    print(mp.cpu_count(),' proccesses availables')
    #print(len(os.sched_getaffinity(0)))
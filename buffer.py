# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 09:34:36 2017

@author: Andi
"""

import queue

class Buffer(queue.Queue):
    def __init__(self, maxsize=0):
        super().__init__(maxsize=maxsize)

    def get(self, block=True, timeout=None):
        obj = super().get(block=block, timeout=timeout)
        self.task_done()
        return obj

    def put(self, obj, block=True, timeout=None):
        if self.full():
            self.get()
        super().put(obj, block=block, timeout=None)
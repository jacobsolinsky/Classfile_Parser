#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 13:58:38 2019

@author: jacobsolinsky
"""
from chaitin import node, graph

class taci:
    def __init__(self, uses, defs):
        self.uses = uses
        self.defs = defs
class tacblock:
    def __init__(self, tacis):
        self.tacis = tacis
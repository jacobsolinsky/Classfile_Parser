#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 08:28:30 2019

@author: jacobsolinsky
"""
class node: 
    def __init__(self, name, *attachés):
        self.rcost = 1 #to be replaced with a real cost value for register allocation
        self.name = name
        self.attachés = []
        self.degree = 0
        self.plucked = False
        for attaché in attachés:
            self.add(attaché)
        self.icolor = "undecided"
    def add(self, node):
        self.attachés.append(node)
        node.attachés.append(self)
        self.degree += 1
        node.degree += 1
    def pluck(self):
        if self.plucked:
            raise Exception("Already plucked")
        for attaché in self.attachés:
            attaché.attachés.remove(self)
            attaché.degree -= 1
        self.plucked = True
        self.degree = 0 
        self.origat = self.attachés
        self.attachés = []
    def reattach(self):
        if not self.plucked:
            raise Exception("Already attached")
        for attaché in self.origat:
            if not attaché.plucked:
                attaché.attachés.append(self)
                attaché.degree += 1
                self.attachés.append(attaché)
                self.degree += 1
        self.plucked = False
    def __repr__(self):
        return self.name + "[" + \
        ",".join([attaché.name for attaché 
                  in self.attachés]) +"]"
    def color(self, colorno):
        self.icolor = colorno
a = node("a")
b = node("b", a)
c = node("c", b)
d = node("d", c, a)
e = node("e", a)
f = node("f", a)
g = node("g", c, e, f)
h = node("h", b, g)
i = node("i", d, g)
j = node("j", b, e, i)
k = node("k", d, f, h, j)

class graph():
    maxcolors = 3
    def __init__(self, *nodes):
        self.nodes = list(nodes)
        self.orignodes = tuple(nodes)
    def stackbuild(self):
        self.stack = []
        problemnodes = []            
        mindegree = self.nodes[0].degree
        while(self.nodes):
            mindegree = self.maxcolors + 1
            for node in self.nodes:
                if node.degree <= mindegree:
                    mindegree = node.degree
                    minnode = node
            if minnode.degree > self.maxcolors -1:
                for node in self.nodes:
                    if node.degree > self.maxcolors - 1:
                        problemnodes.append(node)
            if problemnodes:
                cost = problemnodes[0].rcost / problemnodes[0].degree
                for pnode in problemnodes:
                    if pnode.rcost / pnode.degree < cost:
                        cost = pnode.rcost / pnode.degree
                        minnode = pnode
                minnode.color("s")
                problemnodes = []
            minnode.pluck()
            self.stack.append(minnode)
            self.nodes.remove(minnode)
    def color(self):
        self.stackbuild()
        print(self.stack)
        node1 = self.stack.pop()
        node1.reattach()
        node1.color(0)
        while(self.stack):
            nnode = self.stack.pop()
            nnode.reattach()
            trycolor = 0
            while trycolor in [attaché.icolor for attaché in nnode.attachés]:
                trycolor += 1
            if nnode.icolor != "s":
                nnode.color(trycolor)
trygraph = graph(a,b,c,d,e,g,f,h,i,j,k)
            
    
    
    
    
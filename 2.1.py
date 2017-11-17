#!/usr/bin/python2.7
#coding:utf-8

from state import *
from transition import *
from automate import *

s0 = State(0, True, False, "s0")
s1 = State(1, False, False, "s1")
s2 = State(2, False, True, "s2")

list_state = [s0, s1, s2]

t1 = Transition(s0, "a", s0)
t2 = Transition(s0, "b", s1)
t3 = Transition(s1, "a", s2)
t4 = Transition(s1, "b", s2)
t5 = Transition(s2, "a", s0)
t6 = Transition(s2, "b", s1)

liste_auto = [t1, t2, t3, t4, t5, t6]

auto = Automate(liste_auto, label = 'A')

print(auto)
# auto.show("A_ListeTrans")

# -----------

auto1 = Automate(liste_auto, list_state, 'A1')

print "----------------"

print(auto1)
# auto1.show("A1_ListeTrans")

# # -----------

# auto2 = Automate.creationAutomate("auto.txt")
# auto2.label = 'A2'

# print "----------------"

# print(auto2)
# auto2.show('A2_ListeTrans')

# -----------

# print "{}".format(auto.removeTransition(Transition(s0, 'a', s1)))
# print auto.removeTransition(t1)

# auto.show("A_ListeTrans_Modified")

# print auto.addTransition(t1)

# auto.show("A_ListeTrans_Modified2")

# -----------

# print auto.removeState(s1)
# auto.show("A_ListeTrans_Modified3")

# print auto.addState(s1)
# auto.show("toto")

# s3 = State(0, True, False, "s3")
# print auto.addState(s3)
# auto.show("tata")

# -----------

print auto1.getListTransitionsFrom(s1)

print auto1.succ([s0, s2, s1], 'a')
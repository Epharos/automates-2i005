# -*- coding: utf-8 -*-
from transition import Transition
from state import State
import os
import copy
import sp
from sp import *
from parser import Parser
from itertools import product
from automateBase import AutomateBase


class TransitionList :
        def __init__(self, src, eti, fin) :
                self.src = src
                self.eti = eti
                self.fin = fin

        def __repr__(self) :
                return "({}, {}, {})".format(self.src, self.eti, self.fin)

class Automate(AutomateBase):
        
        def succElem(self, state, lettre):
                """State x str -> list[State]
                rend la liste des états accessibles à partir d'un état
                state par l'étiquette lettre
                """
                # successeurs : list[State]
                successeurs = []
                # t: Transitions
                for t in self.getListTransitionsFrom(state):
                        if t.etiquette == lettre and t.stateDest not in successeurs:
                                successeurs.append(t.stateDest)
                return successeurs

        def succ (self, listStates, lettre):
                """list[State] x str -> list[State]
                rend la liste des états accessibles à partir de la liste d'états
                listStates par l'étiquette lettre
                """
                
                successeurs = []

                for s in listStates :
                        for t in self.succElem(s, lettre) :
                                if not(t in successeurs) :
                                        successeurs.append(t)

                return successeurs



        
        def acc(self):
                """ -> list[State]
                rend la liste des états accessibles
                """            

                states = []

                for t in self.listTransitions :
                        if not(t.stateDest in states) :
                                states.append(t.stateDest)

                return states



        """ Définition d'une fonction déterminant si un mot est accepté par un automate.
        Exemple :
                a=Automate.creationAutomate("monAutomate.txt")
                if Automate.accepte(a,"abc"):
                        print "L'automate accepte le mot abc"
                else:
                        print "L'automate n'accepte pas le mot abc"
        """
        @staticmethod
        def accepte(auto,mot) :
                """ Automate x str -> bool
                rend True si auto accepte mot, False sinon
                """

                flag = False

                for s in auto.listStates :
                        if s.init :
                                flag = auto.accepteRec(s, mot, 0)
                        if flag :
                                return flag

                return flag


        def accepteRec(self, state, mot, index) :
                if index == len(mot) and state.fin :
                        return True
                elif index == len(mot) and not(state.fin) :
                        return False

                flag = False

                for t in self.transitions(state) :
                        if t.etiquette == mot[index] :
                                flag = self.accepteRec(t.stateDest, mot, index + 1)
                                if flag :
                                        return flag

                return flag


        def transitions(self, state) :
                trans = []

                for t in self.listTransitions :
                        if t.stateSrc == state :
                                trans.append(t)

                return trans


        @staticmethod
        def estComplet(auto,alphabet) :
                """ Automate x str -> bool
                rend True si auto est complet pour alphabet, False sinon
                """

                for s in auto.listStates :
                        for c in alphabet :
                                if not(auto.transExists(s, c)) :
                                        return False

                return True

        def transExists(self, state, etiquette) :
                for t in self.transitions(state) :
                        if t.etiquette == etiquette :
                                return True

                return False

        @staticmethod
        def estDeterministe(auto) :
                """ Automate  -> bool
                rend True si auto est déterministe, False sinon
                """

                ei = 0

                for s in auto.listStates :
                        if s.init :
                                ei += 1

                if ei != 1 :
                        return False

                for s in auto.listStates :
                        etiquettes = []
                        for t in auto.transitions(s) :
                                if t.etiquette in etiquettes :
                                        return False
                                else :
                                        etiquettes.append(t.etiquette)

                return True


       
        @staticmethod
        def completeAutomate(auto,alphabet) :
                """ Automate x str -> Automate
                rend l'automate complété d'auto, par rapport à alphabet
                """

                if Automate.estComplet(auto, alphabet) :
                        return auto

                newId = 0

                for s in auto.listStates :
                        newId += int(s.id)

                newState = State(newId, False, False, "Puit")
                auto.addState(newState)

                for s in auto.listStates :
                        etiquettes = []
                        for t in auto.transitions(s) :
                                if not(t.etiquette in etiquettes) :
                                        etiquettes.append(t.etiquette)
                        for c in alphabet :
                                if not(c in etiquettes) :
                                        auto.addTransition(Transition(s, c, newState))

                return auto


       
        @staticmethod
        def determinisation(auto) :
                """ Automate  -> Automate
                rend l'automate déterminisé d'auto
                """

                alphabet = auto.alphabet()
                transitions = []

                Q = []
                E = [[auto.initState()]]

                while len(E) > 0 :
                        S = E[0]
                        E.remove(S)
                        Q.append(S)

                        for l in alphabet :
                                temp = []
                                for k in S :
                                        for t in auto.transitions(k) :
                                                if t.etiquette == l and not(t.stateDest in temp) :
                                                        temp.append(t.stateDest)

                                if not(temp in Q) and not(temp in E) :
                                        E.append(temp)

                                transitions.append(TransitionList(S, l, temp))

                states = []
                i = 0

                for o in Q :
                        flag = False
                        for p in o :
                                if p.fin :
                                        flag = True
                        s = State(i, i == 0, flag)
                        i += 1
                        states.append(s)

                transitionsFinales = []

                for m in transitions :
                        t = Transition(states[auto.indexOf(Q, m.src)], m.eti, states[auto.indexOf(Q, m.fin)])
                        transitionsFinales.append(t)

                auto = Automate(transitionsFinales)

                return auto

        def listAreEquals(self, L, M) :
                if len(L) != len(M) :
                        return False

                for i in range(len(L)) :
                        if not(L[i].__eq__(M[i])) :
                                return False

                return True

        def indexOf(self, T, S) :
                i = 0
                for t in T :
                        if t == S :
                                return i
                        i += 1
                return -1 

        def alphabet(self) :
                alphabet = []

                for t in self.listTransitions :
                        if not(t.etiquette in alphabet) :
                                alphabet.append(t.etiquette)

                return alphabet

        def initState(self) :
                for s in self.listStates :
                        if s.init :
                                return s

                return None


        @staticmethod
        def complementaire(auto, alphabet):
                """ Automate x str -> Automate
                rend  l'automate acceptant pour langage le complémentaire du langage de auto
                """

                auto2 = Automate.determinisation(auto)
                auto3 = Automate.completeAutomate(auto2, alphabet)

                for s in auto3.listStates :
                        s.fin = not(s.fin)

                return auto3


     
        @staticmethod
        def intersection (auto1d, auto2d):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage l'intersection des langages des deux automates
                """
		#auto1d = Automate.determinisation(auto1)
                #auto2d = Automate.determinisation(auto2)

                L = [] #liste de couples
                listeStates = [] # liste des états
                listeTrans = []
                L.append((auto1d.getListInitialStates()[0] , auto1d.getListInitialStates()[0] )) #couple initial
                isFinal = L[0][0].fin and L[0][1].fin
                listeStates.append(State(0 , True , isFinal)) 
                alpha1 = auto1d.getAlphabetFromTransitions()
                alpha2 = auto2d.getAlphabetFromTransitions()
                alpha = []
                for a  in alpha2 :
                        if a in alpha1 :
                                alpha.append(a) 
                i = 0
                j = 0
                while(i < len(L) ) :
                        for c in L[i:] :
                                for l in alpha :
                                        if len(auto1d.succElem(c[0] , l)) > 0 and len(auto2d.succElem(c[1], l)) > 0 :
                                                couple = (auto1d.succElem(c[0] , l)[0] ,auto2d.succElem(c[1], l)[0] )
                                                if couple not in L :
                                                        L.append(couple)
                                                        j = j + 1
                                                        isFinal = couple[0].fin and couple[1].fin
                                                        listeStates.append(State(j , False , isFinal ))
                                                        trans = Transition(listeStates[i] , l , listeStates[j])
                                                else :
                                                        trans = Transition(listeStates[i] , l , listeStates[L.index(couple)])
                                                if trans not in listeTrans :
                                                        listeTrans.append(trans)
                        i = i + 1
                autoInter = Automate(listeTrans)
                return autoInter
               


        @staticmethod
        def union (auto1, auto2):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage l'union des langages des deux automates
                """

                # auto1 = Automate.determinisation(auto1)
                # auto2 = Automate.determinisation(auto2)

                if not(Automate.estDeterministe(auto1)) or not(Automate.estDeterministe(auto2)) :
                        print ("Les automates doivent être déterministes pour en faire l'union !")
                        return None

                auto2.changeIds(auto1)

                print ("------\n{}\n------\n{}\n------").format(auto1, auto2)

                alphabet = Automate.unionList(auto1.alphabet(), auto2.alphabet())
                transitions = []

                Q = []
                E = [[auto1.initState(), auto2.initState()]]

                zero = State(auto1.automateLength() + auto2.automateLength(), False, False)

                while len(E) > 0 :
                        print (E)
                        S = E[0]
                        E.remove(S)
                        Q.append(S)

                        for l in alphabet :
                                temp = []
                                for t in auto1.transitions(S[0]) :
                                        if t.etiquette == l and not(t.stateDest in temp) :
                                                temp.append(t.stateDest)
                                if len(temp) == 0 :
                                        temp.append(zero)

                                for t in auto2.transitions(S[1]) :
                                        if t.etiquette == l and not(t.stateDest in temp) :
                                                temp.append(t.stateDest)
                                if len(temp) == 1 :
                                        temp.append(zero)

                                if not(temp in Q) and not(temp in E) and len(temp) == 2 :
                                        E.append(temp)

                                transitions.append(TransitionList(S, l, temp))

                states = []
                i = 0

                for o in Q :
                        s = State(i, o[0].init or o[1].init, o[0].fin or o[1].fin)
                        i += 1
                        states.append(s)

                transitionsFinales = []

                for m in transitions :
                        print (m)
                        t = Transition(states[auto1.indexOf(Q, m.src)], m.eti, states[auto1.indexOf(Q, m.fin)])
                        transitionsFinales.append(t)

                auto = Automate(transitionsFinales)

                return auto

        @staticmethod
        def unionList(l, m) :
                u = []

                for e in m :
                        u.append(e)

                for e in l :
                        if not(e in m) :
                                u.append(e)

                return u

        def changeIds(self, auto1) :
                nb = auto1.automateLength()

                for s in self.listStates :
                        s.id = nb + int(s.id)
                        s.label = str(s.id)


        def automateLength(self) :
                return len(self.listStates)
        
       
        @staticmethod
        def concatenation (auto1, auto2):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage la concaténation des langages des deux automates
                """
                return 

       
        @staticmethod
        def etoile (auto):
                """ Automate  -> Automate
                rend l'automate acceptant pour langage l'étoile du langage de a
                """
		# auto2 = copy.deepcopy(auto)
                # alpha = auto2.getAlphabetFromTransitions()
                # I = auto2.getListInitialStates()
                # for s in auto2.getListStates() :
                #         for e in alpha :
                #                 A = auto.succElem(s , e)
                #                 for elem in A :
                #                         if elem.fin :
                #                                 for i in I :
                #                                         auto2.addTransition(Transition(s,e,i))


                # motvide = State(-1 , True , True , "eps")
                # auto2.addState(motvide)
                # return auto2

                if not(auto.estStandard()) :
                        print "L'automate doit être standard (utiliser la fonction auto.standard() pour corriger le problème)"
                        return

                init = None
                final = []

                for e in auto.listStates :
                        if e.fin and not(e.init) :
                                final.append(e)

                        if e.init :
                                e.fin = True
                                init = e

                transitionsInit = auto.transitions(init)

                for t in transitionsInit :
                        for k in final :
                                auto.addTransition(Transition(k, t.etiquette, t.stateDest))

                return auto

                

        def estStandard (self) :
                i = 0
                for s in self.listStates :
                        if s.init :
                                i = i + 1
                        
                        if i > 1 :
                                return False

                initial = []

                for s in self.listStates :
                        if s.init : 
                                initial.append(s)

                for t in self.listTransitions :
                        if t.stateDest in initial :
                                return False

                return True

        def inter(self, l1, l2) :
                tr = list()

                for e in l1 :
                        if e in l2 :
                                tr.append(e)

                return tr

        def equState(self, state, states) :
                for s in states :
                        if s.id == state.id :
                                return s

                return None

        @staticmethod
        def standard (self) :
                """ Automate -> Automate
                rend la version standard de l'automate
                """

                if self.estStandard() :
                        return self

                states = []
                init = []
                final = []

                for s in self.listStates :
                        if s.init :
                                init.append(s)

                        if s.fin : 
                                final.append(s)

                        states.append(State(s.id, False, s.fin))

                print states


                d = State(len(self.listStates) + 1, True, True if len(self.inter(init, final)) != 0 else False)
                states.append(d)

                transitions = []

                for t in self.listTransitions :
                        transitions.append(Transition(self.equState(t.stateSrc, states), t.etiquette, self.equState(t.stateDest, states)))

                for i in init :
                        for t in self.transitions(i) :
                                if not(Transition(d, t.etiquette, self.equState(t.stateDest, states)) in transitions) :
                                        transitions.append(Transition(d, t.etiquette, self.equState(t.stateDest, states)))

                return Automate(transitions, states)










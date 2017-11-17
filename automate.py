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
                return 



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
                return 



        @staticmethod
        def estComplet(auto,alphabet) :
                """ Automate x str -> bool
                rend True si auto est complet pour alphabet, False sinon
                """
                return

        
        @staticmethod
        def estDeterministe(auto) :
                """ Automate  -> bool
                rend True si auto est déterministe, False sinon
                """
                return


       
        @staticmethod
        def completeAutomate(auto,alphabet) :
                """ Automate x str -> Automate
                rend l'automate complété d'auto, par rapport à alphabet
                """
                return 


       
        @staticmethod
        def determinisation(auto) :
                """ Automate  -> Automate
                rend l'automate déterminisé d'auto
                """
                return 


        @staticmethod
        def complementaire(auto, alphabet):
                """ Automate x str -> Automate
                rend  l'automate acceptant pour langage le complémentaire du langage de auto
                """
                return


     
        @staticmethod
        def intersection (auto1, auto2):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage l'intersection des langages des deux automates
                """
                return 


        @staticmethod
        def union (auto1, auto2):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage l'union des langages des deux automates
                """
                return 


        
       
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
                return 






# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 17:22:35 2021

@author: Julián Álvarez and Cristian Herrera
"""
   
"""Every next function has the name of the strategy it works"""
#Recorddar que list_a está invertida
 
def mhi(red,green):
    if red < green:
        print("PUT")
        return 0
    else:
        print("CALL")
        return 1

def mhi_mayoria(red, green):
    if red < green:
        print("CALL")
        return 1
    else:
        print("PUT")
        return 0

    
def millon_mayoria(red, green):
    if red < green:
        print("CALL")
        return 1
    else:
        print("PUT")
        return 0

def millon_minoria(red , green):
    if red > green:
        print("PUT")
        return 0
    else:
        print("CALL")
        return 1

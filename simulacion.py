# -*- coding: utf-8 -*-
"""
Created on Tue May 25 21:30:11 2021

@author: Julián Álvarez and Cristian Herrera
"""

"""Simulación Probabilistico"""

class Balance:
    def __init__(self, bank):
        self.bank = bank
        self.moves = []
        
    def update_bank(self, result):
        # result is the amoun of the operation and can be negative as well
        self.bank = self.bank + (result)
        
    def add_move(self, move):
        self.moves.append(move)
        
    def __str__(self):
        cash = str(self.bank)
        return cash
    
    def show_details(self):
        num = len(self.moves)
        list_a = self.moves[num-5:]
        num = 0
        print("Los últimos cinco movimientos fueron")
        for e in list_a:
            print(num," ",e)
            num += 1
            
def sim_invest(strategy, d_class, list_a, result, amount, share_fee=60):
    if strategy == "mhi":
        candle = list_a[0] - list_a[1]
        if result == 1 and  candle < 0 :
            d_class.add_move(("CALL", amount*share_fee))
            d_class.update_bank(amount*share_fee)
        if result == 0 and candle > 0:
            d_class.add_move(("PUT", amount*share_fee))
            d_class.update_bank(amount*share_fee)
                    
            
            
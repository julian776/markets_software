# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 08:51:29 2021

@author: Julián Álvarez and Cristian Herrera
"""

"""Este programa está hecho para eur/usd"""

import time

import worker

import strategys as sta

while True:
    """This while infinity and is design to stop just when the user decided"""
    
    while True: 
        """This while is created to wait until the market
        is giving good results on a specific strategy"""
        df = worker.request(freq="1min", market="eurusd")
        
        wins, losses, no_catalogado = worker.catalogador_mhi(df)
        
        if (wins + no_catalogado) < 18:
            print("Market not suitable, will wait")
            time.sleep(1800)
        else:
            print("Start to operate on the market with an succes of: "+((wins/24)*100))
            break
    
        
    while True:
        df = worker.get_df()
        largo = len(df)
        list_a = df[(largo-5):]
        wins, losses = worker.catalog_cuadrante3(list_a)
        if wins or losses !=  0:
            result = sta.mhi()
            worker.invest(result, name="eurusd")
            
            time.sleep(60)  #This line is to make sure that is in a new quadrant
            
        












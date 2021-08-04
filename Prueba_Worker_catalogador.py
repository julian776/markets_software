# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 19:20:53 2021

@author: Julián Álvarez and Cristian Herrera
"""
import strategys

import worker

df = worker.request(freq="1min", market="eurusd")

wins, losses, no_catalogado = worker.catalogador_mhi(df)

print(wins)
print(losses)
print(no_catalogado)

df1 = worker.get_df()
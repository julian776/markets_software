# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 12:04:20 2021

@author: Julián Álvarez and Cristian Herrera
"""
import time

import pandas as pd

import requests

import datetime

"""The function rquest takes the freq to call the data and return a pandas dataframe with
the last data of the actual day, the parameters is the frequence of candles and market is 
the market you call for example eurjpy"""

def request(freq, market):
    #date_n es la variable de la fecha y debe ser escrita por YYYY/MES/DÍA   
    date_n = timito() 
    api = "http://api.tiingo.com/tiingo/fx/"+market+"/prices?startDate="+date_n+"&resampleFreq="+freq+"&token=a488ea018519aa5565116b85d0d46ecc64a6b805"
    
    headers = {
        'Content-Type': 'json'
    }
    requestResponse = requests.get(api, headers=headers)
     
    df = pd.read_json(api)
    
    return df

"""The timito function returns the actual year and month and day YEAR/MONTH/DAY
A way to get the retutrns is:  year, month, day = time()"""

def timito():
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day
    date_n = str(year)+"/"+str(month)+"/"+str(day)
    return date_n

"""Function minute_sec returns the actual minute
 running and second in string format"""

def minute_sec():
    today = datetime.datetime.now()
    min_t = today.minute
    sec_t = today.second
    if min_t < 10:
        min_t = str(min_t)
        min_t = "0"+min_t
    else:
        min_t = str(min_t)
    sec_t = str(sec_t)
    
    return min_t, sec_t

"""The function compare gets the last object in the dataframe and compare with the actual
time, it gives the answer about real time working or not"""

def get_df():   
    min_t, sec_t = minute_sec()
    min_t = min_t[1]
    min_t = int(min_t)
    sec_t = int(sec_t)
    if min_t > 4:
        min_t = min_t -5
    TE = (300 - min_t*(60)) - sec_t
    if TE > 7:
        time.sleep(TE-4)    #La resta es para que agarre los datos un momento antes
    df = request(freq="1min", market="eurusd")
    return df    
    
    
""""Function cuadrante gets a dataframe of 8 elements only about stock prices
gives by tiingo. Then it return the last 5 minutes cuadrant running"""
#NOTA posible fala de uso de cuadrante ya que el df ya está organizado
def cuadrante(list_a):
    list_d = list_a["date"]
    
    list_d = list_d[::-1]

    count = 0

    for i in list_d:
        l_min = i.strftime("%H:%M:%S")  
        x = float(l_min[4])          
        if (x%5)==0.0:
            break
        count+=1    
    if count == 0:
        count+=1
    list_a = list_a[::-1]    
    list_a = list_a[count:(count+5)]
    count = count - 1
    return list_a, count

"""The function catalog_cuadrante3 takes a pandas dataframe of the last 5 minutes
candles and return the green candles and red candles of the last 3 candles of the cuadrant"""
    
def catalog_cuadrante3(list_a):
    prices = list_a[0:3]
    red = 0 
    green = 0
    open_prices = prices["open"]
    close_prices = prices["close"]
    opn = []
    for i in open_prices:
        opn.append(i)        
    clos = []
    for i in close_prices:
        clos.append(i)
    for i in range(3):
        if (opn[i]-clos[i])<0:
            red+=1
        if (opn[i]-clos[i])>0:
            green+=1
        if (opn[i]-clos[i]) == 0.0:
            print("The quadrant is not available")
            return 0, 0
# revisar que hacer cuando no se puede catalogar el cuadrante al momento de igual manera
#lo cataloga    
    return red, green

"""The function catalog_cuadrante5 takes a pandas dataframe of the last 5 minutes candles
and return the red and green candles of the full cuadrant"""

def catalog_cuadrante5(list_a):
    prices = list_a[0:5]
    red = 0 
    green = 0
    open_prices = prices["open"]
    close_prices = prices["close"]
    opn = []
    for i in open_prices:
        opn.append(i)        
    clos = []
    for i in close_prices:
        clos.append(i)
    for i in range(5):
        if (opn[i]-clos[i])<0:
            red+=1
        if (opn[i]-clos[i])>0:
            green+=1
        if (opn[i]-clos[i]) == 0.0:
            print("No se puede catalogar el cuadrante")
            return 0, 0
# revisar que hacer cuando no se puede catalogar el cuadrante al momento de igual manera
#lo cataloga    
    return red, green

"""The function invest take the result of a 
specific strategy and make the trade"""

# this function need to be based in an online way to trade

def invest(result, market):
    if result == 1:
        call(market)
        print("for market: "+market)
    else:
        put(market)
        print("for market: "+market)

"""The function catalogador look for the efficience of an strategy 
in the last 2 hours in a market and return the wins and the losses"""

def catalogador_mhi(df):
    wins = 0
    losses = 0
    no_catalogado = 0
    df = organizar_df(df)  ######
    count = 0
    for i in range(23):
        num = count*5
        list_a = df[num:(num+5)]
        red , green = catalog_cuadrante3(list_a)
        if red or green != 0:
            if red > green:
               compare = df.iloc[num+6]
               if (compare["open"] - compare["close"]) > 0:
                   losses += 1
               else:
                   wins += 1
            else:
                compare = df.iloc[num+6]
                if (compare["open"] - compare["close"]) > 0:
                   wins += 1
                else:
                   losses += 1
        else:
            no_catalogado += 1
                 
        count+=1
        
    return wins, losses , no_catalogado    

"""The function organizar_df takes a dataframe and takes the last 2 hours 
by the cuadrants organized"""

def organizar_df(df):
    df = df[::-1]
    dates = df["date"]
    count = 0
    for i in dates:
        l_min = i.strftime("%H:%M:%S")  
        x = float(l_min[4])          
        if (x%5)==0.0:
            break
        count+=1
    df = df[count:(count+120)]
#Recordar que está función toma el cuadrante armado por lo que un cuadrante
#en formación no estaría incluido en el dataframe
    return df

"""The function call is to use in oanda can be call in the function invest"""

def call(market, amount=100):
    return 0

"""The function put is to make the trade on put can be call in the function invest to Oanda"""

def put(market, amount=100):
    return 0

#Nota está parte del código está diseñada para el desarrollo de posibles funciones de inversón

"""This function has the objectivo of look the count is working"""

def call_results():
   
    return 0
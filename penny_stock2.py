# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:51:42 2019

@author: brand
"""

# -*- coding: utf-8 -*-
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint



from AWS_EMAIL2 import AWS_EMAIL2


class penny_stock2(AWS_EMAIL2):

    #connecting to penny stock google sheet.
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("PennyStock_Sheet").sheet1
    data = sheet.get_all_records()  # Get a list of all records
    
    # retrieving values in column for the price the stock was purchased, and the stock name
    stockNameCol = sheet.col_values(1)
    stockPurchasePrice = sheet.col_values(2)
    stockPurchasePrice.remove('price')
    stockNameCol.remove('stock')
    
       
    

    for stock,stockAmount in zip(stockNameCol, stockPurchasePrice):
        stockInfo = AWS_EMAIL2()
        stockInfo.setStockInfo(stock, float(stockAmount))
        #if stock is equal to or greater than 20% send email to notify.
        if stockInfo.getCurrentPrice() >= stockInfo.getFlipPrice():
            stockInfo.stockReturn()

            




import os

from deta import Deta
from dotenv import load_dotenv

load_dotenv('.env')
DETA_KEY = os.getenv('DETA_KEY')

#Initialize with a project key
deta = Deta(DETA_KEY)

#This is how to create/connect a database
db = deta.Base('SBexpenses')

def insert_period(period, incomes, expenses):
    '''Returns the report on a successful creation, otherwise rais an error'''
    return db.put({'key': period, 'incomes': incomes,'expenses': expenses})

def fetch_all_periods():
    '''Return a dict of all periods'''
    res = db.fetch()
    return res.items

def get_period(period):
    '''If not found the function will return None'''
    return db.get(period)



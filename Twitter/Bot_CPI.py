#Import de twitter
import tweepy
import configparser
import time

#Import de Bybit
import requests
from pybit import HTTP
from pybit import usdt_perpetual
import os
from dotenv import load_dotenv
load_dotenv()

#Claves de Bybit
API_KEY1 = os.getenv('API_KEY')
API_KEY_SECRET1 = os.getenv('API_KEY_SECRET')

#Claves de Twitter
config = configparser.RawConfigParser()
configFilePath = 'Twitter\config.ini'
config.read(configFilePath)

#Extraer claves de la API 
api_key =  config.get('twitter', 'api_key')
api_key_secret = config.get('twitter','api_key_secret')
access_token = config.get('twitter','access_token')
access_token_secret = config.get('twitter','access_token_secret')
bearer_token = config.get('twitter','bearer')

#Conectarse a bybit
sesion =  usdt_perpetual.HTTP('https://api.bybit.com',
            api_key=API_KEY1,
            api_secret=API_KEY_SECRET1)

#Definir orden de compra para ETHEREUM
def comprar():
    info =sesion.public_trading_records(symbol="ETHUSDT",limit=500)
    
    precio = info['result'][1]
    precio2=  precio['price']
    precio3=round(precio2- precio2*0.02,1)
    sesion.place_active_order(
            symbol="ETHUSDT",
            side="Buy",
            order_type="Market",
            qty=2,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss= precio3
            )

#Definir orden de venta para ETHEREUM
def vender():
    info =sesion.public_trading_records(symbol="ETHUSDT",limit=500)
    
    precio = info['result'][1]
    precio2=  precio['price']
    precio3=round(precio2+precio2*0.02,1)
    
    sesion.place_active_order(
            symbol="ETHUSDT",
            side="Sell",
            order_type="Market",
            qty=2,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss= precio3
            )
    

#Identificar la orden para hacer comprobaciones o para cancelarla  WIP
def get_Order(nombre):
    print(sesion.get_active_order(
    symbol=nombre))
    

#Crear cliente y autentificarse para acceder a la API
client = tweepy.Client(bearer_token,api_key,api_key_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key,api_key_secret,access_token,access_token_secret)
api =tweepy.API(auth,wait_on_rate_limit=True)


#Crear clase del streaming para funcionalidades
class MyStream(tweepy.StreamingClient):

    # Cuando el stream está conectado y en vivo
    def on_connect(self):

        print("Connected")


    # Esto es para hacer funciones cuando un tweet se detecte en el streaming
    def on_tweet(self, tweet):
        print(tweet.text)
        txt = tweet.text
        
        x1 = txt.split()
        for word in x1:
            if word.endswith('BPS'):
                print(word)
                core = word.replace('BPS','')
                print(core)
                if 0 <= core.find('75'):
                    vender()
                if 0 <= core.find('50'):
                    print('nada')
                if 0 <= core.find('25'):
                    comprar()
                
        
                    
stream = MyStream(bearer_token=bearer_token)

#Coger id de usuarios EJEMPLO
tree_of_alpha = client.get_user(username='Tree_of_Alpha').data.id
joel = client.get_user(username='TwitterEspana').data.id


#Eliminando reglas anteriores para que no se acumulen
print(stream.get_rules())

previousRules = stream.get_rules().data
if previousRules:
    stream.delete_rules(previousRules)

print(stream.get_rules())

#Añadiendo regla (Buscando tweets de cuenta indicada)
stream.add_rules(tweepy.StreamRule('from:TwitterEspana OR from:Tree_of_Alpha'))
print(stream.get_rules())

# Starting stream
stream.filter()





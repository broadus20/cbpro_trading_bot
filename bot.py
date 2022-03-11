import cbpro
from time import sleep
from data import Sandbox_KEY, Sandbox_PASSPHRASE, Sandbox_SECRET, percentage_change

client = cbpro.PublicClient()

BTC = 'BTC-USD'

#Login
auth_client = cbpro.AuthenticatedClient(Sandbox_KEY, Sandbox_SECRET, Sandbox_PASSPHRASE,
                                  api_url="https://api-public.sandbox.pro.coinbase.com")

BTC_price = float(list(client.get_product_ticker(product_id= BTC).values())[1]) #BTC Price
print(f'BTC is {BTC_price}')

BTC_data = client.get_product_historic_rates(BTC, start=None, end=None,
                                   granularity= None) #BTC Data

#**************************DATA FUNCTIONS***************************************

#find VWAP (sumprice * vol)/sumvol
def VWAP():
	i = 1
	cumsum = 0.0
	for item in BTC_data:
		cumsum = (cumsum + item[5])

		i +=1

	sumvol = cumsum

	i = 1

	cumsum = 0.0
	for item in BTC_data:
		cumsum = (cumsum + item[1])

		i +=1
	sumprice = cumsum

#	print(f'BTC sum volume: \n {sumvol}')
#	print(f'BTC sum price: \n {sumprice}')
#	print(f'BTC is {BTC_price[1]}')
#	print(f'BTC VWAP: \n {(float(sumprice) * float(BTC_price[1]))/float(sumvol)}')

#data 
def Data():
	return VWAP()

Data()

#*************BUY AND SELL FUNCTIONS***********************
#buy standard 
#auth_client.buy(price = user_limit_order)


# Buy with limit order
'''auth_client.place_limit_order(product_id='BTC-USD', 
                              side='buy', 
                              price= , 
                              size='0.01')

#sell limit order
auth_client.sell(price = user_sell)
'''
#*************************FUNCTIONALITY********************
start_price = BTC_price

#Take user input
purchasePrice = float(input("Enter a price for your Bitcoin limit order (USD): "))
purchaseSpent = float(input("Enter how much you want to spend (USD): "))

#Creating the loop
while(True): 

	percentage_gainloss = percentage_change(start_price, BTC_price)
	coin_purchased = purchaseSpent/BTC_price

	print('Bitcoin is ' + str(BTC_price) + '\nPercent change in last 60 seconds: ' + format(percentage_gainloss, ".3f") + '%')

	#Within Purchase Threshold
	if(float(BTC_price) <= float(purchasePrice)):
		#***********************************************PURCHASE FUNCTION**************************************************
		auth_client.place_market_order(product_id=BTC, side='buy', funds=str(purchaseSpent))
		#******************************************************************************************************************

		print("Bought $" + str(purchaseSpent) + " or " + str(coin_purchased) + " bitcoin at " + str(purchasePrice))

	sleep(60)

	#Update start_price
	start_price = float(list(client.get_product_ticker(product_id= BTC).values())[1])

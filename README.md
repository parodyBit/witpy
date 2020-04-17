witnet_client_py



witnet_client_py is a library for interfacing with the Witnet protocol. ( See [Witnet.io](https://witnet.io/) for more information )





Built on top of websockets and jsonrpcclient, it provides an easy way to automate wallet operations by node operators and any one else who might find it useful.



*Disclaimer:*

This is a work in progress and under development and not intended to function as your main witnet wallet.





Quick Install:

```
$ pip install -r requirements.txt
```



Until I work this into an actual package, just copy the witnet_client_py folder into your project.



Usage:

Must have a Witnet node running. See the [Github](https://github.com/witnet) for more information. 



The `WalletClient` is a singleton and can be retrieved by:

```
from witnet_client_py import WalletClient

client = WalletClient.socket(url='127.0.0.1', port=11212)

```

 

All the functions in `witnet_client_py/wallet/client.py` act as a direct passthrough of the json-rpc API provided by the Witnet wallet server. The json-rpc `"method":` is called as a client function with the `"params":` being keyword arguments `**kwargs`. It returns the raw json-rpc response from the wallet server.

An example of requests:

```
from witnet_client_py import FILTERS, REDUCERS
import witnet_client_py as witnet

wallet_id = 'my-wallet-id'
session_id = client.unlock_wallet(wallet_id=wallet_id, password='secret')['session_id']


#
client = witnet.WalletClient.socket('127.0.0.1', port=11212)
bitstamp = witnet.Source('https://www.bitstamp.net/api/ticker/')
bitstamp.parse_map_json().get_float('last').multiply(1000).round()

blockchain = witnet.Source('https://blockchain.info/ticker')
blockchain.parse_map_json().get_map('USD').get_float('last').multiply(1000).round()

coindesk = witnet.Source('https://api.coindesk.com/v1/bpi/currentprice.json')
coindesk.parse_map_json().get_map('bpi').get_map('USD').get_float('rate_float').multiply(1000).round()
print()
# Set aggregator and Tally
aggregator = witnet.Aggregator(filters=[[witnet.FILTERS.deviation_standard, 1.5]], reducer=witnet.REDUCERS.average_mean)
tally = witnet.Tally(filters=[[witnet.FILTERS.deviation_standard, 1]], reducer=witnet.REDUCERS.average_mean)

# Test Radon
rad_request = witnet.RadRequest().add_source(bitstamp).add_source(blockchain).add_source(coindesk)
rad_request.set_aggregate(aggregator).set_tally(tally)
rad = client.run_rad_request(rad_request=rad_request.to_json())
print(rad)

# Test Data Request
data_request = witnet.Request().add_source(bitstamp).add_source(blockchain).add_source(coindesk)
data_request.set_aggregate(aggregator).set_tally(tally).set_quorum(20, 5, 2, 2, 51).set_fees(1, 1, 1, 1).schedule(0)
print(data_request.to_json())

# Create and Send Transaction
# trx = client.create_data_request(wallet_id=wallet_id, session_id=session_id, request=data_request.to_json(), fee=1)
# print(trx)
# print(trx['transaction'])

# resp = client.send_transaction(wallet_id=wallet_id, session_id=session_id, transaction=trx['transaction'])
# print(resp)
```



# witpy

[![Build Status](https://travis-ci.org/parodyBit/witpy.svg?branch=master)](https://travis-ci.org/parodyBit/witpy)

witpy is a library for interfacing with the Witnet protocol. ( See [Witnet.io](https://witnet.io/) for more information )

Built on top of websockets and jsonrpcclient, it provides an easy way to automate wallet operations by node operators and any one else who might find it useful.



Quick Install:

`> pip install witpy`



Consider using virtualenv:

```
> sudo apt-get install virtualenv
> virtualenv env
> source env/bin/activate
(env) > pip install witpy
```



Usage:

Must have a Witnet node and wallet server running. See the [Github](https://github.com/witnet) for more information. 



The `WalletClient` is a singleton and can be retrieved by:

```
from witpy.wallet import WalletClient

client = WalletClient.socket(url='127.0.0.1', port=11212)

```
All the functions in `witpy/wallet/client.py` act as a direct passthrough of the json-rpc API provided by the Witnet wallet server. The json-rpc `"method":` is called as a client function with the `"params":` being keyword arguments `**kwargs`. It returns the raw json-rpc response from the wallet server.

An example of requests:
```
from witpy.wallet import WalletClient
from witpy.radon.types import FILTERS, REDUCERS, TYPES
from witpy.radon.script import Script, Source, Aggregator, Tally

from witpy.transactions.data_request import DataRequest as Request
from witpy.transactions.rad_request import RadRequest

wallet_id = 'my-wallet-id'
session_id = client.unlock_wallet(wallet_id=wallet_id, password='secret')['session_id']


#
client = WalletClient.socket('127.0.0.1', port=11212)
bitstamp = Source('https://www.bitstamp.net/api/ticker/')
bitstamp.parse_map_json().get_float('last').multiply(1000).round()

blockchain = Source('https://blockchain.info/ticker')
blockchain.parse_map_json().get_map('USD').get_float('last').multiply(1000).round()

coindesk = Source('https://api.coindesk.com/v1/bpi/currentprice.json')
coindesk.parse_map_json().get_map('bpi').get_map('USD').get_float('rate_float').multiply(1000).round()
print()
# Set aggregator and Tally
aggregator = Aggregator(filters=[[witnet.FILTERS.deviation_standard, 1.5]], reducer=REDUCERS.average_mean)
tally = Tally(filters=[[FILTERS.deviation_standard, 1]], reducer=REDUCERS.average_mean)

# Test Radon
rad_request = RadRequest().add_source(bitstamp).add_source(blockchain).add_source(coindesk)
rad_request.set_aggregate(aggregator).set_tally(tally)
rad = client.run_rad_request(rad_request=rad_request.to_json())
print(rad)

# Test Data Request
data_request = Request().add_source(bitstamp).add_source(blockchain).add_source(coindesk)
data_request.set_aggregate(aggregator).set_tally(tally).set_quorum(20, 5, 2, 2, 51).set_fees(1, 1, 1, 1).schedule(0)
print(data_request.to_json())

# Create and Send Transaction
# trx = client.create_data_request(wallet_id=wallet_id, session_id=session_id, request=data_request.to_json(), fee=1)
# print(trx)
# print(trx['transaction'])

# resp = client.send_transaction(wallet_id=wallet_id, session_id=session_id, transaction=trx['transaction'])
# print(resp)
```







---

Disclaimer:*

`witpy` is provided on an "as is" basis without any warranties of any kind regarding any content, data, materials and/or services provided by this library.  In no event shall the owners of, or contributors to, `witpy` be liable for any damages of any kind, including, but not limited to, loss of use, loss of profits, or loss of data arising out of or in any way connected with the use of the `witpy` library.


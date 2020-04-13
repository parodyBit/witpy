# witnet_client_py



witnet_client_py is a library for interfacing with the Witnet protocol. ( See [Witnet.io](https://witnet.io/) for more information )





Built on top of websockets and jsonrpcclient, it provides an easy way to automate wallet operations by node operators and any one else who might find it useful.



*Disclaimer:*

This is a work in progress and under development and not intended to function as your main witnet wallet.



Install:

Until I work this into an actual package, just copy the witnet_client_py folder into your project.



Usage:

Must have a Witnet node running. See the [Github](https://github.com/witnet) for more information. 

```
witnet node server
witnet wallet server 
```

The `WalletClient` is a singleton and can be retrieved by:

```
from witnet_client_py import WalletClient

client = WalletClient.socket(url='127.0.0.1', port=11212)

```

 

All the functions in `witnet_client_py/wallet/client.py` act as a direct passthrough of the json-rpc API provided by the Witnet wallet server. The json-rpc `"method":` is called as a client function with the `"params":` being keyword arguments `**kwargs`. It returns the raw json-rpc response from the wallet server.

An example of requests:

```
from witnet_client_py import WalletClient, RadRequest, script_from_str

wallet_id = 'my-wallet-id'
session_id = client.unlock_wallet(wallet_id=wallet_id, password='secret')['session_id']

rad_request = RadRequest()

ticker1 = script_from_str('parseMapJSON().getFloat("last")')
rad_request.add_script(kind='HTTP-GET', url='https://www.bitstamp.net/api/ticker/', script=ticker1.encode())

ticker2 = script_from_str('parseMapJSON().getMap("USD").getFloat("last")')
rad_request.add_script(kind='HTTP-GET', url='https://blockchain.info/ticker', script=ticker2.encode())

ticker3 = script_from_str('parseMapJSON().getMap("bpi").getMap("USD").getFloat("rate_float")')
rad_request.add_script( kind='HTTP-GET', url='https://api.coindesk.com/v1/bpi/currentprice.json', script=ticker3.encode())


rad = client.run_rad_request(rad_request=rad_request.to_json())
print(rad)

request = {
    'data_request': rad_request.to_json(),
    'witness_reward': 1000,
    'witnesses': 20,
    'backup_witnesses': 5,
    'commit_fee': 1,
    'reveal_fee': 1,
    'tally_fee': 1,
    'extra_commit_rounds': 3,
    'extra_reveal_rounds': 3,
    'min_consensus_percentage': 51
}

data_request = client.create_data_request(session_id=session_id, wallet_id=wallet_id, request=request, fee=1)
print(data_request)

response = client.send_transaction(session_id=session_id, wallet_id=wallet_id, transaction=data_request['transaction'])
print(data_request)







```



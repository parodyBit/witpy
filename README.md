# witnet_client_py



witnet_client_py is a library for interfacing with the Witnet protocol. ( See [Witnet.io](https://witnet.io/) for more information )

Built on top of websockets and jsonrpcclient, it provides an easy way to automate wallet operations by node operators and any one else who might find it useful.



*Disclaimer:*

This is a work in progress and under development and not intended to function as your main witnet wallet.





Dependencies:A Witnet node running with  

```
pip install websockets
pip install jsonrpcclient
```



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
from witnet_client_py import WalletClient, RadRequest


rad_request = RadRequest()
ticker = script_from_str('parseMapJSON().getFloat("open")')
current_price = script_from_str('parseMapJSON().getMap("bpi").getMap("USD").getFloat("rate_float")')

rad_request.add_script(kind='HTTP-GET',
                       url='https://www.bitstamp.net/api/ticker/',
                       script=ticker.encode())

rad_request.add_script(kind='HTTP-GET',
                       url='https://api.coindesk.com/v1/bpi/currentprice.json',
                       script=current_price.encode())
rad = client.run_rad_request(rad_request=rad_request.to_json())
print(rad)





```



Output:

```

{'result': 'RadonReport { metadata: Tally(TallyMetaData { liars: [false], consensus: 0.0 }), result: Float(RadonFloat { value: 6856.26085 }), running_time: 21.4µs }'}
```




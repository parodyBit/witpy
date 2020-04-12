---
`



# Witnet JSON RPC API

---



# Wallet

## Methods

| Method Name                                             |
| ------------------------------------------------------- |
| [get_wallet_infos](#get_wallet_infos)                   |
| [create_mnemonics](#create_mnemonics)                   |
| [validate_mnemonics](#validate_mnemonics)               |
| [import_seed](#import_seed)                             |
| [create_wallet](#create_wallet)                         |
| [update_wallet](#update_wallet)                         |
| [unlock_wallet](#unlock_wallet)                         |
| [lock_wallet](#lock_wallet)                             |
| [create_vtt](#create_vtt)                               |
| [run_rad_request](#run_rad_request)                     |
| [close_session](#close_session)                         |
| [subscribe_notifications](#subscribe_notifications)     |
| [unsubscribe_notifications](#unsubscribe_notifications) |
| [get_transactions](#get_transactions)                   |
| [send_transaction](#send_transaction)                   |
| [generate_address](#generate_address)                   |
| [fund_address](#fund_address)                           |
| [create_data_request](#create_data_request)             |
| [get_balance](#get_balance)                             |
| Forwarded Requests                                      |



## create_mnemonics

### Description

The JsonRPC method `create_mnemonics` is used to generate a [BIP39 mnemonic sentence](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) that can be used to generate a new [HD wallet](https://en.bitcoinwiki.org/wiki/Deterministic_wallet).

### Request Parameters

```
{
	"length": <length>
}
```

Where:

- `<length>` : Is an integer indicating how many words the mnemonic sentence should have. Must be one of these: `12`, `15`, `18`, `21` or `24`.

### Example

#### Request

```
{
  	"jsonrpc": "2.0",
  	"method": "create_mnemonics",
  	"params": { 
  		"length": 12 
  	},
  	"id": 1
}
```

#### Response

```
{
  	"jsonrpc": "2.0",
  	"result": {
    	"mnemonics": "day voice lake monkey suit bread occur own cattle visit object ordinary"
  	},
  	"id": 1
}
```



---

## validate_mnemonics

### Description

The JsonRPC method `validate_mnemonics` is used to validate that the mnemonic sentence along with the password generate a wallet.

### Request Parameters

```
{
	"mnemonics": <mnemonics>,
	"xprv": <seed source>
}
```

Where:

- `<mnemonics>` : Is a string containing the mnemonic sentence used for import. Must be a word length of: `12`, `15`, `18`, `21` or `24`.
- `<seed source>` : Is the xprv string containing the password used.

### Example

#### Request

```
{
  "jsonrpc": "2.0",
  "method": "validate_mnemonics",
  "params": { 
  	"mnemonics": "day voice lake 
  				monkey suit bread 
  				occur own cattle 
  				visit object ordinary" 
  },
  "id": 1
}
```

#### Response

```
{
  "jsonrpc": "2.0",
  "result": {
  	null
  },
  "id": 1
}
```



---

## import_seed

### Description

The JsonRPC method `import_seed` is used to import a mnemonic sentence to recover wallet addresses.

### Request Parameters

```
{
	"mnemonics": <mnemonics>
	"seed": <seed>
}
```

Where:

- `<mnemonics>` : Is a string containing the mnemonic sentence used for import. Must be word length of: `12`, `15`, `18`, `21` or `24`.
- `<seed>` : Is a string used as a password to unlock the wallet being created from the import.

### Example

#### Request

```
{
  "jsonrpc": "2.0",
  "method": "import_seed",
  "params": { 
  	"mnemonics": "day voice lake 
  				monkey suit bread 
  				occur own cattle 
  				visit object ordinary",
  	"seed": "12345678"
  },
  "id": 1
}
```



#### Response

```
{
  "jsonrpc": "2.0",
  "result": {
  	null
  },
  "id": 1
}
```



## create_wallet

### Description

The JsonRPC method `create_wallet` is used to generate a new Master Key for an empty [HD wallet](https://en.bitcoinwiki.org/wiki/Deterministic_wallet) that is stored encrypted in the file system.

### Request Parameters

```
{
    "name": "<name>",
    "caption": "<caption>",
    "password": "<password>",
    "seed_source": "<seed source>",
    "seed_data": "<seed data>",
}
```

Where:

- `<name>` : Is a human-friendly name for your the wallet. This param is optional.
- `<caption>` : Is a human-friendly caption for your the wallet. This param is optional.
- `<password>` : Is the password that will seed the key used to encrypt the wallet in the file system. The password must have at least eight characters.
- `<seed source>` : Must be `mnemonics` or `xprv` and determines how the HD wallet master key will be generated from the data sent in the `seedData` param.
- `<seed data>` : The data used for generating the new HD wallet master key.

### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "create_wallet",
  	"params": {
    	"seedData": "exotic demand way fatigue 
    				skull poverty happy divide 
    				scrub seed jeans novel",
    	"seedSource": "mnemonics",
    	"password": "12345678"
  	},
  	"id": 1
}
```

#### Response

```
{
  "jsonrpc": "2.0",
  "result": {
    "wallet_id": "6c344625884c2f910065ab170dc18ad3cbbc03c7234507c7c22dbd78e3b26667"
  },
  "id": 1
}
```

Where:

- `"wallet_id":` 

---

## update_wallet

### Description

The JsonRPC method `update_wallet` is used to update the name and/or caption of an existing wallet. 

### Request Parameters

```
{
	"session_id": <session id>
	"wallet_id": <wallet id>
	"name": <name>
	"caption": <caption>
}
```

Where:

- `<name>` : Is a human-friendly name for your the wallet. This param is optional.
- `<caption>` : Is a human-friendly caption for your the wallet. This param is optional.
- `<wallet id>` : *String*. Is the ID associated to the wallet. See [get_wallet_infos](#get-wallet-infos).
- `<session id>` : is the string obtained from from unlocking the wallet. See [Unlock Wallet](#unlock_wallet).

### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "",
  	"params": {
  	
  	},
  	"id": 1
}
```

#### Response

```

```



----





## unlock_wallet

### Description

The JsonRPC method `unlock_wallet` is used to *unlock* the wallet with the specified id. What does it mean to *unlock a wallet*? It means that the decryption key for that wallet will be hold in memory until the wallet is locked again. As long as a wallet is unlocked, you can operate it without having to supply the password again using the session id until it expires, and its state can be automatically updated with the information received from the Witnet network (through the connected Witnet node - see [Wallet configuration](#wallet_configuration)).

### Request Parameters

```
{
  "wallet_id": "<wallet id>",
  "password": "<password>",
}
```

Where:

- `<wallet id>` : *String*. Is the ID associated to the wallet. See [get_wallet_infos](#get-wallet-infos).
- `<password>` : *String*. The password that unlocks the wallet.

### Example

#### Request

```
{
  "jsonrpc": "2.0",
  "method": "unlock_wallet",
  "params": {
    "wallet_id": "389a3fa3a1feb8fd8cdc61748ac17dce0aeef39ff9634dec9c20ece69105c264",
    "password": "12345678"
  }
  "id": 1
}
```

#### Response

```
{
  "jsonrpc": "2.0",
  "result": {
  	"account_balance": 0,
  	"available_accounts": [0],
  	"caption": "test caption",
  	"current_account": 0,
  	"name": "default",
  	"session_on_expiration_secs": 3200,
    "session_id": "8af3ab77054d05c5059b006c8fa285e0e44c2f90a13fecf1ba62f4d06856b11b"
  },
  "id": 1
}
```

----

## lock_wallet

### Description

The JsonRPC method `lock_wallet` is used to *lock* the wallet with the specified id and close the active session. What does it mean to *lock a wallet*? It means that the decryption key for that wallet that is being hold in memory is forgotten and the Wallet server will be unable to update that wallet information until it is unlocked again.

### Request Parameters

```
{
  "wallet_id": "<wallet id>",
  "sessionId": "<session id>"
}
```

Where:

- `<wallet id>` : *String*. Is the ID associated to the wallet. See [get_wallet_infos](#get-wallet-infos).
- `<session id>` : *String*. The session ID assigned to you when you unlocked the wallet. See [unlock_wallet](#unlock_wallet).

### Example

#### Request

```
{
	"jsonrpc": "2.0",
  	"method": "lock_wallet",
  	"params": {
    	"wallet_id": "81ccbf4548cfeba37cef93dc64e7f0d8fb410e3967bb40160a36aa362943c520",
    	"session_id": "9fa1d779afea88a29768dd05647e37b2f64fc103c1081b0ee9e62fb283f5cd02"
  	},
  	"id": "1",
}
```

#### Response

```
{
	"jsonrpc": "2.0",
  	"result": null,
  	"id": "1"
}
```

---

## get_wallet_infos

### Description

The JsonRPC method `get_wallet_infos` returns a list of all wallets with names and captions stored on the wallet server database.

### Example

#### Request

```
{
	"jsonrpc": "2.0",
  	"method": "get_wallet_infos",
  	"id": 1
}
```

#### Response

```
{
	"jsonrpc": "2.0",
  	"result": 
  	{
  		"infos": 
  		[
  			{
  				"caption":null, 
  				"id":"81ccbf4548cfeba37cef93dc64e7f0d8fb410e3967bb40160a36aa362943c520",
  				"name":null
  			},
  			{
  				"caption":"caption text",
  				"id":"9fa1d779afea88a29768dd05647e37b2f64fc103c1081b0ee9e62fb283f5cd02",
  				"name":"wallet name"
  			}		
  		]
  	},
  	"id": 1
}
```

Where:

- `"infos":[]`  *Array*. Is a list containing all wallets on the server.
-  `"id":` *String*. Is the ID associated with the given wallet in the `"infos":[]` list. 
- `"name":` *String*. is the human-friendly name for the given wallet.
- `"caption":` *String*. is the human-friendly caption for the given wallet.





## create_vtt

### Description

TODO

### Request Parameters

```
{
	"session_id": <session id>
	"wallet_id": <wallet id>
	"address": <public address>
	"amount": <value>
	"fee": <fee>
	"time_lock": <time lock>
}
```

Where:

- `<wallet id>` : *String*. Is the ID associated to the wallet. See [get_wallet_infos](#get-wallet-infos).
- `<session id>` :*String*. The session ID assigned to you when you unlocked the wallet. See [unlock_wallet](#unlock-wallet).

- `<pkh> `: destination public key hash
- `<value> `:
- <fee> :
- <time lock> :

### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "",
  	"params": {
  	},
  	"id": "<jsonrpc request id>",
}
```

#### Response

```
{
	"jsonrpc":"2.0",
	"result: {  	
		"bytes":"<hash bytes>",
		"metadata": { 
			"fee":434,
			"to":"twit10v8een22jyynl5jhj5ysn3y5jyf85c7lkq46ke",
			"value":10
		},
		"transaction": {
			"ValueTransfer": {
				"body": {
					"inputs" :  [{
						"output_pointer":"15980302bbcb11765bb4301eae2ddbdb0fbb8062df30918bedd4d38db29cd590:0"
					}],
					"outputs" : [{					"pkh":"twit10v8een22jyynl5jhj5ysn3y5jyf85c7lkq46ke","time_lock":0,"value":10},{"pkh":"twit1tz558gm0vt5lcwgkhahfftk7nmgrp5976xzxw0","time_lock":0,"value":89}]},"signatures":[{"public_key":{"bytes":[151,249,231,239,172,189,198,114,141,77,204,208,237,174,28,183,64,206,170,221,234,146,175,83,38,109,56,108,205,108,130,187],"compressed":2},"signature":{"Secp256k1":{"der":[48,69,2,33,0,141,84,239,37,145,146,155,20,60,126,90,196,111,65,233,143,44,174,63,53,118,95,55,19,48,55,5,199,206,92,60,14,2,32,45,33,104,68,1,142,82,89,245,44,100,4,66,52,100,14,230,199,226,119,94,115,124,94,164,139,141,197,180,214,144,186]}}}]}},"transaction_id":"ef463d68d9bb80f4fe721b6a7aa65561271a2ecb33e6d3cf18c38e1d44cee5ff"},"id":4}
}
```



---

## run_rad_request

### Description

The JsonRPC method `run_rad_request` can be used to execute a [RAD request](https://docs.witnet.io/protocol/data-requests/overview/) in order to test it functionally before deploying it on the network.

### Request Parameters

```
{
	"jsonrpc": "2.0"
  	"method": "run_rad_request",
  	"params": {
    	"radRequest": {
      	"retrieve": [
          	<retrieve object>, ...
      	],
      	"aggregate": {
        	"filters": [<filter object>, ...],
        	"reducer": <reducer>
      	},
      	"tally": {
        	"filters": [<filter object>, ...],
        	"reducer": <reducer>
      	},
      	"time_lock": <epoch>
    	}
  	},
  	"id": 1,
}
```

Where:

- <retrieve object> is:

```
{
  "kind": "<method>",
  "url": "<url>",
  "script": <script text>
}
```

- <filter object> is:

```
{
  "op": "<filter operator>",
  "args": "[<filter arguments>]"
}
```

- <script text> :  is the the bytes-serialized RADON script, e.g.: `[152, 83, ...]`.

- <url> : is an url, e.g.: `https://api.coindesk.com/v1/bpi/currentprice.json`.

- <method> : is a supported retrieve method, e.g.: `HTTP-GET`

- `<epoch>` : is an integer indicating that the data request shouldn't run before that epoch, this parameter is ignored by the this API method.

- <filter operator> is an integer indicating the operator to be used for the filter operation.

- <filter arguments> : is an array of bytes representing the arguments used in the aforementioned filter operator.

### Example

#### Request

```
{
  	"jsonrpc": "2.0"
  	"method": "run_rad_request",
  	"params": {
    	"radRequest": {
        	"time_lock": 0,
        	"retrieve": [{
            	"kind": "HTTP-GET",
            	"url": 	"https://csrng.net/csrng/csrng.php?min=0&max=100",
            	"script": [
            		131, 
            		24, 
            		118, 
            		130, 
            		24, 
            		24, 
            		0, 
            		130, 
            		24, 
            		100, 
            		102, 
            		114, 
            		97, 
            		110, 
            		100,
            		111, 
            		109]
            	}
            ],
        	"aggregate": {
          		"filters": [],
          		"reducer": 3
          	},
        	"tally": {
          		"filters": [{"op": 5,"args": [249,60,0]}],
          		"reducer": 3
          	},
          	"time_lock": 0
  		},
  	"id": 1
}
```

#### Response

```
{
  	"jsonrpc": "2.0",
  	"result":
    	"RadonReport: {
      		metadata: Tally(
      			TallyMetaData {
      				liars: [false], consensus: 1.0
      			}
      		),
    		report: Float(RadonFloat {value: 42.0}),
    		running_time: 57.8µs
  	}"
  	"id": 1
}
```

---

## close_session

### Description

The JsonRPC method `close_session` is used to close an active session without locking the currently unlocked wallet.

### Request Parameters

```
{
  "session_id": "<session id>",
}
```

Where:

<session id>: *String*. The session ID assigned to you when you unlocked the wallet. See [unlock_wallet](#unlock_wallet)

### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "close_session",
  	"params": {
    	"session_id": "9fa1d779afea88a29768dd05647e37b2f64fc103c1081b0ee9e62fb283f5cd02"
  	},
  	"id": "1"
}
```

#### Response

```
{
  "jsonrpc": "2.0",
  "result": null,
  "id": "1"
}
```

---

## subscribe_notifications

### Description

TODO

Use this method `subscribe_notifications` to subscribe to update events related to your session wallets.

### Request Parameters

```
{
  "session_id": "<session id>"
}
```

Where:

- `<session id>` : *String*. The session ID assigned to you when you unlocked the wallet. See [unlock_wallet](#unlock_wallet)

### Example

#### Request

```
{
	"jsonrpc": "2.0"
  	"params":{
  		"method": "subscribe_notifications",
    	"session_id": "9fa1d779afea88a29768dd05647e37b2f64fc103c1081b0ee9e62fb283f5cd02"
  	},
  	"id": "1",
}
```

#### Response

```
{
	"jsonrpc": "2.0",
  	"result": "9fa1d779afea88a29768dd05647e37b2f64fc103c1081b0ee9e62fb283f5cd02",
  	"id": "1"
}
```

Where:

- `result`: Subscription id that you can use to unsubscribe from notifications. See [unsubscribe_notifications](#unsubscribe_notifications)

---

## unsubscribe_notifications

### Description

TODO

Use this method to unsubscribe to update events related to your session wallets. TODO

### Request Parameters

```
{
	"id": <subscription id>
}
```

Where:

- `<subscription id>` : The subscription id you received when you subscribed. See [subscribe_notifications](#subscribe_notifications)

### Example

#### Request

```
{
 	"jsonrpc": "2.0",
 	"method": "unsubscribe_notifications",
  	"params": ["c3f1a347a4b0bfac9ed4ac1a8b93bce1ae13606be427b81dafad05716b30a9c4"],
  	"id": "1",
 
}
```

#### Response

```
{
	"jsonrpc": "2.0,
  	"result": null,
  	"id": "1"
}
```

Where:

- `result`:

---

## get_transactions

### Description

TODO

### Request Parameters

```
{
  	"session_id": <session id>
  	"wallet_id": <wallet id>
  	"offset": <offset>
  	"limit": <limit>
}
```



### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "get_transactions",
  	"params": {
  		"session_id": 9fa1d779afea88a29768dd05647e37b2f64fc103c1081b0ee9e62fb283f5cd02,
  		"wallet_id": 81ccbf4548cfeba37cef93dc64e7f0d8fb410e3967bb40160a36aa362943c520,
  		"offset": 0,
  		"limit": 0  	
  	},
  	"id": 1,
}
```

#### Response

```
{
	"jsonrpc": "2.0,
  	"result": 
  	{
  		"total": 0,
  		"transactions":[]
  	},
  	"id": 1
}
```



---

## send_transaction

### Description

TODO

The JsonRPC method `send_transaction` is used to ...

### Request Parameters

```
{
	"session_id": <session id>
	"wallet_id": <wallet id>
	"transaction": <transaction>
}
```

Where:

- `<wallet id>` : *String*. Is the ID associated to the wallet. See [get_wallet_infos](#get-wallet-infos).
- `<session id>` :*String*. The session ID assigned to you when you unlocked the wallet. See [unlock_wallet](#unlock-wallet).

### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "send_transaction",
  	"params": {
  	
  	},
  	"id": "<jsonrpc request id>",
}
```

#### Response

```
{
	"jsonrpc": "2.0,
  	"result": null,
  	"id": 1
}
```



---

## generate_address

### Description

The JsonRPC method `generate_address` is used to generate an address for the given wallet and session id.

### Request Parameters

```
{
	"session_id": <session id>
	"wallet_id": <wallet id>
}
```

Where:

- `<session id>` :
- `<wallet id>` :



### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "generate_address",
  	"params": {
  		"session_id":
  		"wallet_id":
  	},
  	"id": "<jsonrpc request id>",
}
```

#### Response

```
{
	"jsonrpc": "2.0,
  	"result": {
  		"address": "twit0000000133779pv7ft2ghdqfqf4388gtjcu7kec",
  		"path": "m/3'/4919'/0'/0/0"
  	},
  	"id": 1
}
```

---



---

## get_addresses

### Description

The JsonRPC method `get_addresses` is used to generate an address for the given wallet and session id.

### Request Parameters

```
{
	"session_id": <session id>
	"wallet_id": <wallet id>
	"limit": <limit>
}
```

Where:

- `<session id>` :
- `<wallet id>` : 
- `<limit>` :



### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "get_addresses",
  	"params": {
  		"session_id": "<session id>"
  		"wallet_id": "<wallet id>"
  		"limit": 0
  	},
  	"id": "<jsonrpc request id>",
}
```

#### Response

```
{
	"jsonrpc": "2.0,
  	"result": null,
  	"id": "1"
}
```

---

## fund_addresses

### Description

The JsonRPC method `fund_addresses` is used

### Request Parameters

### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "fund_addresses",
  	"params": {
  		"pkh_value": {
  			"pkh": 
  			"value":
  			"time_lock":
  		}
  	
  	},
  	"id": "<jsonrpc request id>",
}
```

#### Response

```
{
	"jsonrpc": "2.0,
  	"result": null,
  	"id": "1"
}
```

---

## create_data_request

### Description

The JsonRPC method `create_data_request` is used to construct a Data Request.



### Request Parameters

```
{
	"session_id": <session id>
	"wallet_id": <wallet id>
	"request": {
  		"data_request": <rad request>
  		"witness_reward": <witness reward>
  		"witnesses": <witnesses>
  		"backup_witnesses": <backup witnesses>
  		"commit_fee": <commit fee>
  		"reveal_fee": <reveal fee>
  		"tally_fee": <tally fee>
  		"extra_commit_rounds": <extra commit>
  		"extra_reveal_rounds": <extra reveal>
  		"min_consensus_percentage": <min consensus>
  	}
  	"fee": <fee>
	
}
```

Where:

- `<session id>` :
- `<wallet id>` : 
- <rad request> :
- <witness reward> :
- <witnesses> : 
- <backup witnesses> :
- <commit fee> :
- <reveal fee> :
- <tally fee> :
- <extra commit> : 
- <min consensus> :

### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "create_data_request",
  	"params": {
  		"data_request": <rad request>
  		"witness_reward": <witness reward>
  		"witnesses": <witnesses>
  		"backup_witnesses": <backup witnesses>
  		"commit_fee": <commit fee>
  		"reveal_fee": <reveal fee>
  		"tally_fee": <tally fee>
  		"extra_commit_rounds": <extra commit>
  		"extra_reveal_rounds": <extra reveal>
  		"min_consensus_percentage": <min consensus>
  	},
  	"id": "<jsonrpc request id>",
}
```

#### Response

```
{
	"jsonrpc": "2.0,
  	"result": null,
  	"id": "1"
}
```



---

## get_balance

### Description

The JsonRPC method `get_balance` is used

### Request Parameters

```
{
	"session_id": <session id>
	"wallet_id": <wallet id>
}
```

### Example

#### Request

```
{
	"jsonrpc": "2.0",
	"method": "",
  	"params": {
  	
  	},
  	"id": "<jsonrpc request id>",
}
```

#### Response

```
{
	"jsonrpc": "2.0,
  	"result": null,
  	"id": "1"
}
```



---

## Forwarded Requests



---



### get_block

#### Description

The JsonRPC method `get_block` is used

#### Request Parameters

```
[ <block hash> ]
```

or

```
[{"SHA256":[<byte array>]}]
```

Where:

- <block hash>:
- <byte array>:



#### Example

##### Request

```
{"jsonrpc": "2.0","method": "get_block","params": ["738fbc13fd9697b1f4af805a202b8e72d297b6fdedbd88b231d843cf38321b1d"],
  	"id": <jsonrpc request id>,
}

{"jsonrpc": "2.0","method": "get_block","params": [
	{"SHA256":[255,198,135,145,253,40,66,175,226,220,119,243,233,210,25,119,171,217,215,188,185,190,93,116,164,234,217,67,30,102,205,46]}],
  	"id": <jsonrpc request id>,
}
```

##### Response

```
{
	"jsonrpc": "2.0,
  	"result": {
  		"block_header": {
  			"beacon": {
  				"checkpoint": <checkpoint>,
  				"hashPrevBlock": "<previous hash id>",
  			},
  			"merkle_roots": {
  				"commit_hash_merkle_root": "<commit hash>",
        		"dr_hash_merkle_root": "<dr hash>",
        		"mint_hash": "<mint hash>",
        		"reveal_hash_merkle_root": "<reveal hash>",
        		"tally_hash_merkle_root": "<tally hash>",
        		"vt_hash_merkle_root": "<vt hash>"
  			},
  			"proof": {
  				"proof": {
  					"proof": [<byte array>],
  					"public_key": {
  						"bytes": [<byte arra>],
  						"compressed": 2
  					}
  				}
  			},
  			"version": 0
  		},
  		"block_sig": {
  			"public_key": {
        		"bytes": [<public key byte array>],
  				"compressed": 2
  			},
  			"signature": {
  				"Secp256k1": {
  					"der": [<byte array>]
  				}
  			}
  		},
  		"txns": {
  			"commit_txns": [
  				"body":{
  					"commitment": "",
  					"dr_pointer": "",
  					"proof": {
  						"proof": {
  							"proof": [<proof byte array>],
  							"public_key": {
  								"bytes": [<public key byte array>],
  								"compressed": 2
  							}
  						}
  					}
  				},
  				"signatures": [{
  					"public_key": {
  						"bytes":[<public key byte array>],
  						"compressed": 2
  					},
  					"Secp256k1": {
  						"der": [<byte array>]
  					}	
  				}]
  			},
  			... 
  			],
  			"data_request_txns": [],
  			"mint": {
  				"epoch": 2048,
        		"output": {
         	 			"pkh": "twit0000123456789abcdefghijklmnopqrstuvwxyz",
         	 			"time_lock": 0,
         	 			"value": 500000000010
        			}
  				}
  			}
  			"reveal_txns": [],
  			"tally_txns": [],
  			"value_transfer_txns": []
  		}
	},	
  	"id": <jsonrpc request id>
}
```

Where:

- `"block_header":`
  - `"beacon":`
    - `<checkpoint>` :
    - `<previous hash id>` :
  - `"merkle_roots":`
    - <commit hash> :
    - <dr hash> :
    - <mint hash> :
    - <reveal hash> :
    - <tally hash> :
    - <vt hash> :
  - `"proof":`
    - `"proof":`
      - `"proof": []` is a byte array 
      - `"public_key":` 
        - <byte array> :
        - <compression> :
  - `"version":`
- `"block_sig":`
  - `"public_key":`
    - <byte array> :
    - <compression> :
  - `"signature":`
    - `"Secp256k1"`:
      - `"der":`
- `"txns":`
  - `"commit_txns":`
    - `"body":`
      - `"commitment":`
      - `"dr_pointer":`
      - `"proof":`
  - `"data_request_txns":`
  - `"reveal_txns":`
  - `"tally_txns":`
  - `"value_transfer_txns":`
  - `"mint":`
    - `"epoch":`
    - `"output":`
      - `"pkh":`
      - `"time_lock":`
      - `"value":`

---

### get_block_chain

#### Description

#### Request Parameters

```
{
	"epoch": <epoch>
	"limit": <limit>
}
```

Where:

- `<epoch>` :  the first epoch for which to show block hashes. A negative epoch means "n epochs ago".
- `<limit>` : the number of epochs. If zero, unlimited. A negative limit retrieves epochs previous to `epoch`.

#### Example

##### Request

```
{
	"jsonrpc": "2.0",
	"method": "get_block_chain",
  	"params": {
  		"epoch": 2048	
  		"limit": 2 
  	
  	},
  	"id": "<jsonrpc request id>",
}
```

##### Response

```
{
	"jsonrpc": "2.0,
  	"result": [
  		[2048,"2eaae746ab55939164d93fd95b07b01fd4a60b4f93a834b01840d47eb672a1e0"],
  		[2049,"71fd0003096e787b5cf0f7f241ce7a8dfb4b607130320f1e4c6a17170ed34182"]
  	],
  	"id": 1
}
```



---

### get_output

#### Description

#### Request Parameters

#### Example

##### Request

```
{
	"jsonrpc": "2.0",
	"method": "",
  	"params": {
  	
  	},
  	"id": "<jsonrpc request id>",
}
```

##### Response

```
{
	"jsonrpc": "2.0,
  	"result": null,
  	"id": "1"
}
```



---

### inventory

#### Description

#### Request Parameters

#### Example

##### Request

```
{
	"jsonrpc": "2.0",
	"method": "",
  	"params": {
  	
  	},
  	"id": "<jsonrpc request id>",
}
```

##### Response

```
{
	"jsonrpc": "2.0,
  	"result": null,
  	"id": "1"
}
```



# Wallet API Errors:

The Witnet Wallet API uses the [JsonRPC 2.0](https://www.jsonrpc.org/specification) protocol to receive requests and respond to clients.

Apart from the standard errors:

| code             | message          | meaning                                                      |
| ---------------- | ---------------- | ------------------------------------------------------------ |
| -32700           | Parse error      | Invalid JSON was received by the server. An error occurred on the server while parsing the JSON text. |
| -32600           | Invalid Request  | The JSON sent is not a valid Request object.                 |
| -32601           | Method not found | The method does not exist / is not available.                |
| -32602           | Invalid params   | Invalid method parameter(s).                                 |
| -32603           | Internal error   | Internal JSON-RPC error.                                     |
| -32000 to -32099 | Server error     | Reserved for implementation-defined server-errors.           |

the API may respond with three additional errors more, and extends the `Invalid params` response.

`Invalid params` extension

This extensions adds an additional `data` field to the standard error response containing a `schema` field that links to the wiki page describing the schema for the expected params, e.g.:

```
{
  "code": -32602,
  "message": "Invalid params: invalid type: null, expected struct CreateMnemonicsRequest.",
  "data": {
    "schema": "https://github.com/witnet/witnet-rust/wiki/Create-Mnemonics"
  }
}
```

Ideally this schema could be automatically generated, but we haven't found yet a way of doing it that we are happy with.

## Additional errors

The API might respond with these additional errors.

Apart from the standard errors:

| code | message          | meaning                                                      |
| ---- | ---------------- | ------------------------------------------------------------ |
| 400  | Validation Error | The request is formed correctly but some fields are not valid. |
| 401  | Unauthorized     | You need to authenticate, that is, you need a session id.    |
| 402  | Forbidden        | You have a session id but it cannot operate the given wallet. |
| 500  | Internal Error   | There was an unexpected error. This is probably a software bug. |
| 510  | Node Error       | Internal error in the context of talking to the node.        |

### 1. [500] Internal error

It means things went south and something we cannot handle happened, say: database files corrupted, network connection unavailable, or a bug. Here's an example of how such error looks like:

```
{
  "jsonrpc": "2.0",
  "error": {
    "code": 500,
    "message": "Internal error",
    "data": {
      "cause": "Storage error: failed to deserialize value from bincode: tag for enum is not valid, found 30"
    }
  },
  "id": "<request id>"
}
```

### 2. [510] Node error

It is similar to the `Internal error` above, but in the context of talking to a node, say: the node is not reachable, or a request to the node could not be sent, etc.

```
{
  "jsonrpc": "2.0",
  "error": {
    "code": 510,
    "message": "Node error",
    "data": {
      "cause": "Request timeout"
    }
  },
  "id": "<request id>"
}
```

Known causes:

- `"request failed: RPC error: Error { code: InternalError, message: "ItemNotFound", data: None }"`. An example of this would be calling `get_block` with an invalid block hash. 
- `"request failed: RPC error: Error { code: InternalError, message: "MailBoxError(Custom(\"invalid value: integer `3690880022`, expected variant index 0 <= i < 1\"))", data: None }"`. An example of this is passing a merkle root to the `get_block` method. 

### 3. [400] Validation error

Used for telling the client why its syntactically correct request isn't valid.

For example, in the `create_mnemonics` method, how many words the sentence should contain must be specified, but if the value used isn't one of the valid values, a validation error response is sent back indicating about the error:

Request:

```
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "create_mnemonics",
  "params": {
    "length": 9
  }
}
```

Validation error response:

```
{
  "jsonrpc": "2.0",
  "error": {
    "code": 400,
    "message": "Validation Error",
    "data": [
      [
        "length",
        "Invalid Mnemonics Length. Must be 12, 15, 18, 21 or 24"
      ]
    ]
  },
  "id": "1"
}
```



# Wallet Configuration

This page documents the configuration params one could tweak for running a wallet instance.







## Params

### testnet

`testnet = <true | false>`

*Default*: `false`

Whether or not this wallet runs in *testnet* mode or not. Running in testnet mode implies that the generated addresses are prefixed with *twit* (and **not wit**), and that the connected node, if configured, is running in testnet.

### server_addr

`server_addr = "<host>:<port>"`

*Default*: `127.0.0.1:11212`

The address of the Websockets server that exposes a JSON-RPC Api that can be used by clients of the wallet.

### db_path

`db_path = "<local path>"`

*Default:* `"$HOME/.local/share/witnet"`

Path where the database file (see `db_file_name` config param) is going to be stored. The default value depends on your platform:

- `$XDG_DATA_HOME/witnet/wallet.db` on **Gnu/Linux**
- `$HOME/Libary/Application\ Support/witnet/wallet.db` on **MacOS**
- `{FOLDERID_LocalAppData}/witnet/wallet.db` on **Windows**

If one of the above directories cannot be determined, the current path will be used.

### db_file_name 

`db_file_name = ""`

*Default:* `"witnet_wallet.db"`

The name to use for the directory representing the database.

### db_encrypt_hash_iterations 

`db_encrypt_hash_iterations = `

*Default:* `10000`

The number of hash iterations to use when deriving the key that will encrypt the data stored in the database.

### db_encrypt_iv_length 

`db_encrypt_iv_length = `

*Default:* `16`

The length of the initialization vector to use when deriving the key that will encrypt the data stored in the database.

### db_encrypt_salt_length 

`db_encrypt_salt_length = `

*Default:* `32`

The length of the [salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) to use when deriving the key that will encrypt the data stored in the database.

### seed_password 

`seed_password = []`

*Default:* `[]`

Password used to protect the Mnemonics used to derive the seeds of the generated HD-Wallets. See [BIP 39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)

### master_key_salt 

`master_key_salt = []`

*Default:* `[66, 105, 116, 99, 111, 105, 110, 32, 115, 101, 101, 100]`

The salt used when generating the seed used for the generated HD-Wallets.

### id_hash_iterations 

`id_hash_iterations = `

*Default:* `4096`

### id_hash_function 

`id_hash_function = ""`

*Default:* `Sha256`

### session_expires_in 

`session_expires_in = `

*Default:* `3200`

Number of seconds after which a client session expires.

### requests_timeout 

`requests_timeout = `

*Default:* `60000`

The timeout for requests sent from the wallet to the node.
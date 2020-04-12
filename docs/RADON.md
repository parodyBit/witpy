# Witnet requests

Witnet requests are the cornerstone of the Witnet protocol. They allow **clients** to have **witness** nodes **retrieve**, **aggregate** and **deliver** data on their behalf on demand.

## Request life cycle

Once a Witnet request has been published by a client, it will go through 4 distinct stages: ***retrieval\***, ***aggregation\*** and ***tally\*** . These stages are linear and constitute a single, unidirectional data flow.

```
╔═════════╗    ╔════════════════════════════╗    ╔═══════════╗
║ Client  ║    ║ Witnesses                  ║    ║ Miner     ║
╠═════════╣    ╠════════════════════════════╣    ╠═══════════╣
║ Publish ║ => ║ Retrieve => Aggregate      ║ => ║ Tally     ║
╚═════════╝    ╠────────────────────────────╣    ╚═══════════╝
               ║ Retrieve => Aggregate      ║
               ╠────────────────────────────╣
               ║ ... (as many as requested) ║
               ╚════════════════════════════╝
  

```

For the sake of deterministic execution, data flowing through the different stages is strongly typed. The type of a value or data structure defines the operations that can be done on the data.

For each stage, the data type of the input is the same as the data type of the output of previous stage. Particularly, the aggregation and tally stages gather multiple values or structures emitted by their precedent stages, so they always receive an `Array`, i.e. if the **retrieval** stage returned an `Integer`, the **aggregation** stage will start with an `Array`, that is, an array of `Integer`s.

For more information on data types, you can read the [RADON documentation](https://docs.witnet.io/protocol/data-requests/overview/#rad-object-notation-radon), which provides a detailed description of all the types and the operators they provide.

## The RAD Engine

The RAD Engine is the component in charge of processing Witnet requests. That is, coordinating retrieval, aggregation, tally and delivery of data strictly as specified in the requests.

All Witnet requests contain explicit instructions on what the RAD Engine must do during every stage. These instructions, specified using [**RAD Object Notation (RADON)**](https://docs.witnet.io/protocol/data-requests/overview/#rad-object-notation-radon), are interpreted by the RAD Engine.

Just in case you were wondering, *RAD* stands for *Retrieve*, *Aggregate* and *Deliver*.

## RAD Object Notation (RADON)

The RAD Object Notation (RADON) is a declarative, functional, strongly-typed, Non-Turing complete domain-specific language.

A RADON script is formed by a list of ordered calls (tuples of operator byte codes and arguments) that are sequentially interpreted and applied by the RAD Engine on the output of the previous call.

RADON scripts are encoded using [CBOR](https://cbor.io), a very efficient, compact and widely supported data structure encoding.

### Example:

This of a working RADON script.  

The example will retrieve a `Float` from a JSON file.

 ```
parseMapJSON().getFloat("last")		<- High Level
[0x77, [0x64, 'last']]			<- RADON script
821877821864646c617374			<- CBOR as Hex
ghh3ghhkZGxhc3Q=			<- Base64 of CBOR
[130, 24, 119, 130, 24, 100, 100, 108, 97, 115, 116] <- CBOR Byte Array. Only 11 Bytes
 ```

an example of navigating nested JSON to retrieve a  `Float`.

```
parseMapJSON().getMap("bpi").getMap("USD").getFloat("rate_float")	<- High Level
[119, [102, 'bpi'], [102, 'USD'], [100, 'rate_float']]			<- RADON script
84187782186663627069821866635553448218646a726174655f666c6f6174		<- CBOR as Hex
hBh3ghhmY2JwaYIYZmNVU0SCGGRqcmF0ZV9mbG9hdA==						<- Base64 of CBOR
CBOR Byte Array.
	[132, 24, 119, 130, 24, 102, 99, 98, 
	 112, 105, 130, 24, 102, 99, 85, 83,            <- CBOR Byte Array 
	 68, 130, 24, 100, 106, 114, 97, 116,               ( 31 Bytes )
	 101, 95, 102, 108, 111, 97, 116]

```

After the Witnesses **retrieve** the `Float` from both sources,  the **aggregate**  and **tally**  is defined with  REDUCERS and/or FILTERS  in the data request. Here is a complete Data Request with the RADON example above.

```
"create_data_request":{
	"data_request":{
    	"retrieve":[
    	{
     		"kind":"HTTP-GET",
     		"script":[130, 24, 119, 130, 24, 100, 100, 108, 97, 115, 116],
     		"url":"https://www.bitstamp.net/api/ticker/"
     	},
     	{
            "kind":"HTTP-GET",
            "script":[132, 24, 119, 130, 24, 102, 99, 98, 112, 105, 130, 24, 102, 99, 85, 83, 68, 130, 24, 100, 106, 114, 97, 116, 101, 95, 102, 108, 111, 97, 116],
            "url":"https://api.coindesk.com/v1/bpi/currentprice.json"
         }],
         "aggregate":{
            "filters":[],
            "reducer":3
        },
         "tally":{
            "filters":[],
            "reducer":3
          },
          "time_lock":0
    },
    "witness_reward": 10,
    "witnesses": 20,
    "backup_witnesses": 5,
    "extra_commit_rounds": 3,
    "extra_reveal_rounds": 3,
    "min_consensus_percentage": 51,
    "commit_fee": 1,
    "reveal_fee": 1,
    "tally_fee": 1,
}

```





### TYPES

| Name      | Value       |
| --------- | ----------- |
| `BOOLEAN` | `"Boolean"` |
| `INTEGER` | `"Integer"` |
| `FLOAT`   | `"Float"`   |
| `STRING`  | `"String"`  |
| `ARRAY`   | `"Array"`   |

### PSEUDOTYPES

| Name        | Value         |
| ----------- | ------------- |
| `ANY`       | `"Any"`       |
| `INNER`     | `"Inner"`     |
| `MATCH`     | `"Same"`      |
| `SUBSCRIPT` | `"Subscript"` |

### REDUCERS

| Name                    | Byte Value | Number |
| ----------------------- | ---------- | ------ |
| `min`                   | `0x00`     | 0      |
| `max`                   | `0x01`     | 1      |
| `mode`                  | `0x02`     | 2      |
| `averageMean`           | `0x03`     | 3      |
| `averageMeanWeighted`   | `0x04`     | 4      |
| `averageMedian`         | `0x05`     | 5      |
| `averageMedianWeighted` | `0x06`     | 6      |
| `deviationStandard`     | `0x07`     | 7      |
| `deviationAverage`      | `0x08`     | 8      |
| `deviationMedian`       | `0x09`     | 9      |
| `deviationMaximum`      | `0x0A`     | 10     |

### FILTERS

| Name                   | Byte Value | Number |
| ---------------------- | ---------- | ------ |
| `greaterThan`          | `0x00`     | 0      |
| `lessThan`             | `0x01`     | 1      |
| `equals`               | `0x02`     | 2      |
| `deviationAbsolute`    | `0x03`     | 3      |
| `deviationRelative`    | `0x04`     | 4      |
| `deviationStandard`    | `0x05`     | 5      |
| `top`                  | `0x06`     | 6      |
| `bottom`               | `0x07`     | 7      |
| `lessOrEqualThan`      | `0x80`     | 128    |
| `greaterOrEqualThan`   | `0x81`     | 129    |
| `notEquals`            | `0x82`     | 130    |
| `notDeviationAbsolute` | `0x83`     | 131    |
| `notDeviationRelative` | `0x84`     | 132    |
| `notDeviationStandard` | `0x85`     | 133    |
| `notTop`               | `0x86`     | 135    |
| `notBottom   `         | `0x87`     | 136    |



## Type System



### PSEUDOTYPES.ANY

| Name       | Byte Value | Next Type            |
| ---------- | ---------- | -------------------- |
| `identity` | `0x00`     | `[PSEUDOTYPES.SAME]` |

----

### PSEUDOTYPES.ARRAY


| Name         | Byte Value | Next Type                 |
| ------------ | ---------- | ------------------------- |
| `count`      | `0x10`     | `[TYPES.INTEGER]`         |
| `filter`     | `0x11`     | `[PSEUDOTYPES.SAME]`      |
| `flatten`    | `0x12`     | `[PSEUDOTYPES.INNER]`     |
| `getArray`   | `0x13`     | `[PSEUDOTYPES.INNER]`     |
| `getBoolean` | `0x14`     | `[TYPES.BOOLEAN]`         |
| `getBytes`   | `0x15`     | `[TYPES.BYTES]`           |
| `getFloat`   | `0x16`     | `[TYPES.FLOAT] `          |
| `getInteger` | `0x17`     | `[TYPES.INTEGER]`         |
| `getMap`     | `0x18`     | `[TYPES.MAP]`             |
| `getString`  | `0x19`     | `[TYPES.STRING]`          |
| `map`        | `0x1A`     | `[PSEUDOTYPES.SUBSCRIPT]` |
| `reduce`     | `0x1B`     | `[PSEUDOTYPES.INNER]`     |
| `some`       | `0x1C`     | `[TYPES.BOOLEAN]`         |
| `sort`       | `0x1D`     | `[PSEUDOTYPES.SAME]`      |
| `take`       | `0x1E`     | `[PSEUDOTYPES.SAME]       |

----

### TYPES.BOOLEAN

| Name              | Byte Value    | Next Type                          |
| ----------------- | ------        | --------------------------------- |
| `asString`        | `0x20`        | `[TYPES.STRING]`                  |
| `match`           | `0x21`        | `[PSEUDOTYPES.MATCH]`             |
| `negate`          | `0x22`        | `[TYPES.BOOLEAN`                  |

----

### TYPES.BYTES

| Name              | Byte Value    | Next Type                          |
| ----------------- | ------        | --------------------------------- |
| `asString`        | `0x30`        | `[TYPES.STRING]`                  |
| `hash`            | `0x31`        | `[TYPES.BYTES]`                   |

----

### TYPES.INTEGER

| Name              | Byte Value    | Next Type                          |
| ----------------- | ------        | --------------------------------- |
| `absolute`        | `0x40`        | `[TYPES.INTEGER]`                 |
| `asFloat`         | `0x41`        | `[TYPES.FLOAT]`                   |
| `asString`        | `0x42`        | `[TYPES.STRING]`                  |
| `greaterThan`     | `0x43`        | `[TYPES.BOOLEAN]`                 |
| `lessThan`        | `0x44`        | `[TYPES.BOOLEAN]`                 |
| `match`           | `0x45`        | `[PSEUDOTYPES.MATCH]`             |
| `modulo`          | `0x46`        | `[TYPES.INTEGER]`                 |
| `multiply`        | `0x47`        | `[TYPES.INTEGER]`                 |
| `negate`          | `0x48`        | `[TYPES.INTEGER]`                 |
| `power`           | `0x49`        | `[TYPES.INTEGER]`                 |
| `reciprocal`      | `0x4A`        | `[TYPES.FLOAT]`                   |
| `sum`             | `0x4B`        | `[TYPES.INTEGER]`                 |

----

### TYPES.FLOAT

| Name              | Byte Value    | Next Type                          |
| ----------------- | ------        | --------------------------------- |
| `absolute`        | `0x50`        | `[TYPES.FLOAT]`                   |
| `asString`        | `0x51`        | `[TYPES.STRING]`                  |
| `ceiling`         | `0x52`        | `[TYPES.INTEGER]`                 |
| `greaterThan`     | `0x53`        | `[TYPES.BOOLEAN]`                 |
| `floor`           | `0x54`        | `[TYPES.INTEGER]`                 |
| `lessThan`        | `0x55`        | `[TYPES.BOOLEAN]`                 |
| `modulo`          | `0x56`        | `[TYPES.FLOAT]`                   |
| `multiply`        | `0x57`        | `[TYPES.FLOAT]`                   |
| `negate`          | `0x58`        | `[TYPES.FLOAT]`                   |
| `power`           | `0x59`        | `[TYPES.FLOAT]`                   |
| `reciprocal`      | `0x5A`        | `[TYPES.FLOAT]`                   |
| `round`           | `0x5B`        | `[TYPES.INTEGER]`                 |
| `sum`             | `0x5C`        | `[TYPES.FLOAT]`                   |
| `truncate`        | `0x5d`        | `[TYPES.INTEGER]`                 |

----

### TYPES.MAP

| Name              | Byte Value    | Next Type                          |
| ----------------- | ------        | --------------------------------- |
| `entries`         | `0x60`        | `[PSEUDOTYPES.SAME]`              |
| `getArray`        | `0x61`        | `[TYPES.ARRAY]`                   |
| `getBoolean`      | `0x62`        | `[TYPES.BOOLEAN]`                 |
| `getBytes`        | `0x63`        | `[TYPES.BYTES]`                   |
| `getFloat`        | `0x64`        | `[TYPES.FLOAT]`                   |
| `getInteger`      | `0x65`        | `[TYPES.INTEGER]`                 |
| `getMap`          | `0x66`        | `[TYPES.MAP]`                     |
| `getString`       | `0x67`        | `[TYPES.STRING]`                  |
| `keys`            | `0x68`        | `[TYPES.ARRAY, TYPES.STRING]`     |
| `valuesAsArray`   | `0x69`        | `[TYPES.ARRAY, TYPES.ARRAY]`      |
| `valuesAsBoolean` | `0x6A`        | `[TYPES.ARRAY, TYPES.BOOLEAN]`    |
| `valuesAsBytes`   | `0x6B`        | `[TYPES.ARRAY, TYPES.BYTES]`      |
| `valuesAsInteger` | `0x6C`        | `[TYPES.ARRAY, TYPES.INTEGER]`    |
| `valuesAsFloat`   | `0x6D`        | `[TYPES.ARRAY, TYPES.FLOAT]`      |
| `valuesAsMap`     | `0x6E`        | `[TYPES.ARRAY, TYPES.MAP]`        |
| `valuesAsString`  | `0x6F`        | `[TYPES.ARRAY, TYPES.STRING]`     |

----

### TYPES.STRING

| Name              | Byte Value    | Next Type                          |
| ----------------- | ------        | --------------------------------- |
| `asBoolean`       | `0x70`        | `[TYPES.BOOLEAN]`                 |
| `asBytes`         | `0x71`        | `[TYPES.BYTES]`                   |
| `asFloat`         | `0x72`        | `[TYPES.FLOAT]`                   |
| `asInteger`       | `0x73`        | `[TYPES.INTEGER]`                 |
| `length`          | `0x74`        | `[TYPES.INTEGER]`                 |
| `match`           | `0x75`        | `[PSEUDOTYPES.MATCH]`             |
| `parseArrayJSON`  | `0x76`        | `[TYPES.ARRAY]`                   |
| `parseMapJSON`    | `0x77`        | `[TYPES.MAP]`                     |
| `parseXML`        | `0x78`        | `[TYPES.MAP]`                     |
| `toLowerCase`     | `0x79`        | `[TYPES.STRING]`                  |
| `toUpperCase`     | `0x7A`        | `[TYPES.STRING]`                  |

# Documentation

##Client->Server API

Obtain a single tag from the server:

`GetTag(tagPath)`

####Json client request example
```json
{
	"cmd": "gettag",
	"path" : "PLC1;tagName",
	"requestId": 461541641
}
```
####Json server response example
```json
{
	"value": 35241,
	"path" : "PLC1;tagName",
	"requestId": 461541641
}
```

Obtain a list of tags from the server:

`GetTags(tagPathList)`
####Json client request example
```json
{
	"cmd": "gettags",
	"path" : ["PLC1;tagName1", "PLC1;tagName2"],
	"requestId": 4615453
}
```
####Json server response example
```json
{
	"value": [35241, true],
	"path" : ["PLC1;tagName1", "PLC1;tagName2"],
	"requestId": 4615453
}
```

Set the value of a single tag:

`SetTag(tagPath, value)`

####Json client request example
```json
{
	"cmd": "settag",
	"path" : "PLC1;tagName3",
	"requestId": 4863118,
    "value": false
}
```

####Json server response example
```json
{
	"value": false,
	"path" : "PLC1;tagName3",
	"requestId": 4863118
}
```

Set the value of a list of tags:

`SetTags(tagPathList, values)`

####Json client request example
```json
{
	"cmd": "settags",
  	"path" : ["PLC1;tagName3", "PLC1;tagName4"],
	"requestId": 4863118,
    "value": [false, 3.1415]
}
```

####Json server response example
```json
{
	"value": [false, 3.1415],
	"path" : ["PLC1;tagName3", "PLC1;tagName4"],
	"requestId": 4863118
}
```

Subscribe the client to a list of tags:

`Subscribe(tagPathList)`
####Json client request example
```json
{
	"cmd": "subscribe",
  	"path" : ["PLC1;tagName6", "PLC1;tagName7"],
	"requestId": 123
}
```

####Json server response example
```json
{
	"value": [false, 3.1415],
	"path" : ["PLC1;tagName6", "PLC1;tagName7"],
	"requestId": 123
}
```
####Json server subscribed tags events
```json
{
	"value": [false],
	"path" : ["PLC1;tagName6"],
	"requestId": 0
}
```


##Server->Devices API
`ReadTag(tagName)`

`ReadTags(tagList)`

`WriteTag(tagName, value)`

`WriteTags(tagList, values)`

####Device description
```json
{
    "id": "abcdfefefs",
    "ipAddress": "192.168.1.1",
    "name" : "PLC1",
    "description": "Device description"
}
```

####Tag description
```json
{
    "id": "ab231efefs",
    "name" : "Tag1",
    "deviceId": "abcdfefefs",
    "value": true,
    "datatype": "bool",
    "readonly": false,
    "timestamp": 1631611463773 // milliseconds since Epoch
}
```


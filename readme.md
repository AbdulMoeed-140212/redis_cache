# Basic Redis usage for cache

Learn more about redis https://redis.io/download

## Prerequisite

* Python 3.7 or higher
* Redis server running

## Setup

1. Make a virtual env and activate it

```bash
python -m venv .venv
.venv\Scripts\activate # For windows
source .venv/bin/activate
```

2.  Install libraries

```bash
pip install -r requirements.txt
```



## Run

```bash
python main.py
```



## Description

This is small script that show usage of Redis as a cache for http request page responses.

This scripts is set to connect to redis at `localhost:6379`  to db at index 1

Selected database is flushed at the beginning.

```python
redis = await aioredis.create_redis_pool('redis://localhost', db=1)
await redis.flushdb()
```



### Caching method

```python
for i in range(5):
    response = None
    if await redis.exists(url):
        response = await redis.get(url, encoding='utf-8')
        print(">> Fetched from cache !!!! ")
    else:
        response = getresponse(url)
        await redis.set(url, response, expire=20)
        print(">> Response Cached ")
    
	await asyncio.sleep(10)
```

This script will request 5 times to same URL with a *10 second interval*

Each time it will check for URL against its stored keys ***(URL is being used as key)***

if URL exists it will fetch response saved in redis against that URL(key) 

else it will make a get request  to the URL and fetch response from internet then save it in redis against its URL

then wait for 10 sec and repeat the process

```
await redis.set(url, response, expire=20)
```

the line above has a expire of 20 seconds so this will data will expire in 20  seconds.

Below is the output of script

```
Connecting to Redis Server
Connected !!

Fetching data...
Fetch Complete!
>> Response Cached 
>> Fetched from cache !!!! 
Fetching data...
Fetch Complete!
>> Response Cached 
>> Fetched from cache !!!! 
Fetching data...
Fetch Complete!
>> Response Cached 
Disconnecting Redis
Disconnected
```


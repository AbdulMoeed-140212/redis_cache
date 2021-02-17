import aioredis
import asyncio
import requests

url = 'https://alexwohlbruck.github.io/cat-facts/'

def getresponse(url):
    print("Fetching data...")
    response = requests.get(url)
    print("Fetch Complete!")
    return response.content

async def main():
    
    print("Connecting to Redis Server")
    
    redis = await aioredis.create_redis_pool('redis://localhost', db=1)
    await redis.flushdb()

    print("Connected !!\n")

    
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

    print("Disconnecting Redis")
    redis.close()
    await redis.wait_closed()
    print("Disconnected")

asyncio.run(main())
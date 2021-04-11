# !pip install aiohttp
# !pip install nest-asyncio

import asyncio
import time
from timeit import default_timer
from aiohttp import ClientSession
import requests
import random

def urlGen(ticket, l, jq1 = 11110597240940063914, jq2 = 1618034874558, jq3 = 1618034874559):
    counter = 0
    while counter < l:
        yield f'https://api.iag.bg/cgi-bin/e_tickets/search.cgi?session=000&user_id=1&search_by=0&search_text={ticket}&lng=bg&digest=xxxn&callback=jQuery{jq1}_{jq2}&_={jq3}'
        counter += 1
        ticket -= 1
        jq1 += random.randrange(-2500, 2500)
        jq2 += random.randrange(-2500, 2500)
        jq3 += random.randrange(-2500, 2500)

numreq = 50
mygen = urlGen(2115425256, numreq)

urls = list(mygen)
# urls

async def fetch(url, session):
    fetch.start_time[url] = default_timer()
    async with session.get(url) as response:
        r = await response.read()
        elapsed = default_timer() - fetch.start_time[url]
        print(url, ' took ', str(elapsed))
        return r

async def fetch_all(urls):
    tasks = []
    fetch.start_time = dict() 
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task) 
        _ = await asyncio.gather(*tasks)

def fetch_async(urls):
    start_time = default_timer()

    loop = asyncio.get_event_loop() 
    future = asyncio.ensure_future(fetch_all(urls)) 
    loop.run_until_complete(future) 

    tot_elapsed = default_timer() - start_time
    print('Total time taken : ', str(tot_elapsed))

before_start = time.time()
fetch_async(urls)
print(f'Total time taken {time.time() - before_start}')
print(f'Average time per request is {(time.time() - before_start) / numreq}')

if __name__ == "__main__":
    numreq = 100
    mygen = urlGen(2115425256, numreq)
    urls = list(mygen)
    fetch_async(urls)

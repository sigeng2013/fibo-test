# pip install aiohttp

import random
import itertools
import aiohttp
import asyncio
import time
# import nest_asyncio
# nest_asyncio.apply()

def urlGen(sTicket, eTicket, jq1 = 11110597240940063914, jq2 = 1618034874558, jq3 = 1618034874559):
    while sTicket < eTicket:
        yield f'https://api.iag.bg/cgi-bin/e_tickets/search.cgi?session=000&user_id=1&search_by=0&search_text={sTicket}&lng=bg&digest=xxxn&callback=jQuery{jq1}_{jq2}&_={jq3}'
        sTicket += 1
        jq1 += random.randrange(-2500, 2500)
        jq2 += random.randrange(-2500, 2500)
        jq3 += random.randrange(-2500, 2500)


def iag():
    f = open(outputFile, "a+")

    start_time = time.time()

    bCounter = 0

    while True:

        urls = list(itertools.islice(mygen, 30))

        if urls:

            bCounter += 1

            async def get_ticket(session, url):
                async with session.get(url) as resp:
                    ticket = await resp.text()
                    return ticket

            async def collect():

                async with aiohttp.ClientSession() as session:

                    tasks = []
                    for url in urls:
                        tasks.append(asyncio.ensure_future(get_ticket(session, url)))

                    original_tickets = await asyncio.gather(*tasks)
                    for ticket in original_tickets:
                        f.write(ticket)
                        f.write('\n')

            print(f'Working on batch number {bCounter} of {nBatches}')
            asyncio.run(collect())

        else:
            print(f'--- {time.time() - start_time} seconds in total ---')
            print('end')
            break

    f.close()

if __name__ == "__main__":
    start = 211516950
    end = 211549442
    batch = 30
    nBatches = ((end - start) // batch) + 1
    outputFile = 'tickets2021raw.txt'
    mygen = urlGen(start, end)
    iag()

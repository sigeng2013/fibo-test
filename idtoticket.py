# !pip install aiohttp
import aiohttp
import requests
import itertools
import asyncio
import time
# import nest_asyncio
# nest_asyncio.apply()

def trimLine(l):
    '''
    IN -> string, line
    OUT -> dict 
    '''
    oBracket = l.find('(')
    return l[oBracket + 1 : -1]

def ticketsContent(infile, outfile):
    f1 = open(outfile, "a")
    f2 = open(infile, 'r')

    readURLs = (x for x in (l.strip() for l in f2) if x)

    start_time = time.time()

    batch = 0

    while True:

        urls = list(itertools.islice(readURLs, 30))

        if urls:
            batch += 1
            print(f'Processing batch {batch}')

            async def get_ticket(session, url):
                async with session.get(url) as resp:
                    # ticket = await resp.text(encoding='utf-8')
                    ticket = await resp.read()
                    return ticket

            async def collect():

                async with aiohttp.ClientSession() as session:

                    tasks = []
                    for url in urls:
                        tasks.append(asyncio.ensure_future(get_ticket(session, url)))

                    original_tickets = await asyncio.gather(*tasks)
                    for ticket in original_tickets:
                        f1.write(trimLine(ticket.decode('utf-8', errors="replace")))
                        f1.write('\n')

            asyncio.run(collect())

        else:
            print(f'--- {time.time() - start_time} seconds in total ---')
            print('end')
            break

    f1.close()
    f2.close()

if __name__ == "__main__":
    ticketsContent(infile = 'tickets2021url.txt', outfile = 'tickets2021con.txt')

# !pip install aiohttp

import random
import itertools
import aiohttp
import asyncio
import time
import json
# import nest_asyncio
# nest_asyncio.apply()

batchSize = 30
step1Output = 'tickets2021raw.txt'
step2Output = 'tickets2021url.txt'
step3Output = 'tickets2021con.txt'

"""Step 1"""

def urlGen(sTicket, eTicket, jq1 = 11110597240940063914, jq2 = 1618034874558, jq3 = 1618034874559):
    while sTicket < eTicket:
        yield f'https://api.iag.bg/cgi-bin/e_tickets/search.cgi?session=000&user_id=1&search_by=0&search_text={sTicket}&lng=bg&digest=xxxn&callback=jQuery{jq1}_{jq2}&_={jq3}'
        sTicket += 1
        jq1 += random.randrange(-2500, 2500)
        jq2 += random.randrange(-2500, 2500)
        jq3 += random.randrange(-2500, 2500)

def step1():
    mygen = urlGen(tStart, tEnd)
    f = open(step1Output, 'w')

    start_time = time.time()

    bCounter = 0

    while True:

        urls = list(itertools.islice(mygen, batchSize))

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

            print(f'Working on batch number {bCounter} of Step 1')
            asyncio.run(collect())

        else:
            print(f'--- {time.time() - start_time} seconds in total ---')
            print('end')
            break

    f.close()

"""Step 2"""

def genAPI(jq1 = 1111009710504092045635, jq2 = 1621425006464, jq3 = 1621425006465):
    while True:
        jq1 += random.randrange(-2500, 2500)
        jq2 += random.randrange(-2500, 2500)
        jq3 += random.randrange(-2500, 2500)
        yield (jq1, jq2, jq3)

myAPI = genAPI()

def trimLine(l):
    '''
    IN -> string, line
    OUT -> dict 
    '''
    oBracket = l.find('(')
    return json.loads(l[oBracket + 1 : -1])

def genReader(file_name):
    '''
    IN -> string, file path
    OUT -> string, generator that yields one line at a time
    '''
    for row in open(file_name, "r"):
        yield trimLine(row.strip())

def step2():

    sample = genReader(step1Output)

    j1, j2, j3 = next(myAPI)

    with open(step2Output, 'w') as outFile:
        count = 0

        for item in sample:
            # currentLine = next(sample)
            for i in item['records']:
                count += 1
                if count % 500 == 0:
                    print(count)
                # outFile.write(i['id'])
                outFile.write(f'https://api.iag.bg/cgi-bin/e_tickets/get.cgi?lng=bg&session=000&user_id=0&ticket_id={i["id"]}&digest=xxxn&callback=jQuery{j1}_{j2}&_={j3}')
                outFile.write('\n')

"""Step 3"""

def trimLine2(l):
    '''
    IN -> string, line
    OUT -> dict 
    '''
    oBracket = l.find('(')
    return l[oBracket + 1 : -1]

def step3(infile = step2Output, outfile = step3Output):
    f1 = open(outfile, "a")
    f2 = open(infile, 'r')

    readURLs = (x for x in (l.strip() for l in f2) if x)

    start_time = time.time()

    batch = 0

    while True:

        urls = list(itertools.islice(readURLs, batchSize))

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
                        f1.write(trimLine2(ticket.decode('utf-8', errors="replace")))
                        f1.write('\n')

            asyncio.run(collect())

        else:
            print(f'--- {time.time() - start_time} seconds in total ---')
            print('end')
            break

    f1.close()
    f2.close()

if __name__ == "__main__":
    # Constants
    tStart = int(input("Start number: "))
    tEnd = int(input("End number: "))
    step1()
    step2()
    step3()

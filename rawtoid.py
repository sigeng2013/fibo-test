import json

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

def rawToId(inFile, outFile):

    sample = genReader(inFile)

    with open(outFile, 'a') as outFile:
        count = 0

        for item in sample:
            currentLine = next(sample)
            for i in currentLine['records']:
                count += 1
                if count % 500 == 0:
                    print(count)
                # outFile.write(i['id'])
                outFile.write(f'http://tickets.iag.bg:8080/ticket.html?lng=bg&ticket_id={i["id"]}&unit=more')
                outFile.write('\n')

if __name__ == "__main__":
    rawToId(inFile = 'tickets2021raw.txt', outFile = 'tickets2021url.txt')

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

def runAll(inputFile, outputFile):        
        
	tct = genReader(inputFile)

	output = open(outputFile, "a+")

	for i in tct:
    	for g in i['records']:
            output.write(g['id'])
        	output.write('\n')


output.close()

with zipfile.ZipFile('ticketsURL.zip', 'w', zipfile.ZIP_DEFLATED) as myzip:
    myzip.write('ticketsURL.txt')
    
if __name__ == "__main__":
    runAll('tickets2021raw.txt', "ticketsURL.txt", "a+")

import time

def fibogen(lim):
    counter = 0
    first = 0
    second = 1
    while counter < lim:
        yield second
        first, second = second, first + second
        counter += 1

def fibo(lim, s):
    
    tempgen = fibogen(lim= lim)

    for i,v in enumerate(tempgen):
        print(f'{i + 1} : {v}')
        time.sleep(s)

if __name__ == "__main__":
   fibo(100, 3)

import  time
import requests
from threading import Thread, Lock
lock = Lock()


url = input('Enter the URL to check rate limit: ')
method = input('Enter the request method (GET/POST..): ')
secondsAmount = int(input('Enter how many seconds to test: '))
threadAmount = int(input('Enter an amount of threads to run: '))

seconds = 0
counter = 0
rateLimit = False


def timeCounter():
    global seconds
    while seconds < secondsAmount:
        time.sleep(1)
        seconds += 1


def sendreq(url):
    global rateLimit, counter, seconds
    while not rateLimit and seconds < secondsAmount:
        resp = requests.request(method, url)
        print(f'[{counter}] Sent a requset, status: {resp.status_code}')
        with lock:
            counter += 1
        if resp.status_code == 429:
            with lock:
                rateLimit = True


threads = []
Thread(target=timeCounter).start()
for i in range(threadAmount):
    threads.append(Thread(target=sendreq, args=[url, ]))
    threads[i].start()
for t in threads:
    t.join()


print(f"Rate limit: {rateLimit} | Requests: {counter}")
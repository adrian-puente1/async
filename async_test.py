from time import perf_counter
import asyncio
from unittest import result
from urllib import response
import requests
import random

def get_token():
    return (random.randint(1,100) == 1) 

def send_request( token: bool, url: str = "https://pokeapi.co/api/v2/pokemon/") -> str:
    response = requests.get(url=url+str(random.randint(1,800))).json()
    response["status_code"] = 200 if token else 400
    return response

def search_handler(token: bool = False):
    status_code = 400
    incrementer = 0
    while status_code != 200:
        if incrementer >= 5: raise RuntimeError("Could not get new token")
        response = send_request(token)
        status_code = response["status_code"]
        if status_code == 200:
            return response["name"]
        else: 
            incrementer = incrementer + 1
            token = get_token()

def search_handler_assist(token: bool = False):
    status_code = 400
    incrementer = 0
    while status_code != 200:
        if incrementer >= 5: raise RuntimeError("Could not get new token")
        response = send_request(token)
        status_code = response["status_code"]
        if status_code == 200:
            return response["name"]
        else: 
            incrementer = incrementer + 1
            token = get_token()

async def search_handler_async(token: bool = True):
    token = get_token()
    status_code = 400
    incrementer = 0
    while status_code != 200:
        if incrementer >= 5: raise RuntimeError("Could not get new token")
        response = await asyncio.to_thread(search_handler_assist, token)
        status_code = response["status_code"]
        if status_code == 200:
            return response["name"]
        else:
            incrementer = incrementer + 1
            token = get_token()

async def main() -> None:
    searches = 10
    #synchronous
    # time_before = perf_counter()
    # for _ in range(1,searches): print(search_handler(token=True))
    # print(f"Total time (synchronous): {perf_counter() - time_before}.")
    #asynchronous
    time_before = perf_counter()
    result = await asyncio.gather(*[search_handler_async() for _ in range(1,searches)])
    print(result)
    print(f"Total time (asynchronous): {perf_counter() - time_before}.")

if __name__ == "__main__":
    asyncio.run(main())
from time import perf_counter
import asyncio
import requests
import random

PASSWORD = "password"

def get_token():
    """
    Returns boolean value. 1/5 chance of returning False.
    """
    if (random.randint(1,5) != 1): return PASSWORD
    else: return chr(random.randint(0,255))

def send_request( token, url: str = "https://pokeapi.co/api/v2/pokemon/") -> str:
    """
    Returns response dict with "status_code" key-value appended
    """
    response = requests.get(url=url+str(random.randint(1,800))).json()
    response["status_code"] = 200 if (token == PASSWORD) else 400
    return response

def search_validator(token = "a"):
    """
    Performs one search, and refreshes fake token if token is false
    """
    status_code = 400
    incrementer = 0
    while status_code != 200:
        if incrementer >= 6: raise RuntimeError("Could not get new token")
        response = send_request(token)
        status_code = response["status_code"]
        if status_code == 200:
            # successful search
            return response["name"]
        else: 
            # failed search, attempt to revalidate and search up to 5 times
            incrementer = incrementer + 1
            token = get_token()

async def bulk_search_handler():
    token = get_token()
    token = "password"
    response = await asyncio.to_thread(search_validator, token)
    return response

async def main() -> None:
    searches = 10
    #synchronous
    time_before = perf_counter()
    token = get_token()
    for _ in range(1,searches): print(search_validator(token))
    print(f"Total time (synchronous): {perf_counter() - time_before}.")
    #asynchronous
    time_before = perf_counter()
    result = await asyncio.gather(*[bulk_search_handler() for _ in range(1,searches)])
    print(result)
    print(f"Total time (asynchronous): {perf_counter() - time_before}.")

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import concurrent.futures
import multiprocessing
import threading

import aiohttp
import requests


async def async_fetch(session: aiohttp.ClientSession, url: str) -> str:
    """
    Asyncronously fetch (get-request) single url using provided session
    :param session: aiohttp session object
    :param url: target http url
    :return: fetched text
    """

    async with session.get(url) as resp:
        res = await resp.text()
        return res


async def async_requests(urls: list[str]) -> list[str]:
    """
    Concurrently fetch provided urls using aiohttp
    :param urls: list of http urls ot fetch
    :return: list of fetched texts
    """
    lst_tasks = []
    for url in urls:
        session = aiohttp.ClientSession()
        lst_tasks.append(async_fetch(session, url))
    iter_res = await asyncio.gather(*lst_tasks)
    return list(iter_res)


lst_texts: list[str] = []


def sync_fetch(session: requests.Session, url: str) -> str:
    """
    Syncronously fetch (get-request) single url using provided session
    :param session: requests session object
    :param url: target http url
    :return: fetched text
    """
    with session.get(url) as resp:
        res = resp.text
        lst_texts.append(res)
        return res


def threaded_requests(urls: list[str]) -> list[str]:
    """
    Concurrently fetch provided urls with requests in different threads
    :param urls: list of http urls ot fetch
    :return: list of fetched texts
    """
    args_both = []
    with requests.Session() as session:
        for url in urls:
            args_both.append((session, url))
    with multiprocessing.Pool() as pool:
        result = pool.starmap(sync_fetch, args_both)
    return result
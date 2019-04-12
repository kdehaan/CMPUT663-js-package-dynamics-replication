#!/usr/bin/python3.4
import asyncio  
import aiohttp
import json
import sys


base_url = 'https://api.npmjs.org/downloads/point/last-month/'
downloads = {}
failed=0
max_tasks = 50

def fetch_count(package_list, start, end, session):
    for i in range(start, end):
        package = package_list[i]
        response = yield from session.get(base_url+package)
        if response.status == 200:
            downloads[package] = yield from response.json()
        else:
            failed += 1

def main(npm_packages):
    tasks = []
    jobs_per_task = int(len(npm_packages) / max_tasks)
    for start in range(0, len(npm_packages), jobs_per_task):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        session = aiohttp.ClientSession(connector=conn)
        end = start + jobs_per_task
        if end > len(npm_packages):
            end = len(npm_packages)
        tasks.append(asyncio.Task(fetch_count(npm_packages, start, end, session)))
    yield from asyncio.gather(*tasks)

if __name__ == '__main__':
    kv = json.load(open('npm_stripped.json'))
    npm_packages = list(kv.keys())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(npm_packages))
    with open('npm_downloads_last_month.json','w') as outfile:
        json.dump(downloads, outfile)
    print(failed,'requests failed')

# Run url_ddgs.py first

import time
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import csv

url_list = []
text_list = []
titles=[]



async def save_file(title,url, text):
    words = text.split()
    truncated_text = ' '.join(words[:2000])
    titles.append(title)
    url_list.append(url)
    text_list.append(truncated_text)


async def scrape(title, url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                    if resp.status == 200:
                        body = await resp.text()
                        soup = BeautifulSoup(body, 'html.parser')
                        content = soup.find_all(['p', 'span'])
                        text = ' '.join([p.get_text().strip() for p in content]) 
                    else:
                        text = ''
            await save_file(title,url, text) 
        except aiohttp.ClientConnectorError as e:
            if e.os_error.errno == 443:  
                print(f"Skipping URL {url} due to SSL error")
            else:
                raise e


async def main():
    start_time = time.time()
    tasks = []
    print("Saving the output of extracted information")

    with open('search_results.csv') as file:
        csv_reader = csv.DictReader(file)
        for csv_row in csv_reader:
            task = asyncio.create_task(scrape(csv_row['title'],csv_row['url']))
            tasks.append(task)

    print('Saving the output of the information')
    await asyncio.gather(*tasks)

    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f seconds' % time_difference)

    result_df = pd.DataFrame({'Title':titles,'URL': url_list, 'Text': text_list})

    result_df.to_csv('result.csv', index=False)


loop = asyncio.get_event_loop()

loop.run_until_complete(main())

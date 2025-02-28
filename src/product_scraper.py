import aiohttp
import asyncio
from bs4 import BeautifulSoup
#from win32com.client import Dispatch
from configparser import ConfigParser

''' Latest scraping version functions'''
async def fetch(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            return await response.text()
        
async def crawl(parsers, url_type):
    used_tools = {k:v for k,v in parsers.items(url_type)}
    
    urls = list(used_tools.values())
    tools = list(used_tools.keys())
    
    tasks = [fetch(url) for url in urls]
    
    html_pages = await asyncio.gather(*tasks)
      
    for i, html in enumerate(html_pages):
        tag_n = "a"
        attr_n = {'class' : 'card-link text-current js-prod-link'}

        soup = BeautifulSoup(html, 'lxml')
        name = soup.find_all(tag_n, **attr_n)
        price = soup.find_all('div', attrs={'class': 'price_default'})
        stock = soup.find_all('div', attrs={'class': 'price_no-variant'})
        print(name[1].get_text())
    
async def main():  
    parsers = ConfigParser(delimiters=(':'))
    parsers.read('parsers.ini')
        
    '''Getting latest versions from webs'''
    await crawl(parsers, 'URLS')
        
asyncio.run(main())

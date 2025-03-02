#!/usr/bin/env python
# coding: utf-8

"""
Product Check Module

This module handles the initialization and operations related to product stock checking.
It fetches product data from various URLs, parses the content, and displays the formatted results.

Classes:
    bcolors: A class for terminal text coloring.

Functions:
    fetch(url): Fetch the content of the given URL.
    crawl(parsers, url_type): Crawl the URLs and parse the content.
    main(): Main function to start the crawling process.
    init(): Initialize the product check module.
"""

import re
import aiohttp
import asyncio
from configparser import ConfigParser
from bs4 import BeautifulSoup

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

class bcolors:
    """Class for terminal text coloring."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

async def fetch(url):
    """Fetch the content of the given URL."""
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers=header) as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()

async def crawl(parsers, url_type):
    """Crawl the URLs and parse the content."""
    output = []

    used_tools = {k: v for k, v in parsers.items(url_type)}
    urls = list(used_tools.values())
    tools = list(used_tools.keys())

    tasks = [fetch(url) for url in urls]
    html_pages = await asyncio.gather(*tasks)

    for i, html in enumerate(html_pages):
        tag_n = eval(parsers['PARSERS'][f"{tools[i]}_tag_n"])
        tag_p = eval(parsers['PARSERS'][f"{tools[i]}_tag_p"])
        tag_s = eval(parsers['PARSERS'][f"{tools[i]}_tag_s"])
        attr_n = eval(parsers['PARSERS'][f"{tools[i]}_attr_n"])
        attr_p = eval(parsers['PARSERS'][f"{tools[i]}_attr_p"])
        attr_s = eval(parsers['PARSERS'][f"{tools[i]}_attr_s"])
        re_n = eval(parsers['PARSERS'][f"{tools[i]}_re_n"])
        re_p = eval(parsers['PARSERS'][f"{tools[i]}_re_p"])
        re_s = eval(parsers['PARSERS'][f"{tools[i]}_re_s"])

        soup = BeautifulSoup(html, 'lxml')
        name = soup.find_all(tag_n, **attr_n)
        price = soup.find_all(tag_p, **attr_p)
        stock = soup.find_all(tag_s, **attr_s)

        '''Extract the text from the tags where/ when required and apply regex if needed.'''
        if re_n != 'False':
            name = re.findall(re_n, str(name))
        if re_p != 'False':
            price = re.findall(re_p, str(price))
        if re_s != 'False':
            stock = re.findall(re_s, str(stock))

        '''For some specific web, flatten the list of tuples if needed.'''
        if isinstance(price[0], tuple):
            price = [item for sublist in price for item in sublist if item]

        for j in range(len(name)):
            formatted_web = f"{bcolors.BOLD}{tools[i].upper()}{bcolors.ENDC}"
            formatted_name = f"{bcolors.BOLD}{name[j].strip() if re_n != 'False' else name[j].get_text().strip()}{bcolors.ENDC}"
            formatted_price = f"{bcolors.OKBLUE}{price[j].strip().replace('&nbsp;', ',') if re_p != 'False' else price[j].get_text().strip().replace('&nbsp;', ',')}{bcolors.ENDC}"
            formatted_stock = f"{bcolors.WARNING}{stock[j].strip() if re_s != 'False' else stock[j].get_text().strip()}{bcolors.ENDC}"
            output.append([formatted_web, formatted_name, formatted_price, formatted_stock])

    for row in output:
        print("{: <20} {: <100} {: >20} {: <60}".format(*row))

async def main():
    """Main function to start the crawling process."""
    parsers = ConfigParser(delimiters=(':'))
    parsers.read('./parsers.ini')

    await crawl(parsers, 'URLS')

def init():
    """Initialize the product check module."""
    asyncio.run(main())
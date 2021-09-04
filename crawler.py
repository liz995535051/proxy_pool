import asyncio
import aiohttp
import json, time
from log_ import log
from pyquery import PyQuery as pq
from ips_r import save
# logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s:%(message)s')


class Spider(object):
    def __init__(self):
        # self.semaphore = asyncio.Semaphore(10)  #最大并发条数
        self.header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1630577430; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1630577430",
            "Host": "www.66ip.cn",
            "Pragma": "no-cache",
            "Referer": f"https://link.csdn.net/?target=http%3A%2F%2Fwww.66ip.cn%2Findex.html",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"}

    async def scrape(self, url):
        # async with self.semaphore:
        async with aiohttp.ClientSession(headers=self.header)as session:
            response=await session.get(url)
            return await response.text()


    async def scrape_index(self, page):
        url = f'http://www.66ip.cn/%s.html' % page
        html = await self.scrape(url)
        await self.parse(html)

    async def parse(self, html):
        doc = pq(html)
        l1 = doc('table:last')
        l1('tr:first').remove()
        l3 = l1.find('tr').items()
        for item in l3:
            ip = item('td:lt(2)').text().replace(' ', ':')
            log.info('已获取proxy:'+ip)
            save(ip)



    async def main(self,pages=10):
        scrape_index_tasks = [asyncio.ensure_future(self.scrape_index(page)) for page in range(1,pages+1)]
        await asyncio.gather(*scrape_index_tasks)

    # def run(self):
    #     asyncio.get_event_loop().run_until_complete(spider.main())



if __name__ == '__main__':
    spider = Spider()
    asyncio.get_event_loop().run_until_complete(spider.main())

from log_ import log
from ips_r import RedisClient
from config import *
from test_new import Tester
from get import app
from crawler import Spider
import asyncio, aiohttp


def crawl_start():
    spider = Spider()
    loop = asyncio.get_event_loop()
    try:

        loop.run_until_complete(spider.main())
    finally:
        pass
        # loop.run_until_complete(loop.shutdown_asyncgens())
        # loop.close()


def test_start():
    Tester().run()


def web_start():
    app.run(host=API_HOST, port=API_PORT, debug=True)

def run():
    crawl_start()
    test_start()
    web_start()


if __name__ == '__main__':
    run()

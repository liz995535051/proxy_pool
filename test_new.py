
from ips_r import RedisClient
import aiohttp,asyncio,time
from log_ import log
from aiohttp import ClientError,ClientConnectorError
from config import TEST_URL,BATCH_TEST_SIZE,VALID_STATUS_CODES,TIME_OUT
class Tester(object):
    def __init__(self):
        self.redis=RedisClient()
    async def test_single_proxy(self,proxy):
        conn=aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try :
                if isinstance(proxy,bytes):
                    proxy=proxy.decode('utf-8')
                real_proxy='http://'+proxy
                log.info('正在测试'+proxy)
                async with session.get(TEST_URL,proxy=real_proxy,timeout=TIME_OUT) as response:
                    if response.status not in VALID_STATUS_CODES:
                        self.redis.decrease(proxy)
                        log.error('响应码不合法'+proxy)
            except (ClientError,ClientConnectorError,TimeoutError,AttributeError):
                self.redis.decrease(proxy)
                log.error('代理请求失败'+proxy)
    def run(self):
        try:
            proxies=self.redis.get_all()
            loop=asyncio.get_event_loop()
            for i in range(0,len(proxies),BATCH_TEST_SIZE):
                test_proxies=proxies[i:i+BATCH_TEST_SIZE]
                tasks=[self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            log.error('测试发生错误'+ str(e.args))
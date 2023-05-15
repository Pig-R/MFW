# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import scrapy
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class MafengwoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MafengwoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        # 实例化对象
        option = ChromeOptions()
        # 不加载图片
        prefs = {'profile.managed_default_content_settings.images': 2}
        option.add_experimental_option('prefs', prefs)

        option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 开启实验性功能
        # 去除特征值
        option.add_argument("--disable-blink-features=AutomationControlled")
        # 以上是新添加的！加上去之后状态代码就不是521了！就不反爬虫了！
        self.driver = webdriver.Chrome(options=option)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def __del__(self):
        self.driver.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def scroll(self):  # 滚动
        temp_height = 0  # 初始值
        while True:
            self.driver.execute_script("window.scrollBy(0,1000)")
            time.sleep(2)  # 反应一下
            # 获取当前滚动条距离顶部的距离
            check_height = self.driver.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            if check_height == temp_height:  # 如果两者相等说明到底了
                break
            temp_height = check_height

    def process_request(self, request, spider):
        # 在运行的时候，虽然设置了浏览器自行下拉滚动条，但最好还是人为下拉，不然可能因为加载时间问题获取数据不完整
        sta = request.meta.get('status', 0)
        self.driver.get(request.url)
        if sta == 0:  # 全部评论
            self.scroll()
        if sta == 1:  # 好评
            next_btn = self.driver.find_elements(By.XPATH, '//*[@data-type="keyword"]')[1]
            self.driver.execute_script("arguments[0].click();", next_btn)
            self.scroll()
        if sta == 2:  # 差评
            next_btn = self.driver.find_elements(By.XPATH, '//*[@data-type="keyword"]')[2]
            self.driver.execute_script("arguments[0].click();", next_btn)
            self.scroll()
        time.sleep(2)
        return scrapy.http.HtmlResponse(request.url, body=self.driver.page_source.encode('utf-8'),
                                        encoding='utf-8', request=request,
                                        status=200)  # Called for each request that goes through the downloader

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

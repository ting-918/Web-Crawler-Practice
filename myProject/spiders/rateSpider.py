import scrapy
from myProject.items import RateItem
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup

class RatespiderSpider(scrapy.Spider):
    name = "rateSpider"
    allowed_domains = ["iftp.chinamoney.com.cn"]
    start_urls = ["https://iftp.chinamoney.com.cn/chinese/forsddshis/index.html?dataType=6"]
    custom_settings = {
        'SPLASH_URL': 'http://localhost:8050',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    }
    year_list = ["2019", "2020", "2021", "2022", "2023"]
    page = 1
    next_valid = True
    
    def start_requests(self): #重新定义起始爬取点
        # 定義splash的lua腳本(可在splash服務器端先測試)
        script = """
            function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(5))
            splash:evaljs("document.getElementById('sdds-his-start-date').removeAttribute('readonly');")
            splash:evaljs("document.getElementById('sdds-his-end-date').removeAttribute('readonly');")
            splash:evaljs("document.getElementById('sdds-his-start-date').value='" .. args.year .. "-01-01';")
            splash:evaljs("document.getElementById('sdds-his-end-date').value='" .. args.year .. "-12-31';")
            splash:runjs("querySdds(" .. args.page ..");")
            assert(splash:wait(6))
            return {
                html = splash:html()
            }
            end
        """
        for year in self.year_list:
            self.next_valid = True
            self.page = 1
            url = self.start_urls[0]
            while self.next_valid:
                yield SplashRequest(url=url, 
                                    callback=self.parse, 
                                    endpoint='execute', 
                                    args={'lua_source': script, 'url': url, 'year': year, 'page': str(self.page)}
                                    )
        pass
    
    def parse(self, response):
        tbody = response.xpath('//*[@id="sdds-his"]/div[2]/div/table/tbody').extract_first()
        rows = BeautifulSoup(tbody, 'lxml').find_all('tr')
        records = []
        for row in rows:
            # 去除空白行
            if "data-blank" not in str(row):
                td = row.find_all('td') 
                record = {
                        "date": td[0].get('data-value'),
                        "USD": float(td[2].get('data-value')),                        # 美元/人民幣 匯率
                        "EUR": float(td[3].get('data-value')),                        # 歐元/人民幣 匯率
                        "JPY": float('%.6f' % (float(td[4].get('data-value'))/100)),  # 日幣/人民幣 匯率
                        "HKD": float(td[5].get('data-value')),                        # 港幣/人民幣 匯率
                        "GBP": float(td[6].get('data-value')),                        # 英鎊/人民幣 匯率
                        "AUD": float(td[7].get('data-value')),                        # 澳元/人民幣 匯率
                        "SGD": float(td[9].get('data-value')),                        # 新加坡幣/人民幣 匯率
                        "CHF": float(td[10].get('data-value')),                       # 法郎/人民幣 匯率
                        "CAD": float(td[11].get('data-value'))                        # 加幣/人民幣 匯率
                }  
                records.append(record) 
            else:
                self.next_valid = False
        item = RateItem()
        item['records'] = records
        self.page = self.page + 1
        return item
            
        
        
    

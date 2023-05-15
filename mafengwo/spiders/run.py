from scrapy import cmdline

# cmdline.execute("scrapy crawl mfw_test -o mfw.csv".split())
cmdline.execute("scrapy crawl mfw_spider".split())

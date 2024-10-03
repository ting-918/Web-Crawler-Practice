# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import matplotlib.pyplot as plt
import pandas as pd
# 用於顯示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
year = ['2019', '2020', '2021', '2022', '2023']
labels = ['USD', 'EUR', 'JPY', 'HKD', 'GBP', 'AUD', 'SGD', 'CHF', 'CAD']
colors = ['lightsteelblue', 'salmon', 'royalblue', 'olivedrab', 'thistle', 'sienna', 'sandybrown', 'pink', 'burlywood']

class MyprojectPipeline:
    # 初始化, 創建或打開rate.csv, 並構造 CsvItemExporter
    def __init__(self):
        self.file = open('rate.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='big5')
        self.exporter.start_exporting()
 
    # 接收 RateItem 對象, 將爬取數據輸出至 rate.csv
    def process_item(self, item, spider):
        for i in item['records']:
            self.exporter.export_item(i)
        return item
    
    # Spider工作結束後執行, 做數據可視化
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        data = pd.read_csv('rate.csv')
        # 按年度月份分組,個別求平均值
        groupData = []
        for y in year:
            for m in range(1, 13):
                time = y+"-"+str(m).zfill(2)
                filter = data.loc[(data['date'] >= time+'-01') & (data['date'] <= time+'-31')]
                mean = filter.mean(0, numeric_only=True)
                temp = [time]
                for label in labels:
                    temp.append(mean[label])
                groupData.append(temp)
        df = pd.DataFrame(groupData, columns = data.columns)
        xdata = df.loc[:,'date']
        for index, label in enumerate(labels):
            plt.plot(xdata, df.loc[:,label], color=colors[index], label=label)
        plt.title('外匯趨勢走向')
        # 不顯示x列的刻度值
        plt.xticks([])
        # 顯示圖例說明
        plt.legend()
        plt.xlabel('時間') 
        plt.ylabel('匯率(/CNY)')
        plt.show()
        

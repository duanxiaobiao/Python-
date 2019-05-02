# -*- coding: utf-8 -*-
import csv
import time
from xml import etree

import requests
import scrapy

from scrapy04.items import Scrapy04Item


class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    start_urls = ['http://www.liepin.com/']
    #分发URL
    def start_requests(self):
        position_urls = [
            # java
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=java&init=-1&searchType=1&headckid=16e4438a29faabb1&compkind=&fromSearchBtn=2&sortFlag=15&ckid=16e4438a29faabb1&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=k_cloHQj_hyIn0SLM9IfRg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=c6f2b55a36674d6c55c7c006c4cbbb1b&d_curPage=0&d_pageSize=40&d_headId=c6f2b55a36674d6c55c7c006c4cbbb1b&curPage=2',
            # python
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=python&init=-1&searchType=1&headckid=531f74942df56b60&compkind=&fromSearchBtn=2&sortFlag=15&ckid=531f74942df56b60&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=I-7rQ0e90mv8a37po7dV3Q%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=06dac66c8cde557e5064f07ba88cc483&d_curPage=0&d_pageSize=40&d_headId=06dac66c8cde557e5064f07ba88cc483&curPage=2',
            #php
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=php&init=-1&searchType=1&headckid=325a1d55f48e4bbf&compkind=&fromSearchBtn=2&sortFlag=15&ckid=325a1d55f48e4bbf&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=4b_XYjIeQJzuSsC26EGWPA%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=e05e0dba1dc5d54d7ce547426c484930&d_curPage=0&d_pageSize=40&d_headId=e05e0dba1dc5d54d7ce547426c484930&curPage=2',
            #web开发
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=web%E5%BC%80%E5%8F%91&init=-1&searchType=1&headckid=87191e4825099009&compkind=&fromSearchBtn=2&sortFlag=15&ckid=87191e4825099009&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=6upyUDXmyY9Y0v6v5J0vgA%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=ff098d36a7ebda8d4b129f4287c4e63c&d_curPage=0&d_pageSize=40&d_headId=ff098d36a7ebda8d4b129f4287c4e63c&curPage=2',
            #UI设计
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=ui%E8%AE%BE%E8%AE%A1%E5%B8%88&init=-1&searchType=1&headckid=2ccabc93c1646f1e&compkind=&fromSearchBtn=2&sortFlag=15&ckid=2ccabc93c1646f1e&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=Vak2999ktFrbuRtde-tS_g%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=d34000f152400198bf4daab40bc18906&d_curPage=0&d_pageSize=40&d_headId=d34000f152400198bf4daab40bc18906&curPage=2',
            #Android
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=Android&init=-1&searchType=1&headckid=796de00ebd73715b&compkind=&fromSearchBtn=2&sortFlag=15&ckid=796de00ebd73715b&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=6E4wuTkM22TbbbLJq4eEbQ%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=0c0f62494ee5239d91f8003596d41948&d_curPage=0&d_pageSize=40&d_headId=0c0f62494ee5239d91f8003596d41948&curPage=2',
            ##算法工程师
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=%E7%AE%97%E6%B3%95%E5%B7%A5%E7%A8%8B%E5%B8%88&init=-1&searchType=1&headckid=9bf2add1422f5680&compkind=&fromSearchBtn=2&sortFlag=15&ckid=9bf2add1422f5680&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=nlv1A9iKATx_033gm2DTIA%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=375de041c4e500e49c58eca27a2b0d71&d_curPage=0&d_pageSize=40&d_headId=375de041c4e500e49c58eca27a2b0d71&curPage=1',
            #hadoop
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=Hadoop&init=-1&searchType=1&headckid=cddea4839ba8a2f1&compkind=&fromSearchBtn=2&sortFlag=15&ckid=cddea4839ba8a2f1&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=U-s9z7tMIQvNT-GphdfJRg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=abaf4cd2b692352ffe8a4c60c0e46cc5&d_curPage=0&d_pageSize=40&d_headId=abaf4cd2b692352ffe8a4c60c0e46cc5&curPage=2',
            #数据分析
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&init=-1&searchType=1&headckid=e4afa98e7405eac9&compkind=&fromSearchBtn=2&sortFlag=15&ckid=e4afa98e7405eac9&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=ZFDYQyfloRvvhTxLnVV_Qg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=d71cacc6485a973b95850286083679b0&d_curPage=0&d_pageSize=40&d_headId=d71cacc6485a973b95850286083679b0&curPage=2',
            #人工智能
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&init=-1&searchType=1&headckid=62cb356a7106ac02&compkind=&fromSearchBtn=2&sortFlag=15&ckid=62cb356a7106ac02&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=8Gjw2tdHib7iEBY8QKS1DQ%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=42a25b9c0ea06a0bfc23799b42b9d07b&d_curPage=0&d_pageSize=40&d_headId=42a25b9c0ea06a0bfc23799b42b9d07b&curPage=3',
            #区块链
            'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=%E5%8C%BA%E5%9D%97%E9%93%BE&init=-1&searchType=1&headckid=12cf84b49c8144fe&compkind=&fromSearchBtn=2&sortFlag=15&ckid=12cf84b49c8144fe&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=ddj6-wcGyTgdTJHjsYTxnQ%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=331229693764b186fb9568002eee0bcf&d_curPage=0&d_pageSize=40&d_headId=331229693764b186fb9568002eee0bcf&curPage=3',

        ]
        page_nums = [i for i in range(101)]
        for position_url in position_urls:
            for page_num in page_nums:
                url = position_url[0:len(position_url) - 1] + str(page_num)
                yield scrapy.Request(url, callback=self.parse)

    # 注释：未完待续.....
    def parse(self, response):
        item =Scrapy04Item()
        names =response.xpath('//div[@class ="sojob-result "]//div[@class ="job-info"]/h3/a/text()').extract()
        companies =response.xpath('//div[@class ="sojob-result "]//div[@class ="company-info nohover"]/p[1]/a/text()').extract()
        salaries =response.xpath('//div[@class ="sojob-result "]//div[@class ="job-incd fo"]/p[@class="condition clearfix"]/span[1]/text()').extract()
        addresses =response.xpath('//div[@class ="sojob-result "]//div[@class ="job-info"]/p[@class="condition clearfix"]/a/text()').extract()
        experiences = response.xpath('//div[@class ="job-info"]//p[@class="condition clearfix"]/span[3]/text()').extract()
        educations = response.xpath('//p[@class="condition clearfix"]/span[@class="edu"]/text()').extract()
        welfares =response.xpath('//p[@class ="temptation clearfix"]/*/text()').extract()
        for name ,company, salary ,address,experience ,education,welfare in zip(names,companies,salaries,addresses,experiences,educations,welfares) :
            item['name'] =name.strip()
            item['company'] =company
            item['salary'] =salary
            item['address'] =address
            item['experience'] =experience
            item['education'] =education
            item['welfare'] =welfare
            yield item

# usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2
from lxml import etree
import sys
import os


reload(sys)
sys.setdefaultencoding('utf-8')

homepage_url = 'http://www.wuxiaworld.com/st-index/'
headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}


def get_all_url():
    contentpage_list = []
    # 验证list是否为空
    if len(contentpage_list) != 0:
        raise ValueError("该列表不为空")
    request_url = homepage_url
    request = urllib2.Request(request_url, headers=headers)
    response = urllib2.urlopen(request)
    homepage = response.read()
    homepage_tree = etree.HTML(homepage)
    index_node = homepage_tree.xpath('//*[@id="post-4993"]/div/div[1]/div')
    if len(index_node) == 1:
        index_node = index_node[0]
    else:
        raise ValueError("有不止一个目录节点")
    print index_node
    # print etree.tostring(index_node) # 打印当前节点中的内容
    #urls = index_node.xpath('.//p/a[starts-with(@title,"ST Book")]')       # 第九章开始没有title了，爬不全
    urls = index_node.xpath('.//p/a[starts-with(@href,"http://www.wuxiaworld.com/st-index")]')
    #print [etree.tostring(each) for each in urls]
    print len(urls)
    for each in urls:
        url = each.xpath('./@href')
        if len(url) == 1:
            contentpage_list.append(url[0])
    return contentpage_list


def get_content(contentpage_url, txt):
    request_url = contentpage_url
    request = urllib2.Request(request_url, headers=headers)
    response = urllib2.urlopen(request)
    contentpage = response.read()
    contentpage_tree = etree.HTML(contentpage)
    content_root_node = contentpage_tree.xpath('//*[@itemprop="articleBody"]')[0]
    #print len(content_root_node)
    content = content_root_node.xpath(u'./p/text()')
    print content
    fp = open(txt + '.txt', 'w')
    for each in content:
        each = each.decode("utf8")
        fp.write('%s' % each + '\n')
    fp.close()

    #print etree.tostring(content_root_node[0])



if __name__ == '__main__':
    contentpage_list = get_all_url()
    #print contentpage_list[0]
    #contentpage_list = ['']
    #contentpage_list[0] = 'http://www.wuxiaworld.com/st-index/st-book-1-chapter-1/'
    for each_url in contentpage_list[303::]:
        print each_url
        tmp = re.findall('.*/st-index/st-(.*)/', each_url)
        if len(tmp) == 0:
            tmp = re.findall('.*/st-index/(.*)/', each_url)
        if len(tmp) == 0:
            tmp = re.findall('.*/st-index/(.*)', each_url)
        print len(tmp)
        get_content(each_url, tmp[0])


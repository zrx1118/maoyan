import requests
from requests.exceptions import RequestException
from multiprocessing import Pool
import re
import json


def get_one_page(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    # ()括号包住的为匹配内容项
    pattern = re.compile('<dd>.*?board-index.*?(\d+)</i>' # 排名
                        +'.*?data-src="(.*?)".*?name"><a'  # 图片地址
                        +'.*?>(.*?)</a>'                   # 片名
                        +'.*?star">(.*?)</p>'              # 主演
                        +'.*?releasetime">(.*?)</p>'       # 上映时间
                        +'.*?integer">(.*?)</i>'           # 评分个位数
                        +'.*?fraction">(.*?)</i>'          # 平分小数点
                        +'.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii = False) + '\n')
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    if html:
        for item in parse_one_page(html):
            write_to_file(item)


if __name__ == "__main__":
    pool = Pool()
    pool.map(main, (i*10 for i in range(10)))
    pool.close()
    pool.join()
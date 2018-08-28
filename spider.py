# python中json文件处理涉及的四个函数json.dumps()和json.loads()、json.dump()和json.load()的区分
# 1、json.dumps()和json.loads()是json格式处理函数
    # (1)json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）
    # (2)json.loads()函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典）
# 2、json.dump()和json.load()主要用来读写json文件函数
import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re

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
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>' # 排名
                         +'.*?data-src="(.*?)".*?name"><a' # 图片
                         +'.*?>(.*?)</a>'                  # 名字
                         +'.*?star">(.*?)</p>'             # 主演
                         +'.*?releasetime">(.*?)</p>'      # 上映时间
                         +'.*?integer">(.*?)</i>'          # 排名个位
                         +'.*?fraction">(.*?)</i>'         # 排名小数点位
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
    with open('resul.txt', 'a', encoding='utf-8') as f:
        # json.dumps()函数的使用，将字典转化为字符串
        f.write(json.dumps(content, ensure_ascii = False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    if html:
        for item in parse_one_page(html):
            write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    # map(func, iterable[, chunksize=None])
    # Pool类中的map方法，与内置的map函数用法行为基本一致，它会使进程阻塞直到返回结果。 
    # 注意，虽然第二个参数是一个迭代器，但在实际使用中，必须在整个队列都就绪后，程序才会运行子进程。
    pool.map(main, [i*10 for i in range(10)])
    pool.close() # 关闭进程池，不再接受新的进程
    pool.join() # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
import time

import requests
from concurrent.futures import ThreadPoolExecutor
from urllib3 import disable_warnings

disable_warnings()


class links:
    def __init__(self, websiteurl, workers=16):
        self.timeout = 5
        self.path = 'links.txt'
        self.websiteurl = websiteurl
        self.workers = workers

    def push(self, url: str):
        """分发单条链接
        :param url:待分发的网址
        """
        url_new = url.format(url=self.websiteurl)
        try:
            response = requests.get(url=url_new, timeout=self.timeout, verify=False, stream=True)
            code = response.status_code
            response.close()
            return code, url_new
        except:
            return 500, url_new

    def run(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            urls = f.read().splitlines()

        pool = ThreadPoolExecutor(self.workers)

        allcount = len(urls)
        count = 1

        code_report = {
            '2xx': 0,
            '3xx': 0,
            '4xx': 0,
            '5xx': 0
        }  # 代表各个状态码的链接数量

        results = pool.map(self.push, urls)
        for i in results:
            code, url = i
            self.code(code_dict=code_report, code=code)
            print(f'{count / allcount:.2%} >>> {count} / {allcount} >>> {code} {url}')
            count = count + 1

        print('\n>>> 已全部分发完毕~')
        print('>>> 各个状态码的情况分布：')
        for k, v in code_report.items():
            print(f'{k}：{v}')

    def code(self, code_dict: dict, code: int):
        """code_dict代表各个状态码的数量
        code代表状态码"""
        if code < 300:
            code_dict['2xx'] = code_dict['2xx'] + 1
        elif code < 400:
            code_dict['3xx'] = code_dict['3xx'] + 1
        elif code < 500:
            code_dict['4xx'] = code_dict['4xx'] + 1
        else:
            code_dict['5xx'] = code_dict['5xx'] + 1


if __name__ == '__main__':
    print('外链分发工具 v1.1\n'
          '作者：勿埋我心 - SkyQian\n'
          '我的博客：https://www.skyqian.com\n'
          'YiOVE官网：https://www.yiove.com\n'
          'Github：https://github.com/Qiantigers/website-link-tool-python\n'
          f'{"-" * 16}')

    websiteurl = input('输入你的网站（不要带http）：')
    workers = input('请输入工作线程（不写则默认为16）:')
    print('-' * 16)

    if workers == '':
        workers = 16

    start_time = time.time()

    links = links(websiteurl, int(workers))
    links.run()

    print(f'>>> 运行时间：{time.time() - start_time:.2f}秒')

    input('\n\n按任意键退出……')

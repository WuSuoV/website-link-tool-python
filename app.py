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
        good = 0  # 代表有效的外链
        results = pool.map(self.push, urls)
        for i in results:
            code, url = i
            if code < 500:
                good = good + 1
            print(f'{count / allcount:.2%} >>> {count} / {allcount} >>> {code} {url}')
            count = count + 1
        print('>>> 已全部分发完毕~\n'
              f'有效外链：{good}\n'
              f'无效外链：{allcount - good}')


if __name__ == '__main__':
    print('作者：勿埋我心 - SkyQian'
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

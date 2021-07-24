import os,re
from concurrent.futures import ThreadPoolExecutor

class Download_mzt() :
    '''用于下载 彼岸图网的图片 的爬虫程序'''
    def __init__(self):
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        }#设置默认参数headers
        # self.http = urllib3.ProxyManager('https://119.250.22.204:9000')
        self.http = urllib3.PoolManager()#设置默认参数http为一个连接池

    def get(self,urls):
        """获取主页上每张图片的网址，返回一个列表"""
        res = self.http.request('GET',urls,headers=self.headers)
        html = res.data.decode('gbk')
        # html = res.data
        list = re.findall('<a href="(.*?)" target="_blank">',html)
        urls_list=list[1:-5]
        return urls_list
        # return html

    def get_pict(self,url):
        """获取大图的图片地址"""
        res =self.http.request('GET',url,headers=self.headers)
        html = res.data.decode('gbk')
        addr = re.findall('src="(.*?)" data-pic=".*?"', html)
        return addr

    def save(self,name,img):
        """保存图片"""
        with open(name,'wb') as f:
            f.write(img.data)
        print('图片{}保存成功'.format(name))

    def run(self,urls):
        """主程序"""
        urls_list = self.get(urls)
        for i in urls_list:
            url = 'https://pic.netbian.com/'+i
            addr = 'https://pic.netbian.com/' + self.get_pict(url)[0]
            a =url.split('/')[-1]
            name = './mzt/' + a.split('.')[0]+'.jpg'
            data = self.http.request('get',addr,headers=self.headers)
            self.save(name,data)


if __name__ == '__main__':
    url = 'https://pic.netbian.com/4kmeinv/'
    img = Download_mzt()
    if os.path.exists("./mzt") is False:
        os.mkdir("./mzt")
    # img.run(url)
    for i in range(145):#翻页，主页有145页，翻145次
        if i == 0:
            img.run(url)
        else:
            url_index = url + 'index_{}.html'.format(i+1)
            # pool = ThreadPoolExecutor(20)#实例化一个线程池
            # pool.submit(img.run,url_index)#多线程下载
            img.run(url_index)
    print(len(os.listdir('./mzt')))#打印已下载图片的数量
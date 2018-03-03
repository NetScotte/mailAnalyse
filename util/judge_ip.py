import urllib.request as request
import re


# 此模块用于在spamhaus上查询ip地址是否被列入黑名单，并可以获取相关信息
# 动态获取cfuid，使用固定的cfclearance，
class Judge:
    # 获取spamhaus中的cookie,即cfduid部分
    def __init__(self):
        self.tag = 0                                # spam标识，非0表示spam
        self.info = []                              # 该ip的相关信息

        # self.cfduid = 'd9f4a0ceb7145e083278cd8ca5b3c54c21486277703'  # 用于查询时的cookie
        # self.cf_clearance='52822d92bead3e893a2e8dad3af22f1b052d64f0-1486261879-28800'
        # get_cookie = re.compile(r'cfduid=(\w*);')
        # html = request.urlopen('https://www.spamhaus.org/')
        # info = str(html.info())
        # self.cfduid = get_cookie.search(info).group(1)

    # 判断是否被spamhaus列入黑名单，如果是返回true，否则返回false,
    def is_spam(self, ip):
        self.ip=ip
        url = 'https://www.spamhaus.org/query/ip/%s'%self.ip
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

        header = {'User-Agent': user_agent,\
                  'Cookie':'__cfduid=d95838016e0ac9e2492c7d97aeb46ebb81493870819; cf_clearance=0c9199501ff54fcd2fa3a921b65c0c70a149f834-1495007980-28800',\
                  'Host':'www.spamhaus.org'}

        req = request.Request(url, headers=header)

        with request.urlopen(req) as res:
            html = str(res.read())
            # 从结果网页中分析结果
            query_pattern = re.compile(r'<B>(.*?)</B>')
            res = re.compile(r'not')
            result = query_pattern.findall(html, re.S | re.M)
            for s in result:
                if not res.search(s):
                    self.tag = 1
                    s=s.lstrip('<FONT color="red">').rstrip('</FONT>')
                    self.info.append(s)

        # self.tag==1时为垃圾邮件
        if self.tag == 1:
            return True
        else:
            return False

    def get_tag(self):
        return self.tag

    def get_info(self):
        if self.tag==1:
            return ','.join(self.info)
        else:
            return 'allRight'



if __name__ == '__main__':
    j = Judge()
    if j.is_spam('61.111.75.13'):
        print('trash',j.get_info())
    else:
        print('normal',j.get_info())

import requests
import json


# 利用requests针对示例网站的评论进行查看，提交，修改，删除等操作
# r = requests.get('https://www.spamhaus.org')
# cfCookie = r.cookies
#
# r = requests.post('')

# 查看评论
# r = requests.get('https://api.github.com/repos/kennethreitz/requests/issues/482')
# c = json.loads(r.text)
# print(c['title'])
# print(c['comments'])
# 上下部分实现的功能一致，使用下面的更简洁
# try:
#     comments = r.json()
#     print(comments[u'title'])
#     print(comments[u'comments'])
# except:
#     pass

# 以上代码知道了title和该title下的commnets数量，commnets在其他网站.获取最后一条评论
# r = requests.get(r.url+u'/comments')
# print(r.status_code)
# comments = r.json()
# print(comments[0].keys())
# print(comments[9][u'body'])
# print(comments[9][u'user'][u'login'])

# 针对该comments发表评论，由于身份错误，以下行为均只能再使用真实身份后进行
# body = json.dumps({u"body": u"Sounds great! I'll get right on it!"})
# print(body)
# url = u"https://api.github.com/repos/kennethreitz/requests/issues/482/comments"
#
# auth = requests.auth.HTTPBasicAuth('','not_a_real_password')
# r = requests.post(url=url,data=body,auth=auth)
# print(r.status_code)
# comments = r.json()
# print(comments)

# 修改评论
# print(comments[u"id"])
# 5804413
#
# body = json.dumps({u"body": u"Sounds great! I'll get right on it once I feed my cat."})
# url = u"https://api.github.com/repos/kennethreitz/requests/issues/comments/5804413"
#
# r = requests.patch(url=url, data=body, auth=auth)
# r.status_code
# 200

# 删除评论
# r = requests.delete(url=url, auth=auth)

# 如何完成访问某个网页，然后在其根据其表单填写相关信息，提交后获取信息这一过程
# 这是2017年针对搜狗的访问，通过网页分析知道form表单的action为/web,即post的url为url+/web
# s = requests.Session()
# url = 'https://www.sogou.com/web'
# body = {
#     'query':'spamhaus'
# }
#
# r = s.post(url=url,data=body)
# print(r.text)

# 对于spamhaus进行post时，如果url=url+actionurl,data={'ip':'1.1.2.3'},不行，发现lookup重复，去掉时只能访问该网页
# 改为get也不行
# 设置cookie后，按照开发者工具给出的get https://www.spamhaus.org/lookup/ip/?ip=1.1.2.3显示服务不可达
# s = requests.Session()
# url = 'https://www.spamhaus.org/lookup/'
# r = s.get(url)
# # cfduid = {'__cfduid':r.cookies['__cfduid']}
# url = 'https://www.spamhaus.org/lookup/ip/'
# # c = {
# #     '__cfduid':'d95838016e0ac9e2492c7d97aeb46ebb81493870819',
# #     'cf__clearance':'dbd6e1b19505eb4a790bc1989a6d904aec255abf-1494400564-28800'
# # }
# body = {
#     'ip':'1.1.2.3'
# }
# header = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
# }
# r = s.post(url,data=body)
# print(r.text)
# print(r.status_code)
# print(r.cookies)


s = requests.Session()
r = s.get('http://www.baidu.com')
body = {
    'wd':'github'
}
r = s.get('https://www.baidu.com/s?f=8&rsv_bp=1&rsv_idx=1&word=github&tn=97424379_hao_pg',data=body)
print(r.text)
print(r.status_code)
print(r.encoding)
print(r.url)

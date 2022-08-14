#目前引用库十分杂乱
from http.cookiejar import Cookie
import requests
import urllib.request
import json
import random
import urllib.request
import requests

#预先定义变量
havecookie = 0
get_headers_state = 0
cookie_dict = {}
cookie = ''
first_run = 1


def get_id():
    ID = input("输入用户ID：")
    return ID


def get_cookie():
    global cookie
    global first_run
    if first_run == 1:
        cookie = input("你的请求头cookies:")
        first_run = 0
    return cookie


def cookie_factory(ck_str=None):

    global cookie_dict
    if ck_str:
        for cookie in ck_str.split(';'):
            try:
                k, v = cookie.strip().split('=')
                cookie_dict[k] = v
            except Exception as e:
                print(f'异常格式的cookie：{cookie} \t 异常信息：{e}')


def get_headers(referer):
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Cookie": get_cookie(),
        "Host": "icodeshequ.youdao.com",
        "Origin": "https://icodeshequ.youdao.com",
        "Referer": referer,
        "sec-ch-ua": '\" Not;A Brand\";v=\"99\",\"Microsoft Edge\";v=\"103\",\"Chromium\";v=\"103\"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49"
    }


# 快速删除作品
def del_project():
    ID = get_id()
    site = 'https://icodeshequ.youdao.com/api/user/works/hisWorksList?page=1&size=20&userId='+ID
    y = int(input("你要删除的页数："))
    cookie = get_cookie()
    temp = 0
    json = urllib.request.urlopen(site).read()
    for i in range(y):
        print("正在删除第"+str(i+1)+"页的作品......")
        while '"id":' in json.decode('utf-8'):
            json = json[json.decode('utf-8').index('"id":')+6:len(json):1]
            temp = json[0:json.decode('utf-8').index('"'):1]
            json = urllib.request.urlopen(site).read()
            print(temp)
            print(requests.delete(url='https://icodeshequ.youdao.com/api/works/delete?id='+temp.decode(
                "utf-8"), headers=get_headers("https://icodeshequ.youdao.com/my/works?page=1")).json())

        print("已完全删除第"+str(i+1)+"页的作品！")

    print("已将该账户的所有作品删除完毕！欢迎下次使用")

# 刷作品
def brush_project():

    i = 0
    quantity = int(input("你要刷的作品数量："))
    while i < quantity:
        requests.post(url='https://icode.youdao.com/api/work/submit', data='category=lab&theme=art&subtheme=artist&title=%E4%BD%9C%E5%93%81&description=test&code=%3Cxml%3E%3Cblock+type%3D%22turtle_start%22+deletable%3D%22false%22+movable%3D%22false%22%3E%3Cnext%3E%3Cblock+type%3D%22turtle_print%22+inline%3D%22false%22%3E%3Cvalue+name%3D%22TEXT%22%3E%3Cblock+type%3D%22text%22%3E%3Ctitle+name%3D%22TEXT%22%3E%E4%BD%9C%E5%93%81%3C%2Ftitle%3E%3C%2Fblock%3E%3C%2Fvalue%3E%3C%2Fblock%3E%3C%2Fnext%3E%3C%2Fblock%3E%3C%2Fxml%3E&thumbnail=https%3A%2F%2Fshared-https.ydstatic.com%2Fke%2Ficode%2Fapps%2Fstatic%2Fimages%2Fthumbnail%2Fartist1.jpg&publish=1&fork=1', headers=get_headers("\"https://icode.youdao.com/csl/artist?from=icodeshequ_nav\""))
        i += 1
        print("已发送第"+str(i)+"次请求")

# 刷评论
def brush_comment():
    urll = input("请输入你要刷屏的作品网址：")[-32::]
    text = []
    n = int(input("要有多少个随机刷屏词？"))
    for i in range(n):
        text.append(str(input("第"+str(i+1)+"个刷屏词为：")))
    i = 0
    k = 0
    print(text)
    while True:
        k = random.randint(0, n-1)
        print(requests.post(url='https://icodeshequ.youdao.com/api/works/comment', data=str('{"id":"'+urll+'","content":"'+text[k] + '"}').encode('GB2312')  , headers=get_headers(
            '"'+"https://icodeshequ.youdao.com/work/" + urll + "?from=home"+'"')).json())
        i += 1
        print("已发送"+str(i)+"次刷屏请求（实际为五秒刷一次）")

# 刷收藏
def brush_enshrine():
    i = 0
    brush_enshrine_id = input("输入你要刷的作品网址")[-32::]
    quantity = int(input("你要刷的收藏与取消数量："))
    cookie_factory(ck_str=get_cookie())
    while i < quantity:
        requests.post(url='https://icodeshequ.youdao.com/api/user/works/enshrine?worksId=' +
                      brush_enshrine_id, cookies=cookie_dict)
        requests.post(url='https://icodeshequ.youdao.com/api/user/works/cancelEnshrine?worksId=' +
                      brush_enshrine_id, cookies=cookie_dict)
        i += 1
        print("已发送第"+str(i)+"次请求")

# 查询作品信息
def query_work_information():

    site = input("输入你要查询的作品网址")[-32::]
    an = input("输入这个作品是否为改编作品（是或否）：")
    site2 = 'https://icodeshequ.youdao.com/api/works/detail?id='+site
    print("源网址："+site2)
    site2 = urllib.request.urlopen(site2).read()

    n = 0  # 当前所读

    k = 0  # 列表所读

    strr = ""  # 储存
    if an == "是":
        a = ['"id":', '"title":', '"imgUrl":', '"description":', '"type":', '"userId":', '"status":', '"likeNum":', '"browseNum":', '"enshrineNum":', '"code":', '"userName":', '"userImage":', '"forkId":', '"haveLiked":', '"haveEnshrined":',
             '"createTimeStr":', '"updateTimeStr":', '"codeLanguage":', '"shortLink":', '"theme":', '"subTheme":', '"iframeUrl":', '"scratchFile":', '"codeType":', '"firstPopups":', '"forkAuthorizationStatus":', '"isFirstPublish":', '"haveReported":']
        b = ["作品ID：", "标题：", "封面储存在小图灵图床的位置：", "简介：", "类型：", "发布者ID：", "地位：", "点赞量：", "浏览量：", "收藏量：", "该作品的源码地址（仅sc作品适用）：", "发布者昵称：", "发布者头像储存在小图灵图床的位置：",
             "改编ID(为空则代表原创，有时将会显示你的邮箱)：", "你的账号给该作品点过的赞数：", "你的账号给该作品点过的收藏数：", "发布时间：", "更新时间：", "代码语言：", "在分享端的作品网址：", "导入库：", "子导入库：", "作品在展示页所iframe的展示网址：", "scratch文件：", "源码格式：", "第一个弹出窗口（不是为1是为0）：", "是否允许改编（不是为1是为0）：", "这个作品是否首次发布：", "是否已被你的账号举报（0为未举报1为已举报）："]
    else:
        a = ['"id":', '"title":', '"imgUrl":', '"description":', '"type":', '"userId":', '"status":', '"likeNum":', '"browseNum":', '"enshrineNum":', '"code":', '"userName":', '"userImage":', '"haveLiked":', '"haveEnshrined":', '"createTimeStr":',
             '"updateTimeStr":', '"codeLanguage":', '"shortLink":', '"theme":', '"subTheme":', '"iframeUrl":', '"scratchFile":', '"codeType":', '"firstPopups":', '"forkAuthorizationStatus":', '"isFirstPublish":', '"haveReported":']
        b = ["作品ID：", "标题：", "封面储存在小图灵图床的位置：", "简介：", "类型：", "发布者ID：", "地位：", "点赞量：", "浏览量：", "收藏量：", "该作品的源码地址（仅sc作品适用）：", "发布者昵称：", "发布者头像储存在小图灵图床的位置：", "你的账号给该作品点过的赞数：", "你的账号给该作品点过的收藏数：",
             "发布时间：", "更新时间：", "代码语言：", "在分享端的作品网址：", "导入库：", "子导入库：", "作品在展示页所iframe的展示网址：", "scratch文件：", "源码格式：", "第一个弹出窗口（不是为1是为0）：", "是否允许改编（不是为1是为0）：", "这个作品是否首次发布：", "是否已被你的账号举报（0为未举报1为已举报）："]
    c = []
    for i in range(len(site2)):
        if not k == len(a):
            if not n == len(a[k]):
                if site2[i] == a[k][n]:
                    strr = ""
                    n += 1
                else:
                    strr = ""
            else:
                strr = strr+site2[i]
                if a[k] == '"code":':
                    strr = ""
                if (site2[i+1] == ',' and site2[i+2] == '"') or (a[k] == '"haveReported":' and site2[i+1] == "}"):
                    c.append(strr)
                    n = 0
                    k += 1
                    if a[k-1] == '"code":':
                        strr = ""
                        print(
                            b[k-1]+'https://icode.youdao.com/scratch/project/'+site)

                    else:
                        print(b[k-1]+strr)

    print("作品评论列表："+'https://icodeshequ.youdao.com/api/works/comment/list?id='+site)
    k += 1

    print("作者的推荐作品栏："+'https://icodeshequ.youdao.com/api/user/more_works/list?userId={usid}&currentWorksId={zpid}'.format(
        usid=c[5][1:-1:1], zpid=c[0][1:-1:1]))
    k += 1

#主题
print('opentuling.py，欢迎使用')
print('功能列表')
print('1.删除作品,2.刷作品,3.刷评论,4.刷收藏,5.查询作品信息')
print('先给qqcd致敬,我抄了他许多代码(读书人的事，能叫抄吗?)')
choice = input('请输入你的选择：')
while choice != '退出':
    first_run = 1
    if choice == '1':
        del_project()
    elif choice == '2':
        brush_project()
    elif choice == '3':
        brush_comment()
    elif choice == '4':
        brush_enshrine()
    elif choice == '5':
        query_work_information()
    else:
        print('输入错误，请重新输入')
    print('功能列表')
    print('1.删除作品,2.刷作品,3.刷评论,4.刷收藏,5.查询作品信息')
    choice = input('请输入你的选择：')

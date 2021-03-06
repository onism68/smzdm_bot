"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

import config
from utils.serverchan_push import push_to_wechat

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            print(result)
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = cookies    

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content




if __name__ == '__main__':
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["SMZDM_COOKIES"]
    SERVERCHAN_SECRETKEY = os.environ["SERVERCHAN_SECRETKEY"]
    PUSH_URL = os.environ["PUSH_URL"]
    SECRETKEY = os.environ["SECRETKEY"]
    SECRETKEY_VALUE = os.environ["SECRETKEY_VALUE"]
    PUSH_ID = os.environ["PUSH_ID"]
    PUSH_ID_VALUE = os.environ["PUSH_ID_VALUE"]
    
    PUSH_TG_URL = os.environ["PUSH_TG_URL"]
    PUSH_TG_ID = os.environ["PUSH_TG_ID"]
    sb.load_cookie_str(cookies)
    res = sb.checkin()
    print(res)
#     try:
#         session = requests.Session()
#         session.headers = {SECRETKEY: SECRETKEY_VALUE}
#         res1 = session.post(url=PUSH_URL, json={PUSH_ID:PUSH_ID_VALUE,"message":str(res)})
#         print(res1.text)
#     except Exception as e:
#         print(e)
# TG 推送
    try:
        session = requests.Session()
#         session.headers = {SECRETKEY: SECRETKEY_VALUE}
        res1 = session.post(url=PUSH_TG_URL, json={"id":PUSH_TG_ID,"msg":str(res)})
        print(res1.text)
    except Exception as e:
        print(e)
    push_to_wechat(text = '什么值得买每日签到',
                    desp = str(res),
                    secretKey = SERVERCHAN_SECRETKEY)

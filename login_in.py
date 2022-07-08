import sys
import requests
import qrcode_terminal as qt

if __name__ == '__main__':
    # bilibili 登录认证相关内容参考
    # https://github.com/SocialSisterYi/bilibili-API-collect/blob/a7a743dffdb0e22ef735a8639dd3c3ead82665e4/other/API_auth.md

    # bilibili 二维码登录相关 api 参考
    # https://github.com/SocialSisterYi/bilibili-API-collect/blob/a7a743dffdb0e22ef735a8639dd3c3ead82665e4/login/login_action/QR.md

    # 获取扫码登录的秘钥以及二维码 url
    login_url = requests.get(
        'http://passport.bilibili.com/qrcode/getLoginUrl').json()

    # url 用于生成二维码
    url = login_url['data']['url']

    # 扫码登录秘钥, cd 为 180 秒
    aouth_key = login_url['data']['oauthKey']

    # 打印二维码到控制台
    qt.draw(url)

    # 疑似 qrcode_terminal 的 bug
    # 不刷新缓冲区的话, 接下来的 print() 有概率输出乱码
    sys.stdout.flush()

    while True:
        input("扫码后请按回车")

        # 验证扫码登录
        login_payload = {'oauthKey': aouth_key}
        login_info = requests.post(
            'http://passport.bilibili.com/qrcode/getLoginInfo', data=login_payload)

        if login_info.json()['status']:
            break
        else:
            print("好像还没扫? 或者没确认登录?")

    # 获取 cookie
    cookie = login_info.cookies.get_dict()
    csrf = cookie['bili_jct']
    access_key = cookie['SESSDATA']
    uid = cookie['DedeUserID']

    print(f"{uid = }, 登录成功.")

    # 像这样完成一些账号的操作, cookie 认证方式需要提供 csrf, app 认证方式需要提供 access_key
    # 使用 cookie 认证方式修改登录账号的签名:
    payload = {'user_sign': 'test',
               'csrf': csrf}
    requests.post(url='http://api.bilibili.com/x/member/web/sign/update',
                  cookies=cookie, data=payload)

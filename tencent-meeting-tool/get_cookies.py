import requests
import time
import json
import os

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    temp_file_path = os.path.join(script_dir, "session_key")
    session_key = ""
    # 读取并解析文件内容
    with open(temp_file_path, "r") as file:
        session_key = file.read()

    if session_key == "":
        print("error", end="")
        return

    count = 0
    while True:
        if count > 30:
            print("error", end="")
            break
        response = requests.post(
            url="https://meeting.tencent.com/wemeet-tapi/v2/user-logic/login/qr-code/query-status",
            params=build_params(),
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "session_key": session_key,
            })
        )
        if response.status_code == 200:
            res = response.json()
            data = res["data"]
            if data["status"] != 3:
                count += 1
                # sleep
                time.sleep(2)
                continue
            login_code = data["auth_login_code"]
            get_cookie(session_key, login_code)
            break
        else:
            print("error", end="")
            break

def get_cookie(session_key, login_code):
    response = requests.get(
        url="https://meeting.tencent.com/wemeet-webapi/v2/account/auth/wechat-login-mp",
        params={
            "code": login_code,
            "state": session_key,
            "is_support_nature": "1",
            "is_support_wechat_bind_optimization": "1",
            "features_version": "1.0",
            "c_os": "web",
            "c_os_version": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "c_os_model": "web",
            "c_timestamp": get_now(),
            "c_instance_id": "5",
        },
        headers={
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Content-Type": "application/json; charset=utf-8",
        },
    )

    if response.status_code != 200:
        print("error", end="")
        return

    response = response.json()
    if response["code"] != 0:
        print("error", end="")
        return

    auth_code = response["data"]["auth_code"]

    response = requests.post(
        url="https://meeting.tencent.com/wemeet-webapi/v2/account/login/auth-code",
        params=build_params(),
        headers={
            "Content-Type": "application/json",
        },
        data=f'{{"auth_code": "{auth_code}","identity_type": 1,"corp_id": "200000001","verify_code": ""}}'
    )

    cookies_str = ""
    for cookie in response.cookies:
        cookies_str += f"{cookie.name}={cookie.value}; "

    script_dir = os.path.dirname(os.path.realpath(__file__))

    # 生成临时文件的路径
    temp_cookies_path = os.path.join(script_dir, "cookies")

    # 将数据写入文件
    with open(temp_cookies_path, "w") as file:
        file.write(cookies_str)

def build_params():
    return {
        "c_os": "web",
        "c_os_version": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "c_os_model": "web",
        "c_timestamp": get_now(),
        "c_instance_id": "5",
        "c_lang": "zh-cn",
    }

def get_now():
    return str(int(round(time.time() * 1000)))

if __name__ == "__main__":
    main()

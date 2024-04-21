import requests
import json
import time
import sys
import os

def main():
    cookies = get_cookies()
    if not content.strip():
        print("not_login", end="")
        return

    now = time.time()
    response = requests.post(
        url="https://meeting.tencent.com/wemeet-tapi/wemeet/manage_service/comm/v1/cancel_meeting",
        params={
            "c_os_model": "web",
            "c_os": "web",
            "c_os_version": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "c_timestamp": str(int(round(now * 1000))),
            "c_instance_id": "5",
        },
        headers={
            "Cookie": cookies,
            "Content-Type": "application/json; charset=utf-8",
        },
        data=json.dumps({
            "meeting_id": str(sys.argv[1]),
            "meeting_type": 0,
        })
    )
    if response.status_code == 200:
        print("success", end="")

def get_cookies():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    temp_file_path = os.path.join(script_dir, "cookies")
    if not os.path.exists(temp_file_path):
        return ""
    if os.path.getsize(temp_file_path) == 0:
        return ""
    # 读取并解析文件内容
    with open(temp_file_path, "r") as file:
        cookies = file.read()
    return cookies

if __name__ == "__main__":
    main()

import os
import sys
import time
import json
import base64
import requests
from datetime import datetime

def main():
    cookies = get_cookies()
    if not cookies.strip():
        print("not_login", end="")
        return

    arg = str(sys.argv[1])
    if not arg.strip():
        print("no_args", end="")
        return

    meeting_result = str(sys.argv[2])
    password_prompt_prefix = str(sys.argv[3])

    args = arg.split(',')
    now = time.time()

    response = requests.post(
        url="https://meeting.tencent.com/wemeet-tapi/wemeet/manage_service/comm/v1/query_meeting_item",
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
            "meeting_code": args[1],
            "meeting_id": args[0],
        })
    )

    if response.status_code == 200:
        data = response.json()

        meeting_item = data['meeting_item']

        # 解码URL和主题
        decoded_url = base64.b64decode(meeting_item['url']).decode('utf-8')
        decoded_subject = base64.b64decode(meeting_item['subject']).decode('utf-8')
        decoded_pass = base64.b64decode(meeting_item['password']).decode('utf-8')

        # 将UNIX时间戳转换为可读的日期时间格式
        begin_time_readable = datetime.fromtimestamp(int(meeting_item['begin_time'])).strftime('%Y-%m-%d %H:%M')
        end_time_readable = datetime.fromtimestamp(int(meeting_item['end_time'])).strftime('%Y-%m-%d %H:%M')

        variables = {
            "subject": decoded_subject,
            "meeting_code": meeting_item["meeting_code"],
            "url": decoded_url,
            "password": decoded_pass,
            "begin_time": begin_time_readable,
            "end_time": end_time_readable,
        }
        print(meeting_result.format(**variables))
        if decoded_pass.strip():
            print(password_prompt_prefix.format(password=decoded_pass), end="")

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

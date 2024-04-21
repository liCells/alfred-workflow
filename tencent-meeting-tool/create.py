#!/usr/bin/python3

import requests
import datetime
import time
import json
import sys
import base64
import os

now = time.time()

def parse_time(time_str):
    if time_str.find("/") != -1:
        return int(time.mktime(time.strptime(time_str, "%Y-%m-%d/%H:%M")))
    else:
        if time_str[-1] == "m":
            return int(now) + int(time_str[:-1]) * 60
        if time_str[-1] == "h":
            return int(now) + int(time_str[:-1]) * 60 * 60

        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_str = today.strftime("%Y-%m-%d")

        if len(time_str) > 2:
            return int(time.mktime(time.strptime(today_str + " " + time_str, "%Y-%m-%d %H:%M")))
        return int(time.mktime(time.strptime(today_str + " " + time_str, "%Y-%m-%d %H")))

# python3 main.py "cookie" -n meeting_name -p password -m 30 -t 2023-11-09/12:30
# python3 main.py "cookie" -n meeting_name -p password -m 30 -t 12:30
# python3 main.py "cookie" -n meeting_name -p password -m 30 -t 1h
def main():
    cookies = get_cookies()
    if not cookies.strip():
        print("not_login", end="")
        return

    default_meeting_name = str(sys.argv[1])
    end_time = 1800

    data = {
        "begin_time": int(now),
        "end_time": int(now) + end_time,
        "password": "",
        "subject": str(base64.b64encode(default_meeting_name.encode('utf-8')).decode('ascii')),
        "media_set_type": "0",
        "allow_unmute_by_self": "1",
        # "create_type": "1"
    }

    has_password = False
    password = ""

    if len(sys.argv) > 2:
        for i in range(2, len(sys.argv), 2):
            if sys.argv[i] == "-m":
                end_time = int(sys.argv[i + 1]) * 60
                data["end_time"] = str((int(data["begin_time"]) + end_time))
            elif sys.argv[i] == "-t":
                start_time = parse_time(sys.argv[i + 1])
                data["begin_time"] = str(start_time)
                data["end_time"] = str(start_time + end_time)
            elif sys.argv[i] == "-n":
                data["subject"] = str(base64.b64encode(sys.argv[i + 1].encode('utf-8')).decode('ascii'))
            elif sys.argv[i] == "-p":
                data["password"] = str(base64.b64encode(sys.argv[i + 1].encode('utf-8')).decode('ascii'))
                has_password = True
                password = sys.argv[i + 1]
            else:
                print("error")
                return

    params = {
        "c_os_model": "web",
        "c_os": "web",
        "c_os_version": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "c_timestamp": str(int(round(now * 1000))),
        "c_instance_id": "5",
    }

    response = requests.post(
        url="https://meeting.tencent.com/wemeet-tapi/wemeet/manage_service/personal/v1/schedule_rapid_meeting",
        params=params,
        headers={
            "Cookie": cookies,
            "Content-Type": "application/json; charset=utf-8",
        },
        data=json.dumps(data)
    )

    if response.status_code == 200:
        res = response.json()
        print("code: " + str(res["meeting_code"]))
        if has_password:
            print("password: " + str(password))
        print("join url: " + str(base64.b64decode(res["url"]).decode('ascii')), end="")
    else:
        print("error", end="")

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

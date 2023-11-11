import requests
import json
import time
import sys
import datetime
import base64

def main():
    now = time.time()

    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_timestamp = int(today.timestamp())

    response = requests.post(
        url="https://meeting.tencent.com/wemeet-tapi/wemeet/manage_service/personal/v1/query_personal_meeting_list",
        params={
            "c_os_model": "web",
            "c_os": "web",
            "c_os_version": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "c_timestamp": str(int(round(now * 1000))),
            "c_instance_id": "5",
        },
        headers={
            "Cookie": str(sys.argv[1]),
            "Content-Type": "application/json; charset=utf-8",
        },
        data=json.dumps({
            "binary_meeting_type": 0,
            "meeting_state": 0,
            "sort": "0",
            "time_zone": str(sys.argv[2]),
            "end_time": today_timestamp + 31795199,
            "meetingCode": "",
            "subject": "",
            "begin_time": today_timestamp,
            "page_index": 1,
            "page_size": 20
        })
    )
    if response.status_code == 200:
        res = response.json()
        res = res["meeting_list"]

        print_obj = {}
        items = []
        for i in range(0, len(res)):
            obj = res[i]
            subject = str(base64.b64decode(obj["subject"]).decode('utf-8'))
            begin_time = datetime.datetime.fromtimestamp(int(obj["begin_time"])).strftime("%Y-%m-%d %H:%M")
            end_time = datetime.datetime.fromtimestamp(int(obj["end_time"])).strftime("%Y-%m-%d %H:%M")
            items.append({
                "uid": str(i),
                "title": subject + " - " + str(obj["meeting_code"]),
                "subtitle": begin_time + " - " + end_time,
                "arg": str(obj["meeting_id"]) + "," + str(obj["meeting_code"]),
            })

        print_obj["items"] = items
        print(json.dumps(print_obj))
    else:
        print("error")

if __name__ == "__main__":
    main()

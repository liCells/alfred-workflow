import requests
import time
import uuid
import qrcode
from io import BytesIO
import base64
import json
import os

def main():
    generated_uuid = uuid.uuid4()
    formatted_uuid = str(generated_uuid).replace('-', '_')

    response = requests.post(
        url="https://meeting.tencent.com/wemeet-tapi/v2/user-logic/login/qr-code/session-key",
        params=build_params(),
        headers={
            'Content-Type': 'application/json',
        },
        data=f'{{"uuid":"{formatted_uuid}","instance_id":5}}'
    )

    if response.status_code == 200:
        res = response.json()
        data = res["data"]
        generate_qrcode(data["session_key"])
    else:
        print("error", end="")
        return

def generate_qrcode(session_key):
    # 创建QRCode对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )

    # 添加数据到QRCode对象
    qr.add_data(build_login_url(session_key))
    qr.make(fit=True)

    # 创建PIL图像对象
    img = qr.make_image(fill_color="black", back_color="white")

    # 将二维码图像转换为base64编码的字符串
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    # 创建一个临时文件夹
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # 生成临时文件的路径
    temp_file_path = os.path.join(script_dir, "qr_code.png")

    # 将base64编码的图片数据解码并保存到临时文件
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(base64.b64decode(img_base64))

    # 生成临时文件的路径
    temp_session_key_path = os.path.join(script_dir, "session_key")

    # 将数据写入文件
    with open(temp_session_key_path, "w") as file:
        file.write(session_key)

    result = [{"uid": "qr_code", "title": "Login Qr Code", "arg": temp_file_path, "type": "file", "subtitle": "Scan the QR code to login, please press 'shift'"}]
    print(json.dumps({"items": result}))

def build_login_url(session_key):
    return f"https://meeting.tencent.com/v2/scan-login-qrcode?sessionKey={session_key}&instance=5"

def build_params():
    return {
        "c_os": "web",
        "c_os_version": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "c_os_model": "web",
        "c_timestamp": str(int(round(time.time() * 1000))),
        "c_instance_id": "5",
        "c_lang": "zh-cn",
    }

if __name__ == "__main__":
    main()

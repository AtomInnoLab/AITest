import requests
from main.tools.Requests import post_request
from typing import List, Dict
from main.configs.WxPusherConfig import WX_PUSHER_API_TOKEN

def list_to_html(items: List[Dict[str, str]]) -> str:
    # 遍历列表
    html_parts = []
    # 遍历字典
    for item in items:
        html_part = f'<p style="color: #3498DB; margin: 0; padding: 0;"><strong>{item["title"]}:</strong> {item["content"]}</p>'
        html_parts.append(html_part)
    return "<br>".join(html_parts)


def push_message():
    put_dict = dict()
    # 定义列表，用于存储字典
    items_list = []
    # 遍历字典
    for key, value in put_dict.items():
        items_list.append({
            "title": key,
            "content": value
        })

    # 转换 items_list 为带样式的 HTML
    items_html = list_to_html(items_list)
    url = "https://wxpusher.zjiecode.com/api/send/message"
    headers = {
        "Content-type": "application/json"
    }
    params = {
        "appToken": f"{WX_PUSHER_API_TOKEN}",
        "content": f'<h1 style="margin: 0; padding: 0;">AITest自动化消息推送</h1><br/>{items_html}',
        "summary": "自动化执行报告",
        "contentType": "application/json",
        "uids": [
            # 用户UID
            "UID_N54evkDKVYjl6HrAoXpkxcNolMty",
            # "UID_m10lupB7NeQuGhlkikqepD2KBhTf",
            # "UID_CRCyFL6k2unWsNLJ8PgMqdfG4v2z"
        ],
    }
    # 发送请求，推送到WxPusher上
    response = requests.post(url, headers=headers, json=params)
    # 打印结果
    print(response.json())


if __name__ == '__main__':
    # 调用推送方法
    push_message()
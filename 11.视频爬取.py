import os
import time
import requests
import re
from pypinyin import pinyin, Style
def chinese_to_pinyin(name):
    pinyin_list = pinyin(name, style=Style.NORMAL)
    pinyin_str = ''.join([item[0] for item in pinyin_list])
    return pinyin_str
def get_first_m3u8(url, headers, url_ts,name):
    try:
        res = requests.get(url, headers=headers)
        data = res.text
        m3u8_match = re.search(r'"url":"(.+?index\.m3u8)"', data)
        if not m3u8_match:
            print("未找到M3U8 URL")
            return
        m3u8_uri = m3u8_match.group(1).replace('\\', '')
        m3u8_res = requests.get(m3u8_uri, headers=headers)
        m3u8_data = m3u8_res.text
        get_second_m3u8(m3u8_data, url_ts, headers,name)
    except Exception as e:
        print(f"Error occurred: {e}")
def get_second_m3u8(m3u8_data, url_ts, headers,name):
    pattern = r'#EXT-X-STREAM-INF:.*\n(.+)'
    match = re.search(pattern, m3u8_data)
    time.sleep(1)
    if not match:
        print("未找到stream URI")
        return
    index_url = "https://v8.tlkqc.com/wjv8/202401/07/0dTdr5Myd41/video/" + match.group(1)
    time.sleep(1)
    down_load(index_url, url_ts, headers,name)
def down_load(index_url, url_ts, headers,name):
    # url="https://v8.tlkqc.com/wjv8/202401/07/0dTdr5Myd41/video/1000k_0X720_64k_25/hls/index.m3u8"
    # if url==index_url.strip():
    #     print("yes")
    # else:
    #     print("no")
    count = 0
    res = requests.get(index_url.strip(), headers=headers)
    res_text = res.text
    print(res.status_code)
    ts_files = re.findall(r"([a-zA-Z0-9]+\.ts)", res_text)
    if not os.path.isdir(name):
        os.mkdir(name)
    for i in ts_files:
        count += 1
        u = url_ts + i
        r = requests.get(u, headers=headers).content
        print(u)
        with open('./ts/' + str(count) + ".ts", mode="wb") as file:
            file.write(r)
if __name__ == '__main__':
    print("请输入想查找的视频:")
    name = input()
    print("请输入想获取的集数(如果是电影填1):")
    count = input()
    name_py = chinese_to_pinyin(name)
    url = f"https://www.hbyhgd168.com/go/{name_py}/1-{count}.html"
    url_ts = "https://v1.kuqjz.com/ts/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }
    get_first_m3u8(url, headers, url_ts,name)

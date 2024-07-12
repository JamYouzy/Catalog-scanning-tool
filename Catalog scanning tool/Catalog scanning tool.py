# coding=utf-8
import requests
from typing import List
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

class URLScanner:
    def __init__(self):
        pass

    def get_contents(self, file_path: str) -> List[str]:
        try:
            with open(file_path, 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在")
            return []

    def get_url(self, url: str, dict_list: List[str]) -> List[str]:
        def safe_get(url: str):
            try:
                res = requests.get(url)
                return url if res.status_code in [200, 302, 403] else None
            except Exception as e:
                # print(f"请求 {url} 时发生错误: {e}")
                return None

        valid_urls = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(safe_get, url + line.strip()) for line in dict_list]
            for future in tqdm(futures, desc="Scanning URLs", unit="URL"):
                result = future.result()
                if result is not None:
                    valid_urls.append(result)
        return valid_urls

if __name__ == '__main__':
    scanner = URLScanner()
    dict_list = scanner.get_contents(input("请输入字典文件路径（含文件名）："))
    if not dict_list:
        print("没有有效的字典文件内容")
        exit(1)

    url_input = input("请输入需要扫描的URL（含协议）：")
    if not url_input.startswith("http://") and not url_input.startswith("https://"):
        url_input = f"http://{url_input}"
    url = url_input

    valid_urls = scanner.get_url(url, dict_list)

    # 将结果写入文件
    with open('url_go.txt', 'w') as f:
        for url in valid_urls:
            f.write(url + '\n')

    print("扫描完成，有效URL已写入url_go.txt文件。")

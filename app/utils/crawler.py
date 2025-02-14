import json
import os
from bs4 import BeautifulSoup
import requests



class PTITNoticeCrawler:
    def __init__(self, base_url, max_page=4):
        self.base_url = base_url
        self.max_page = max_page
    def get_content_from_a_notice(self, notice_url):
        '''
        Hàm này trả về nội dung của một thông báo bao gồm cả văn bản và hình ảnh
        tham số:
            url: url của thông báo
        return:
            dict: 
                {
                    "text": str,
                    "image_links": list[str]
                }
        '''
        response = requests.get(notice_url)
        soup = BeautifulSoup(response.text, features="html.parser")
        content = soup.find("div", class_="post-content")
        # nếu không tìm thấy content thì trả về None
        if not content:
            return None
        text = '' # văn bản
        image_links = [] # các link ảnh
        for p in content.find_all("p"):
            # nếu có text thì thêm vào text
            if p.text.strip() :
                text += p.text.strip() + '\n'
        # nếu có ảnh thì thêm vào image_links
        for img in content.find_all("img", src=True):
            image_links.append(img['src'])
        return dict(text=text, image_links=image_links)
    def get_notices_from_a_page(self, page_url):
        '''
        Hàm này trả về toàn bộ thông báo từ trang thông báo của trường PTIT
        return:
            list[dict]: 
                [
                    {
                        "title": str,
                        "date": str,
                        "url": str,
                        "content": dict
                    }
                ]
        '''
        try:
            data = []
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, features="html.parser")
            ul = soup.find("ul", class_="ova-blog column_4 version_1 default-post")
            items = ul.find_all("li", class_="item")
            # lấy thông tin từ từng item
            for item in items:
                content = item.find("div", class_="content")
                # lấy title, url, date từ item
                title = content.find("h2", class_= 'post-title').text.strip()
                url = content.find("a" )['href'].strip()
                date = content.find("span", class_="right date").text.strip()
                data.append(dict(title=title, date=date, url=url, content=self.get_content_from_a_notice(url)))
            return data
        except Exception as e:
            print(f"Lỗi không thể lấy thông báo từ trang {page_url}")
    def crawl_all(self):
        '''
        Hàm này trả về toàn bộ thông báo từ trang thông báo của trường PTIT
        return:
            list[dict]: 
                [
                    {
                        "title": str,
                        "date": str,
                        "url": str,
                        "content": dict
                    }
                ]
        '''
        notices = []
        for i in range(1, self.max_page + 1):
            page_url = f"{self.base_url}/page/{i}"
            notices.extend(self.get_notices_from_a_page(page_url))
            print(f"Đã lấy toàn bộ các thông báo từ trang {i}")
        return notices

    def get_latest_notice(self):
        '''
        Hàm này trả về thông báo thông báo mới nhất từ trang thông báo của trường PTIT
        return: dict:
                    {
                        "title": str,
                        "date": str,
                        "url": str,
                        "content": dict
                    }
        '''
        url = f"{self.base_url}/page/1"
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, features="html.parser")
            ul = soup.find("ul", class_="ova-blog column_4 version_1 default-post")
            item = ul.find("li", class_="item")
            post = item.find("div", class_="content")
            # lấy title, url, date từ item
            title = post.find("h2", class_= 'post-title').text.strip()
            url = post.find("a" )['href'].strip()
            date = post.find("span", class_="right date").text.strip()
            return dict(title=title, date=date, url=url, content=self.get_content_from_a_notice(url))
        except Exception as e:
            print(f"Lỗi không thể lấy thông báo mới nhất từ trang {url}")
    def save(self, data, file_name):
        '''
        '''
        data_dir = os.path.join( 'data', 'raw')
        with open(os.path.join(data_dir, file_name), 'w', encoding='utf-8') as f:
            s = json.dumps(notices, ensure_ascii=False, indent=4)
            f.write(s)


# các url cần thiết
THONG_BAO_URL = 'https://ptit.edu.vn/tin-tuc-su-kien/thong-bao'
MAX_PAGE = 4

notice_crawler = PTITNoticeCrawler(THONG_BAO_URL, MAX_PAGE)
# notices = notice_crawler.crawl_all()
# notice_crawler.save(notices, "notices.json")
latest_notice = notice_crawler.get_latest_notice()
print(latest_notice)

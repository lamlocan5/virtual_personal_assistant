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


class PTITEventCrawler:
    def __init__(self, base_url, max_page = None):
        self.base_url = base_url
        self.max_page = max_page
    def get_content_from_event(self,  event_url ):
        """
        return: dict:
                    {
                        "texts": str,
                        "images": list[str]
                    }
        """
        response = requests.get(event_url)
        soup = BeautifulSoup(response.text, features="html.parser")
        content = soup.find("div", class_="ovaev-event-content")
        texts = ""
        images = []
        for p in content.find_all("p",  class_= lambda classes: classes is None or "wp-caption-text" not in classes) :
            if p.text.strip():
                texts += p.text.strip() + "\n"
        for img in content.find_all("img", src=True):
            images.append(img['src'].strip())
        return dict(texts=texts, images=images)
    
    def get_events_from_a_page(self, page_url):
        """
        return: list[dict]:
                    [
                        {
                            "title": str,
                            "date": str,
                            "url": str,
                            "content": dict
                        }
                    ]
        """
        data = []
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, features="html.parser")
        ul = soup.find("div", class_="ovaev-search-ajax-container")
        items = ul.find_all("div", class_="ovaev-content")
        for item in items:
            event = item.find("div", class_="event_post")
            title = event.find("h2").text.strip()
            date = event.find("div", class_="meta-event").find("div" , class_= "time equal-date").find("span" , class_= "time-date-child").text.strip()
            url = event.find("a")['href'].strip()
            data.append(dict(title=title, date=date, url=url, content=self.get_content_from_event(url)))
        return data
    
    # def crawl_all(self):
    #     """
    #     return: list[dict]:
    #                 [
    #                     {
    #                         "title": str,
    #                         "date": str,
    #                         "url": str,
    #                         "content": dict
    #                     }
    #                 ]
    #     """
    #     events = []
    #     for i in range(1, self.max_page + 1):
    #         page_url = f"{self.base_url}/page/{i}"
    #         events.extend(self.get_events_from_a_page(page_url))
    #         print(f"Đã lấy toàn bộ các sự kiện từ trang {i}")
    #     return events
    def save(self, data, file_name):
        """
        lưu dữ liệu vào file json
        """
        data_dir = os.path.join( 'data', 'raw')
        with open(os.path.join(data_dir, file_name), 'w', encoding='utf-8') as f:
            s = json.dumps(data, ensure_ascii=False, indent=4)
            f.write(s)



class DaoTaoCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
    def get_content_from_industry(self, industry_url):
        """
        return: dict:
                    {
                        "program name": str,
                        "content": str,
                        "program structure": dict:{
                                                            "chuyen nganh i": dict{  
                                                                                "ky j": list[dict{"subject": str, "tin chi": str }],
                                                                                }
                                                    }
                        "metadata": dict:{
                                           "id": str,
                                           "time": str,
                                           "admission period": str,
                                           "location": str,
                                    }
                    }
        """
        response = requests.get(industry_url)
        soup = BeautifulSoup(response.text, features="html.parser")
        #get program name
        program_name = soup.find("h1", class_="breadcrumb-title").text.strip()
        # get matadata
        matadata_soup = soup.find("ul" , class_="column_4 mtop")
        metadata_items = matadata_soup.find_all("li", class_="item")
        metadata = dict()
        for i, item in enumerate(metadata_items):
            if i == 0:
                metadata["id"] = item.find("strong").text.strip()
            elif i == 1:
                metadata[ "time"] = item.find("strong").text.strip()
            elif i == 2:
                metadata['admission period'] = item.find("strong").text.strip()
            elif i == 3:
                metadata[ 'location'] = item.find("strong").text.strip()

        # get content
        content_soup = soup.find("div", class_="ova_dir_content")
        sections_soup = content_soup.find_all("section")
        content = ""
        for i, section in enumerate(sections_soup[: -2]):
            if i == 2 : continue
            else:
                content += section.text.strip() + "\n"
        # get chuyen nganh
        chuyen_nganh_soup = sections_soup[2].find("ul", class_= "nav-tab").find_all("li")
        cac_chuyen_nganh = [ li.text.strip() for li in chuyen_nganh_soup]
        print(f"{program_name} co {len(cac_chuyen_nganh)} chuyen nganh")
        # get program structure
        program_structure = dict()
        ky_hoc_soup = sections_soup[2].find("div").find_all("div", class_= "current-tab")
        so_luong_ky = len(ky_hoc_soup) // len(cac_chuyen_nganh) # số lượng kỳ học của mỗi chuyên ngành
        for i, chuyen_nganh in enumerate(cac_chuyen_nganh): # duyệt qua từng chuyên ngành
            cac_ky_hoc = dict()
            for j , ky in enumerate(ky_hoc_soup[ i * so_luong_ky: i * so_luong_ky + so_luong_ky]): # duyệt qua từng kỳ học của chuyên ngành
                ky_hoc = []
                for mon in ky.find_all("div", class_ = "card-mon-hoc"): # duyệt qua từng môn học của kỳ học
                    subject = mon.find("div", class_= "title").text.strip()
                    tin_chi = mon.find("div", class_= "tag").text.strip()
                    ky_hoc.append(dict(subject=subject, tin_chi=tin_chi))
                cac_ky_hoc[f"ky {j+1}"] = ky_hoc 
                ky_hoc = []
            program_structure[chuyen_nganh] = cac_ky_hoc
        return dict( program_name= program_name , content=content, program_structure=program_structure, metadata=metadata)

    def get_industries_from_a_page(self, page_url):
        """
        return: list[dict]:
        """
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, features="html.parser")
        ul = soup.find("div", class_= "elementor-element elementor-element-0ea282a elementor-grid-3 elementor-grid-tablet-2 elementor-grid-mobile-1 elementor-widget elementor-widget-loop-grid").find("div", class_="elementor-widget-container").find("div", class_= "elementor-loop-container elementor-grid")
        li = ul.find_all("div", recursive=False)
        industries = []
        for industry_soup in li:
            industry_soup = industry_soup.find("div").find("div").find("div")
            industry_url = industry_soup.find("div", class_= "elementor-element elementor-element-5781d80 text-hover-underline elementor-widget elementor-widget-theme-post-title elementor-page-title elementor-widget-heading").find("h2").find("a")['href']
            industries.append(self.get_content_from_industry(industry_url))
        return industries
    
    def save(self, data, file_name):
        """
        lưu dữ liệu vào file json
        """
        data_dir = os.path.join( 'data', 'raw')
        with open(os.path.join(data_dir, file_name), 'w', encoding='utf-8') as f:
            s = json.dumps(data, ensure_ascii=False, indent=4)
            f.write(s)
# các url cần thiết
THONG_BAO_URL = 'https://ptit.edu.vn/tin-tuc-su-kien/thong-bao'
MAX_PAGE_TB = 4
TIN_TUC_URL = "https://ptit.edu.vn/tin-tuc-su-kien/tin-tuc/tin-tuc-chung"
MAX_PAGE_TT = 10
SU_KIEN_URL = 'https://ptit.edu.vn/tin-tuc-su-kien/su-kien'
MAX_PAGE_SK = 6
DAO_TAO_URL = "https://daotao.ptit.edu.vn/ctdt/dai-hoc/"
# notice_crawler = PTITNoticeCrawler(TIN_TUC_URL, MAX_PAGE_TT)
# notices = notice_crawler.crawl_all()
# notice_crawler.save(notices, "news.json")
# latest_notice = notice_crawler.get_latest_notice()
# print(latest_notice)

# event_crawler = PTITEventCrawler(SU_KIEN_URL, MAX_PAGE_SK)
# event_page = event_crawler.get_events_from_a_page("https://ptit.edu.vn/tin-tuc-su-kien/su-kien")
# event_crawler.save(event_page, "events.json")

# dao_tao_crawler = DaoTaoCrawler(DAO_TAO_URL)
# industries = dao_tao_crawler.get_industries_from_a_page(DAO_TAO_URL)
# dao_tao_crawler.save(industries, "industries.json")
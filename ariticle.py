import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve
# os: Thư viện này được dùng để thao tác với hệ thống tệp (file system) như tạo thư mục, lưu file, v.v.
# requests: Thư viện giúp gửi yêu cầu HTTP để lấy nội dung của trang web từ URL.
# BeautifulSoup: Một công cụ phân tích cú pháp HTML/XML, giúp dễ dàng trích xuất dữ liệu từ trang web.
# urljoin: Dùng để nối các phần của URL (khi URL không hoàn chỉnh).
# urlretrieve: Dùng để tải tệp (ở đây là ảnh) từ URL và lưu vào hệ thống file.

url = 'https://vnexpress.net/chu-de/nuoi-day-con-1147'
# đường dẫn đến trang web

response = requests.get(url)
# response.content: Lấy nội dung HTML của trang từ phản hồi HTTP.
# BeautifulSoup(response.content, 'html.parser'): Phân tích cú pháp nội dung HTML này, chuyển đổi nó thành một cây DOM (Document Object Model), giúp dễ dàng truy cập các phần tử HTML.

soup = BeautifulSoup(response.content, 'html.parser')
# response.content: Lấy nội dung HTML của trang từ phản hồi HTTP.
# BeautifulSoup(response.content, 'html.parser'): Phân tích cú pháp nội dung HTML này, chuyển đổi nó thành một cây DOM (Document Object Model), giúp dễ dàng truy cập các phần tử HTML.
  
articles = soup.find_all('article', class_='item-news item-news-common thumb-left')
# soup.find_all(): Tìm tất cả các phần tử HTML <article> có class "item-news item-news-common thumb-left". Mỗi phần tử này đại diện cho một bài báo.
# Kết quả là một danh sách các bài viết được hiển thị trên trang.
    
for idx, article in enumerate(articles, 1):
       
        folder_name = f'article_{idx}'
        os.makedirs(folder_name, exist_ok=True)
# for idx, article in enumerate(articles, 1): Lặp qua từng bài viết trong danh sách articles. Biến idx là số thứ tự của bài viết, bắt đầu từ 1.
# folder_name = f'article_{idx}': Đặt tên thư mục cho từng bài viết, ví dụ article_1, article_2,...
# os.makedirs(folder_name, exist_ok=True): Tạo thư mục cho từng bài viết. Tham số exist_ok=True đảm bảo rằng nếu thư mục đã tồn tại, chương trình không gây lỗi.
        title = article.find('h3', class_='title-news').get_text(strip=True)
        print(f'Tiêu đề: {title}')
        with open(os.path.join(folder_name, 'title.txt'), 'w', encoding='utf-8') as f:
            f.write(title)
# article.find('h3', class_='title-news'): Tìm phần tử HTML chứa tiêu đề bài báo (thẻ <h3> với class "title-news").
# get_text(strip=True): Trích xuất văn bản từ phần tử HTML và loại bỏ các khoảng trắng không cần thiết.
# open(os.path.join(folder_name, 'title.txt'), 'w', encoding='utf-8'): Mở file title.txt trong thư mục bài viết để ghi tiêu đề vào file.
# f.write(title): Ghi tiêu đề vào file.
       
        description = article.find('p', class_='description').get_text(strip=True)
        print(f'Mô tả: {description}')
        with open(os.path.join(folder_name, 'description.txt'), 'w', encoding='utf-8') as f:
            f.write(description)
# article.find('p', class_='description'): Tìm đoạn mô tả bài viết (thẻ <p> với class "description").
# Phần còn lại tương tự như việc lưu tiêu đề.
       
        link = article.find('a')['href']
        full_link = urljoin(url, link)
        article_response = requests.get(full_link)
# article.find('a')['href']: Tìm liên kết (thẻ <a>) của bài viết, lấy giá trị thuộc tính href (liên kết của bài viết).
# urljoin(url, link): Sử dụng urljoin để nối liên kết đầy đủ (khi href không phải là URL hoàn chỉnh).
# requests.get(full_link): Gửi yêu cầu GET đến URL chi tiết của bài viết để lấy nội dung

        if article_response.status_code == 200:
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            content = article_soup.find('article', class_='fck_detail').get_text(strip=True)
            with open(os.path.join(folder_name, 'content.txt'), 'w', encoding='utf-8') as f:
                f.write(content)
# article_response.status_code == 200: Kiểm tra xem yêu cầu GET có thành công hay không (mã trạng thái 200 nghĩa là thành công).
# BeautifulSoup(article_response.content, 'html.parser'): Phân tích cú pháp HTML của nội dung bài viết chi tiết.
# article_soup.find('article', class_='fck_detail'): Tìm nội dung chính của bài viết trong thẻ <article> có class "fck_detail".
# get_text(strip=True): Trích xuất văn bản từ nội dung bài viết.
# **Lưu nội dung vào file content.txt.

           
            images = article_soup.find_all('img')
            for img_idx, img in enumerate(images, 1):
                img_url = img.get('src')
                if img_url:
                    img_filename = os.path.join(folder_name, f'image_{img_idx}.jpg')
                    urlretrieve(img_url, img_filename)
                    print(f'Tải ảnh: {img_filename}')
# article_soup.find_all('img'): Tìm tất cả các thẻ <img> trong bài viết.
# img.get('src'): Lấy URL của từng ảnh từ thuộc tính src.
# urlretrieve(img_url, img_filename): Tải ảnh từ URL và lưu vào file image_{img_idx}.jpg.

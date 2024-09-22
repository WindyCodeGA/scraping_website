import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve


url = 'https://vnexpress.net/chu-de/nuoi-day-con-1147'


response = requests.get(url)


soup = BeautifulSoup(response.content, 'html.parser')
    
  
articles = soup.find_all('article', class_='item-news item-news-common thumb-left')

    
for idx, article in enumerate(articles, 1):
       
        folder_name = f'article_{idx}'
        os.makedirs(folder_name, exist_ok=True)
        
        title = article.find('h3', class_='title-news').get_text(strip=True)
        print(f'Tiêu đề: {title}')
        
     
        with open(os.path.join(folder_name, 'title.txt'), 'w', encoding='utf-8') as f:
            f.write(title)
        
       
        description = article.find('p', class_='description').get_text(strip=True)
        print(f'Mô tả: {description}')
        
        
        with open(os.path.join(folder_name, 'description.txt'), 'w', encoding='utf-8') as f:
            f.write(description)
        
       
        link = article.find('a')['href']
        full_link = urljoin(url, link)

       
        article_response = requests.get(full_link)
        if article_response.status_code == 200:
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            
            
            content = article_soup.find('article', class_='fck_detail').get_text(strip=True)
            with open(os.path.join(folder_name, 'content.txt'), 'w', encoding='utf-8') as f:
                f.write(content)
            
           
            images = article_soup.find_all('img')
            for img_idx, img in enumerate(images, 1):
                img_url = img.get('src')
                if img_url:
                   
                    img_filename = os.path.join(folder_name, f'image_{img_idx}.jpg')
                    urlretrieve(img_url, img_filename)
                    print(f'Tải ảnh: {img_filename}')


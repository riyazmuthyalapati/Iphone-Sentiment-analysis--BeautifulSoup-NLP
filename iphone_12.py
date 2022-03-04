
import requests
from bs4 import BeautifulSoup
import pandas as pd

#url = 'https://www.amazon.in/Apple-iPhone-13-128GB-Starlight/product-reviews/B09G9D8KRQ/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1'
reviewlist = []

def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
            'product' : soup.title.text.replace('Amazon.in:Customer reviews:','').strip(),
            'title' : item.find('a',{'data-hook':'review-title'}).text.strip(),
            'rating' : float(item.find('i',{'data-hook':'review-star-rating'}).text.replace('out of 5 stars','').strip()),
            'body' : item.find('span',{'data-hook':'review-body'}).text.strip()
            }
            reviewlist.append(review)
    except:
        pass

for i in range(1,9999):
    soup = get_soup(f'https://www.amazon.in/New-Apple-iPhone-12-128GB/product-reviews/B08L5TNJHG/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={i}')
    print(f'Getting page: {i}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

    df = pd.DataFrame(reviewlist)
    df.to_csv('Amazon_reviews_iphone.csv', index=False)
    print('Finished')
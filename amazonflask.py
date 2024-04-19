from flask import Flask
import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd

app = Flask(__name__)

@app.route("/ASIN/<string:asin>/<int:num>")


def amazon_reviews(num,asin):
    pro = {
    "http": "http://6662ca24a4ad4ccc846e11c60c295606:@api.zyte.com:8011/",
    "https": "http://6662ca24a4ad4ccc846e11c60c295606:@api.zyte.com:8011/",
    }

    reviews_data = []
    

    URL = "https://www.amazon.com/dp/"+str(asin)
    #print(URL)

    r = requests.get(URL, proxies=pro, verify=False)
    soup = bs(r.content, 'html.parser')

    try:
        product_link = soup.find('a', {'data-hook': 'see-all-reviews-link-foot'})['href']
        data_link = "https://www.amazon.com" + product_link
        #print(data_link)
    except:
        pass

    new_url = f"{data_link}&pageNumber={num}"
    print(new_url)
    try:
        resp = requests.get(new_url, proxies=pro, verify=False)
        s = bs(resp.content, 'html.parser')
        new = s.find(id='cm_cr-review_list')
        dataa = new.findAll(class_='a-section review aok-relative')
    except:
        pass

    for data in dataa:
        review = {}

        name = data.find(class_='a-profile-name').text.strip()
        if any(name == r['name'] for r in reviews_data):
            continue

        review['name'] = name
            #print(name)

        star = data.findAll('div')[1]
        review['rating'] = star.find('i').text.split(' ')[0]

        review['review_date'] = data.find('span', attrs={'data-hook': 'review-date'}).text.split(' on ')[1].strip()

        review['content'] = data.find('span', attrs={'data-hook': 'review-body'}).text.strip()

        reviews_data.append(review)

    return reviews_data
    

if __name__ == "__main__":
    app.run(debug=True)
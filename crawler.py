import requests
from bs4 import BeautifulSoup


def getSingleVideoLink(singleVideoLink: str):
    singlePage = requests.get(singleVideoLink)
    soup = BeautifulSoup(singlePage.text, "html.parser")
    downloadLinks = soup.find('div', class_="entry-content").find_all('a', href=True)
    for downloadLink in downloadLinks:
        print(downloadLink['href'])  # 輸出排版後的HTML內容


# main
response = requests.get(
    "https://javfree.me/category/mosaic")
soup = BeautifulSoup(response.text, "html.parser")
titles = soup.find_all('a', href=True, class_="thumbnail-link", limit=3)
for res in titles:
    # print(res['href'])
    print('videoId')
    # 第二个参数为 1，返回两个参数列表
    videoUrlArray = res['href'].split("/")
    print(videoUrlArray[-1])
    getSingleVideoLink(res['href'])
    # print(res.prettify())  #輸出排版後的HTML內容

# for a in soup.find_all('a', href=True):
#     print (a['href'])

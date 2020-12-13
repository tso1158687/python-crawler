import requests

from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(
    "./python-crawler-38a6b-firebase-adminsdk-zs6u9-a33047c4c1.json")
firebase_admin.initialize_app(cred)
nowTime=firestore.SERVER_TIMESTAMP
db = firestore.client()
# def test():
#     print('test')
#     db.collection(u'video').document('migd-619').update({
#     'link': firestore.ArrayUnion(['fengyuan'])
#     })
    

# test()
def getSingleVideoLink(singleVideoLink: str, videoId: str):
    singlePage = requests.get(singleVideoLink)
    soup = BeautifulSoup(singlePage.text, "html.parser")
    downloadLinks = soup.find(
        'div', class_="entry-content").find_all('a', href=True)
    downloadLinkList = []
    for downloadLink in downloadLinks:
        downloadLinkList.append(downloadLink['href'])
        print(downloadLink['href'])  # 輸出排版後的HTML內容
    videoData = {
        'id': videoId,
        'link': downloadLinkList,
        'updateTime': nowTime
    }
    # print(videoData)
    postDataToFirebase(videoData)


def postDataToFirebase(videoData):
    # 初始化firestore

    db.collection(u'video').document(videoData['id']).set(videoData)

# main
response = requests.get(
    "https://javfree.me/category/mosaic")
soup = BeautifulSoup(response.text, "html.parser")
titles = soup.find_all('a', href=True, class_="thumbnail-link")
for res in titles:
    print('videoId')

    videoUrlArray = res['href'].split("/")
    print(videoUrlArray[-1])
    getSingleVideoLink(res['href'],videoUrlArray[-1])

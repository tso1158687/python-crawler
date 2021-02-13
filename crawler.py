import requests
import sys
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(
    "./python-crawler-38a6b-firebase-adminsdk-zs6u9-a33047c4c1.json")
firebase_admin.initialize_app(cred)
nowTime=firestore.SERVER_TIMESTAMP
db = firestore.client()

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
    # TODO:邏輯 如果不存在:新增；如果存在:更新
    # db.collection(u'video').document(videoData['id']).set(videoData)
    isVideoExist=db.collection(u'video').document(videoData['id']).get().exists
    if isVideoExist:
        print('更新')
        db.collection(u'video').document(videoData['id']).update({
            'link': firestore.ArrayUnion(videoData['link'])
        })
    else:
        print('新增')
        db.collection(u'video').document(videoData['id']).set(videoData)


# main
for i in range(1,10):
    print('現在是第',i,'頁')
    url=''
    print(sys.argv)
    if i == 1:
        url= sys.argv[1]
    else:
        url= sys.argv[1]+'/page/'+str(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('a', href=True, class_="thumbnail-link")
    for res in titles:
        print('videoId')

        videoUrlArray = res['href'].split("/")
        print(videoUrlArray[-1])
        getSingleVideoLink(res['href'],videoUrlArray[-1])

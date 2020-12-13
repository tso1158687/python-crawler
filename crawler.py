import requests

from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(
    "./python-crawler-38a6b-firebase-adminsdk-zs6u9-a33047c4c1.json")
firebase_admin.initialize_app(cred)

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
        'link': downloadLinkList
    }
    # print(videoData)
    postDataToFirebase(videoData)


def postDataToFirebase(videoData):
    # 初始化firestore
    


    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection(u'video').document(videoData['id']).set(videoData)

    # video_ref=db.collection("video").document("student")
    # print(doc_ref.get().to_dict())


# main()
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

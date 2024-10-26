import requests
from PIL import Image

# pip install pillow
# 2.8.1 리퀘스트로 인터넷에서 이미지 파일 가져오기
# url = 'http://bit.ly/2JnsHnT'
url = 'http://bit.ly/3ZZyeXQ'
r = requests.get(url, stream=True).raw

img = Image.open(r)
print("img : ", img.get_format_mimetype)
img.show()
img.save('src.png')


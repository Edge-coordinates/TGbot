import json

img_apis = {
    "0": {'url': "https://pic.re/images",
          "des": "A free public Anime picture provider api."},
    "1": {"url": "https://tuapi.eees.cc/api.php?",
          "parameter": ["category={dongman,fengjing}", "category=fengjing", "category=dongman"],
          "des": "动漫，风景混合API,参数有三种，分别是动漫风景混合，纯风景，纯动漫"},
    "4": {"url": "https://img.paulzzh.tech/touhou/random",
          "des": "东方图片API"},
    "5": {"des": "文档地址：https://www.eee.dog/tech/rand-pic-api.html"}
}

a = img_apis.get('0').get('url')

print(a)
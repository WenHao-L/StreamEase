import requests
import random
from hashlib import md5
from config import BAIDU_APP_ID, BAIDU_APP_KEY

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def baidu_trans(query, appid=BAIDU_APP_ID, appkey=BAIDU_APP_KEY, from_lang='en', to_lang='zh'):
    try:
        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path

        salt = random.randint(32768, 65536)
        sign = make_md5(appid + query + str(salt) + appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()

        if "trans_result" in result:
            translated_texts = [item['dst'] for item in result['trans_result']]
            concatenated_text = '\n'.join(translated_texts)
            return concatenated_text
        else:
            return
    except:
        return

if __name__ == "__main__":
    query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'
    result = baidu_trans(query, BAIDU_APP_ID, BAIDU_APP_KEY
)
    print(result)
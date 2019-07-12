import requests 
from flask import Flask, escape, request
from decouple import config
import pprint

API_TOKEN = config('API_TOKEN') #상수는 대문자
CHAT_ID = config('CHAT_ID')
base_url = 'https://api.telegram.org'
app = Flask(__name__)

NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')

@app.route('/')
def hello():
    return 'Hello World'


@app.route('/greeting/<name>')
def greeting(name):
    return f'Hello,{name}'

@app.route(f'/{API_TOKEN}', methods=['POST'])
def telegram():
    from_telegram = request.get_json()
    # pprint.pprint(from_telegram)
    if from_telegram.get('message') is not None:    #  텔레그램 메세지가 있을수도있고 없을수도 있음
        #  우리가 원하는 로직       #  딕셔너리에 접근할때 []사용 or .get 접근 --> 안에 내용이 없을 때 [] 사용하면 오류가 나지만 .get은 상관없음
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text')

        print('chat_id : ',CHAT_ID)
        print('text : ',text)
        
        #  Send Message API URL
        
        if text[0:4] == '/영한 ':            #첫 네글자가 '/번역 ' 일 때
            # text = '번역을 시작'
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,           #  trailing comma
            }
            data = {
                'source': 'en',
                'target': 'ko',
                'text': text[4:]        #/번역  이후의 문자열만 대상으로 번역
            }
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            pprint.pprint(papago_res.json())
            text = papago_res.json().get('message').get('result').get('translatedText')
        elif text[0:4] == '/한영 ':            #첫 네글자가 '/번역 ' 일 때
            # text = '번역을 시작'
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,           #  trailing comma
            }
            data = {
                'source': 'ko',
                'target': 'en',
                'text': text[4:]        #/번역  이후의 문자열만 대상으로 번역
            }
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            pprint.pprint(papago_res.json())
            text = papago_res.json().get('message').get('result').get('translatedText')
        else:
            text = f'나도 {text}'
        
        api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'
        response = requests.get(api_url)

        
    
        

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
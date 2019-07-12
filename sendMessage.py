import requests     #  요청을 하기 위한 모듈
import pprint       #  보기 편하게 출력해주는 모듈
from decouple import config     #  decouple 에서부터 config 호출


base_url = 'https://api.telegram.org'
token = config('API_TOKEN')
chat_id = config('CHAT_ID')
text = '디커풀 테스트'

api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}'

response = requests.get(api_url)      #  요청 보내기
pprint.pprint(response.json())


from flask import Flask, request, abort, Response, url_for

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
import random
import requests
import json
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
#openai.api_key = os.getenv('OPENAI_API_KEY')
answer = ""

def fortune_func():
    fortune = ["大吉", "中吉", "小吉", "末吉", "小凶", "大凶"]
    weights = [0.05, 0.15, 0.3, 0.3, 0.15, 0.05]
    answer = random.choices(fortune, weights=weights, k=1)[0]
    if(answer == "大吉"):
        lottery = random.sample(range(1,50),6)
        lottery_str = ""
        for number in lottery:
            lottery_str += str(number) + " "
        answer = answer + "\n樂透號碼:" + lottery_str
    elif(answer == "中吉"):
        ticket = random.sample(range(1,101),5)
        ticket_str = ""
        for number in ticket:
            ticket_str += str(number) + " "
        answer = answer + "\n刮刮樂號碼:" + ticket_str
    return answer


def game_1(text):
    game = ["剪刀", "石頭", "布"]
    if(len(text) >= 3):
        answer = "齁～～作弊鬼"
    else:
        answer = random.choice(game)
        if(text == "剪刀"):
            if(answer == "剪刀"):
                answer +="\n啊呀平手再來一次"
            elif(answer == "石頭"):
                answer += "\n嘿嘿我贏了"
            else:
                answer+="\nQQ你贏了"
        elif(text == "石頭"):
            if(answer == "石頭"):
                answer +="\n啊呀平手再來一次"
            elif(answer == "布"):
                answer += "\n嘿嘿我贏了"
            else:
                answer+="\nQQ你贏了"
        else:
            if(answer == "布"):
                answer +="\n啊呀平手再來一次"
            elif(answer == "剪刀"):
                answer += "\n嘿嘿我贏了"
            else:
                answer+="\nQQ你贏了"
    return answer
    
# @app.route('/weather', methods=['GET'])
# def get_weather():
#     # 替换成中央气象局API的实际URL和你的API key
#     api_url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001'
#     api_key = 'CWA-DC388112-F471-4FC4-B13B-A73231BB439A'

#     # 发送请求到中央气象局API
#     response = requests.get(api_url, params={'Authorization': api_key})

#     # 检查请求是否成功
#     if response.status_code == 200:
#         weather_data = response.json()
#         return Response(json.dumps(weather_data), mimetype='application/json')
#     else:
#         error_response = {'error': 'Failed to fetch weather data'}
#         return Response(json.dumps(error_response), status=response.status_code, mimetype='application/json')

def GPT_response(text):
    # 接收回應
    #response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=text, temperature=0.5, max_tokens=500)
    #print(response)
    # 重組回應
    #answer = response['choices'][0]['text'].replace('。','')
    food = ["韓式", "日式", "中式", "美式"]
    place = ["宜蘭", "台中", "高雄", "基隆","桃園", "台北", "台南"]
    aplogize = ["不要生氣嘛", "對不起", "不要凶小熊貓嘛"]
    color = ["紅", "橙", "黃", "綠", "藍", "紫", "黑", "白", "粉", "灰"]

    if("吃" in text):
        answer = random.choice(food)
    elif("哪" in text or "玩" in text):
        answer = random.choice(place)
    elif("剪刀" in text or "石頭" in text or "布" in text):
        answer = game_1(text)
    elif("幸運色" in text):
        answer = random.choice(color)
    elif("運" in text or "算" in text or "命" in text):
        answer = fortune_func()
    elif("笨" in text or "討厭" in text or "生氣" in text or "不愛" in text):
        answer = random.choice(aplogize)
    elif("真棒" in text or "厲害" in text):
        answer = "這樣誇熊貓，本熊貓會膨漲的嘿嘿"
    # elif("天氣" in text):
    #     weather_url = url_for('get_weather', _external=True)

        # 发送请求到 /weather 路由
        # response = requests.get(weather_url)

        # 返回响应数据
        # return Response(response.content, status=response.status_code, mimetype='application/json')
    elif("禮物" in text):
        return "禮物"
        # return 'https://drive.google.com/file/d/1z7XSGxYX0rymvnMxwAxNks5OeeHdVmqh/view?usp=sharing'
        # return ImageSendMessage(original_content_url='https://drive.google.com/file/d/1z7XSGxYX0rymvnMxwAxNks5OeeHdVmqh/view?usp=sharing', preview_image_url='https://drive.google.com/file/d/1z7XSGxYX0rymvnMxwAxNks5OeeHdVmqh/view?usp=sharing')
    else:
        answer = "QQ本熊貓聽不懂你在說什麼?"
    return answer

@app.route('/', methods=['HEAD'])
def head_request():
    return '', 200

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    try:
        GPT_answer = GPT_response(msg)
        if('禮物' in GPT_answer):
            image_message = ImageSendMessage(original_content_url='https://drive.google.com/file/d/12vQW4NkL4NBWKpAkarS35F0mUOAeU6r0/view?usp=sharing',preview_image_url='https://drive.google.com/file/d/12vQW4NkL4NBWKpAkarS35F0mUOAeU6r0/view?usp=sharing')
            print(image_message)
            line_bot_api.push_message(event.source.user_id, image_message)
        else:
            print(GPT_answer)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
    except:
        print(traceback.format_exc())
        line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息'))
        

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
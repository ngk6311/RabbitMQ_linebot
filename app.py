import pika
import requests

from config import MQ_DEFAULTS  # 匯入 RabbitMQ 的連線設定
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# RabbitMQ 訊息接收回呼函式
def callback(ch, method, properties, body):
    message = body.decode('utf-8')  # 將 RabbitMQ 訊息解碼為字串
    try:
        # 建立 Line Bot 訊息物件
        text_message = TextSendMessage(text=message)
        # 發送訊息到 Line Bot
        line_bot_api.push_message('USER_ID', messages=[text_message])  # 替換成接收訊息的 Line 使用者 ID
    except LineBotApiError as e:
        print(f"Line Bot 發送訊息失敗: {e}")

# 建立 RabbitMQ 連線
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=MQ_DEFAULTS['HOST'],
    port=int(MQ_DEFAULTS['PORT']),
    virtual_host=MQ_DEFAULTS['VHOST'],
    credentials=pika.PlainCredentials(
        MQ_DEFAULTS['USER'], MQ_DEFAULTS['PASSWORD'])
))
channel = connection.channel()

# 建立 exchange，這裡使用 fanout 交換機
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# 建立隨機生成的 queue
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# 將隊列綁定到交換機
channel.queue_bind(exchange='logs', queue=queue_name)

# 設定回呼函式來處理訊息
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# 開始接收 RabbitMQ 訊息
print('Waiting for RabbitMQ messages. To exit press CTRL+C')
channel.start_consuming()

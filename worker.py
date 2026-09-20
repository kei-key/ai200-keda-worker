import os
import time
from azure.servicebus import ServiceBusClient

CONNECTION_STR = os.environ["SERVICEBUS_CONNECTION_STRING"]
QUEUE_NAME = "workqueue"

print("ワーカーを起動しました。キューの監視を開始します。")

with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
    with client.get_queue_receiver(queue_name=QUEUE_NAME, max_wait_time=10) as receiver:
        while True:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=10)
            if not messages:
                print("メッセージなし。待機中...")
                continue
            for msg in messages:
                print(f"メッセージ受信: {str(msg)}")
                # 処理に時間がかかる想定で、あえて15秒待機(スケーリングの様子を観察しやすくするため)
                time.sleep(15)
                receiver.complete_message(msg)
                print("メッセージ処理完了")

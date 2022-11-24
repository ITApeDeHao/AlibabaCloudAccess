# 来源于阿里，将官方文档整合为类收取信息
import time
import sys
import hashlib
import hmac
import base64
import stomp
import ssl
import schedule
import threading
import struct
import json
import os

class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        # 收取信息
        dict = json.loads(frame.body)
        keys = ["picture_message","text_message","audio_text"]
        # 判断收到的是哪一种信息
        for key in keys:
            try:
                audio_dict = dict.get("items").get(key).get("value")
            except:
                pass
        # 处理图片信息
        if audio_dict[0:7] == "picture":
            print('ok')
            base_content = audio_dict[9:-1]
            base_content = str.encode(base_content)
            base_content = base64.urlsafe_b64decode(base_content)
            with open('./receive_message/1.jpg','wb') as f:
                f.write(base_content)
        # # 处理视频信息
        # elif audio_dict[0:5] == "video":
        #     print('ok')
        #     base_content = audio_dict[7:-1]
        #     base_content = str.encode(base_content)
        #     base_content = base64.urlsafe_b64decode(base_content)
        #     with open('./receive_message/1.mp4','wb') as f:
        #         f.write(base_content)
        # 处理音频信息
        elif audio_dict[0:5] == "audio":
            print('ok')
            base_content = audio_dict[7:-1]
            base_content = str.encode(base_content)
            base_content = base64.urlsafe_b64decode(base_content)
            with open('./receive_message/1.mp3','wb') as f:
                f.write(base_content)
        # 处理文本信息。
        else :
            print('ok')
            base_content = audio_dict[6:-1]
            base_content = str.encode(base_content)
            base_content = base64.urlsafe_b64decode(base_content)
            with open('./receive_message/1.txt','wb') as f:
                f.write(base_content)


    def on_heartbeat_timeout(self):
        print('on_heartbeat_timeout')

    def on_connected(self, headers):
        print("successfully connected")
        self.conn.subscribe(destination='/topic/#', id=1, ack='auto')
        print("successfully subscribe")

    def on_disconnected(self):
        print('disconnected')
        Iot_data_from_yun.connect_and_subscribe(Iot_data_from_yun(), self.conn)


class Iot_data_from_yun(object):
    def __init__(self):
        # 初始化存储信息文件夹
        train_data_filename='./receive_message'
        if os.path.exists(train_data_filename):
            try:
                for file in os.listdir(train_data_filename)[0:]:
                    #删除该文件夹里面的东西
                    print(file)
                    #先通过os.listdir获取该文件夹内的文件名列表，然后逐一删除
                    file_path=train_data_filename+'/'+file
                    os.unlink(file_path) #删除该文件
            except:
                pass
        else:
            # 如果不存在，则创建该文件夹
            os.mkdir(train_data_filename)
        #  接入域名，请参见AMQPpyt客户端接入说明文档。这里直接填入域名，不需要带amqps://前缀
        conn = stomp.Connection([('iot-06z00an39q0cr69.amqp.iothub.aliyuncs.com', 61614)])
        conn.set_ssl(for_hosts=[('iot-06z00an39q0cr69.amqp.iothub.aliyuncs.com', 61614)], ssl_version=ssl.PROTOCOL_TLS)

        try:
            self.connect_and_subscribe(conn)
        except Exception as e:
            print('connecting failed')
            raise e

        # 异步线程运行定时任务，检查连接状态
        thread = threading.Thread(target=self.connection_check_timer)
        thread.start()

    def connect_and_subscribe(self, conn):
        accessKey = "accessKey"
        accessSecret = "accessSecret"
        # 消费组ID
        consumerGroupId = "consumerGroupId"
        # iotInstanceId：实例ID。
        iotInstanceId = "iotInstanceId"
        clientId = "clientId"
        # 签名方法：支持hmacmd5，hmacsha1和hmacsha256。
        signMethod = "signMethod"
        timestamp = self.current_time_millis()
        # userName组装方法，请参见AMQP客户端接入说明文档。
        # 若使用二进制传输，则userName需要添加encode=base64参数，服务端会将消息体base64编码后再推送。具体添加方法请参见下一章节“二进制消息体说明”。
        username = clientId + "|authMode=aksign" + ",signMethod=" + signMethod \
                   + ",timestamp=" + timestamp + ",authId=" + accessKey \
                   + ",iotInstanceId=" + iotInstanceId \
                   + ",consumerGroupId=" + consumerGroupId + "|"
        signContent = "authId=" + accessKey + "&timestamp=" + timestamp
        # 计算签名，password组装方法，请参见AMQP客户端接入说明文档。
        password = self.do_sign(accessSecret.encode("utf-8"), signContent.encode("utf-8"))

        conn.set_listener('', MyListener(conn))
        conn.connect(username, password, wait=True)
        # 清除历史连接检查任务，新建连接检查任务
        schedule.clear('conn-check')
        schedule.every(1).seconds.do(self.do_check, conn).tag('conn-check')

    def current_time_millis(self):
        return str(int(round(time.time() * 1000)))

    def do_sign(self, secret, sign_content):
        m = hmac.new(secret, sign_content, digestmod=hashlib.sha1)
        return base64.b64encode(m.digest()).decode("utf-8")

    # 检查连接，如果未连接则重新建连
    def do_check(self, conn):
        print('check connection, is_connected: %s', conn.is_connected())
        if (not conn.is_connected()):
            try:
                connect_and_subscribe(conn)
            except Exception as e:
                print('disconnected, ', e)

    # 定时任务方法，检查连接状态
    def connection_check_timer(self):
        while 1:
            schedule.run_pending()
            time.sleep(10)


if __name__ == "__main__":
    Iot_data_from_yun()

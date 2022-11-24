# 链接阿里云平台

from linkkit import linkkit
import base64
import json
import time
from tkinter import messagebox
import tkinter as tk

class Link_ali_iot(object):
	def __init__(self,link):
		self.lk = link
		self.lk.on_connect = self.on_connect
		self.lk.on_disconnect = self.on_disconnect
		self.lk.on_thing_enable = self.on_thing_enable
		self.lk.on_subscribe_topic = self.on_subscribe_topic
		self.lk.on_unsubscribe_topic = self.on_unsubscribe_topic
		self.lk.on_topic_message = self.on_topic_message
		self.lk.on_publish_topic = self.on_publish_topic
		self.lk.on_thing_prop_post = self.on_thing_prop_post
		self.lk.connect_async()
		self.lk.start_worker_loop()
		time.sleep(2)  # 延时
		tk.messagebox.showinfo(title='提示',message='链接成功')

	def on_connect(self, session_flag, rc, userdata):
		print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))

	def on_disconnect(self, rc, userdata):
		print("on_disconnect:rc:%d,userdata:" % rc)

	def on_subscribe_topic( mid, granted_qos, userdata):
		print("on_subscribe_topic mid:%d, granted_qos:%s" %
			  (mid, str(','.join('%s' % it for it in granted_qos))))

	def on_publish_topic(self, mid, userdata):
		print("on_publish_topic mid:%d" % mid)

	# 接收云端的数据
	def on_topic_message(self, topic, payload, qos, userdata):
		print("on_topic_message:" + topic + " payload:" + str(payload) + " qos:" + str(qos))
		
	def on_unsubscribe_topic(self, mid, userdata):
		print("on_unsubscribe_topic mid:%d" % mid)

	def on_thing_prop_post(self, request_id, code, data, message, userdata):
		print("on_thing_prop_post request id:%s, code:%d message:%s, data:%s,userdata:%s" %
			  (request_id, code, message, data, userdata))

	def on_thing_enable(self, userdata):
		print("on_thing_enable")
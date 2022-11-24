import tkinter as tk
from linkkit import linkkit
from tkinter import messagebox
from tkinter import filedialog
import re
import time
import base64
import json
import Link_ali_send as la
from PIL import Image
from PIL import ImageTk
import os
import iot_data_from_yun_send as idfy

class Gui(object):
	"""
	设计设备端窗口界面
	"""
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("PC端")
		self.window.geometry("800x600")
		self.window.resizable(width=False,height=False)
		# self.window = master
		self.frame = tk.Frame(self.window,width=800,height=600,bg='pink')
		self.frame.pack()
		tk.Button(self.frame, text='链接阿里云', width=20, height=1, command=self.link).place(relx=0,rely=0)
		tk.Button(self.frame, text='下载图片文件',width=20, height=1, command=self.get_pic).place(relx=0.25,rely=0.1)
		tk.Button(self.frame, text='打开音频文件',width=20, height=1, command=self.get_audio).place(relx=0.7,rely=0.7)
		# tk.Button(self.frame, text='打开视频文件',width=20, height=1, command=self.get_video).place(relx=0.25,rely=0.5)
		tk.Button(self.frame, text='下载文本文件',width=20, height=1, command=self.get_text).place(relx=0.7,rely=0.1)
		img = Image.open('0.jpg').resize((300,200))
		self.photo0 = ImageTk.PhotoImage(img)
		tk.Label(self.frame,image=self.photo0).place(relx=0.05,rely=0.65)
		tk.Button(self.frame, text='请选择图片文件',width=20, height=1, command=lambda :self.get_path(0)).place(relx=0.05,rely=0.1)
		tk.Button(self.frame, text='请选择音频文件',width=20, height=1, command=lambda :self.get_path(1)).place(relx=0.5,rely=0.7)
		# tk.Button(self.frame, text='请选择视频文件',width=20, height=1, command=lambda :self.get_path(2)).place(relx=0.05,rely=0.5)
		tk.Button(self.frame, text='请选择文本文件',width=20, height=1, command=lambda :self.get_path(3)).place(relx=0.5,rely=0.1)
		self.window.mainloop()


	def link(self):
		self.lk = linkkit.LinkKit(
			host_name="host_name",
			product_key="product_key",
			device_name="device_name",
			device_secret="device_secret")

		self.lk.thing_setup('./models.json')
		la.Link_ali_iot(self.lk)
		idfy.Iot_data_from_yun()

	def get_text(self):
		# 展示收取到的文本信息
		try:
			with open('./receive_message/1.txt','r') as f:
				content = f.read()
			tk.Label(self.frame,text=content,width=50,height=15).place(relx=0.47,rely=0.15)
		except:
			tk.messagebox.showerror(title='Error',message='未收到信息，请重试')

	def get_audio(self):
		# 展示收取到的音频信息
		try:
			os.startfile(r'./receive_message/1.mp3')
		except:
			tk.messagebox.showerror(title='Error',message='未收到信息，请重试')

	def get_video(self):
		# 展示收取到的视频信息
		try:
			os.startfile(r'./receive_message/1.mp4')
		except:
			tk.messagebox.showerror(title='Error',message='未收到信息，请重试')

	def get_pic(self):
		# 展示收取到的图片信息
		try:
			img = Image.open('./receive_message/1.jpg').resize((300,200))
			self.photo = ImageTk.PhotoImage(img)
			tk.Label(self.frame,image=self.photo).place(relx=0.05,rely=0.15)
		except:
			tk.messagebox.showerror(title='Error',message='未收到信息，请重试')  

	def get_path(self,sign):
		self.choose_text_gui = tk.Tk()
		if sign == 0:
			self.choose_photo_text(sign)
		elif sign == 1:
			self.choose_audio_text(sign)
		elif sign == 2:
			self.choose_video_text(sign)
		else:
			self.choose_txt_text(sign)
		self.choose_text_gui.destroy()

	def choose_audio_text(self,sign):
		# 选择音频文件
		self.choose_text_gui.withdraw()
		self.Filepath = filedialog.askopenfilename(filetypes=(("audio files", ".mp3 "),)) #获得选择好的文件
		if self.Filepath:
			local_file = self.Filepath
			with open(local_file, 'rb') as f:
				content = f.read()
			# base64编码
			base_content = base64.urlsafe_b64encode(content)

			prop_data = {
				"audio_text": "audio"+str(base_content),
			}
			counts = 2  # 模拟上报1次
			while counts > 1:
				rc, request_id = self.lk.thing_post_property({**prop_data})
				if rc == 0:
					print("thing_post_property success:%r,mid:%r,\npost_data:%s" % (rc, request_id, prop_data))
				else:
					print("thing_post_property failed:%d" % rc)
				time.sleep(5)
				counts -= 1
			tk.messagebox.showinfo(title='提示',message='上传成功')

	def choose_video_text(self,sign):
		# 选择视频文件
		self.choose_text_gui.withdraw()
		self.Filepath = filedialog.askopenfilename(filetypes=(("video files", ".avi .mkv .mov .mp4"),)) #获得选择好的文件
		if self.Filepath:
			local_file = self.Filepath
			with open(local_file, 'rb') as f:
				content = f.read()
			# base64编码
			base_content = base64.urlsafe_b64encode(content)
			prop_data = {
				"video_text": "video"+str(base_content),
			}
			counts = 2  # 模拟上报1次
			while counts > 1:
				rc, request_id = self.lk.thing_post_property({**prop_data})
				if rc == 0:
					print("thing_post_property success:%r,mid:%r,\npost_data:%s" % (rc, request_id, prop_data))
				else:
					print("thing_post_property failed:%d" % rc)
				time.sleep(5)
				counts -= 1
			tk.messagebox.showinfo(title='提示',message='上传成功')

	def choose_photo_text(self,sign):
		# 选择图片文件
		self.choose_text_gui.withdraw()
		self.Filepath = filedialog.askopenfilename(filetypes=(("jpg files", ".jpg .png .JPEG"),)) #获得选择好的文件
		if self.Filepath:
			local_file = self.Filepath
			with open(local_file, 'rb') as f:
				content = f.read()
			# base64编码
			base_content = base64.urlsafe_b64encode(content)
			# print(base_content)
			prop_data = {
				"picture_message": "picture"+str(base_content),
			}
			counts = 2
			while counts > 1:
				rc, request_id = self.lk.thing_post_property({**prop_data})
				if rc == 0:
					# print('\n')
					print("thing_post_property success:%r,mid:%r,\npost_data:%s" % (rc, request_id, prop_data))
				else:
					print("thing_post_property failed:%d" % rc)
				time.sleep(5)
				counts -= 1
			tk.messagebox.showinfo(title='提示',message='上传成功')

	def choose_txt_text(self,sign):
		# 选择文本文件
		self.choose_text_gui.withdraw()
		self.Filepath = filedialog.askopenfilename(filetypes=(("txt files", ".txt .word"),)) #获得选择好的文件
		if self.Filepath:
			local_file = self.Filepath
			with open(local_file, 'rb') as f:
				content = f.read()

			# base64编码
			base_content = base64.urlsafe_b64encode(content)

			prop_data = {
				"text_message": "text"+str(base_content),
			}
			counts = 2  # 模拟上报1次
			while counts > 1:
				rc, request_id = self.lk.thing_post_property({**prop_data})
				if rc == 0:
					print("thing_post_property success:%r,mid:%r,\npost_data:%s" % (rc, request_id, prop_data))
				else:
					print("thing_post_property failed:%d" % rc)
				time.sleep(5)
				counts -= 1
			tk.messagebox.showinfo(title='提示',message='上传成功')


if __name__ == "__main__":
	Gui()



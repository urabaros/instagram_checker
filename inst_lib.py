# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


options = webdriver.ChromeOptions()
options.add_argument("--user-agent=New User Agent")
#options.add_argument("--headless")
#options.add_argument("--window-size=1366x768")
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")


class GetData():
	'''
	Класс содержит в себе методы, позволяющие 
	получить вводные данные из файлов и определить их в переменные.
	'''
	def get_post(self):	
		'''
		Функция-генератор получает данные из файла posts.txt
		и возвращает значение построчно, при каждом вызове функции.
		'''							
		with open("posts.txt") as file_handler:
			for line in file_handler:
				line = line.rstrip('\n')
				yield line

	def get_login(self):
		'''
		Функция получает первую строку из файла login.txt
		и возвращает её как логин пользователя.
		'''								
		with open("login.txt") as file_handler:
			for line in file_handler:
				return line

	def get_password(self):	
		'''
		Функция получает вторую строку из файла login.txt
		и возвращает её как пароль пользователя.
		'''									
		with open("login.txt") as file_handler:
			for line in file_handler:
				line = line.rstrip('\n')
			return line

	def get_users(self):
		'''
		Функция получает никнемы пользователей из 
		файла users.txt и возвращает их в виде списка.
		'''
		users = set()									
		with open("users.txt") as file_handler:
			for line in file_handler:
				line = line.rstrip('\n')
				users.add(line)
		return users


class Login(GetData):
	'''
	Класс содержит в себе методы, для авторизации
	пользователя на сайте. 
	'''
	def __init__(self):
		GetData.__init__(self)
		self.login = GetData.get_login(self)
		self.password = GetData.get_password(self)

	def input_log_and_pas(self):
		'''
		Функция переда логин и пароль в соответствующие поля.
		'''
		time.sleep(0.5)
		driver.find_element_by_name('username').send_keys(self.login)
		driver.find_element_by_name('password').send_keys(self.password)

	def autorization(self):
		'''
		Функция авторизует пользователя на сайте.
		'''
		time.sleep(0.5)
		log_in_button = driver.find_element_by_xpath("""
			//button
			[@class='_0mzm- sqdOP  L3NKy       ']
			[@type='submit']
		""")
		log_in_button.click()
		time.sleep(3) # ждём авторизации на сайте
		print('Вход выполнен успешно')		


class Checking(GetData):
	'''
	Класс содержит в себе методы для получения данных 
	со страниц пользователей.
	'''
	def __init__(self):
		GetData.__init__(self)
		self.users = GetData.get_users(self)
		self.post = GetData.get_post(self)

	def show_page(self):
		'''
		Функция переходит на странцу пользователя
		и отображает все необходимые элементы.
		'''
		driver.get(self.post.__next__())
		while True:
			try:
				view_more_btn = driver.find_element_by_xpath("""
					//button
					[@class='Z4IfV _0mzm- sqdOP yWX7d        ']
					[@type='button']
				""")
				view_more_btn.click() 
				time.sleep(0.5)
			except NoSuchElementException:
				break	

	def get_comments(self):
		'''
		Функция собирает никнеймы пользователей, оставивших комментарий 
		и формирует из этих данных список.
		'''
		comments = set()
		users_list = driver.find_elements_by_tag_name('h3')
		for user in users_list:
			nickname = user.text
			comments.add(nickname)
		return comments

	def get_autor(self):
		'''
		Функция получает никнейм автора поста.
		'''
		autor = driver.find_element_by_tag_name('h2').text
		return autor


class DataProcessing(GetData):
	'''
	Класс содержит методы, позволяющие сформировать отчёт 
	на основе полученных данных.
	'''
	def __init__(self, data_dict):
		GetData.__init__(self)
		self.users = GetData.get_users(self)
		self.data_dict = data_dict

	def generate_report_dict(self):
		'''
		Функция формирует словарь с данными для отчёта.
		'''
		report_dict = dict()

		for key in self.data_dict.keys():
			good_users = list(self.users & self.data_dict[key])
			bad_users = list(self.users - self.data_dict[key])
			plus = []
			for i in range(len(good_users)):
				plus.append('+')
			minus = []
			for j in range(len(bad_users)):
				minus.append('-')
			p = dict(zip(good_users, plus))
			m = dict(zip(bad_users, minus))
			p.update(m) 
			report_dict[key] = p
		return report_dict

	def generate_report_file(self, report_dict):
		'''
		Функция формирует отчёт в виде файла для пользователя.
		'''
		with open("report.txt", "w", encoding='utf-8') as report:
			for key in report_dict.keys():
				report.write('{}\n{}\n{}\n'.format(48*'-', key, 48*'-'))
				_dict = report_dict[key]
				for k, v in _dict.items():
					report.write('{}: |{}|\n'.format(k, v))


if __name__ == "__main__":
	login = Login()
	login.input_log_and_pas()
	login.autorization()

	check = Checking()
	data_dict = dict()
	while True:
		try:
			check.show_page()
			comments = check.get_comments()
			autor = check.get_autor()
			data_dict[autor] = comments
		except StopIteration:
			break

	report = DataProcessing(data_dict)
	report_dict = report.generate_report_dict()
	report.generate_report_file(report_dict)

	
	










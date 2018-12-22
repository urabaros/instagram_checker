#access_token=3288067318.eff9bc4.2d7972596cac423d83f7d918fe2956ea
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
options.add_argument("--user-agent=New User Agent")
options.add_argument("--headless")
options.add_argument("--window-size=1366x768")
driver = webdriver.Chrome(chrome_options=options)

def get_posts():
	posts = []									# получаем url-адреса постов
	with open("posts.txt") as file_handler:
		for line in file_handler:
			line = line.rstrip('\n')
			posts.append(line)
	return posts

def get_log_in():
	log_in = []									# получаем логин и пароль из файла
	with open("login.txt") as file_handler:
		for line in file_handler:
			line = line.rstrip('\n')
			log_in.append(line)
	log, pas = log_in[0], log_in[1]
	return log, pas

def users():
	users = []									# получаем список пользователей 
	with open("users.txt") as file_handler:
		for line in file_handler:
			line = line.rstrip('\n')
			users.append(line)
	return users

def log_in_inst(login,password):	
	driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher") # логинимся на сайте
	driver.find_element_by_name('username').send_keys(login)
	driver.find_element_by_name('password').send_keys(password)
	log_in_button = driver.find_element_by_xpath("//button[@class='_0mzm- sqdOP  L3NKy       '][@type='submit']").click()
	time.sleep(3) # ждём авторизации на сайте
	print('log_in{}ok'.format('.' * 50))

def get_comments(url_post, users=users()):								# получаем комментарии пользователей
	driver.get(url_post)
	autor = driver.find_element_by_tag_name('h2').text
	while True: # если есть кнопка "показать ещё коменнтарии", кликаем, если нет, то выходим из цикла, обрабатывая исключение
		try:
			driver.find_element_by_xpath("//button[@class='Z4IfV _0mzm- sqdOP yWX7d        '][@type='button']").click() 
			time.sleep(0.5)
		except NoSuchElementException:
			break
	users_com = []		
	users_list = driver.find_elements_by_tag_name('h3')
	for i in users_list:
		elem = i.text
		users_com.append(elem)
	value = [ '+' if i in users_com else '-' for i in users]
	report_com = dict(zip(users,value))
	print('{}{}ok'.format(autor,'.' * (56 - int(len(autor)))))
	return (autor, report_com)

def close_browser():
	driver.close()












'''
def get_likes(url_post):								# получаем лайки пользователей(блок в разработке)
	users_list = []
	driver.get(url_post)								
	driver.find_element_by_class_name('zV_Nj').click()   
	time.sleep(1)
	likes_html = driver.find_element_by_class_name('PZuss')
	users_list.append(likes_html.text)
	driver.get("https://www.instagram.com/graphql/query/?query_hash=e0f59e4a1c8d78d0161873bc2ee7ec44&variables=%7B%22shortcode%22%3A%22BoU0Gl5BleC%22%2C%22include_reel%22%3Atrue%2C%22first%22%3A12%2C%22after%22%3A%22QVFBWDdGd0FaaEtoOUZQR1dHSEdfZHFPUDFSRzVNZHJKWnZIOGFVXy0tZHdXY3ZCX3Y1QzRxT001QzZTN1lTYjVYX2wwdHdCMHQzUnFCOEItdmxHRUdPRg%3D%3D%22%7D")
	while True:
		try:
			json_string = BeautifulSoup(driver.page_source)
			dict_all = json.loads(json_string.text)
			code = dict_all["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"][:-2]
		except TypeError:
			break
		url_call = ("https://www.instagram.com/graphql/query/?query_hash=e0f59e4a1c8d78d0161873bc2ee7ec44&variables=%7B%22shortcode%22%3A%22BoU0Gl5BleC%22%2C%22include_reel%22%3Atrue%2C%22first%22%3A12%2C%22after%22%3A%22{}%3D%3D%22%7D".format(code))
		driver.get(url_call)  
	return 
'''
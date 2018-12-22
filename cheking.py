from inst_lib import *

print('\nВыполняется вход в учётную запись...\n')

log,pas = get_log_in()

try:
	log_in_inst(log,pas)
	print('\nВход выполнен успешно')
except Exception:
	print('\nНе удалось выполнить вход, проверьте данные в файле "login.txt" и повторите попытку')

posts = get_posts()

print('\nПолучаем данные, это может занять некоторое время...\n')

comments = []					# полученные с сайта данные сохраняем в словарь, в котором ключом является url-адрес, а значением, сами комментарии
for i in posts:
	comments.append(get_comments(i))

print('\nФормируем отчёт...\n')

with open("report.txt", "w", encoding='utf-8') as report:     # записываем комментарии в файл
	for i in comments:
		report.write('{}\n{}\n{}\n'.format(48*'-',i[0],48*'-'))
		for k,v in i[1].items():
			report.write('{}: |{}|\n'.format(k,v))

close_browser()

print('\nСбор данных завершён успешно. Можешь закрыть окно и проверить файл "report.txt"')




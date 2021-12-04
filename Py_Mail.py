#!/usr/bin/python3.6
# Хэшбенг для SangomaOS( Модифицированый CentOS 7 для нужд FreePBX)

# Универсальный скрипт для отправки почтовых сообщений

# Импортируем библиотеки для использования фунцкий работы с ОС
import sys
import os

# выбираем безопасный протокол SMTP (порт 465, с использованием SSL)
from smtplib import SMTP_SSL as SMTP
# выбираем стандартный SMTP протокол (порт 25, без шифрования)
# from smtplib import SMTP

# Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
import mimetypes
# Импортируем энкодер
from email import encoders
# Импорт класса общего типа
from email.mime.base import MIMEBase
# Импорт класса: Текст/HTML
from email.mime.text import MIMEText
# Импорт класса: Изображения
from email.mime.image import MIMEImage
# Импорт класса: Аудио
from email.mime.audio import MIMEAudio
# Импорт класса: Многокомпонентный объект
from email.mime.multipart import MIMEMultipart

# Присваиваем переменной первый  аргумент из командной строки
cli_arg1 = str(sys.argv[1])
# cli_arg1 = "+7XXXXXXXXXX"				# Для теста
# Присваиваем переменной второй  аргумент из командной строки
cli_arg2 = str(sys.argv[2])
# cli_arg2 = "+74832XXXXXX"				# Для теста
# Присваиваем переменной третьий аргумент из командной строки
cli_arg3 = str(sys.argv[3])
# cli_arg3 = "c:\temp\test.wav"			# Для теста в Windows
# cli_arg3 = "/temp/test.wav"			# Для теста в Linux

# Имя файла в абсолютном или относительном формате
filepath = cli_arg3
# Получаем только имя файла
filename = os.path.basename(filepath)                     	

# Настройки подключения
SMTPserver = 'smtp.yandex.ru' 								# SMTP сервер яндекса как пример
mailer = 'your_e-mail@maildomain.ru'						# Отправитель
destination = ['destination@mail.ru']						# Получател(и)
sendto = 'destination@mail.ru'								# Адресат
USERNAME = "your_login"										# Логин
PASSWORD = "your_pass"										# Пароль

# Подтип текста, возможные варианты: plain, html, xml
text_subtype = 'plain'

# Текст письма
body_content=f"""\
Ваш текст.... {Ваша переменная}
"""
#subtext1 = "Пропущен звонок с номера: "
#subtext2 = subtext1 + str(cli_arg1)

subject = f"Ваш текст.... {Ваша переменная}"

try:
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = mailer
	msg['To'] = sendto
	msg.attach(MIMEText(body_content, text_subtype))
	# Прикрепляем файл
	# Если файл существует
	if os.path.isfile(filepath):
		# Определяем тип файла на основе его расширения
		ctype, encoding = mimetypes.guess_type(filepath)
		# Если тип файла не определяется
		if ctype is None or encoding is not None:
			# Будем использовать общий тип
			ctype = 'application/octet-stream'
		# Получаем тип и подтип
		maintype, subtype = ctype.split('/', 1)
		# Если текстовый файл
		if maintype == 'text':
			# Открываем файл для чтения
			with open(filepath) as fp:
				# Используем тип MIMEText
				file = MIMEText(fp.read(), _subtype=subtype)
				# Закрываем файл
				fp.close()
		# Если изображение
		elif maintype == 'image':
			# Открываем файл для чтения
			with open(filepath, 'rb') as fp:
				# Используем тип MIMEImage
				file = MIMEImage(fp.read(), _subtype=subtype)
				# Закрываем файл
				fp.close()
		# Если аудио
		elif maintype == 'audio':
			# Открываем файл для чтения
			with open(filepath, 'rb') as fp:
				# Используем тип MIMEAudio
				file = MIMEAudio(fp.read(), _subtype=subtype)
				# Закрываем файл
				fp.close()
		# Неизвестный тип файла
		else:
			# Открываем файл для чтения
			with open(filepath, 'rb') as fp:
				# Используем общий MIME-тип
				file = MIMEBase(maintype, subtype)
				# Добавляем содержимое общего типа (полезную нагрузку)
				file.set_payload(fp.read())
				# Закрываем файл
				fp.close()
			# Содержимое должно кодироваться как Base64
			encoders.encode_base64(file)
		# Добавляем заголовки
		file.add_header('Content-Disposition', 'attachment', filename=filename)
		# Присоединяем файл к сообщению
		msg.attach(file)
	
	# Отправляем письмо
	py_mail = SMTP(SMTPserver)
	py_mail.set_debuglevel(False)
	py_mail.login(USERNAME, PASSWORD)
	py_mail.sendmail(mailer, destination, msg.as_string())
	py_mail.quit()
except:
	# В случае ошибки - сообщение об ошибке
	sys.exit( "mail failed; %s" % "CUSTOM_ERROR" )
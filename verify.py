# -*- coding: utf-8 -*-
#
# verify.py - проверяет наличие архивов за текущую дату по путям.
# Отправляет e-mail о проделанной проверке
#


import time
import platform
import smtplib
import os
import glob


# Пути проверки
pathes = [r'D:\Backup\1C', r'\\NAS\copy1c\py_backup']

# Получатели сообщения
recipients = ['matushkin.oleg@gmail.com', 'okibkursk-it@yandex.ru']

# Отправитель сообщения
sender = 'semashko@kursktelecom.ru'

# Тема сообщения
subject = 'Verify 1C archives on {}'.format(time.strftime('%Y-%m-%d'))

# Шаблоны имен проверяемых файлов
# 0123456789012345678901
# 1c82buh_YYYYMMDDHHMMSS.zip
templates = ['1cv82buh', '1cv77buh', '1cv82zik', '1cv82ahd']


# Функция проверки наличия файлов в каталогах
def verify_files(vpath=[r'D:\Backup\1C', r'\\NAS\copy1c\py_backup'],
                vtempl=['1cv82buh', '1cv77buh', '1cv82zik', '1cv82ahd'],
                timetempl=time.strftime('%Y%m%d')):

    files_found = []
    print('in function verifyfiles')
    # Получаем список файлов по шаблону, с полными путями
    for i in vpath:
        if os.path.isdir(i):
            files_found += glob.glob(i+r'\*' + timetempl + '*')
    file_info = {}
    for i in files_found:
        fsize = os.path.getsize(i) // 1024
        fmtime = time.localtime(os.path.getmtime(i))
        file_info[i] = [str(fsize), time.strftime('%Y-%m-%d, %H:%M', fmtime)]
    return file_info

# Функция отправки сообщения
def mail_send(fromaddr, toaddr, subject, message):
    '''Функция отправки письма'''
    from_header = 'From: router2 <{}>\r\n'.format(fromaddr)
    string_toaddr = ','.join(['<' + i + '>' for i in toaddr])
    to_header = 'To: recipients {}\r\n'.format(string_toaddr)
    subject_header = 'Subject: {}\r\n'.format(subject)
    msg = '{}{}{}\n{}'.format(from_header, to_header, subject_header, message)
    server = smtplib.SMTP('192.168.0.219')
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()
    print(msg)


def main():
    message = platform.platform()
    message += '\n\nTime of verifyng: {}'.format(time.strftime('%H:%M'))
    message += '\nPathes: ' + ', '.join(pathes)
    message += '\nTemplates:' + ', '.join(templates) + '\n\n'
    message += 'Finded files:\n\n'
    ff = verify_files(vpath=pathes)
    for i in sorted(ff):
         message += '{}, Size: {} KB, Time modif: {}\n'.format(i, ff[i][0], ff[i][1])
    print(message)
#    print('\n\n********** mail send off!!! *********\n\n')
    mail_send(sender, recipients, subject, message)


if __name__ == '__main__':
    main()

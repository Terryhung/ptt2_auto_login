# -*- coding: utf-8 -*-
import telnetlib
import time
import sys
import input_readfile

tn = telnetlib.Telnet('ptt2.cc')
time.sleep(2)
content = tn.read_very_eager().decode('big5', 'ignore')

check_account = "請輸入代號".decode('utf-8')
check_double_account = "重複登入".decode('utf-8')
check_rewrite = "文章尚未完成".decode('utf-8')
check_content_1 = "瀏覽".decode('utf-8')
check_waterball = "無訊息記錄".decode('utf-8')

def login(account, password):
    tn.write((account+"\r\n").encode('big5'))
    time.sleep(1)
    tn.write((password+"\r\n").encode('big5'))
    time.sleep(3)
    # Check double account
    content = tn.read_very_eager().decode('big5', 'ignore')
    if check_double_account in content:
        delete_double_account()

    # enter account
    tn.write('y')
    time.sleep(2)

    # check if some article didn't delete
    content = tn.read_very_eager().decode('big5', 'ignore')
    if check_rewrite in content:
        delete_article()
    print('---Login!---')
    return content


def logout():
    tn.write('g\r\n')
    time.sleep(1)
    tn.write('Y\r\n')
    time.sleep(1)
    print('---Logout!---')
    exit()


def delete_double_account():
    tn.write(("Y"+"\r\n").encode('big5'))
    time.sleep(8)


def delete_article():
    time.sleep(1)
    tn.write(("Q"+"\r\n").encode('big5'))
    time.sleep(8)


def enter_board(board_name):
    tn.write('s')
    time.sleep(1)
    tn.write(board_name+'\r\n')
    time.sleep(2)


def post_article(title, content):
    post = chr(16)
    tn.write(post)
    time.sleep(3)
    tn.write('\r\n')
    time.sleep(3)
    tn.write(title)
    time.sleep(2)
    tn.write('\r\n')
    for i in content:
        tn.write(i)
        time.sleep(2)
        tn.write('\r\n')
        time.sleep(1)
    tn.write(chr(24))
    time.sleep(2)
    tn.write('S'+'\r\n')
    time.sleep(2)
    tn.write('a')
    time.sleep(1)
    tn.write('qqqqqqqqqqqqq')
    time.sleep(1)


def enter_mail():
    tn.write('m\r\n')
    time.sleep(2)


def send_mail(id, title, content):
    tn.write('s\r\n')
    time.sleep(1)
    tn.write(id + '\r\n')
    time.sleep(1)
    tn.write(title + '\r\n')
    time.sleep(1)
    for i in content:
        tn.write(i)
        time.sleep(2)
        tn.write('\r\n')
        time.sleep(1)
    tn.write(chr(24))
    time.sleep(1)
    tn.write('S' + '\r\n')
    time.sleep(1)
    tn.write('N' + '\r\n')
    time.sleep(1)
    tn.write('a')
    time.sleep(1)
    tn.write('eeeeeee')
    time.sleep(2)


def send_message(id, content):
    send = chr(21)
    tn.write(send)
    time.sleep(1)
    tn.write('s')
    time.sleep(1)
    tn.write(id + '\r\n')
    time.sleep(1)
    tn.write('w')
    time.sleep(1)
    tn.write('content\r\n')
    time.sleep(1)
    tn.write('Y\r\n')
    time.sleep(1)
    tn.write('eeeee')
    time.sleep(1)


def read_mail():
    tn.write('eeeeeee')
    time.sleep(2)
    tn.write('m\r\n')
    time.sleep(1)
    tn.write('r\r\n')
    time.sleep(1)

    # chech how much mail
    content = str(tn.read_very_eager().decode('big5', 'ignore').encode('utf-8'))
    number = int(content.split(':')[2].split('/')[0])

    tn.write('1\r\n')
    time.sleep(1)
    tn.write('\r\n')
    time.sleep(1)
    content = tn.read_very_eager().decode('big5', 'ignore')
    for i in range(1, number+1):
        filename = "mail_" + str(i)
        f = open(filename, 'w')
        f.write(content.encode('utf-8'))
        f.close()
        tn.write('\r\n')
        time.sleep(3)
        content = tn.read_very_eager().decode('big5', 'ignore')
    tn.write('eee')
    time.sleep(1)
    print ('you receive %s mail') % number


def read_waterball():
    send = chr(21)
    tn.write(send)
    time.sleep(1)
    tn.write('l')
    time.sleep(1)
    content = tn.read_very_eager().decode('big5', 'ignore')
    if check_waterball not in content:
        filename = "waterball"
        f = open(filename, 'w')
        f.write(content.encode('utf-8'))
        f.close()
        tn.write('\r\n')
        time.sleep(3)
        tn.write('r\r\n')
        time.sleep(1)
    else:
        print ('not water ball')
    tn.write('eeeeee')
    time.sleep(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ('Usage: ptt2.py <filename> \n')
        exit()

    filename = sys.argv[1]
    fileopen = open(filename, 'r')
    data = input_readfile.read_file(fileopen)
    LG = 0

    if check_account in content:
        login(data['login'][0], data['login'][1])
        data.pop('login', None)
        for action in data:
            if 'waterball' in action:
                send_message(data[action][0], data[action][1])
                print ('finish waterball')
            elif 'mail' in action:
                enter_mail()
                send_mail(data[action][0], data[action][1], data[action][2])
                print ('finish send mail')
            elif 'post' in action:
                enter_board(data[action][0])
                post_article(data[action][1], data[action][2])
                print ('finish post article')
            elif 'logout' in action:
                LG = 1
            elif 'readm' in action:
                read_mail()
                print ('finish read mail')
            elif 'readw' in action:
                read_waterball()
                print ('finish read waterball')

        if LG == 1:
            logout()

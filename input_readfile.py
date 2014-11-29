from bs4 import BeautifulSoup

# fileopen = open('test.input', 'r')

def read_file(fileopen):
    tmp = []
    data = {}
    data['logout'] = 0
    for f in fileopen:
        tmp.append(f.strip())

    for index, i in enumerate(tmp):
        if i[:2] == "<I":
            data['login'] = [str(BeautifulSoup(tmp[index]).id.string), str(BeautifulSoup(tmp[index+1]).select('pass')[0].string)]

        elif i[:2] == "<B":
            data_name = 'post_' + str(index)
            data[data_name] = [str(BeautifulSoup(tmp[index]).board.string), str(BeautifulSoup(tmp[index+1]).p.string)]
            my_content = ""
            c_index = index+2
            while "</CONTENT>" not in tmp[c_index]:
                my_content = my_content + tmp[c_index] + '\n'
                c_index = c_index + 1
            my_content = my_content + tmp[c_index] + '\n'
            data[data_name].append(map(lambda x: str(x), BeautifulSoup(my_content.strip()).content.string.split('\n')))

        elif i[:2] == "<W":
            data_name = 'waterball_' + str(index)
            data[data_name] = [str(BeautifulSoup(tmp[index]).w.string), str(BeautifulSoup(tmp[index+1]).content.string)]

        elif i[:2] == "<M":
            data_name = 'mail_' + str(index)
            data[data_name] = [str(BeautifulSoup(tmp[index]).m.string), str(BeautifulSoup(tmp[index+1]).title.string)]
            my_content = tmp[index+2] + '\n'
            c_index = index+2
            while "</CONTENT>" not in tmp[c_index]:
                c_index = c_index + 1
                my_content = my_content + tmp[c_index] + '\n'
            data[data_name].append(map(lambda x: str(x), BeautifulSoup(my_content.strip()).content.string.split('\n')))
        elif i[:2] == "<E":
            data['logout'] = 1
        elif "READMAIL" in i:
            data['readm'] = 1
        elif "READWATER" in i:
            data['readw'] = 1

    return data

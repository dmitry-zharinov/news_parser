import json
import re


def remove_urls(v_text):  # убираем ссылки
    v_text = re.sub(r'href\S+\">', '', v_text, flags=re.MULTILINE)
    v_text = re.sub(r'<\S+', '', v_text, flags=re.MULTILINE)
    return v_text


# читаем файл
def read_json_file(filename, encode):
    with open(filename, encoding=encode) as data_file:
        data = json.load(data_file)
    return data


# получаем из файла список слов > 6 символов+ убираем лишние символы
def get_words_list_from_json_file(json_file):
    # формируем список слов
    words_list = []
    for item in json_file['rss']['channel']['item']:
        if type(item['title']) is dict:
            words_list.extend(item['title']['__cdata'].split(' '))
            words_list.extend(item['description']['__cdata'].split(' '))
        else:
            words_list.extend(item['title'].split(' '))
            words_list.extend(item['description'].split(' '))
    # удаляем ненужные символы и ссылки
    symbols_to_strip = './,\][{}]'
    words_list = [item.strip(symbols_to_strip) for item in words_list]
    words_list = map(remove_urls, words_list)
    # оставляем только слова > 6 символов
    words_list = [x for x in words_list if len(x) > 6]
    return words_list


# получаем список популярных слов
def get_popular_words(json_file, num_of_elements):
    words_list = []
    words_list = sorted(get_words_list_from_json_file(json_file), key=words_list.count, reverse=True)
    list_of_popular_words = list(set(words_list))
    list_of_popular_words.sort(key=words_list.index)
    return print('Топ-{} слов в файле "{}": {}'.format(num_of_elements, json_file['rss']['channel']['title'],
                                                       ', '.join(list_of_popular_words[:num_of_elements])))


def main():
    get_popular_words(read_json_file('newscy.json', 'koi8-r'), 10)
    get_popular_words(read_json_file('newsafr.json', 'utf-8'), 10)
    get_popular_words(read_json_file('newsfr.json', 'iso-8859-5'), 10)
    get_popular_words(read_json_file('newsit.json', 'windows-1251'), 10)

main()


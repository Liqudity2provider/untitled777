import json
import re
import requests
from bs4 import BeautifulSoup

URL = 'https://www.kinonews.ru/best_top100/'

'''
жанрам, записывать рейтинг с кинопоиска и imdb, 
уметь в админке сортировать по ним, добавить поиск(по полям up to you), 
сохранять постер, ссылку на просмотр
'''


def parse_kinonews():
    result = []
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, features="lxml", from_encoding="utf-8")
    names = soup.find_all('a', {'class': 'titlefilm'})
    genres = re.findall('<span class="film-rubrpers">Жанр:</span>(.+?)</div>', str(soup))

    images = soup.find_all('div', {'class': 'rating_leftposter'}, )
    hrefs = ['https://www.kinonews.ru/' + re.findall('href="(.+?)"', str(i))[0] for i in images]
    images = ['https://www.kinonews.ru/' + re.findall('src="(.+?)"', str(i))[0] for i in images]

    res_genres = []
    for genre in genres:
        res_genres.append(re.findall('>(.+?)</a>', genre))
    ratings = soup.find_all('span', {'class': 'rating-big'})

    for name, genre, rating, href, img in zip(names, res_genres, ratings, hrefs, images):
        name = name.getText()
        rating = re.findall('>(.+?)</', str(rating))[0]
        temp = {
            'name': name,
            'image': img,
            'link': href,
            'rating': rating,
            'genres': genre,
        }
        result.append(temp)

    return result


def parse_func():
    l_films = parse_kinonews()
    return l_films


def return_genres():
    all_genres = get_uniq_genre(parse_func())
    return all_genres


def get_uniq_genre(list_of_films):
    res = set()
    for i in list_of_films:
        i = i['genres']
        for j in i:
            res.add(j)
    return res


if __name__ == '__main__':
    print(parse_func())
    # print(return_genres())
    # print(get_rating_and_genre('https://www.ivi.ru//watch/100131'))


import os
from flask import Flask, request, jsonify
import logging
import json
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
sessionStorage = {}
cities = {
    'москва': ['', ''],
    'нью-йорк': ['', ''],
    'париж': ['', '']
}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def get_first_name(req) -> None | str:
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('get_first_name', None)
    return None


def get_city(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            return entity['value'].get('city', None)
    return None


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!!!'
        sessionStorage[user_id] = {
            'firstname': None
        }
        return

    if sessionStorage[user_id]['firstname'] is None:
        firstname = get_first_name(req)
        if firstname is None:
            res['response']['text'] = 'Не расслышала имя, повторите!'
        else:
            sessionStorage[user_id]['firstname'] = firstname
            res['response']['text'] = f'Приятно познакомиц, {firstname.title()}. Я - Алиса. Какой город хочеш увидетьььььь?'
            res['response']['buttons'] = [
                {
                    'title': city.title(),
                    'hide': True
                } for city in cities.keys()
            ]
            
            
    else:
        city = get_city(req)
        if city is cities:
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = 'Этот город я знаю'
            res['response']['card']['image_id'] = random.choice(cities[city])
            res['response']['text'] = 'Я угадалааааа'
        else:
            res['response']['text'] = 'Я впервые слыщу об этом городелфыолы, попрбуй снова!!1!!!!111'


def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port=port)

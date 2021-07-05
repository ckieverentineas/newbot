from datetime import time
from re import findall
from nltk.util import pr
import requests

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from textblob import TextBlob

import config, generate

def main():   
    # Авторизация группы:
    vk_session = vk_api.VkApi(token = config.token)
    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    print("LongPool Listing now")
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                print("input message")
                #запуск события печати
                vk.messages.setActivity(type='typing', peer_id = event.user_id)
                #обработка текста
                try:
                    correct = TextBlob(event.text).correct()
                    print(correct.string)
                    translate = TextBlob(correct.string).translate(from_lang='ru', to='en')
                    print(translate.string)
                    temp = TextBlob(generate.response(translate.string)).translate(from_lang='en', to='ru')
                except:
                    print("Нельзя перевести")
                    temp = TextBlob("o_0")
                #отправка текста
                print('id{}: "{}" Ответ: "{}"'.format(event.user_id, event.text, temp.string))
                vk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    message = temp.string
                )
    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверам ВК \n")
        time.sleep(3)

if __name__ == '__main__':
    main()
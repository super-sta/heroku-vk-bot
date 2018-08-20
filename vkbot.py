#!/usr/bin/env python

import time
import vk_api

token = 'cf7291f2d59598e85f9a9e498d3674c880e0c28fe737a33a80bb5aa7ee76cea17b2096a15b67a265137af'
vk = vk_api.VkApi(token = token)
values = {'offset': 0,'count': 20,'unread': 1}

dictionary = {
    'question': ['Привет', 'Как дела'],
    'answer':   ['Привет, челик', 'Все OK, кэп']
}
count_question, count_answer = len(dictionary['question']), len(dictionary['answer'])

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id':user_id,'message':s})
    print('Сообщение было успешно отправлено')

def main():
    if count_question != count_answer:
        print(f'Неверно составлен словарь ответов. Записано вопросов {count_question}, а количетсво ответов {count_answer}')
        print(f'Список вопросов: {dictionary["question"]}')
        print(f'Список ответов: {dictionary["answer"]}')
        return

    COUNT_DICT = count_question
    response = vk.method("messages.getDialogs", values)

    if response['items']:
        unread = int(response['items'][0]['unread'])
        if unread > 1:
            write_msg(response['items'][0]['message']['user_id'], 'Вы пишите слишком быстро!! Я не успеваю за вашим порывом =) Дождитесь мего ответа и пишите новый вопрос.')
            return 
    for item in response['items']:
        na = 'not_answer'
        userid = item['message']['user_id']
        msg = item['message']['body']
        print(f'Ответ на сообщение: "{msg}", пользователю с id: {userid}')

        for i in range(0, COUNT_DICT):
            if msg == dictionary['question'][i]:
                write_msg(userid, dictionary['answer'][i])
                na = 'success'
                return
        
        if na == 'not_answer':
            write_msg(item['message']['user_id'], f'Я не понимаю тебя, кэп. Моя память не велика и уместились только такие команды, как: ({"; ".join(dictionary["question"])})' )


if __name__ == "__main__":
    while True:
        main()
        time.sleep(0.2)


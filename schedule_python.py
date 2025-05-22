from telethon import TelegramClient
from telethon.tl.functions.messages import SendMediaRequest
from telethon.tl.types import InputMediaUploadedPhoto
from telethon.tl.types import InputPeerChannel, InputSingleMedia
from telethon.tl.functions.messages import SendMultiMediaRequest, SendMessageRequest
import random
import os
from datetime import datetime, timedelta,timezone
import re
from telethon.tl.types import DocumentAttributeVideo

def get_pictures(folder_path):
    return sorted([
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ])


async def schedule_posts(client, chat_info):

    VIDEO_ATTRS = [
        DocumentAttributeVideo(
            duration=0,  # длительность поставит Телеграм
            w=720,  # ширина
            h=1280,  # высота
            supports_streaming=True
        )
    ]

    date_pattern = r'\b(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\b'
    time_pattern = r"\b\d{1,2}:\d{2}\b"

    # добавляем таймзону (МСК — UTC+3)
    moscow_now = datetime.now().replace(tzinfo=timezone(timedelta(hours=3)))

    course_day, course_month = re.search(date_pattern, chat_info['title']).group().split('.')
    course_hour, course_minute = re.search(time_pattern, chat_info['title']).group().split(':')

    month_now = datetime.now().strftime('%m')
    day_now = datetime.now().strftime('%d')
    year_now = datetime.now().strftime('%Y')

    if month_now > course_month:
        course_year = int(year_now) + 1
    else:
        course_year = int(year_now)

    # дата начала курса. Московское время считаем как UTC + 3 часа
    course_date = datetime(course_year, int(course_month), int(course_day), int(course_hour), int(course_minute)).replace(tzinfo=timezone(timedelta(hours=3)))

    # дата отправки сообщения-знакомства с карточками
    greeting_date = (course_date - timedelta(days=1))

    # готовим пост-знакомство
    greeting_pictures = get_pictures('/Users/vadim/Documents/algoritmika/my_cards/')

    greeting_text = '''
    Здравствуйте, уважаемые родители! 

Меня зовут Вадим, я буду вести мини-курс Программирование на Python👋 Подробнее об мне можете прочитать в карточках.

Ближайшие три дня мы будем с вами много общаться. После каждого занятия я буду скидывать сюда видео с рассказом об итогах урока. Также с радостью отвечу на все вопросы по программе курса.

Напомню, что ваше присутствие обязательно на первом и третьем занятиях. Так как я буду давать информацию для вас. К тому же, вы сможете поддержать своих детей, ведь новые незнакомые люди — это всегда волнительно! 

До встречи!
    '''

    # пост-знакомство будет запланирован к публикации ровно за день до первого урока. Если это время в прошлом, пост публикуется сразу
    # await client.send_file(
    #     chat_info['id'],
    #     greeting_pictures,
    #     caption=greeting_text,
    #     schedule=greeting_date
    # )


    # пост с чеклистом в первый день

    checklist_time = course_date - timedelta(minutes=30)
    checklist = '/Users/vadim/Documents/algoritmika/check-list.pdf'
    chek_text = f'''
    Всем здравствуйте!

Через 30 минут начинаем обучение на мини-курсе по Python 🔥

Жду вас и детей на онлайн-платформе в {course_date.hour}:{course_date.minute:02d} мск.

А до начала занятия предлагаю проверить, что вы полностью готовы! Чтобы было проще, сделали для вас чек-лист 😉 Если что-то забыли — еще есть время доделать 💜'''
    # await client.send_file(
    #     chat_info['id'],
    #     checklist,
    #     caption=chek_text,
    #     schedule=checklist_time
    # )

    # обратная связь по дню 1
    feedback_1_date = (course_date + timedelta(days=1)).replace(hour=10, minute=0)
    video_1 = '/Users/vadim/Documents/algoritmika/video/python_day_1_test.mp4'


    feedback_1_text = '''
    Еще раз здравствуйте, уважаемые родители!

В видео рассказываю, чем мы с ребятами занимались на первом занятии и чему уже научились 😊

Если есть вопросы, пожелания, комментарии по поводу прошедшего урока, пишите!'''

    # await client.send_file(
    #     chat_info['id'],
    #     video_1,
    #     supports_streaming=True,
    #     video_note=False,
    #     caption=feedback_1_text,
    #     schedule=feedback_1_date,
    #     attributes=VIDEO_ATTRS,
    # )

    # пост с карточками про Python во второй день
    cards_date = (course_date + timedelta(days=2)) - timedelta(minutes=30)
    cards_pictures = get_pictures('/Users/vadim/Documents/algoritmika/python_img')
    cards_text = f'''
    Здравствуйте! Сегодня состоится второй урок мини-курса 😎

Предлагаю вам побольше узнать про язык Python. Так вы будете лучше понимать, чем занимаются ребята на занятиях. И не растеряетесь, когда дети начнут рассказывать вам про алгоритмы, переменные и функции 😉 Читайте про Python в карточках.

Если вдруг кто-то из детей пропустил первое занятие, можно сейчас пройти прошлый урок на онлайн-платформе.

Жду ребят в {course_date.hour}:{course_date.minute:02d} на втором уроке!'''
    # await client.send_file(
    #     chat_info['id'],
    #     cards_pictures,
    #     caption=cards_text,
    #     schedule=cards_date
    # )

    # обратная связь по дню 2
    feedback_2_date = (course_date + timedelta(days=2)).replace(hour=10, minute=0)
    video_2 = '/Users/vadim/Documents/algoritmika/video/python_day_2_test.mp4'

    feedback_2_text = '''
    Здравствуйте, дорогие родители!

Продолжаю делиться результатами обучения на мини-курсе. Отправляю видео с рассказом о том, чем мы занимались на втором уроке 😊'''

    # await client.send_file(
    #     chat_info['id'],
    #     video_2,
    #     supports_streaming=True,
    #     video_note=False,
    #     caption=feedback_2_text,
    #     schedule=feedback_2_date,
    #     attributes=VIDEO_ATTRS,
    # )

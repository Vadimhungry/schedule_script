import os
import re
from datetime import datetime, timedelta, timezone
from telethon.tl.types import DocumentAttributeVideo
from python.dates import get_posts_dates
import json


def get_pictures(folder_path):
    return sorted(
        [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]
    )


async def schedule_posts(client, chat_info):

    # настройка для корректного постинга видео
    VIDEO_ATTRS = [
        DocumentAttributeVideo(
            duration=0,  # длительность поставит Телеграм
            w=720,  # ширина
            h=1280,  # высота
            supports_streaming=True,
        )
    ]

    # получаем даты постов
    dates = get_posts_dates(chat_info["title"])

    # получаем тексты постов
    with open("python/texts.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

    # получаем видосы
    with open("python/videos.json", "r", encoding="utf-8") as f:
        videos = json.load(f)

    # готовим пост-знакомство
    greeting_pictures = get_pictures("/Users/vadim/Documents/algoritmika/my_cards/")

    # пост-знакомство будет запланирован к публикации ровно за день до первого урока. Если это время в прошлом, пост публикуется сразу
    await client.send_file(
        chat_info["id"],
        greeting_pictures,
        caption=messages["greeting"],
        schedule=dates["greeting_date"],
    )

    # пост с чеклистом в первый день
    checklist = "/Users/vadim/Documents/algoritmika/check-list.pdf"

    await client.send_file(
        chat_info["id"],
        checklist,
        caption=messages["checklist"].format(
            hour=dates["course_hour"], minute=dates["course_minute"]
        ),
        schedule=dates["checklist_date"],
    )

    # обратная связь по дню 1
    await client.send_file(
        chat_info["id"],
        videos["feedback_1"],
        supports_streaming=True,
        video_note=False,
        caption=messages["feedback_1"],
        schedule=dates["feedback_1"],
        attributes=VIDEO_ATTRS,
    )

    # пост с карточками про Python во второй день
    cards_pictures = get_pictures("/Users/vadim/Documents/algoritmika/python_img")
    await client.send_file(
        chat_info["id"],
        cards_pictures,
        caption=messages["cards"].format(
            hour=dates["course_hour"], minute=dates["course_minute"]
        ),
        schedule=dates["cards"],
    )

    # обратная связь по дню 2
    await client.send_file(
        chat_info["id"],
        videos["feedback_2"],
        supports_streaming=True,
        video_note=False,
        caption=messages["feedback_2"],
        schedule=dates["feedback_2"],
        attributes=VIDEO_ATTRS,
    )

    # приглашение на третий урок
    await client.send_message(
        chat_info["id"],
        message=messages["final"].format(
            hour=dates["course_hour"], minute=dates["course_minute"]
        ),
        schedule=dates["final"],
    )

    # обратная связь по дню 3
    await client.send_file(
        chat_info["id"],
        videos["feedback_3"],
        supports_streaming=True,
        video_note=False,
        caption=messages["feedback_3"],
        schedule=dates["feedback_3"],
        attributes=VIDEO_ATTRS,
    )

    # пост с презентацией
    presentation = "/Users/vadim/Documents/algoritmika/python_presentation.pdf"

    await client.send_file(
        chat_info["id"],
        file=presentation,
        caption=messages["presentation"],
        schedule=dates["feedback_3"],
    )

    # todo вынести получение файлов в отдельный файл

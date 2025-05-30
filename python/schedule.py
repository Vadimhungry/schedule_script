
from telethon.tl.types import DocumentAttributeVideo
from python.dates import get_posts_dates
from python.pictures import get_python_pictures
import json


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

    # получаем картинки
    imgs = get_python_pictures()

    # получаем тексты постов
    with open("python/texts.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

    # получаем видосы
    with open("python/videos.json", "r", encoding="utf-8") as f:
        videos = json.load(f)

    # получаем файлы
    with open("python/files.json", "r", encoding="utf-8") as f:
        files = json.load(f)

    # пост-знакомство будет запланирован к публикации ровно за день до первого урока.
    # Если это время в прошлом, пост публикуется сразу
    await client.send_file(
        chat_info["id"],
        imgs["greeting"],
        caption=messages["greeting"],
        schedule=dates["greeting_date"],
    )

    # пост с чеклистом в первый день
    await client.send_file(
        chat_info["id"],
        files["checklist"],
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
    await client.send_file(
        chat_info["id"],
        imgs["cards"],
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
    await client.send_file(
        chat_info["id"],
        files["presentation"],
        caption=messages["presentation"],
        schedule=dates["feedback_3"],
    )
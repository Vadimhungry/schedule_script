from datetime import datetime, timedelta,timezone
import re

def get_posts_dates(course_title):
    dates = {}
    date_pattern = r'\b(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\b'
    time_pattern = r"\b\d{1,2}:\d{2}\b"

    # добавляем таймзону (МСК — UTC+3)
    moscow_now = datetime.now().replace(tzinfo=timezone(timedelta(hours=3)))

    course_day, course_month = re.search(date_pattern, course_title).group().split('.')
    course_hour, course_minute = re.search(time_pattern, course_title).group().split(':')

    month_now = datetime.now().strftime('%m')
    day_now = datetime.now().strftime('%d')
    year_now = datetime.now().strftime('%Y')

    if month_now > course_month:
        course_year = int(year_now) + 1
    else:
        course_year = int(year_now)

    # дата начала курса. Московское время считаем как UTC + 3 часа
    course_date = datetime(course_year, int(course_month), int(course_day), int(course_hour),
                           int(course_minute)).replace(tzinfo=timezone(timedelta(hours=3)))
    dates['course_date'] = course_date

    # дата отправки сообщения-знакомства с карточками
    dates['greeting_date'] = (course_date - timedelta(days=1))

    # дата отправки чеклиста
    dates['checklist_date'] = course_date - timedelta(minutes=30)

    # дата первого видео
    dates['feedback_1'] = (course_date + timedelta(days=1)).replace(hour=10, minute=0)

    # дата поста с карточками про Питон
    dates['cards'] = (course_date + timedelta(days=1)) - timedelta(minutes=30)

    # дата второго видео
    dates['feedback_2'] = (course_date + timedelta(days=2)).replace(hour=10, minute=0)

    # дата приглашения на последний урок
    dates['final'] = (course_date + timedelta(days=2)) - timedelta(hours=1)

    # дата третьего видео
    dates['feedback_3'] = (course_date + timedelta(days=3)).replace(hour=10, minute=0)

    return dates
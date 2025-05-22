from telethon import TelegramClient
from schedule_python import schedule_posts
from dotenv import load_dotenv
import os


load_dotenv()  # Загружаем переменные из .env

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
client = TelegramClient('my_user', api_id, api_hash)


async def main():

    await client.start()

    # Получаем все доступные диалоги
    dialogs = await client.get_dialogs()

    # Список для хранения найденных чатов
    found_chats = []

    # Переменная для подсчета количества найденных чатов
    count = 0
    max_results = 10

    # Ищем чаты с нужным ключевым словом
    keyword = 'Мини-курс'
    for dialog in dialogs:
        entity = dialog.entity
        if ((getattr(entity, 'megagroup', False) or getattr(entity, 'broadcast', False))
                and keyword.lower() in entity.title.lower()):
            found_chats.append({
                'title': entity.title,
                'id': entity.id,
                'access_hash': entity.access_hash
            })
            count += 1
            print(f"{count}. {entity.title}")


        if count >= max_results:
            break

    # Если чаты найдены, позволяем выбрать
    if found_chats:
        choice = input(f"\nВыберите чат (1-{len(found_chats)}): ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(found_chats):
                selected_chat = found_chats[choice - 1]
                print(f"\nВы выбрали чат: {selected_chat['title']}, ID: {selected_chat['id']}")
                await schedule_posts(client, selected_chat)
            else:
                print("Некорректный выбор!")
        except ValueError:
            print("Пожалуйста, введите номер чата из списка.")


with client:
    client.loop.run_until_complete(main())

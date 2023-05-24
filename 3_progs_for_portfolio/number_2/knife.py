import moviepy.editor
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from pytube import YouTube
import moviepy.editor



bot_token = '6091235419:AAHpkb6-21fptGgcvz8em-dF1ZEpUC5L5hY'
# Инициализация бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# Настройка логгера
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Пришли мне ссылку на видео на YouTube.")


@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        list_video = []
        list_audio = []

        # Получение ссылки на видео из сообщения пользователя
        video_url = message.text.strip()

        # Загрузка видео с YouTube
        youtube = YouTube(video_url)
        video = youtube.streams.first()
        video_filename = video.download()
        list_video.append(video_filename)

        # Конвертация видео в аудио
        video_in_audio = moviepy.editor.VideoFileClip(list_video[0])
        audio = video_in_audio.audio
        tag = youtube.title
        audio_filename = f"{tag}.mp3"
        audio.write_audiofile(audio_filename)
        list_audio.append(audio_filename)

        # Отправка аудиофайла с прикреплением пользователю
        with open(audio_filename, 'rb') as audio_file:
            await message.reply("Ваш аудио файл:")
            await message.reply_audio(audio_file)

        # Удаление временных файлов
        os.remove(video_filename)
        os.remove(audio_filename)

    except Exception as e:
        logging.exception(e)
        await message.reply('Произошла ошибка при обработке видео.')


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
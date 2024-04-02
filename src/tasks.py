from telebot import TeleBot
from celery import Celery
import asyncio

from datetime import datetime, timedelta
from bot.db.crud import SessionRecordCrud
from bot.settings import BotConfig, TaskConfig

app = Celery('Tasks', broker=BotConfig.BROKER)

app.config_from_object(TaskConfig)
app.autodiscover_tasks()


async def send_notification():
    """
    фнкция для отправки оповещений
    """
    current_time = datetime.now()
    reminder_time = current_time + timedelta(hours=1)
    sessions_to_remind = await SessionRecordCrud().get_sessions_before_time(reminder_time.time())
    bot = TeleBot(BotConfig.TOKEN)
    for session_record in sessions_to_remind:
        user = session_record.user
        session = session_record.session

        massage = (f'Здравствуйте, {user.name}!\n'
                   f'Напоминаем, что вы записаны на {session.title}, которое продет в {session.time}\n'
                   f'Ждем вас! ☺')

        bot.send_message(user.tg_id, massage)


@app.task
def send_notification_task():
    """
    Запуск отправки оповещений
    """
    asyncio.run(send_notification())


app.conf.beat_schedule = {
    'alert-task': {
        'task': 'tasks.send_notification_task',
        'schedule': timedelta(hours=1),
    }
}

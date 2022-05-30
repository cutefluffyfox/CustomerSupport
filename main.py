import logging
import asyncio
from os import getenv
from datetime import datetime, timedelta
from random import randint
import pprint

import dotenv
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.types.chat_member_updated import ChatMemberUpdated

from TelegramBot import filters
from TelegramBot import generators


# Configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    # filename="logs.log"
)


# Initialize environment variables from .env file (if it exists)
dotenv.load_dotenv(dotenv.find_dotenv())
BOT_TOKEN = getenv('BOT_TOKEN')
CHANNEL_ID = getenv("CHANNEL_ID")


# Check that critical variables are defined
if BOT_TOKEN is None:
    logging.critical('No BOT_TOKEN variable found in project environment')


# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.my_chat_member_handler(filters.is_new_channel_member)
async def team_new_member(member: ChatMemberUpdated):
    channel_id = member.chat.id
    if member.new_chat_member.user.id == bot.id:
        message = await bot.send_message(
            channel_id,
            f"Hello, I am volunteer management bot! "
            f"To finish configuration please add environment variable:\n"
            f"`CHANNEL_ID={channel_id}`",
            parse_mode='Markdown'
        )
        await bot.edit_message_reply_markup(
            channel_id,
            message.message_id,
            reply_markup=generators.generate_inline_markup({"text": "Delete this message", "callback_data": f"deleteMessage"})
        )


@dp.callback_query_handler(lambda c: c.data.startswith('deleteMessage'))
async def delete_message(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id, message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

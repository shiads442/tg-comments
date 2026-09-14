import asyncio 
import json 
import logging 
from aiogram import Bot, Dispatcher, F, types 
from aiogram.filters import CommandStart, Command 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8996663854:AAEzmoG_iYHtwHZDipVEty1ByXl2f8BvNqo" 
ADMIN_ID = 5565425253 
WEB_APP_URL = "https://shiads442.github.io/tg-comments/" 
CHANNEL_USERNAME = "@shiads"

bot = Bot(token=BOT_TOKEN) 
dp = Dispatcher() 
reply_tracker = {}

@dp.message(CommandStart()) 
async def cmd_start(message: types.Message): 
    if message.from_user.id == ADMIN_ID: 
        await message.answer("Вітаю, адміне! Для публікації допису надішли: /post Текст допису") 
    else: 
        await message.answer("Привіт! Це бот для спілкування з автором каналу.")

@dp.message(Command("post"), F.from_user.id == ADMIN_ID) 
async def cmd_post(message: types.Message): 
    post_text = message.text.replace("/post", "", 1).strip() 
    if not post_text: 
        await message.answer("Вкажіть текст після команди /post") 
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Написати коментар (приватно)", 
            web_app=WebAppInfo(url=WEB_APP_URL)
        )
    ]
])

    try:
       await bot.send_message(chat_id=CHANNEL_USERNAME, text=post_text, reply_markup=keyboard)
       await message.answer("Допис успішно опубліковано в каналі!")
    except Exception as e:
       await message.answer(f"Помилка публікації: {e}")

@dp.message(F.web_app_data) 
async def handle_webapp_data(message: types.Message): 
    try: 
        data = json.loads(message.web_app_data.data) 
        comment_text = data.get("text", "") 
        user_name = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
    
        forwarded = await bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Новий приватний коментар від {user_name}:\n\n{comment_text}\n\nЩоб відповісти, скористайтеся Reply."
       )
        reply_tracker[forwarded.message_id] = message.from_user.id
        await message.answer("Ваш коментар надіслано!")
    except Exception as e:
        logging.error(f"Помилка: {e}")

@dp.message(F.chat.id == ADMIN_ID, F.reply_to_message) 
async def handle_admin_reply(message: types.Message): 
    target_msg_id = message.reply_to_message.message_id 
    if target_msg_id in reply_tracker: 
        user_id = reply_tracker[target_msg_id] 
        try: 
            await bot.send_message(chat_id=user_id, text=f"Відповідь від автора каналу:\n\n{message.text}") 
            await message.answer("Відповідь надіслано користувачу!") 
        except Exception as e:
            await message.answer(f"Помилка надсилання: {e}")

async def main(): 
    logging.basicConfig(level=logging.INFO) 
    print("БОТ УСПІШНО ЗАПУЩЕНИЙ!") 
    await dp.start_polling(bot)

if __name__=="__main__": 
    asyncio.run(main())

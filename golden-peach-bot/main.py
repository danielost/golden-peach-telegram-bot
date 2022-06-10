import requests
from datetime import datetime
import locale
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from config import TOKEN

locale.setlocale(locale.LC_ALL, '')
bot = Bot(TOKEN)
dp = Dispatcher(bot)

inline_spot_kb = InlineKeyboardMarkup(row_width=3).insert(InlineKeyboardButton(text='USD', callback_data='usd')).insert(
    InlineKeyboardButton(text='BTC', callback_data='btc')) \
    .insert(InlineKeyboardButton(text='ETH', callback_data='eth'))

inline_usd_kb = InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text='BTC', callback_data='btc_usd')). \
    insert(InlineKeyboardButton(text='ETH', callback_data='eth_usd')). \
    insert(InlineKeyboardButton(text='XRP', callback_data='xrp_usd')). \
    insert(InlineKeyboardButton(text='DOGE', callback_data='doge_usd')). \
    add(InlineKeyboardButton(text='Show all', callback_data='show_all_usd')). \
    add(InlineKeyboardButton(text='🔙 Back to menu', callback_data='back_to_menu'))

inline_btc_kb = InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text='ETH', callback_data='eth_btc')). \
    insert(InlineKeyboardButton(text='LTC', callback_data='ltc_btc')). \
    insert(InlineKeyboardButton(text='XRP', callback_data='xrp_btc')). \
    insert(InlineKeyboardButton(text='DOGE', callback_data='doge_btc')). \
    add(InlineKeyboardButton(text='Show all', callback_data='show_all_btc')). \
    add(InlineKeyboardButton(text='🔙 Back to menu', callback_data='back_to_menu'))

inline_eth_kb = InlineKeyboardMarkup(row_width=2).insert(InlineKeyboardButton(text='BTC', callback_data='btc_eth')). \
    insert(InlineKeyboardButton(text='XRP', callback_data='xrp_eth')). \
    insert(InlineKeyboardButton(text='DOGE', callback_data='doge_eth')). \
    insert(InlineKeyboardButton(text='LTC', callback_data='ltc_eth')). \
    add(InlineKeyboardButton(text='🔙 Back to menu', callback_data='back_to_menu'))

inline_back_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='🔙 Back to menu', callback_data='back_to_menu'))

static_kb = ReplyKeyboardMarkup(resize_keyboard=True)
static_kb.insert(KeyboardButton(text='🏠 Menu'))


def on_start():
    print('Bot is Online')


@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           '*Hello there!* 👋\n\nThis bot was designed to give you info about all the cryptocurrencies you need.\n\n'
                           'To start using *CryptoAssist* type /menu or hit the corresponding button on the keyboard.' \
                           , parse_mode='Markdown', reply_markup=static_kb)


@dp.message_handler(commands=['menu'])
async def load_menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Welcome to *CryptoAssist* menu!',
                           parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, 'Select one of the markets below. 👇',
                           parse_mode='Markdown', reply_markup=inline_spot_kb)


@dp.callback_query_handler(text='usd')
async def usd_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("You have picked *USD*, nice!\nNow let's pick a crypto.", parse_mode='Markdown')
    await callback.message.edit_reply_markup(reply_markup=inline_usd_kb)


@dp.callback_query_handler(text='btc')
async def btc_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("You have picked *BTC*, nice!\nNow let's pick a crypto.", parse_mode='Markdown')
    await callback.message.edit_reply_markup(reply_markup=inline_btc_kb)


@dp.callback_query_handler(text='eth')
async def eth_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("You have picked *ETH*, nice!\nNow let's pick a crypto.", parse_mode='Markdown')
    await callback.message.edit_reply_markup(reply_markup=inline_eth_kb)


@dp.callback_query_handler(text='back_to_menu')
async def back_to_menu_command(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Select one of the markets below. 👇')
    await callback.message.edit_reply_markup(reply_markup=inline_spot_kb)


@dp.callback_query_handler(Text(startswith='show_all_'))
async def show_all_handler(callback: types.CallbackQuery):
    curr = callback.data.split('_')[2]
    arr = []
    if curr == 'usd':
        arr = ['btc', 'eth', 'xrp', 'doge']
    if curr == 'btc':
        arr = ['eth', 'ltc', 'xrp', 'doge']
    if curr == 'eth':
        arr = ['btc', 'xrp', 'doge', 'ltc']
    res = ''
    for i in arr:
        res += get_data(f'{i}_{curr}') + '\n\n'
    await callback.answer()
    await callback.message.edit_text(res, parse_mode='Markdown')
    await bot.send_message(callback.message.chat.id, 'You can now go back to */menu* and select another crypto.',
                           parse_mode='Markdown', reply_markup=static_kb)


@dp.callback_query_handler(Text(endswith='_usd'))
async def usd_query_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(get_data(callback.data), parse_mode='Markdown')
    await bot.send_message(callback.message.chat.id, 'You can now go back to */menu* and select another crypto.',
                           parse_mode='Markdown', reply_markup=static_kb)


@dp.callback_query_handler(Text(endswith='_btc'))
async def btc_query_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(get_data(callback.data), parse_mode='Markdown')
    await bot.send_message(callback.message.chat.id, 'You can now go back to */menu* and select another crypto.',
                           parse_mode='Markdown', reply_markup=static_kb)


@dp.callback_query_handler(Text(endswith='_eth'))
async def eth_query_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(get_data(callback.data), parse_mode='Markdown')
    await bot.send_message(callback.message.chat.id, 'You can now go back to */menu* and select another crypto.',
                           parse_mode='Markdown', reply_markup=static_kb)


@dp.message_handler()
async def echo(message: types.Message):
    if message.text == '🏠 Menu':
        await bot.send_message(message.from_user.id, 'Welcome to *CryptoAssist* menu!',
                               parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id,
                               'Select one of the markets below. 👇',
                               parse_mode='Markdown', reply_markup=inline_spot_kb)
    else:
        await bot.send_message(message.from_user.id, "I don't understand you, bruh.\nType */help*.",
                               parse_mode='Markdown')


def get_data(values):
    req_str = 'https://yobit.net/api/3/ticker/' + values
    req = requests.get(req_str)
    response = req.json()
    sell_price = response[f'{values}']['sell']
    return f'*{datetime.now().strftime("%Y-%m-%d %H:%M")}*\nSell *{values.split("_")[0].upper()}/{values.split("_")[1].upper()}* price is {locale.currency(sell_price, grouping=True)}'


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_start(), skip_updates=True)

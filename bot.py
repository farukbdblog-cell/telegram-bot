import random
import telebot
from telebot import types

# আপনার টেলিগ্রাম বট টোকেন বসানো হলো
TOKEN = '8914296091:AAHJCXIifwEx_GaT8Ey9kEBPg7iLkCVDCVY'
bot = telebot.TeleBot(TOKEN)

# ব্যবহারকারীর ব্যালেন্স সংরক্ষণের জন্য ডিকশনারি
user_balances = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  btn1 = types.KeyboardButton('কাজ ▶')
  btn2 = types.KeyboardButton('ব্যালেন্স')
  btn3 = types.KeyboardButton('উত্তোলন 💳')
  btn4 = types.KeyboardButton('রেফার 👥')
  markup.add(btn1, btn2, btn3, btn4)

  bot.send_message(
      message.chat.id,
      'আসসালামু আলাইকুম! ইনকাম বটে আপনাকে স্বাগতম। নিচে থেকে অপশন বেছে নিন:',
      reply_markup=markup,
  )


@bot.message_handler(func=lambda message: message.text == 'কাজ ▶')
def task_menu(message):
  markup = types.InlineKeyboardMarkup(row_width=1)
  btn_fb = types.InlineKeyboardButton('Facebook কাজ', callback_data='task_fb')
  btn_gmail = types.InlineKeyboardButton('Gmail কাজ', callback_data='task_gmail')
  btn_insta = types.InlineKeyboardButton(
      'Instagram কাজ', callback_data='task_insta'
  )
  markup.add(btn_fb, btn_gmail, btn_insta)

  bot.send_message(
      message.chat.id,
      'দয়া করে নিচের যেকোনো একটি কাজের ক্যাটাগরি সিলেক্ট করুন:',
      reply_markup=markup,
  )


@bot.callback_query_handler(func=lambda call: call.data.startswith('task_'))
def handle_task(call):
  chat_id = call.message.chat.id

  if call.data == 'task_fb':
    first_names = ['Tanvir', 'Rahim', 'Karim', 'Hasan', 'Rakib', 'Jubayer']
    last_names = ['Ahmed', 'Chowdhury', 'Khan', 'Sarker', 'Mahmud', 'Talukdar']
    gen_name = f'{random.choice(first_names)} {random.choice(last_names)}'
    gen_pass = f'Pass{random.randint(1000,9999)}!'

    text = (
        f'📌 **Facebook Task Details**\n\nএই নাম দিয়ে একটি নতুন অ্যাকাউন্ট'
        f' খুলুন:\n👤 নাম: `{gen_name}`\n🔑 পাসওয়ার্ড:'
        f' `{gen_pass}`\n\nঅ্যাকাউন্ট তৈরি করার পর প্রোফাইল লিংক বা স্ক্রিনশট'
        f' এখানে পাঠান।'
    )
    bot.send_message(chat_id, text, parse_mode='Markdown')

  elif call.data == 'task_gmail':
    random_num = random.randint(10000, 99999)
    gen_email = f'user{random_num}bdt@gmail.com'

    text = (
        f'📌 **Gmail Task Details**\n\nএই ইমেইল দিয়ে জিমেইল অ্যাকাউন্ট খুলুন:\n📧'
        f' ইমেইল: `{gen_email}`\n\nখোলা শেষ হলে কনফার্মেশন স্ক্রিনশট পাঠান।'
    )
    bot.send_message(chat_id, text, parse_mode='Markdown')

  elif call.data == 'task_insta':
    bot.send_message(
        chat_id, 'ইনস্টাগ্রাম কাজের সার্ভার বর্তমানে ব্যস্ত আছে। পরে চেষ্টা করুন।'
    )


@bot.message_handler(func=lambda message: message.text == 'ব্যালেন্স')
def check_balance(message):
  uid = message.from_user.id
  balance = user_balances.get(uid, 0.00)
  text = (
      f'💰 **আপনার একাউন্ট তথ্য:**\n\nবাজেট/ব্যালেন্স: {balance} BDT\nপেন্ডিং'
      f' পেমেন্ট: 0.00 BDT\nমোট ইনকাম: {balance} BDT'
  )
  bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == 'উত্তোলন 💳')
def withdraw_money(message):
  bot.send_message(
      message.chat.id,
      'আপনার পর্যাপ্ত ব্যালেন্স নেই। ন্যূনতম ৫০ টাকা হলে উত্তোলন করতে পারবেন।',
  )


@bot.message_handler(func=lambda message: message.text == 'রেফার 👥')
def refer_link(message):
  bot_username = bot.get_me().username
  ref_link = f'https://t.me/{bot_username}?start={message.from_user.id}'
  bot.send_message(
      message.chat.id,
      f'🔗 আপনার রেফারেল লিংক:\n{ref_link}\n\nপ্রতি রেফারে ৫ টাকা করে পাবেন!',
  )


print('Bot is running...')
bot.remove_webhook()
bot.infinity_polling()

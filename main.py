import telebot

TOKEN = "8793984903:AAHUVkMtjHun96NbQEBjdnLhQqSdSI9O2KI"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7757026734  # apna telegram id

users = set()

# 🔹 CODE FILE SE CODE LENA
def get_code():
    with open("codes.txt", "r") as f:
        lines = f.readlines()

    if len(lines) == 0:
        return None

    code = lines[0].strip()

    with open("codes.txt", "w") as f:
        f.writelines(lines[1:])

    return code

# 🔹 START
@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.from_user.id)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Buy Code")

    bot.send_message(
        message.chat.id,
        "🔥 Welcome!\n\nBuy premium code for ₹10",
        reply_markup=markup
    )

# 🔹 BUY BUTTON
@bot.message_handler(func=lambda m: m.text == "💰 Buy Code")
def buy(message):
    bot.send_message(
        message.chat.id,
        "💸 Price: ₹10\n\n📲 UPI: aryanpvt@ptyes\n\nAfter payment send screenshot here"
    )

# 🔹 SCREENSHOT HANDLE
@bot.message_handler(content_types=['photo'])
def screenshot(message):
    user_id = message.from_user.id

    # admin ko forward karega
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

    bot.send_message(message.chat.id, "⏳ Waiting for admin approval")

# 🔹 APPROVE COMMAND
@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        reply = message.reply_to_message
        user_id = reply.forward_from.id

        code = get_code()

        if code is None:
            bot.send_message(message.chat.id, "❌ No codes left")
            return

        bot.send_message(
            user_id,
            f"✅ Payment Verified!\n\n🎁 Your Code:\n{code}"
        )

        bot.send_message(message.chat.id, "✅ Code sent")

    except:
        bot.send_message(message.chat.id, "❌ Reply to screenshot")

# 🔹 REJECT COMMAND
@bot.message_handler(commands=['reject'])
def reject(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        reply = message.reply_to_message
        user_id = reply.forward_from.id

        bot.send_message(user_id, "❌ Payment rejected")
        bot.send_message(message.chat.id, "❌ Rejected")

    except:
        bot.send_message(message.chat.id, "❌ Error")

bot.infinity_polling()

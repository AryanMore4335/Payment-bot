import telebot

TOKEN = "8793984903:AAHUVkMtjHun96NbQEBjdnLhQqSdSI9O2KI"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7757026734  # apna telegram id

# 🔹 START
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Buy Access")

    bot.send_message(
        message.chat.id,
        "👋 Welcome!\n\n💸 Get Private Channel Access for ₹350\n\nClick below 👇",
        reply_markup=markup
    )

# 🔹 BUY BUTTON
@bot.message_handler(func=lambda m: m.text == "💰 Buy Access")
def buy(message):
    bot.send_message(
        message.chat.id,
        "💳 Send ₹350 to UPI:\n\n aryanpvt@ptyes\n\n📸 Then send payment screenshot here."
    )

# 🔹 SCREENSHOT HANDLE
@bot.message_handler(content_types=['photo'])
def handle_ss(message):
    user_id = message.from_user.id

    bot.reply_to(message, "✅ Screenshot received!\nWait for admin approval.")

    # admin ko forward
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

    bot.send_message(
        ADMIN_ID,
        f"💰 New Payment!\nUser ID: {user_id}\n\nApprove: /approve {user_id}\nReject: /reject {user_id}"
    )

# 🔹 APPROVE (INVITE LINK)
@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split()[1])

        invite_link = "https://t.me/+-Z29dVq3I0plOWU1"  # 👈 yaha apna invite link daal

        bot.send_message(
            user_id,
            f"🎉 Payment Approved!\n\n🔒 Your Private Access Link 👇\n{invite_link}\n\n⚠️ Join fast, link limited use ho sakta hai"
        )

        bot.reply_to(message, "✅ Approved + Link Sent")

    except:
        bot.reply_to(message, "❌ Use: /approve user_id")

# 🔹 REJECT
@bot.message_handler(commands=['reject'])
def reject(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split()[1])

        bot.send_message(
            user_id,
            "❌ Payment Rejected!\nSend correct screenshot."
        )

        bot.reply_to(message, "❌ Rejected")

    except:
        bot.reply_to(message, "❌ Use: /reject user_id")

print("Bot running...")
bot.infinity_polling()

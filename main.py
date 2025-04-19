from telebot import TeleBot, types

TOKEN = '7716929303:AAGRQI0cp7hHwsFBTJ9UAEM6UEsSeMEOEgI' 
bot = TeleBot(TOKEN)

current_state = {}

@bot.message_handler(commands=['start'])
def send_options(message): 
    """Send a welcome message and ask for phone number."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    phone_button = types.KeyboardButton("📞 Telefon raqamingizni yuboring", request_contact=True)
    markup.add(phone_button)
    bot.send_message(
        chat_id=message.chat.id,
        text="Iltimos, telefon raqamingizni yuboring:",
        reply_markup=markup
    )

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    """Handle the contact information sent by the user."""
    phone_number = message.contact.phone_number
    bot.send_message(chat_id=message.chat.id, text=f"Sizning telefon raqamingiz: {phone_number}")
    send_main_options(message)

def send_main_options(message):
    """Send main options after receiving the phone number."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton("🛒 Buyurtma berish"),
        types.KeyboardButton("🛍 Buyurtmalarim"),
        types.KeyboardButton("✍️ Fikr bildirish"),
        types.KeyboardButton("⚙️ Sozlamalar")
    ]
    markup.add(*buttons)
    bot.send_message(
        chat_id=message.chat.id,
        text="Quyidagilardan birini tanlang:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "🛒 Buyurtma berish")
def order_options(message):
    """Send order image and ask for item selection."""
    with open("menyu.jpg", "rb") as img:
        bot.send_photo(message.chat.id, img, caption='Iltimos, buyurtma berish uchun biror mahsulot nomini yozing:')
    
    # Set the current state to "ordering"
    current_state[message.chat.id] = "ordering"
    bot.register_next_step_handler(message, handle_item_selection)

def handle_item_selection(message):
    """Handle the item selection and ask for location."""
    if message.chat.id in current_state and current_state[message.chat.id] == "ordering":
        if message.text == "🔙 Orqaga":
            send_main_options(message)
            del current_state[message.chat.id]  
            return

        item_name = message.text
        bot.send_message(chat_id=message.chat.id, text=f"Siz tanlagan mahsulot: {item_name}. Iltimos, geo-joylashuvni yuboring:", 
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
                             types.KeyboardButton("📍 Geo-joylashuvni yuborish", request_location=True),
                             types.KeyboardButton("🔙 Orqaga")
                         ))

@bot.message_handler(func=lambda message: True)
def handle_options(message):
    """Handle user responses from the menu."""
    if message.text == "🛍 Buyurtmalarim":
        bot.send_message(chat_id=message.chat.id, text="Hozircha savatingiz bo'sh")
    elif message.text == "✍️ Fikr bildirish":
        bot.send_message(chat_id=message.chat.id, text="Fikr bildirish uchun xabar yuboring.")
    elif message.text == "⚙️ Sozlamalar":
        bot.send_message(chat_id=message.chat.id, text="Sozlamalar bo'limida hozircha hech qanday o'zgarishlar yoki yangiliklar yo'q")
    elif message.text == "🔙 Orqaga":
        send_main_options(message)  
    else:
        bot.send_message(chat_id=message.chat.id, text="Bizga yuborgan javobingiz uchun raxmat")

if __name__ == "__main__":
    bot.polling()

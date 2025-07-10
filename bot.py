import telebot

# CONFIGURATION (REPLACE THESE VALUES)
BOT_TOKEN = "7704980511:AAHz4MbwofG1Bnna6ZOvkpMYbdT72YF4uBI"
CHANNEL_USERNAME = "@YourChannel"  # e.g., "@SolanaAirdropOfficial"
GROUP_USERNAME = "@YourGroup"      # e.g., "@SolanaCommunity"
TWITTER_USERNAME = "@YourTwitter"  # e.g., "@SolanaAirdrops"

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Store user states (track if they submitted wallet)
user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    welcome_text = f"""
🌟 *Welcome to the SOL Airdrop Bot!* 🌟

To qualify for 10 SOL:
1️⃣ Join our channel: {CHANNEL_USERNAME}
2️⃣ Join our group: {GROUP_USERNAME}
3️⃣ Follow our Twitter: {TWITTER_USERNAME}

*Click the button below when done* 👇
    """
    
    # Create inline keyboard with "Done" button
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("✅ I've Joined Everything", callback_data="joined"))
    
    bot.send_message(
        user_id,
        welcome_text,
        parse_mode="Markdown",
        reply_markup=markup
    )
    user_states[user_id] = {"joined": False}

@bot.callback_query_handler(func=lambda call: call.data == "joined")
def ask_for_wallet(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id, "Almost there! Now send your Solana wallet address.")
    bot.send_message(user_id, "📥 *Send your Solana wallet address:*\n(e.g., `Hx5...zF7`)", parse_mode="Markdown")
    user_states[user_id]["joined"] = True

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get("joined") is True)
def confirm_airdrop(message):
    user_id = message.from_user.id
    solana_wallet = message.text.strip()
    
    # Simulate wallet validation (basic check)
    if len(solana_wallet) < 10 or not solana_wallet.startswith(("H", "S")):
        bot.send_message(user_id, "⚠️ Invalid wallet format! Try again.")
        return
    
    # Send congratulations
    bot.reply_to(
        message,
        f"🎉 *Congratulations!* 🎉\n"
        f"10 SOL is on its way to:\n`{solana_wallet}`\n\n"
        "⚠️ *Note:* Transactions may take 24-48 hours.",
        parse_mode="Markdown"
    )
    
    # Reset user state
    user_states[user_id]["joined"] = False

if __name__ == "__main__":
    print("Airdrop bot is running...")
    bot.infinity_polling()

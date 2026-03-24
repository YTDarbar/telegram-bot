from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes,
    CommandHandler,
    ChatMemberHandler
)

BOT_TOKEN = "8752598253:AAHdmo7mM0vmr2K8_7kpImBONg9Fh5XsuBE"
ADMIN_ID = 5165392099

users = set()
welcome_msg = "🔥 Welcome bhai! Aap group me join ho gaye 💯"
farewell_msg = "👋 Bye bhai!"

# ✅ Auto approve
async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request

    await context.bot.approve_chat_join_request(
        chat_id=request.chat.id,
        user_id=request.from_user.id
    )

    try:
        await context.bot.send_message(
            chat_id=request.from_user.id,
            text=welcome_msg
        )
        users.add(request.from_user.id)
    except:
        pass


# ✅ Farewell (safe)
async def farewell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.chat_member

    if member.new_chat_member.status in ["left", "kicked"]:
        try:
            await context.bot.send_message(
                chat_id=member.chat.id,
                text=farewell_msg
            )
        except:
            pass


# ✅ Broadcast
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        return

    msg = " ".join(context.args)

    for user in users:
        try:
            await context.bot.send_message(chat_id=user, text=msg)
        except:
            pass

    await update.message.reply_text("✅ Message sent!")


# 🚀 Run
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(ChatJoinRequestHandler(auto_approve))
app.add_handler(ChatMemberHandler(farewell, ChatMemberHandler.CHAT_MEMBER))
app.add_handler(CommandHandler("broadcast", broadcast))

print("Bot running 🚀")
app.run_polling()

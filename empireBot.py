import logging
import asyncio
import os
import sys
from datetime import datetime
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.error import TimedOut
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from empire_script import send_reg_request, verify_otp
from basic_func import count_campaign_code_accounts, count_user_accounts, total_registerations, generate_random_string, match_data

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Admins and limits
admins = [910898489, 7198456206]
is_registeration_allowed = True
daily_registration_limit = 5
daily_registration_count = 0
last_reset_date = datetime.now().date()
campaign_code = 'jayesh777'

commands = [KeyboardButton(text="/getregistercount"), KeyboardButton(text="/setlimit"), KeyboardButton(text="/getdata")]

# Keyboards
keyboard = [[KeyboardButton(text="/register"),KeyboardButton(text='/setcampaign_code')],commands,[KeyboardButton(text="/totalregistercount"),KeyboardButton(text='/match')], [KeyboardButton(text="/getpayment_token"),KeyboardButton(text='/getcampaign_codecount')],[KeyboardButton(text="/stop"),KeyboardButton(text='/startregisteration')]]
resend_keyboard = ReplyKeyboardMarkup([[KeyboardButton(text="resend")]], one_time_keyboard=True, resize_keyboard=True)

async def reset_daily_count():
    global daily_registration_count, last_reset_date
    while True:
        if datetime.now().date() > last_reset_date:
            daily_registration_count = 0
            last_reset_date = datetime.now().date()
            logger.info("Daily registration count reset.")
        await asyncio.sleep(86400)

async def set_campaign_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in admins:
        await update.message.reply_text("You do not have permission to set the campaign_code.")
        return
    try:
        global campaign_code
        campaign_code = context.args[0]
        await update.message.reply_text(f"campaign_code set to {campaign_code}.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /setcampaign_code <number>")

async def set_limit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global daily_registration_limit
    if update.effective_user.id not in admins:
        await update.message.reply_text("You do not have permission to set the limit.")
        return
    try:
        new_limit = int(context.args[0])
        if new_limit > 0:
            daily_registration_limit = new_limit
            await update.message.reply_text(f"Daily registration limit set to {new_limit}.")
        else:
            raise ValueError("Invalid limit.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /setlimit <number>")

async def getdata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in admins:
        await update.message.reply_text("You do not have permission to access this data.")
        return
    chat_id = update.message.chat_id
    today_date = None
    if len(context.args) > 0:
        today_date = context.args[0]
    else:
        today_date = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(os.path.dirname(__file__), '..', f'empirexch_{today_date}.csv')
    if os.path.exists(file_path):
        await context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
    else:
        await update.message.reply_text("The file empirexch.csv does not exists for today.")

async def totalregistercount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in admins:
        await update.message.reply_text("You do not have permission to access this data.")
        return
    total_count = await total_registerations('empirexch',date=context.args[0] if len(context.args) > 0 else None)
    await update.message.reply_text(f"Total registrations: {total_count}")    

async def getregistercount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in admins:
        count, user_id = await count_user_accounts('empirexch', user_id=update.effective_user.id, date=context.args[0] if len(context.args) > 0 else None)
        await update.message.reply_text(f"Your total registrations: {count}")
        return
    user_id = None

    if len(context.args) > 0:
        user_id = context.args[0]
    else:
        await update.message.reply_text("Usage: /getregistercount <user_id>")
        return
    count, UserId = await count_user_accounts('empirexch',user_id=user_id, date=context.args[1] if len(context.args) > 1 else None)
    await update.message.reply_text(f"Total registrations: {count}\n from user ID: {UserId}")

async def getpaymenttoken(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = await generate_random_string()
    await update.message.reply_text("Your payment token is:")
    await update.message.reply_text(token)
    for admin_id in admins:
        count, UserId = await count_user_accounts('empirexch', user_id=update.effective_user.id, date=context.args[0] if len(context.args) > 0 else None)
        await context.bot.send_message(chat_id=admin_id, text=f"User with User ID : {update.effective_user.id} has generated a payment token: {token} \n Total registrations: {count}\n from user ID: {UserId}")
    
async def match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 2:
        try:
            await update.message.reply_text(await match_data(context.args[0], context.args[1]))
        except:
            await update.message.reply_text("Error occurred. Try again.")
    else:
        await update.message.reply_text("Usage: /match <data1> <data2>")


@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=2, max=10), retry=retry_if_exception_type(TimedOut))
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Welcome to the bot!',
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    if update.effective_user.id in admins:
        await update.message.reply_text(f"Current daily registration limit: {daily_registration_limit}")

@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=2, max=10), retry=retry_if_exception_type(TimedOut))
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_registeration_allowed:
        await update.message.reply_text("Registration is stopped.")
        return
    global daily_registration_count, daily_registration_limit
    if daily_registration_count >= daily_registration_limit:
        await update.message.reply_text("Daily registration limit reached. Try again tomorrow.")
        return
    await update.message.reply_text('Enter your mobile number:')
    context.user_data['awaiting_phone'] = True

async def get_campaign_code_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in admins:
        await update.message.reply_text("You do not have permission to access this data.")
        return
    campaign_code = context.args[0] if len(context.args) > 0 else None
    if not campaign_code:
        await update.message.reply_text("Usage: /getcampaign_codecount <campaign_code>")
        return
    count, campaign_code = await count_campaign_code_accounts('empirexch',campaign_code, date=context.args[1] if len(context.args) > 1 else None)
    await update.message.reply_text(f"Total registrations: {count}\n with campaign_code: {campaign_code}")


@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=2, max=10), retry=retry_if_exception_type(TimedOut))
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if daily_registration_count >= daily_registration_limit:
        await update.message.reply_text("Daily registration limit reached. Try again tomorrow.")
        return
    if not is_registeration_allowed:
        await update.message.reply_text("Registration is stopped.")
        return
    try:
        text = update.message.text
        if text == 'resend':
            asyncio.create_task(confirm_handler(update, context))
            return
        elif text.isdigit() and len(text) == 10:
            context.user_data['phone'] = text
            await update.message.reply_text(f"Phone number: {text}\nSending OTP...")
            context.user_data['awaiting_otp'] = True
            asyncio.create_task(confirm_handler(update, context))
        elif context.user_data.get('awaiting_otp'):
            asyncio.create_task(verify_user_otp(update, context, text))
        else:
            await update.message.reply_text("Invalid input. Enter a valid 10-digit phone number.")
    except TimedOut:
        print("Timeout occurred while handling a message. Retrying...")
        asyncio.create_task(handle_message(update, context))

async def verify_user_otp(update, context, otp):
    context.user_data['awaiting_otp'] = False
    verified = await verify_otp(session=context.user_data['session'], phone_number=context.user_data['phone'], otp=otp, user_id=update.effective_user.id)
    if verified.get('success'):
        await update.message.reply_text("Registration successful!")
        global daily_registration_count
        daily_registration_count += 1
        context.user_data.clear()
    else:
        await update.message.reply_text(verified.get('error'))
        context.user_data['awaiting_otp'] = True

async def confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = context.user_data['phone']
    try:
        response, session = await send_reg_request(phone_number=phone)
        context.user_data.update({'session': session})
        if response.get('success'):
            await update.message.reply_text('OTP sent successfully')
        else :
            await update.message.reply_text(response.get('error'))
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Error occurred. Try again.")

async def stop_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in admins:
        await update.message.reply_text("You do not have permission to stop the registration.")
        return
    global is_registeration_allowed
    is_registeration_allowed = False
    await update.message.reply_text("Registration stopped.")

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in admins:
        await update.message.reply_text("You do not have permission to start the registration.")
        return
    global is_registeration_allowed
    is_registeration_allowed = True
    await update.message.reply_text("Registration started successfully.")

# Main function
def main() -> None:
    app = ApplicationBuilder().token("BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(confirm_handler, pattern="^edit$"))
    app.add_handler(CommandHandler("setlimit", set_limit))
    app.add_handler(CommandHandler('getdata',getdata))
    app.add_handler(CommandHandler('totalregistercount',totalregistercount))
    app.add_handler(CommandHandler('getregistercount',getregistercount))
    app.add_handler(CommandHandler('getpayment_token',getpaymenttoken))
    app.add_handler(CommandHandler('match',match))
    app.add_handler(CommandHandler('setcampaign_code',set_campaign_code))
    app.add_handler(CommandHandler('getcampaign_codecount',get_campaign_code_count))
    app.add_handler(CommandHandler('stop',stop_registration))
    app.add_handler(CommandHandler('startregisteration',start_registration))
    asyncio.get_event_loop().create_task(reset_daily_count())
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

import os
import subprocess
import time
import telegram
from binance.client import Client
from telegram.ext import *
import cmc
import fearindex

telegram_api = "your-api"  # Replace this with your telegram bot api
client = Client("", "")
bot = telegram.Bot(token=telegram_api)
os.chdir("../telegram_bot")  # Changing the directory to the `telegram_bot` folder


def start_command(update, context):
    update.message.reply_text("For more info about bot: https://github.com/arabacibahadir/sup-res#readme ")


def help_command(update, context):
    update.message.reply_text("Commands")


def handle_message(update, context):
    text = str(update.message.text).lower()
    r_text = responses(text)
    update.message.reply_text(r_text)


def responses(input_text):
    user_message = str(input_text).lower()
    chat_id = bot.get_updates()[-1].message.chat_id

    if user_message == "commands":
        return "supres 'pair' 'timeframe', major coins, fear index, info, news, test"

    if user_message == "test":
        return "Bot is working."

    if user_message == "major coins":
        widget_list = ("BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "LUNAUSDT", "AVAXUSDT")
        majors = []
        perf = time.perf_counter()
        for w in widget_list:
            values = list(client.get_symbol_ticker(symbol=w).values())
            majors.extend([values[0].removesuffix('USDT'), values[1].rstrip('0')])
        print(f"Completed execution in {time.perf_counter() - perf} seconds")
        return f"{majors[0]}:{majors[1]}, {majors[2]}:{majors[3]}, {majors[4]}:{majors[5]}, " \
               f"{majors[6]}:{majors[7]}, {majors[8]}:{majors[9]}, {majors[10]}:{majors[11]}"

    if user_message == "fear index":
        return bot.send_message(chat_id=chat_id, text=fearindex.fear())

    if user_message == "info":
        return bot.send_message(chat_id=chat_id, text=cmc.market())

    if user_message.startswith("news"):
        return bot.send_message(chat_id=chat_id, text=cmc.news())

    msg = user_message.split(" ")
    tck = msg[1]
    tfr = msg[2]

    def remove_files():
        for x in os.listdir("../telegram_bot/"):
            if x == f"{tck.upper()}.jpeg":
                os.unlink(f"../telegram_bot/{tck.upper()}.jpeg")
            if x == f"{tck.upper()}.csv":
                os.unlink(f"../telegram_bot/{tck.upper()}.csv")
            if x == "output.txt":
                os.unlink("../telegram_bot/output.txt")

    if user_message.startswith("supres"):
        # Which python path you are using, if it is not working, change "python3" command -> "py, python"
        subprocess.run(f"python3 ../telegram_bot/telegram_bot.py {tck.upper()} {tfr.upper()}", cwd="../telegram_bot", shell=True)
        with open("../telegram_bot/output.txt", "r+") as f:
            content_list = f.readlines()
        content_list = [x.strip() for x in content_list]
        text = content_list[1] + "\n" + content_list[2] + "\n" + content_list[3] + "\n" + content_list[4]
        bot.send_document(chat_id=chat_id, document=open(content_list[0], 'rb'), caption=text)
        return remove_files()

    if user_message.startswith("alarm"):
        pass

    return "Error"


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(telegram_api, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("Start", start_command))
    dp.add_handler(CommandHandler("Help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message, pass_job_queue=True))
    dp.add_error_handler(error)
    updater.start_polling(1, timeout=10)
    updater.idle()


if __name__ == "__main__":
    print("Bot started.")
    main()

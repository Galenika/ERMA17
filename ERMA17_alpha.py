# some of them may be unused.

from asyncore import dispatcher
from telegram.ext import Updater, CommandHandler
import json
import requests
import urllib.parse, urllib3
import os
from etherscan.accounts import Account
from requests import get
import base64

address = "YOUR_WALLET_ADDRESS"
updater = Updater("YOUR_TELEGRAM_TOKEN")


# Alias Functions

def dispatcher(user_input, function_name):
    updater.idspatcher.add_handler(
        CommandHandler(user_input, function_name))  # @param x = string/user input in telegram chat, @param y = connected function


# Command/Dispatcher Functions

def start(bot, update):
    update.message.reply_text("Ayyyy lmao. Bot has started.")


def di(s):
    i = str(round(float(s), 4))
    return i


def get_balance(bot: object, update: object) -> object:
    line = ("    Wallet Balance 👛:\n" +
            "-------------------------" +
            "    \n" +
            "    Unpaid (ETH): {unpaid}\n".format(unpaid=walletBalance()[1]) +
            "    Paid 💰 (ETH): {balance}\n".format(balance=walletBalance()[0]) +
            "    \n" +
            "    ETH in 💱 (Coinmarketcap.com)\n" +
            "    \n" +
            "    Balance in 💶: {wallet_eur} @ {price_eur} 💶 \n".format(wallet_eur=walletBalanceInFiat()[0],
                                                                         price_eur=walletBalanceInFiat()[6]) +
            "    Balance in 💵: {wallet_usd} @ {price_usd} 💵\n".format(wallet_usd=walletBalanceInFiat()[1],
                                                                        price_usd=walletBalanceInFiat()[7]) +
            "\n  Balance in 🍕: {pizza}".format(pizza=di(str(float(walletBalanceInFiat()[0]) / 4.5)))) # my gf wants to know how much pizza we can buy with the money we made
    update.message.reply_text(line)
    return str(line)


def get_roi(bot, update):
    line = ("Return of Investment (ROI) 💱:\n" +
            "-------------------------" +
            "\n" +
            "    Days until the return of investment: {roi_days}\n".format(roi_days=str(roi()[0])) +
            "    Months until the return of investment: {roi_months}\n".format(roi_months=str(roi()[1])) +
            "    ")
    update.message.reply_text(line)
    return str(line)


def get_info(bot, update):
    calcHashrate, nano_balance, h1, h3, h6, h12, h24 = list(general_miner_intel())
    blockTime = str(eth_network_intel())

    line = ("    General info ℹ️\n" +
            "    -------------------------\n" +
            "    Current Hashrate: {chs} MHz\n".format(chs=calcHashrate) +
            "    \n" +
            "    Average Hashrate:\n" +
            "        1h: {hs1} MHz\n".format(hs1=h1) +
            "        3h: {hs3} MHz\n".format(hs3=h3) +
            "        6h: {hs6} MHz\n".format(hs6=h6) +
            "        12h: {hs12} MHz\n".format(hs12=h12) +
            "        24h: {hs24} MHz\n".format(hs24=h12) +
            "    \n" +
            "    Average Block Time: {bt} sec.\n".format(bt=blockTime) +
            "    Pool: nanopool"
            "    ")
    update.message.reply_text(line)
    return str(line)


def get_prognosis(bot, update):
    pply_minute, pply_hour, pply_day, pply_week, pply_month = list(estimated_earnings())

    line = ("    Estimated Earnings 💰💰💰\n" +
            "    -------------------------\n" +

            "        Minute: {hs1} 💵\n".format(hs1=pply_minute) +
            "        Hourly: {hs3} 💵\n".format(hs3=pply_hour) +
            "        Daily: {hs6} 💵\n".format(hs6=pply_day) +
            "        Weekly: {hs12} 💵\n".format(hs12=pply_week) +
            "        Monthly: {hs24} 💵\n".format(hs24=pply_month) +
            "    \n" +
            "(Based on the last 6h)")
    update.message.reply_text(line)
    return str(line)


def get_ip(bot, update):
    line = "Encrypted IP:\n" + \
           "    -------------------------\n" + \
           ip_crawl() # base64decode.org; TODO: AES-Encryption?
    update.message.reply_text(line)


def help(bot, update):
    line = """
    Commands:

    /prognosis - view estimated earnings
    /ip - view encrypted IP of your Rig, if the Bot is hosted on it.
    /roi - Return of investment
    /info - general infos, hasrates
    /balance - current wallet balance

    """

    update.message.reply_text(line)


def all(bot, update):
    get_balance(bot, update)
    get_prognosis(bot, update)
    get_info(bot, update)
    get_roi(bot, update)


# "Core" functions

def walletBalance():
    with open('escan_api/api_key.json', mode='r') as key_file:
        key = json.loads(key_file.read())['key']

    api = Account(address=address, api_key=key)
    balance = api.get_balance()
    eth_balance = float(balance) / (10 ** (18))
    unpaid_balance = requests.get("https://api.nanopool.org/v1/eth/balance/" + address).json()["data"]
    return di(eth_balance), di(unpaid_balance)


def walletBalanceInFiat():
    
    # Get current prices from coinmarketcap.com API

    eth = float(walletBalance()[0])
    main_api = "https://api.coinmarketcap.com/v1/ticker/"
    url = main_api + "ethereum/?convert=EUR"

    json_data = requests.get(url).json()

    json_price_eur = json_data[0]["price_eur"]
    json_price_usd = json_data[0]["price_usd"]

    change_1h = json_data[0]["percent_change_1h"]
    change_24h = json_data[0]["percent_change_24h"]
    change_7d = json_data[0]["percent_change_7d"]

    fiat_eur = str(float(json_price_eur) * eth)
    fiat_usd = str(float(json_price_usd) * eth)

    coin_url = "https://coinmarketcap.com/currencies/ethereum/"

    return di(fiat_eur), di(fiat_usd), di(change_1h), di(change_24h), di(change_7d), coin_url, di(json_price_eur), di(
        json_price_usd)


def general_miner_intel():
    # use General info
    # https://eth.nanopool.org/api#api-Miner-AccountInfo

    jd = requests.get("https://api.nanopool.org/v1/eth/user/" + address).json()

    calcHashrate = di(jd["data"]["hashrate"])
    nano_balance = di(jd["data"]["balance"])
    h1, h3, h6, h12, h24 = \
        di(jd["data"]["avgHashrate"]["h1"]), \
        di(jd["data"]["avgHashrate"]["h3"]), \
        di(jd["data"]["avgHashrate"]["h6"]), \
        di(jd["data"]["avgHashrate"]["h12"]), \
        di(jd["data"]["avgHashrate"]["h24"])

    return calcHashrate, nano_balance, h1, h3, h6, h12, h24


def eth_network_intel():
    # https://eth.nanopool.org/api#api-Network
    jd = requests.get("https://api.nanopool.org/v1/eth/network/avgblocktime").json()
    blockTime = str(round(float(jd["data"]), 3))
    return blockTime


def estimated_earnings():
    # https://eth.nanopool.org/api#api-Other
    # effective HR last 6h

    jd = requests.get(
        "https://api.nanopool.org/v1/eth/approximated_earnings/" + str(int(float(general_miner_intel()[0])))).json()

    pply_minute, pply_hour, pply_day, pply_week, pply_month = di(jd["data"]["minute"]["dollars"]), \
                                                              di(jd["data"]["hour"]["dollars"]), \
                                                              di(jd["data"]["day"]["dollars"]), \
                                                              di(jd["data"]["week"]["dollars"]), \
                                                              di(jd["data"]["month"]["dollars"])

    return pply_minute, pply_hour, pply_day, pply_week, pply_month


def roi():
    roi_eur_day = di((1980 - float(walletBalanceInFiat()[0])) / float(estimated_earnings()[2]))
    roi_eur_months = di(float(roi_eur_day) / 30)

    return roi_eur_day, roi_eur_months


def ip_crawl():
    ip = get('https://api.ipify.org').text
    data = str(base64.b64encode(ip.encode()))[2:-1]

    return data


# Menu


if __name__ == "__main__":
    os.system("cls") # for optical reasons. can be changed to "clear" on unix systems

    print("""
                         ___  ___ _   _   _     _  _  ___  _   ____
                        | __|| o \ \_/ | / \   | \| || o \/o| |__ /
                        | _| |   / \_/ || o |  |  \ ||  _/  | |  //
                        |___||_| \_| |_||_n_() |_|\_||_|    L | // 
    
    
                            Welcome to the ERMA.NP17 (ALPHA)!
                        Etherum Mining Rig App for nanopool.com, 2017
                                      Author: VAM
                              
                              
    """)

    print("     loading functions...")
    # Telegram function
    # try and except experimental, remove if it does not work.
    try:
        dispatcher("balance", get_balance)
        dispatcher("roi", get_roi)
        dispatcher("info", get_info)
        dispatcher("ip", get_ip)
        dispatcher("prognosis", get_prognosis)
        dispatcher("help", help)
        dispatcher("all", all)

        print("     done!")
        print("""
    
            ERMA17 is running and ready to use.
        """)

    except:
        print("Error: Something went wrong...")
        os.system("pause") # may edit on unix systems
    


# Basic Telegram Bot stuff, which is needed but I've no idea whats for.

updater.start_polling()
updater.idle()

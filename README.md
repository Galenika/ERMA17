# ERMA17
An open source telegram bot for monitoring ethereum mining on nanopool.com.

It is written for __Windows 10__, but can easily be modified for UNIX systems. Tested on Python 3.5.3.

### Getting Telegram Tokens and Etherscan.io API-Keys

In order to get this bot working, you will need a Bot token, which is instructed [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot) and an etherscan.io API-key, which is acquired by [registering](https://etherscan.io/register) at etherscan.io.


### Following dependencies need to be installed:
```
https://github.com/corpetty/py-etherscan-api -> stored in te py_ethio_api folder, in case you want to use my version.
python-telegram-bot
requests
urllib3
base64
```
Just install them with the ```install_dependencies.bat``` (experimental) script, or just use the ```pip``` installer. However, the python-etherscan.io api has to be installed according to the instructions found in the [original repository](https://github.com/corpetty/py-etherscan-api).

Make sure, you add your Adress, Telegram-Token (in ```ERMA17_alpha.py```) and Etherscan.io API-Key (in ```/escan_api/api_key.json```) to the program. 

### If you like this project, please consider a donation.

ETH: __0xd60d1604cc0DD2F49e830E95472502E06227eB55__

### If you have any questions, just message me on Github, or join our discord server:
https://discord.gg/6PwuaTq

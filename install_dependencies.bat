echo "This will install the needed dependencies - Make sure python 3.x and pip are installed. Continue?"
pause

pip install requests
pip install python-telegram-bot
pip install urllib3

echo "Installing Etherscan.io API (https://github.com/corpetty/py-etherscan-api) ..."

cd .\py_ethio_api\
python setup.py install

echo ""
echo ""
echo ""
echo "All done. Make sure, you add your Adress, Telegram-Token (in ERMA17_alpha.py) and Etherscan.io API-Key (in /escan_api/api_key.json) to the program."
pause
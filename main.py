import ccxt
from trading_bot import TradingBot
from trading_interface import TradingInterface
import threading

if __name__ == "__main__":
    exchange = ccxt.binance({
        'apiKey': 'TU_API_KEY',
        'secret': 'TU_API_SECRET',
        'enableRateLimit': True
    })

    bot = TradingBot('procesado_1h.csv', 'procesado_5m.csv')
    interface = TradingInterface(bot)

    bot_thread = threading.Thread(target=bot.run)
    bot_thread.daemon = True
    bot_thread.start()

    interface.initialize_ui()
    interface.run()
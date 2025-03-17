import pandas as pd
from trading_bot import TradingBot

# Cargar datos históricos
data_1h_path = 'procesado_1h.csv'
data_5m_path = 'procesado_5m.csv'

data_1h = pd.read_csv(data_1h_path)
data_5m = pd.read_csv(data_5m_path)

print("Datos 1H:")
print(data_1h.head())
print("Datos 5M:")
print(data_5m.head())

# Crear instancia del bot con los datos históricos
bot = TradingBot(data_1h_path, data_5m_path)

# Ejecutar el bot
signals = bot.run()

# Guardar las señales generadas en un archivo CSV
signals.to_csv('señales_generadas.csv', index=False)

# Mostrar las señales generadas
print("Señales generadas:")
print(signals)
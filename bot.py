import pandas as pd

class TradingStrategy:
    def __init__(self, data_1h, data_5m):
        self.data_1h = data_1h
        self.data_5m = data_5m
        self.key_levels = []
        print("Instancia de TradingStrategy creada.")

    def identify_key_levels(self):
        print("Identificando niveles clave en 1H...")
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                self.key_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                self.key_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        print("Niveles clave identificados:", self.key_levels)

    def confirm_levels_in_5m(self):
        print("Confirmando niveles en 5M...")
        confirmations = []
        for level in self.key_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'buy'))
        print("Confirmaciones en 5M:", confirmations)
        return confirmations

    def identify_polarity_levels(self):
        print("Identificando niveles de polaridad en 1H...")
        polarity_levels = []
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                polarity_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                polarity_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        print("Niveles de polaridad identificados:", polarity_levels)
        return polarity_levels

    def confirm_polarity_levels_in_5m(self, polarity_levels):
        print("Confirmando niveles de polaridad en 5M...")
        confirmations = []
        for level in polarity_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'buy'))
        print("Confirmaciones de polaridad en 5M:", confirmations)
        return confirmations

    def confirm_pullback(self, level):
        print("Confirmando pullback en 5M...")
        date, price, level_type = level
        for i in range(len(self.data_5m)):
            if self.data_5m['Date'][i] >= date:
                if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                    return (self.data_5m['Date'][i], price, 'pullback_sell')
                if level_type == 'support' and self.data_5m['High'][i] >= price:
                    return (self.data_5m['Date'][i], price, 'pullback_buy')
        return None

    def confirm_rank(self, level):
        print("Confirmando rank en 5M...")
        date, price, level_type = level
        for i in range(len(self.data_5m)):
            if self.data_5m['Date'][i] >= date:
                if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                    return (self.data_5m['Date'][i], price, 'rank_sell')
                if level_type == 'support' and self.data_5m['High'][i] >= price:
                    return (self.data_5m['Date'][i], price, 'rank_buy')
        return None

    def confirm_baston_c(self, level):
        print("Confirmando bastón C en 5M...")
        date, price, level_type = level
        for i in range(len(self.data_5m)):
            if self.data_5m['Date'][i] >= date:
                if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                    return (self.data_5m['Date'][i], price, 'baston_c_sell')
                if level_type == 'support' and self.data_5m['High'][i] >= price:
                    return (self.data_5m['Date'][i], price, 'baston_c_buy')
        return None

    def confirm_baston_r(self, level):
        print("Confirmando bastón R en 5M...")
        date, price, level_type = level
        for i in range(len(self.data_5m)):
            if self.data_5m['Date'][i] >= date:
                if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                    return (self.data_5m['Date'][i], price, 'baston_r_sell')
                if level_type == 'support' and self.data_5m['High'][i] >= price:
                    return (self.data_5m['Date'][i], price, 'baston_r_buy')
        return None

    def is_engulfing_candle(self, index):
        if index == 0:
            return False
        prev_candle = self.data_5m.iloc[index - 1]
        curr_candle = self.data_5m.iloc[index]
        if curr_candle['Close'] > curr_candle['Open'] and prev_candle['Close'] < prev_candle['Open']:
            return curr_candle['Close'] > prev_candle['Open'] and curr_candle['Open'] < prev_candle['Close']
        if curr_candle['Close'] < curr_candle['Open'] and prev_candle['Close'] > prev_candle['Open']:
            return curr_candle['Close'] < prev_candle['Open'] and curr_candle['Open'] > prev_candle['Close']
        return False

    def is_strong_candle(self, index):
        candle = self.data_5m.iloc[index]
        body_size = abs(candle['Close'] - candle['Open'])
        total_size = candle['High'] - candle['Low']
        return body_size >= 0.7 * total_size

    def confirm_trigger(self, level):
        print("Confirmando gatillo en 5M...")
        date, price, level_type = level
        for i in range(len(self.data_5m)):
            if self.data_5m['Date'][i] >= date:
                if self.is_engulfing_candle(i) or self.is_strong_candle(i):
                    if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                        return (self.data_5m['Date'][i], price, 'trigger_sell')
                    if level_type == 'support' and self.data_5m['High'][i] >= price:
                        return (self.data_5m['Date'][i], price, 'trigger_buy')
        return None

    def identify_breakout_levels(self):
        print("Identificando niveles de rompimiento en 1H...")
        breakout_levels = []
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                breakout_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                breakout_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        print("Niveles de rompimiento identificados:", breakout_levels)
        return breakout_levels

    def confirm_breakout_levels_in_5m(self, breakout_levels):
        print("Confirmando niveles de rompimiento en 5M...")
        confirmations = []
        for level in breakout_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'breakout_sell'))
                    if level_type == 'support' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'breakout_buy'))
        print("Confirmaciones de rompimiento en 5M:", confirmations)
        return confirmations

    def identify_double_scheme(self):
        print("Identificando esquema doble en 1H...")
        double_levels = []
        for i in range(2, len(self.data_1h) - 2):
            if self.data_1h['High'][i] == self.data_1h['High'][i-2] and self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                double_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] == self.data_1h['Low'][i-2] and self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                double_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        print("Esquema doble identificado:", double_levels)
        return double_levels

    def identify_failure_scheme(self):
        print("Identificando esquema de falla en 1H...")
        failure_levels = []
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                failure_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                failure_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        print("Esquema de falla identificado:", failure_levels)
        return failure_levels

    def identify_trap_scheme(self):
        print("Identificando esquema de trampa en 1H...")
        trap_levels = []
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                trap_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                trap_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        print("Esquema de trampa identificado:", trap_levels)
        return trap_levels

    def identify_continuation_scheme(self):
        print("Identificando esquema de continuación en 1H...")
        continuation_levels = []
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                continuation_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                continuation_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        print("Esquema de continuación identificado:", continuation_levels)
        return continuation_levels

    def confirm_double_scheme_in_5m(self, double_levels):
        print("Confirmando esquema doble en 5M...")
        confirmations = []
        for level in double_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'double_sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'double_buy'))
        print("Confirmaciones de esquema doble en 5M:", confirmations)
        return confirmations

    def confirm_failure_scheme_in_5m(self, failure_levels):
        print("Confirmando esquema de falla en 5M...")
        confirmations = []
        for level in failure_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'failure_sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'failure_buy'))
        print("Confirmaciones de esquema de falla en 5M:", confirmations)
        return confirmations

    def confirm_trap_scheme_in_5m(self, trap_levels):
        print("Confirmando esquema de trampa en 5M...")
        confirmations = []
        for level in trap_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'trap_sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'trap_buy'))
        print("Confirmaciones de esquema de trampa en 5M:", confirmations)
        return confirmations

    def confirm_continuation_scheme_in_5m(self, continuation_levels):
        print("Confirmando esquema de continuación en 5M...")
        confirmations = []
        for level in continuation_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'continuation_sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'continuation_buy'))
        print("Confirmaciones de esquema de continuación en 5M:", confirmations)
        return confirmations

# Cargar datos de ejemplo
data_1h = pd.read_csv('procesado_1h.csv')
data_5m = pd.read_csv('procesado_5m.csv')

# Convertir la columna 'Date' a formato datetime
data_1h['Date'] = pd.to_datetime(data_1h['Date'])
data_5m['Date'] = pd.to_datetime(data_5m['Date'])

print("Datos cargados correctamente.")

# Crear instancia de la estrategia y ejecutar
strategy = TradingStrategy(data_1h, data_5m)
strategy.identify_key_levels()
confirmations = strategy.confirm_levels_in_5m()

print("Confirmaciones finales:", confirmations)
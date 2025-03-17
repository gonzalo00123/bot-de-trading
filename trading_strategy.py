import pandas as pd

class TradingStrategy:
    def __init__(self, data_1h, data_5m):
        self.data_1h = data_1h
        self.data_5m = data_5m
        self.key_levels = []

    def identify_key_levels(self):
        # Identificar máximos y mínimos relevantes en 1H
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                self.key_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                self.key_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))

    def confirm_levels_in_5m(self):
        # Confirmar niveles en 5M
        confirmations = []
        for level in self.key_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'buy'))
        return confirmations

    def identify_polarity_levels(self):
        # Identificar niveles de polaridad en 1H
        polarity_levels = []
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                polarity_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                polarity_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        return polarity_levels

    def confirm_polarity_levels_in_5m(self, polarity_levels):
        # Confirmar niveles de polaridad en 5M
        confirmations = []
        for level in polarity_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'buy'))
        return confirmations

    def confirm_pullback(self, level):
        # Confirmar pullback en 5M
        date, price, level_type = level
        for i in range(len(self.data_5m)):
            if self.data_5m['Date'][i] >= date:
                if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                    return (self.data_5m['Date'][i], price, 'pullback_sell')
                if level_type == 'support' and self.data_5m['High'][i] >= price:
                    return (self.data_5m['Date'][i], price, 'pullback_buy')
        return None

    def confirm_rank(self, level):
        # Confirmar rank en 5M
        date, price, level_type = level
        for i in range(len(self.data_5m)):
            if self.data_5m['Date'][i] >= date:
                if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                    return (self.data_5m['Date'][i], price, 'rank_sell')
                if level_type == 'support' and self.data_5m['High'][i] >= price:
                    return (self.data_5m['Date'][i], price, 'rank_buy')
        return None

    def confirm_baston_c(self, level):
        # Confirmar bastón C en 5M
        date, price, level_type = level
        for i in range(len(self.data_5m)):
            if self.data_5m['Date'][i] >= date:
                if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                    return (self.data_5m['Date'][i], price, 'baston_c_sell')
                if level_type == 'support' and self.data_5m['High'][i] >= price:
                    return (self.data_5m['Date'][i], price, 'baston_c_buy')
        return None

    def confirm_baston_r(self, level):
        # Confirmar bastón R en 5M
        date, price, level_type = level
        for i in range(len(self.data_5m)):
            if self.data_5m['Date'][i] >= date:
                if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                    return (self.data_5m['Date'][i], price, 'baston_r_sell')
                if level_type == 'support' and self.data_5m['High'][i] >= price:
                    return (self.data_5m['Date'][i], price, 'baston_r_buy')
        return None

    def is_engulfing_candle(self, index):
        # Confirmar si la vela es envolvente
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
        # Confirmar si la vela tiene el 70% de relleno
        candle = self.data_5m.iloc[index]
        body_size = abs(candle['Close'] - candle['Open'])
        total_size = candle['High'] - candle['Low']
        return body_size >= 0.7 * total_size

    def confirm_trigger(self, level):
        # Confirmar gatillo en 5M
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
        # Identificar niveles de rompimiento en 1H
        breakout_levels = []
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                breakout_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                breakout_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        return breakout_levels

    def confirm_breakout_levels_in_5m(self, breakout_levels):
        # Confirmar niveles de rompimiento en 5M
        confirmations = []
        for level in breakout_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'breakout_sell'))
                    if level_type == 'support' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'breakout_buy'))
        return confirmations

    def identify_double_scheme(self):
        # Identificar esquema doble en 1H
        double_levels = []
        for i in range(2, len(self.data_1h) - 2):
            if self.data_1h['High'][i] == self.data_1h['High'][i-2] and self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                double_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] == self.data_1h['Low'][i-2] and self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                double_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        return double_levels

    def identify_failure_scheme(self):
        # Identificar esquema de falla en 1H
        failure_levels = []
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                failure_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                failure_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        return failure_levels

    def identify_trap_scheme(self):
        # Identificar esquema de trampa en 1H
        trap_levels = []
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                trap_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                trap_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        return trap_levels

    def identify_continuation_scheme(self):
        # Identificar esquema de continuación en 1H
        continuation_levels = []
        for i in range(1, len(self.data_1h) - 1):
            if self.data_1h['High'][i] > self.data_1h['High'][i-1] and self.data_1h['High'][i] > self.data_1h['High'][i+1]:
                continuation_levels.append((self.data_1h['Date'][i], self.data_1h['High'][i], 'resistance'))
            if self.data_1h['Low'][i] < self.data_1h['Low'][i-1] and self.data_1h['Low'][i] < self.data_1h['Low'][i+1]:
                continuation_levels.append((self.data_1h['Date'][i], self.data_1h['Low'][i], 'support'))
        return continuation_levels

    def confirm_double_scheme_in_5m(self, double_levels):
        # Confirmar esquema doble en 5M
        confirmations = []
        for level in double_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'double_sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'double_buy'))
        return confirmations

    def confirm_failure_scheme_in_5m(self, failure_levels):
        # Confirmar esquema de falla en 5M
        confirmations = []
        for level in failure_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'failure_sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'failure_buy'))
        return confirmations

    def confirm_trap_scheme_in_5m(self, trap_levels):
        # Confirmar esquema de trampa en 5M
        confirmations = []
        for level in trap_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'trap_sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'trap_buy'))
        return confirmations

    def confirm_continuation_scheme_in_5m(self, continuation_levels):
        # Confirmar esquema de continuación en 5M
        confirmations = []
        for level in continuation_levels:
            date, price, level_type = level
            for i in range(len(self.data_5m)):
                if self.data_5m['Date'][i] >= date:
                    if level_type == 'resistance' and self.data_5m['High'][i] >= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'continuation_sell'))
                    if level_type == 'support' and self.data_5m['Low'][i] <= price:
                        confirmations.append((self.data_5m['Date'][i], price, 'continuation_buy'))
        return confirmations

# Cargar datos de ejemplo
data_1h = pd.read_csv('procesado_1h.csv')
data_5m = pd.read_csv('procesado_5m.csv')

# Crear instancia de la estrategia y ejecutar
strategy = TradingStrategy(data_1h, data_5m)
strategy.identify_key_levels()
confirmations = strategy.confirm_levels_in_5m()

print(confirmations)

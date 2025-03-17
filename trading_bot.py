import pandas as pd
from h1_analyzer import H1Analyzer
from m5_analyzer import M5Analyzer

class TradingBot:
    def __init__(self, data_1h_path, data_5m_path):
        self.data_1h = pd.read_csv(data_1h_path, parse_dates=['Date'])
        self.data_5m = pd.read_csv(data_5m_path, parse_dates=['Date'])
        self.levels = []
        self.signals = []
        self.h1_analyzer = H1Analyzer()
        self.m5_analyzer = M5Analyzer()

    def identify_key_levels(self):
        self.levels = self.h1_analyzer.identify_key_levels(self.data_1h)

    def analyze_polarity(self):
        self.polarities = self.h1_analyzer.analyze_polarity(self.data_1h, self.levels)

    def analyze_breakout_support(self):
        self.breakout_supports = self.h1_analyzer.analyze_breakout_support(self.data_1h, self.levels)

    def confirm_entry_in_5m(self):
        pullbacks = self.m5_analyzer.analyze_pullbacks(self.data_5m, self.levels)
        ranks = self.m5_analyzer.analyze_ranks(self.data_5m, self.levels)
        baston_c = self.m5_analyzer.analyze_baston_c(self.data_5m, self.levels)
        baston_r = self.m5_analyzer.analyze_baston_r(self.data_5m, self.levels)
        self.signals = pullbacks + ranks + baston_c + baston_r

    def run(self):
        self.identify_key_levels()
        self.analyze_polarity()
        self.analyze_breakout_support()
        self.confirm_entry_in_5m()
        return pd.DataFrame(self.signals)
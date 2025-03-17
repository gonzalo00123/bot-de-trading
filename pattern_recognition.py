class PatternRecognition:
    def detect_engulfing(self, data, index):
        if index <= 0 or index >= len(data):
            return False

        current = data.iloc[index]
        previous = data.iloc[index-1]

        if (current["close"] > current["open"] and previous["close"] < previous["open"] and
            current["close"] > previous["open"] and current["open"] < previous["close"]):
            return {"type": "bullish_engulfing", "strength": self._calculate_strength(current, previous)}

        elif (current["close"] < current["open"] and previous["close"] > previous["open"] and
              current["close"] < previous["open"] and current["open"] > previous["close"]):
            return {"type": "bearish_engulfing", "strength": self._calculate_strength(current, previous)}

        return False

    def detect_doji(self, data, index):
        if index < 0 or index >= len(data):
            return False

        candle = data.iloc[index]
        body_size = abs(candle["close"] - candle["open"])
        total_size = candle["high"] - candle["low"]

        if total_size > 0 and body_size / total_size < 0.1:
            return {"type": "doji", "strength": 1 - (body_size / total_size)}

        return False

    def detect_hammer(self, data, index):
        pass

    def detect_shooting_star(self, data, index):
        pass

    def detect_strong_candle(self, data, index, threshold=0.7):
        if index < 0 or index >= len(data):
            return False

        candle = data.iloc[index]
        body_size = abs(candle["close"] - candle["open"])
        total_size = candle["high"] - candle["low"]

        if total_size > 0 and body_size / total_size >= threshold:
            direction = "bullish" if candle["close"] > candle["open"] else "bearish"
            return {
                "type": f"strong_{direction}", 
                "strength": body_size / total_size,
                "direction": "buy" if direction == "bullish" else "sell"
            }

        return False

    def _calculate_strength(self, current, previous):
        pass
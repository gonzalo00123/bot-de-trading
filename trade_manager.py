import datetime

class TradeManager:
    def __init__(self):
        self.active_positions = []
        self.trade_history = []
        self.risk_percentage = 1.0  # % del capital a arriesgar por operación

    def open_position(self, exchange, symbol, direction, entry_price, stop_loss, take_profit):
        account_balance = exchange.get_balance()
        risk_amount = account_balance * (self.risk_percentage / 100)
        risk_per_unit = abs(entry_price - stop_loss)
        position_size = risk_amount / risk_per_unit

        order = exchange.create_order(
            symbol=symbol,
            type="limit",
            side="buy" if direction == "buy" else "sell",
            amount=position_size,
            price=entry_price
        )

        position = {
            "id": order["id"],
            "symbol": symbol,
            "direction": direction,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "size": position_size,
            "status": "open",
            "entry_time": datetime.datetime.now(),
            "exit_time": None,
            "profit_loss": None,
            "exit_reason": None
        }

        self.active_positions.append(position)
        return position

    def manage_positions(self, exchange, current_data):
        current_price = current_data.iloc[-1]["close"]

        for position in self.active_positions:
            if position["status"] == "open":
                if (position["direction"] == "buy" and current_price <= position["stop_loss"]) or \
                   (position["direction"] == "sell" and current_price >= position["stop_loss"]):
                    self.close_position(exchange, position, current_price, "stop_loss")
                elif (position["direction"] == "buy" and current_price >= position["take_profit"]) or \
                     (position["direction"] == "sell" and current_price <= position["take_profit"]):
                    self.close_position(exchange, position, current_price, "take_profit")
                else:
                    self._update_trailing_stop(position, current_price)

    def close_position(self, exchange, position, exit_price, reason):
        order = exchange.create_order(
            symbol=position["symbol"],
            type="market",
            side="sell" if position["direction"] == "buy" else "buy",
            amount=position["size"]
        )

        if position["direction"] == "buy":
            profit_loss = (exit_price - position["entry_price"]) * position["size"]
        else:
            profit_loss = (position["entry_price"] - exit_price) * position["size"]

        position["status"] = "closed"
        position["exit_price"] = exit_price
        position["exit_time"] = datetime.datetime.now()
        position["profit_loss"] = profit_loss
        position["exit_reason"] = reason

        self.trade_history.append(position)
        self.active_positions.remove(position)

        return position

    def _update_trailing_stop(self, position, current_price):
        pass
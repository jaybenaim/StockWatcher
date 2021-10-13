from StockWatcher.lib.helpers.stockWatcher.LiveUpdate import LivePriceUpdate


def refresh_stock_prices_and_send_price_alerts():
    live_update = LivePriceUpdate()
    live_update.get_quotes_from_yahoo()

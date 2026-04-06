import time
import requests

BTC_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
ETH_URL = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

ALERT_THRESHOLD = 0.1


def get_price(url):
    response = requests.get(url, timeout=10)
    data = response.json()
    return float(data["price"])


def calc_change(old, new):
    return ((new - old) / old) * 100


def alert(symbol, change):
    direction = "UP" if change > 0 else "DOWN"
    print(f"🚨 ALERT {symbol}: {direction} {change:.4f}%")


def run():
    prev_btc = get_price(BTC_URL)
    prev_eth = get_price(ETH_URL)

    while True:
        try:
            time.sleep(10)

            btc = get_price(BTC_URL)
            eth = get_price(ETH_URL)

            btc_change = calc_change(prev_btc, btc)
            eth_change = calc_change(prev_eth, eth)

            print(f"BTC: {btc} ({btc_change:.4f}%)")
            print(f"ETH: {eth} ({eth_change:.4f}%)")

            if abs(btc_change) >= ALERT_THRESHOLD:
                alert("BTC", btc_change)

            if abs(eth_change) >= ALERT_THRESHOLD:
                alert("ETH", eth_change)

            prev_btc = btc
            prev_eth = eth

        except Exception as e:
            print("ERROR:", e)


if __name__ == "__main__":
    run()

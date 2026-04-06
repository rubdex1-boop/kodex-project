import requests
import time

def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json()
    return float(data["price"])

def get_eth_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
    response = requests.get(url)
    data = response.json()
    return float(data["price"])

def main():
    print("SYSTEM START...")

    while True:
        try:
            btc = get_btc_price()
            eth = get_eth_price()

            print(f"BTC: {btc} | ETH: {eth}")

            time.sleep(10)

        except Exception as e:
            print("ERROR:", e)
            time.sleep(10)

if __name__ == "__main__":
    main()

import time
import requests


BTC_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
ETH_URL = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"


def get_price(url: str) -> float:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return float(data["price"])


def get_btc_price() -> float:
    return get_price(BTC_URL)


def get_eth_price() -> float:
    return get_price(ETH_URL)


def main() -> None:
    print("SYSTEM START...")

    while True:
        try:
            btc = get_btc_price()
            eth = get_eth_price()

            print(f"BTC: {btc:.2f} | ETH: {eth:.2f}")

        except requests.RequestException as e:
            print(f"NETWORK ERROR: {e}")

        except KeyError:
            print("DATA ERROR: Missing 'price' in API response.")

        except ValueError as e:
            print(f"VALUE ERROR: {e}")

        except Exception as e:
            print(f"UNKNOWN ERROR: {e}")

        time.sleep(10)


if __name__ == "__main__":
    main()

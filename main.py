import time
import requests


BTC_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
ETH_URL = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

ALERT_THRESHOLD_PCT = 0.10  # alert przy zmianie >= 0.10% względem poprzedniego odczytu


def get_price(url: str) -> float:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return float(data["price"])


def get_btc_price() -> float:
    return get_price(BTC_URL)


def get_eth_price() -> float:
    return get_price(ETH_URL)


def calculate_change(current: float, previous: float | None) -> tuple[str, float, float]:
    if previous is None:
        return "NO DATA", 0.0, 0.0

    diff = current - previous
    pct = (diff / previous) * 100 if previous != 0 else 0.0

    if diff > 0:
        direction = "UP"
    elif diff < 0:
        direction = "DOWN"
    else:
        direction = "FLAT"

    return direction, diff, pct


def format_change(direction: str, diff: float, pct: float, has_previous: bool) -> str:
    if not has_previous:
        return "brak poprzedniego odczytu"

    return f"{direction} | {diff:+.2f} ({pct:+.4f}%)"


def should_alert(pct: float) -> bool:
    return abs(pct) >= ALERT_THRESHOLD_PCT


def main() -> None:
    print("SYSTEM START...")
    print(f"ALERT THRESHOLD: {ALERT_THRESHOLD_PCT:.2f}%")

    previous_btc = None
    previous_eth = None

    while True:
        try:
            btc = get_btc_price()
            eth = get_eth_price()

            btc_direction, btc_diff, btc_pct = calculate_change(btc, previous_btc)
            eth_direction, eth_diff, eth_pct = calculate_change(eth, previous_eth)

            btc_change_text = format_change(
                btc_direction, btc_diff, btc_pct, previous_btc is not None
            )
            eth_change_text = format_change(
                eth_direction, eth_diff, eth_pct, previous_eth is not None
            )

            print("=" * 60)
            print(f"BTC: {btc:.2f} | {btc_change_text}")
            print(f"ETH: {eth:.2f} | {eth_change_text}")

            if previous_btc is not None and should_alert(btc_pct):
                print(f"ALERT BTC: {btc_direction} {btc_pct:+.4f}%")

            if previous_eth is not None and should_alert(eth_pct):
                print(f"ALERT ETH: {eth_direction} {eth_pct:+.4f}%")

            previous_btc = btc
            previous_eth = eth

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

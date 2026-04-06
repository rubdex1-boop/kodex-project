from signal_engine import TradingSignalEngine, MarketInput

engine = TradingSignalEngine()

sample = MarketInput(
    btc_price=69000,
    eth_price=3400,
    oi_change_pct=2.5,
    volume_change_pct=10.0,
    retail_long_short=1.3,
    toptrader_long_short=1.1,
    long_liquidations=2000000,
    short_liquidations=800000,
    liquidity_above=9.0,
    liquidity_below=4.0,
    price_reaction_bullish=True,
    price_reaction_bearish=False,
    session="london",
    macro_risk="medium",
    news_risk="medium"
)

result = engine.evaluate(sample)

print(result["signal"])
print(result["confidence"])
print(result["alert_message"])

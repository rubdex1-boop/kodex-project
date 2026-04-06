from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MarketInput:
    btc_price: float
    eth_price: float

    oi_change_pct: float
    volume_change_pct: float

    retail_long_short: float
    toptrader_long_short: float

    long_liquidations: float
    short_liquidations: float

    liquidity_above: float
    liquidity_below: float

    price_reaction_bullish: bool
    price_reaction_bearish: bool

    session: str
    macro_risk: str
    news_risk: str


class TradingSignalEngine:
    def evaluate(self, data: MarketInput) -> Dict[str, Any]:
        reasons = []
        confidence = 50

        oi_up = data.oi_change_pct > 0
        vol_up = data.volume_change_pct > 0

        retail_heavy_long = data.retail_long_short > 1.2
        toptrader_supportive = data.toptrader_long_short >= 1.0

        more_liquidity_above = data.liquidity_above > data.liquidity_below
        more_liquidity_below = data.liquidity_below > data.liquidity_above

        shorts_hit_more = data.short_liquidations > data.long_liquidations
        longs_hit_more = data.long_liquidations > data.short_liquidations

        trap_detected = False
        long_bias = False

        if oi_up and vol_up:
            reasons.append("OI rośnie + volume rośnie = ruch bardziej real")
            confidence += 10
        elif oi_up and not vol_up:
            reasons.append("OI rośnie + volume nie rośnie = możliwy trap")
            trap_detected = True
            confidence += 5
        elif not oi_up:
            reasons.append("OI spada = flush / czyszczenie pozycji")
            confidence -= 5

        if retail_heavy_long:
            reasons.append("Retail jest mocno w longach = bearish ostrzeżenie")
            confidence -= 10
        else:
            reasons.append("Retail nie jest skrajnie zapakowany w longi")
            confidence += 5

        if toptrader_supportive:
            reasons.append("Top traderzy nie blokują wzrostu")
            confidence += 5
        else:
            reasons.append("Top traderzy nie wspierają wzrostu")
            confidence -= 10

        if longs_hit_more:
            reasons.append("Więcej wyczyszczono longów = możliwe paliwo pod odbicie")
            confidence += 8
        elif shorts_hit_more:
            reasons.append("Więcej wyczyszczono shortów = część ruchu wzrostowego już wykonana")
            confidence -= 5

        if more_liquidity_above:
            reasons.append("Więcej płynności nad ceną = potencjał pod ruch w górę")
            confidence += 10
            long_bias = True
        elif more_liquidity_below:
            reasons.append("Więcej płynności pod ceną = ryzyko zrzutu przed longiem")
            confidence -= 10

        if data.price_reaction_bullish:
            reasons.append("Cena reaguje byczo = ważniejsze niż sam news")
            confidence += 15
            long_bias = True

        if data.price_reaction_bearish:
            reasons.append("Cena reaguje słabo / odrzuca poziom = ryzyko fake move")
            confidence -= 15
            trap_detected = True

        if data.session == "asia":
            reasons.append("Azja = częściej range, niższa jakość sygnału")
            confidence -= 5
        elif data.session == "london":
            reasons.append("Londyn = sweep / ustawianie kierunku")
        elif data.session == "nasdaq":
            reasons.append("Nasdaq = kluczowy moment decyzji")
            confidence += 5

        if data.macro_risk == "high":
            reasons.append("Wysokie ryzyko makro = większa szansa chaosu")
            confidence -= 10
            trap_detected = True

        if data.news_risk == "high":
            reasons.append("Wysokie ryzyko newsowe = reakcja może być niestabilna")
            confidence -= 10
            trap_detected = True

        confidence = max(0, min(confidence, 100))

        if trap_detected and confidence < 55:
            signal = "TRAP"
        elif long_bias and confidence >= 60 and not trap_detected:
            signal = "LONG (wzrost)"
        elif long_bias and confidence >= 65:
            signal = "LONG (wzrost)"
        else:
            signal = "BRAK TRADE"

        return {
            "signal": signal,
            "confidence": confidence,
            "reasons": reasons,
            "alert_message": self._build_alert(signal, confidence, reasons, data)
        }

    def _build_alert(self, signal: str, confidence: int, reasons: list, data: MarketInput) -> str:
        top_reasons = "\n- " + "\n- ".join(reasons[:5]) if reasons else ""
        return (
            f"ALERT: {signal}\n"
            f"Confidence: {confidence}%\n"
            f"BTC: {data.btc_price}\n"
            f"ETH: {data.eth_price}\n"
            f"Session: {data.session}\n"
            f"Macro risk: {data.macro_risk}\n"
            f"News risk: {data.news_risk}\n"
            f"Reasons:{top_reasons}\n"
        )

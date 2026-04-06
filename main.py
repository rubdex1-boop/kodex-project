Zaprojektuj i wygeneruj kompletny system alertowy do tradingu kryptowalut (BTC, ETH), zgodny z poniższą specyfikacją.

SYSTEM NIE MA HANDLOWAĆ AUTOMATYCZNIE.
To ma być narzędzie analityczne + alertowe. Ja podejmuję decyzje.

Email do alertów:
rubdex@gmail.com
TEL do sms 536887561
==================================================
1. CEL SYSTEMU
==================================================

Zbuduj system działający 24/7, który:

- monitoruje newsy (priorytet)
- monitoruje dane rynkowe (BTC, ETH, Nasdaq, VIX, US10Y, Oil)
- analizuje flow (OI, volume, liquidations, long/short)
- wykrywa setupy tradingowe według mojego frameworku
- wysyła alerty (email)
- generuje raporty (przed Nasdaq, po newsach, setupy)

==================================================
2. ARCHITEKTURA (OBOWIĄZKOWA)
==================================================

Zbuduj projekt w Pythonie z podziałem na moduły:

/app
  /news
  /market
  /macro
  /signals
  /alerts
  /storage
  /config
  /utils

Dodatkowo:
- scheduler (np. APScheduler)
- baza danych (SQLite)
- logger
- retry logic
- .env config
- Docker + docker-compose
- README z instrukcją

==================================================
3. MODUŁ NEWSÓW (PRIORYTET)
==================================================

Źródła:
- RSS feeds
- public news APIs (jeśli dostępne)
- fallback: scraping headlines

Wykrywaj słowa kluczowe:
Iran, Trump, war, attack, oil, Brent, Hormuz, ETF, SEC, Fed, Powell, CPI, PCE, NFP, hack, exploit, sanctions, ceasefire, escalation

Klasyfikuj news:
- bullish crypto
- bearish crypto
- risk-on
- risk-off
- mixed / contradictory

Logika:
- jeśli sprzeczne newsy → ALERT: "FAKE MOVE RISK"
- jeśli breaking news → ALERT natychmiast
- przed Nasdaq open → summary newsów

==================================================
4. MODUŁ MAKRO
==================================================

Pobieraj kalendarz makro (API lub fallback statyczny).

Wykrywaj wydarzenia:
- CPI, PCE, NFP, Jobless Claims, PMI, ISM, Consumer Confidence

Alerty:
- 2h przed
- 1h przed
- 15 min przed

Jeśli <1h do danych:
→ ALERT: "NO TRADE WINDOW"

==================================================
5. MODUŁ MARKET DATA
==================================================

Monitoruj:
- BTC price
- ETH price
- Nasdaq
- VIX
- US10Y
- Oil (Brent)

Jeśli możliwe:
- Open Interest
- Futures Volume
- Spot Volume
- Options Volume
- Long/Short Ratio
- Top Traders
- Liquidations
- Funding Rate

System musi:
- zapisywać stan co X minut
- porównywać:
  - teraz vs 15 min
  - teraz vs 1h
  - teraz vs start dnia

==================================================
6. LOGIKA (CORE SYSTEM)
==================================================

RYNEK:
- headline-driven
- news > price reaction > macro

FLOW:
- OI ↑ = build
- OI ↓ = flush
- OI ↑ + vol ↑ = REAL
- OI ↑ + vol ↓ = TRAP
- OI ↓ + move = LIQUIDATION

SPRING:
- OI rośnie + cena stoi → obserwacja
- wybicie + utrzymanie → LONG EARLY
- wybicie + powrót → TRAP

VOLUME:
- duży vol + brak ruchu → absorpcja
- duży vol + impuls → real move
- niski vol → fake

RANGE:
- top → nie long
- bottom → szukaj long
- middle → NO TRADE

BTC → ETH:
- BTC = direction
- ETH = execution

ETH RANGE:
- <20$ → NO TRADE
- 20–30 → scalp
- 30–40 → OK
- 40+ → ideal

==================================================
7. SYGNAŁY
==================================================

System generuje:

- LONG ALERT
- SHORT ALERT (tylko jako ostrzeżenie)
- TRAP ALERT
- SWEEP ALERT
- LIQUIDATION ALERT
- NO TRADE ALERT
- NEWS ALERT
- MACRO ALERT

==================================================
8. FORMAT ALERTU
==================================================

Każdy alert:

TERAZ:
LONG X% / SHORT X% / NO TRADE X%

BTC:
- direction
- probability
- reaction (sweep/build/flush/trap)
- liquidity (up/down)

ETH:
- price
- target range
- probability

FLOW:
- session (Asia/London/Nasdaq)
- Nasdaq ON/OFF
- OI/Vol (real/trap/build/flush)
- strength %

TRADERS:
- top traders bias
- retail positioning

WNIOSEK:
- kto wyczyszczony
- kto następny
- czy setup czy brak trade

==================================================
9. ALERTY KLUCZOWE
==================================================

1. BREAKING NEWS
2. PRE-NASDAQ REPORT
3. LONG SETUP
4. TRAP ALERT
5. NO TRADE
6. LIQUIDATION EVENT

==================================================
10. ALERTY – IMPLEMENTACJA
==================================================

- email SMTP (gmail)
- cooldown (np. brak powtórzeń przez X minut)
- priorytety alertów
- brak spamu

==================================================
11. OUTPUT
==================================================

Wygeneruj:

- pełny kod projektu
- README (jak uruchomić krok po kroku)
- .env.example
- docker setup
- przykładowe alerty
- instrukcję konfiguracji

==================================================
12. WAŻNE
==================================================

- wybieraj najlepsze dostępne darmowe źródła
- jeśli coś nie istnieje → stwórz placeholder
- system ma być działający MVP + skalowalny
- nie twórz auto trading bota
- skup się na alertach i newsach (to najważniejsze)

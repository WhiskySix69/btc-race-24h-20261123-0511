# btc-race-24h-20261123-0511

[![make.fun · btc-race-24h-20261123-0511](https://make.fun/badge/btc-race-24h-20261123-0511.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)
[![rank](https://make.fun/badge/btc-race-24h-20261123-0511/WhiskySix69/btc-race-24h-20261123-0511/rank.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)
[![reward](https://make.fun/badge/btc-race-24h-20261123-0511/WhiskySix69/btc-race-24h-20261123-0511/reward.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)

Breakout rider: a long-only cbBTC trend bot for make.fun's "Race a BTC trading bot live for 24 hours" bounty. It buys only on a fresh 24-bar high, rides the move with a 3% trailing stop, and sits in cash otherwise — few trades, because every round trip costs about 25 bps in fees, slippage and price impact.

## Run it

```sh
python3 -P -s main.py
```

The bot speaks agent-fun/bars-replay/v1 (newline-delimited JSON on stdin/stdout) through the kit's Python shim, vendored unchanged under `vendor/`. Standard library only; no network, no wall clock, no randomness — two runs on the same bars produce the same orders.

---

<sub>Entered on [make.fun](https://make.fun/?ref=5fdd4463&utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511) · AI agents build software for cash rewards</sub>

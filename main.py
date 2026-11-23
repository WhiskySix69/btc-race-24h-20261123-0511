"""Breakout rider: a long-only cbBTC trend bot for agent-fun/bars-replay/v1.

The idea is deliberately simple. One-minute bars are noisy and every round
trip costs roughly 25 bps in fees, slippage and price impact, so the bot
trades rarely: it buys only when the close breaks the high of the last 24
bars while the last 2 hours are net positive (a regime filter, so it does
not chase dead-cat bounces in a falling market), rides the move with a
trailing stop, and sits in cash the rest of the time. The wide stop (2.5%
below the peak close) keeps it from being shaken out by ordinary chop,
while still getting it out of a real downtrend instead of riding a falling
market to the floor.

Rules, all decided from the bars the harness sends (never the wall clock,
never the environment, never a random draw, so two runs agree byte for byte):
  - flat, close > max close of the previous 24 bars, and close above the
    close 120 bars ago (the 2-hour trend is up)  -> buy, all cash
  - long and close < peak close * (1 - 0.025)            -> sell everything
  - no new entries in the last 60 bars of the window
  - at most one order per reply; a buy spends the whole cash balance,
    a sell empties the whole position

The bot speaks the protocol through the kit's Python shim, vendored
unchanged under vendor/.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))

import makefun_bars

SYMBOL = "CBBTC"

# Bars of history a new high must beat before the bot buys.
LOOKBACK_BARS = 24
# Bars of history the regime filter looks back: the close must be above
# the close this many bars ago, so breakouts are only chased in an uptrend.
MOMENTUM_BARS = 120
# Exit when the close falls this far below the peak close while long.
TRAIL_FRACTION = 0.025
# Do not open a new position after this batch (last hour of the window).
NO_ENTRY_AFTER_SEQ = 1380
# Worst fill the bot tolerates, measured from the latest close in bps.
MAX_SLIPPAGE_BPS = 200
# Smallest buy the replay accepts, in micro-USDC ($1).
MIN_BUY_QUOTE_UNITS = 1_000_000


class BreakoutRider:
    """Keeps the bar history and the peak close of the open position."""

    def __init__(self):
        self.closes = []
        self.peak_close = 0

    def on_batch(self, state, batch):
        bar = state.latest.get(SYMBOL)
        if bar is None:
            return []
        close = int(bar["c"])
        self.closes.append(close)
        if state.warming_up:
            return []

        holding = state.positions.get(SYMBOL)
        if holding is not None and holding.qty > 0:
            self.peak_close = max(self.peak_close, close)
            if close < self.peak_close * (1 - TRAIL_FRACTION):
                return [{
                    "side": "sell",
                    "symbol": SYMBOL,
                    "qty": holding.qty,
                    "max_slippage_bps": MAX_SLIPPAGE_BPS,
                }]
            return []

        self.peak_close = 0
        if state.seq >= NO_ENTRY_AFTER_SEQ:
            return []
        if len(self.closes) <= LOOKBACK_BARS:
            return []
        recent_high = max(self.closes[-LOOKBACK_BARS - 1:-1])
        if close <= recent_high:
            return []
        if len(self.closes) <= MOMENTUM_BARS:
            return []
        if close <= self.closes[-MOMENTUM_BARS - 1]:
            return []
        spend = state.cash
        if spend <= MIN_BUY_QUOTE_UNITS:
            return []
        return [{
            "side": "buy",
            "symbol": SYMBOL,
            "notional_quote_units": spend,
            "max_slippage_bps": MAX_SLIPPAGE_BPS,
        }]


makefun_bars.run(BreakoutRider().on_batch)

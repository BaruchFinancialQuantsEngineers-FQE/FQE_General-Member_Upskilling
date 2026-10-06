# Trading Competition Debrief

Use this template for the **Trading Competition on Friday, October 9**. Fill it in within 48 hours of the event and post it in the FQE Discord. Keep it to half a page. A posted debrief is required for Checkpoint 1.

## Quick start

1. Copy this file to a new file named `debrief-<your-name>.md`, or paste the blank section into a Discord post.
2. Answer the three prompts in two to four sentences each. Use numbers wherever you have them.
3. Read the filled example below if you are unsure how much detail to include.

## Blank template

**Name:** 
**Date:** 
**Final P&L:** 

**1. Where did your P&L come from, by instrument?**
List each instrument you traded and its P&L. State which one contributed most and why.

**2. What was your largest loss, and what caused it?**
Give the size, the instrument, and the decision that led to it. Separate bad luck from a bad decision.

**3. What is one change you will make next time?**
Name one specific, testable change. Avoid general goals such as "be more careful."

## Filled example (invented numbers)

**Name:** Jordan Lee
**Date:** October 10, 2026
**Final P&L:** +$1,150

**1. Where did your P&L come from, by instrument?**
Dice sum market: +$1,400. Card total market: -$450. Coin-flip spread: +$200. Most of the profit came from the dice market, where I quoted a 2-point spread around 10.5 and was filled on both sides about equally.

**2. What was your largest loss, and what caused it?**
I lost $600 in one round of the card market. After two high cards were revealed, I kept my quote centered on the prior fair value instead of moving it up. A counterparty bought my ask three times. This was a decision error, not bad luck.

**3. What is one change you will make next time?**
I will recompute fair value after every piece of revealed information before I quote again. I will practice this with `python drills/market_making/drill.py --reveal` for three sessions before the next competition.

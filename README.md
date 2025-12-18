# Mean-Reversion Spread Backtesting Engine

**Python | Quantitative Trading | Futures Market Simulation**

---

## Project Overview
This project implements a **high-frequency backtesting engine** for futures spreads. The system models realistic market conditions including:

- Slippage and transaction costs
- Expiry force-close logic
- Rolling SMA/SD and winsorized statistics for spread normalization
- Configurable Z-score entry, take-profit, and stop-loss

It generates **per-minute P&L**, **trade logs**, and **daily summaries**, enabling robust evaluation of multiple trading strategies.

---

## File Structure

| File | Description |
|------|-------------|
| `run_sim.py` | Core backtesting engine. Builds universe, calculates stats, and simulates mean-reversion trades. |
| `combine_results.py` | Consolidates multiple strategy outputs into single datasets for analysis. |
| `analyse_results.py` | Computes performance metrics like net/gross P&L, drawdowns, and Sharpe ratios. |
| `compare_strategies.py` | Compares multiple strategies side-by-side for parameter optimization. |

---
## Dataset

The dataset required for running the backtesting scripts is hosted on Google Drive due to file size constraints.

**Download link:** (https://drive.google.com/file/d/1H5f_A8efs4YrqqPidpkPBxKbAjrhTFhw/view?usp=drive_link))

> **Note:** Place the downloaded files in a folder called `data/` inside the repo before running the scripts.


## Core Features

- **Backtesting Engine (`run_sim.py`)**  
  - Normalizes futures spreads and computes rolling statistics.
  - Z-score-based trade entry with configurable thresholds.
  - Dynamic lot-sizing with volume-based throttling.
  - Models slippage, transaction costs, and end-of-day expiry force-close logic.

```python
from run_sim import run_sim
from run_sim import RelZParams

# Example simulation for a single underlying
zp = RelZParams(entry=1.5, tp_off=0.5, stop_off=1.5)
perf, summary, trades, daily = run_sim(
    folder="./data",
    out_prefix="mr_spread"
)


Supports parallel processing for multiple underlyings using ProcessPoolExecutor.

Provides daily P&L breakdown with carry-forward, enabling accurate strategy evaluation.

Modular structure enables easy comparison of strategies and parameters.

Detailed Results per each strategy can be found here:-https://drive.google.com/drive/folders/1lAIHSe7-WvQH6_97gNp-EysCT6pWrsRc?usp=sharing


# Intraday-Mean-Reverting-Strategy
Mean-Reversion Spread Backtesting Engine

Language: Python
Domain: Quantitative Trading / Algorithmic Backtesting

Overview

This project implements a high-frequency mean-reversion trading simulator for futures spreads. It provides a robust backtesting engine with per-minute P&L, trade logs, and daily summaries for multiple underlyings. The system models position sizing, slippage, transaction costs, and expiry handling, making it suitable for evaluating strategy performance under realistic market conditions.

File Structure
.
├── run_sim.py            # Core backtesting engine: spread construction, rolling stats, simulation
├── combine_results.py    # Consolidates multiple simulation outputs for analysis
├── analyse_results.py    # Computes performance metrics, daily summaries, and visualizations
├── compare_strategies.py # Compares multiple parameter configurations or strategy variants
├── data/                 # CSV files with historical futures and cash prices
├── results/              # Output per-minute, trades, summary, daily CSVs
├── README.md

Core Functionality
run_sim.py

Builds the universe of futures and cash instruments.

Computes normalized spreads and rolling statistics (SMA, SD, winsorized stats).

Runs mean-reversion trading simulation with:

Z-score based entry thresholds, TP, and SL offsets

Lot sizing with trade-size and spreadable volume limits

Slippage and transaction cost modeling

Expiry force-close logic

Outputs per-minute P&L, per-trade logs, and daily breakdowns.

combine_results.py

Merges multiple simulation outputs (per-minute, trades, summary) for aggregate analysis.

Handles multi-config or multi-underlying simulations.

analyse_results.py

Computes detailed performance metrics: net/gross P&L, drawdowns, Sharpe ratio, etc.

Provides daily and cumulative breakdowns for each underlying.

Can generate charts or CSVs for visualization and further analysis.

compare_strategies.py

Allows side-by-side comparison of different parameter sets (entry, TP, SL) or strategies.

Evaluates efficiency, risk-adjusted returns, and trade activity metrics.

Installation
git clone <repo_url>
cd mean-reversion-backtest
pip install -r requirements.txt


Dependencies:

pandas, numpy

tqdm

concurrent.futures

math, os, re, glob

Usage

Single configuration simulation:

python run_sim.py \
    --entry 1.5 \
    --tp_off 0.5 \
    --stop_off 1.5 \
    --data_folder ./data \
    --result_folder ./results


Grid search or multiple strategies:

# Run multiple simulations and combine results
python combine_results.py --input_folder ./results --output_file ./results/combined_summary.csv

# Analyse performance
python analyse_results.py --input_file ./results/combined_summary.csv

# Compare multiple strategies
python compare_strategies.py --strategy_files ./results/summary*.csv

Key Parameters
Parameter	Description
entry	Z-score threshold to open positions
tp_off	Take-profit offset relative to entry
stop_off	Stop-loss offset relative to entry
lot_notional	Notional per trading lot
max_lots	Maximum concurrent lots per underlying
ROLL_WINDOW_DAYS	Rolling window length for SMA/SD
MIN_PERIODS	Minimum data points required for rolling stats
NO_TRADE_WARMUP_DAYS	Initial cooldown period before trading
Highlights

Handles slippage, transaction costs, and cumulative traded quantities realistically.

Supports parallel processing for multiple underlyings using ProcessPoolExecutor.

Provides daily P&L breakdown with carry-forward, enabling accurate strategy evaluation.

Modular structure enables easy comparison of strategies and parameters.

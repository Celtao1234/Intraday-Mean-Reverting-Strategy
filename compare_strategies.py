
import pandas as pd
import sys
import os
import glob

def compare_results_csv_files(folder="summ_res"):
    """
    Compare Results_1.csv, Results_2.csv, Results_3.csv files
    """
    
    # Find all Results_*.csv files
    result_files = sorted(glob.glob(os.path.join(folder, "Results_*.csv")))
    
    if not result_files:
        print(f"No Results_*.csv files found in {folder}")
        print(f"Looking for: Results_1.csv, Results_2.csv, Results_3.csv")
        return None
    
    print("=" * 90)
    print("STRATEGY COMPARISON - RESULTS FILES")
    print("=" * 90)
    print()
    
    print(f"Found {len(result_files)} result files:\n")
    for f in result_files:
        print(f"  - {os.path.basename(f)}")
    print()
    
    # Load and analyze each
    strategies = []
    
    for i, file in enumerate(result_files, 1):
        try:
            df = pd.read_csv(file)
            
            # Calculate summary statistics
            total_net_pnl = df['net_pnl'].sum()
            total_gross_pnl = df['gross_pnl'].sum()
            total_cost = df['cost_pnl'].sum()
            total_slippage = df['slippage_fut1'].sum() + df['slippage_fut2'].sum()
            total_contracts = df['total_lots_traded'].sum()
            total_volume = df['total_volume'].sum()
            max_dd = df['drawdown'].max()
            
            profitable_stocks = (df['net_pnl'] > 0).sum()
            losing_stocks = (df['net_pnl'] < 0).sum()
            zero_stocks = (df['net_pnl'] == 0).sum()
            
            # Get best and worst performers
            best_stock = df.loc[df['net_pnl'].idxmax()]
            worst_stock = df.loc[df['net_pnl'].idxmin()]
            
            strategy = {
                'Strategy': f"Strategy {i}",
                'File': os.path.basename(file),
                'Net_PnL': total_net_pnl,
                'Gross_PnL': total_gross_pnl,
                'Total_Cost': total_cost,
                'Total_Slippage': total_slippage,
                'Contracts': int(total_contracts),
                'Volume': int(total_volume),
                'Max_DD': max_dd,
                'Profitable': profitable_stocks,
                'Losing': losing_stocks,
                'Zero_PnL': zero_stocks,
                'Total_Stocks': len(df),
                'Best_Stock': best_stock['stock_name'],
                'Best_PnL': best_stock['net_pnl'],
                'Worst_Stock': worst_stock['stock_name'],
                'Worst_PnL': worst_stock['net_pnl'],
                'Avg_PnL_Per_Stock': total_net_pnl / len(df),
                'Win_Rate': profitable_stocks / (profitable_stocks + losing_stocks) * 100 if (profitable_stocks + losing_stocks) > 0 else 0,
                'Profit_Factor': total_gross_pnl / total_cost if total_cost > 0 else 0,
                'Net_Per_Contract': total_net_pnl / total_contracts if total_contracts > 0 else 0,
                'Risk_Adjusted': total_net_pnl / max_dd if max_dd > 0 else 0
            }
            
            strategies.append(strategy)
            
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue
    
    if not strategies:
        print("No valid strategy files could be loaded")
        return None
    
    # Create comparison DataFrame
    comp_df = pd.DataFrame(strategies)
    comp_df = comp_df.sort_values('Net_PnL', ascending=False)
    
    # Rankings
    print("=" * 90)
    print("OVERALL RANKINGS (by Net PnL):")
    print("=" * 90)
    for idx, row in comp_df.iterrows():
        rank = list(comp_df.index).index(idx) + 1
        symbol = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
        print(f"{symbol} {rank}. {row['Strategy']:12s} ({row['File']:15s})  "
              f"Net PnL: ₹{row['Net_PnL']:>12,.0f}  |  "
              f"Contracts: {row['Contracts']:>5,}  |  "
              f"Win Rate: {row['Win_Rate']:>5.1f}%")
    print()
    
    # Detailed comparison
    print("=" * 90)
    print("DETAILED PERFORMANCE METRICS:")
    print("=" * 90)
    print()
    
    for idx, row in comp_df.iterrows():
        rank = list(comp_df.index).index(idx) + 1
        print(f"{'='*90}")
        print(f"{row['Strategy']} - {row['File']}")
        print(f"{'='*90}")
        print(f"  Net PnL:               ₹{row['Net_PnL']:>15,.2f}")
        print(f"  Gross PnL:             ₹{row['Gross_PnL']:>15,.2f}")
        print(f"  Total Costs:           ₹{row['Total_Cost']:>15,.2f}")
        print(f"  Total Slippage:        ₹{row['Total_Slippage']:>15,.2f}")
        print()
        print(f"  Trading Activity:")
        print(f"    Contracts Traded:    {row['Contracts']:>15,}")
        print(f"    Total Volume:        {row['Volume']:>15,}")
        print(f"    Net per Contract:    ₹{row['Net_Per_Contract']:>14,.0f}")
        print()
        print(f"  Stock Performance:")
        print(f"    Profitable Stocks:   {row['Profitable']:>15} ({row['Win_Rate']:.1f}%)")
        print(f"    Losing Stocks:       {row['Losing']:>15}")
        print(f"    Zero PnL Stocks:     {row['Zero_PnL']:>15}")
        print(f"    Avg PnL per Stock:   ₹{row['Avg_PnL_Per_Stock']:>14,.0f}")
        print()
        print(f"  Risk Metrics:")
        print(f"    Max Drawdown:        ₹{row['Max_DD']:>15,.2f}")
        print(f"    Profit Factor:       {row['Profit_Factor']:>16.2f}")
        print(f"    Risk-Adjusted Ret:   {row['Risk_Adjusted']:>16.2f}")
        print()
        print(f"  Best Performer:        {row['Best_Stock']:>15s}  (₹{row['Best_PnL']:>12,.0f})")
        print(f"  Worst Performer:       {row['Worst_Stock']:>15s}  (₹{row['Worst_PnL']:>12,.0f})")
        print()
    
    # Side-by-side comparison table
    print("=" * 90)
    print("SIDE-BY-SIDE COMPARISON:")
    print("=" * 90)
    
    comparison_metrics = {
        'Metric': ['Net PnL', 'Gross PnL', 'Contracts', 'Win Rate', 
                   'Profit Factor', 'Net/Contract', 'Max Drawdown', 'Profitable Stocks']
    }
    
    for idx, row in comp_df.iterrows():
        comparison_metrics[row['Strategy']] = [
            f"₹{row['Net_PnL']:,.0f}",
            f"₹{row['Gross_PnL']:,.0f}",
            f"{row['Contracts']:,}",
            f"{row['Win_Rate']:.1f}%",
            f"{row['Profit_Factor']:.2f}",
            f"₹{row['Net_Per_Contract']:,.0f}",
            f"₹{row['Max_DD']:,.0f}",
            f"{row['Profitable']}/{row['Total_Stocks']}"
        ]
    
    comp_table = pd.DataFrame(comparison_metrics)
    print(comp_table.to_string(index=False))
    print()
    
    # Recommendation
    best = comp_df.iloc[0]
    print("=" * 90)
    print("🏆 RECOMMENDED STRATEGY FOR SUBMISSION:")
    print("=" * 90)
    print(f"\nUse: {best['Strategy']} ({best['File']})")
    print()
    print("Why this strategy wins:")
    if best['Net_PnL'] == comp_df['Net_PnL'].max():
        print(f"  ✓ Highest Net PnL: ₹{best['Net_PnL']:,.0f}")
    if best['Win_Rate'] >= comp_df['Win_Rate'].max() * 0.9:
        print(f"  ✓ Strong Win Rate: {best['Win_Rate']:.1f}%")
    if best['Profit_Factor'] >= comp_df['Profit_Factor'].max() * 0.9:
        print(f"  ✓ Good Profit Factor: {best['Profit_Factor']:.2f}")
    if best['Risk_Adjusted'] >= comp_df['Risk_Adjusted'].max() * 0.9:
        print(f"  ✓ Best Risk-Adjusted Return: {best['Risk_Adjusted']:.2f}")
    print()
    
    # Save comparison
    output_file = os.path.join(folder, "strategy_comparison_summary.csv")
    comp_df.to_csv(output_file, index=False)
    print(f"✓ Detailed comparison saved to: {output_file}")
    
    # Create markdown report
    report_file = os.path.join(folder, "COMPARISON_REPORT.md")
    with open(report_file, 'w') as f:
        f.write("# Strategy Comparison Report\n\n")
        f.write("## Winner\n\n")
        f.write(f"**{best['Strategy']}** ({best['File']})\n\n")
        f.write(f"- Net PnL: ₹{best['Net_PnL']:,.2f}\n")
        f.write(f"- Win Rate: {best['Win_Rate']:.1f}%\n")
        f.write(f"- Contracts: {best['Contracts']:,}\n\n")
        
        f.write("## All Strategies\n\n")
        f.write("| Rank | Strategy | Net PnL | Contracts | Win Rate | Profit Factor |\n")
        f.write("|------|----------|---------|-----------|----------|---------------|\n")
        for idx, (i, row) in enumerate(comp_df.iterrows(), 1):
            f.write(f"| {idx} | {row['Strategy']} | ₹{row['Net_PnL']:,.0f} | "
                   f"{row['Contracts']:,} | {row['Win_Rate']:.1f}% | {row['Profit_Factor']:.2f} |\n")
    
    print(f"✓ Report saved to: {report_file}")
    print()
    
    return comp_df


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "summ_res"
    
    print(f"Comparing Results_*.csv files in: {folder}\n")
    compare_results_csv_files(folder)
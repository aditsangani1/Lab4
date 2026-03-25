# Lab4 - Blackstone AI Portfolio Analytics

A lightweight Python tool for portfolio analytics with AI-style recommendations.

## Features
- Portfolio expected return and volatility
- Sharpe ratio and 1-day parametric VaR (95%)
- ESG and concentration analysis
- Regime-aware rebalancing recommendations

## Run
```bash
python3 Lab4.py
```

## Customize
Edit the `assets` list inside `run_demo()` in `Lab4.py` with your own portfolio:
- `ticker`
- `weight` (must sum to 1.0)
- `annual_return`
- `annual_volatility`
- `esg_score` (0-100)

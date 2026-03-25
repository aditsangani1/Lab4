"""Blackstone AI Powered Portfolio Analytics Tool.

This module provides a lightweight, dependency-free portfolio analytics engine
that computes core risk/return metrics and generates AI-style recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Dict, Iterable, List

TRADING_DAYS = 252


@dataclass
class Asset:
    """Represents an asset in a portfolio."""

    ticker: str
    weight: float
    annual_return: float
    annual_volatility: float
    esg_score: float = 50.0


class PortfolioAnalytics:
    """Compute portfolio-level analytics for weighted assets."""

    def __init__(self, assets: Iterable[Asset], risk_free_rate: float = 0.03):
        self.assets = list(assets)
        self.risk_free_rate = risk_free_rate
        self._validate()

    def _validate(self) -> None:
        if not self.assets:
            raise ValueError("Portfolio must include at least one asset.")

        total_weight = sum(asset.weight for asset in self.assets)
        if abs(total_weight - 1.0) > 1e-6:
            raise ValueError(
                f"Asset weights must sum to 1.0. Current total: {total_weight:.6f}"
            )

        for asset in self.assets:
            if asset.weight < 0:
                raise ValueError(f"Negative weight detected for {asset.ticker}.")
            if asset.annual_volatility < 0:
                raise ValueError(
                    f"Negative annual volatility detected for {asset.ticker}."
                )
            if not (0 <= asset.esg_score <= 100):
                raise ValueError(f"ESG score for {asset.ticker} must be between 0 and 100.")

    def expected_return(self) -> float:
        """Weighted expected annual return."""
        return sum(asset.weight * asset.annual_return for asset in self.assets)

    def volatility(self) -> float:
        """Approximate annualized volatility using weighted RMS.

        Note: This simplification assumes low cross-asset covariance.
        """
        var = sum((asset.weight * asset.annual_volatility) ** 2 for asset in self.assets)
        return sqrt(var)

    def sharpe_ratio(self) -> float:
        vol = self.volatility()
        if vol == 0:
            return 0.0
        return (self.expected_return() - self.risk_free_rate) / vol

    def var_95(self) -> float:
        """Parametric 1-day VaR at 95% confidence (as positive loss fraction)."""
        daily_mean = self.expected_return() / TRADING_DAYS
        daily_vol = self.volatility() / sqrt(TRADING_DAYS)
        z_95 = 1.645
        loss_quantile = z_95 * daily_vol - daily_mean
        return max(loss_quantile, 0.0)

    def esg_score(self) -> float:
        """Weighted portfolio ESG score."""
        return sum(asset.weight * asset.esg_score for asset in self.assets)

    def concentration_index(self) -> float:
        """Herfindahl-Hirschman style concentration index."""
        return sum(asset.weight**2 for asset in self.assets)


class BlackstoneAIAdvisor:
    """Heuristic AI-style advisor for portfolio recommendations."""

    def __init__(self, analytics: PortfolioAnalytics):
        self.analytics = analytics

    def market_regime_score(self) -> float:
        """Synthetic regime score (0-100), higher means risk-on."""
        portfolio = self.analytics
        sharpe = portfolio.sharpe_ratio()
        concentration_penalty = portfolio.concentration_index() * 100
        esg_bonus = portfolio.esg_score() * 0.2

        score = 50 + (sharpe * 15) + esg_bonus - concentration_penalty
        return min(max(score, 0), 100)

    def rebalance_plan(self) -> List[str]:
        """Generate plain-language rebalancing recommendations."""
        recommendations: List[str] = []
        regime = self.market_regime_score()
        concentration = self.analytics.concentration_index()
        var95 = self.analytics.var_95()

        if concentration > 0.25:
            recommendations.append(
                "Reduce concentration: shift 5-10% from top holdings into diversified assets."
            )

        if var95 > 0.02:
            recommendations.append(
                "Portfolio downside risk is elevated; increase defensive or low-volatility exposure."
            )

        if regime >= 65:
            recommendations.append(
                "Risk-on regime detected; selectively add growth assets with strong risk-adjusted returns."
            )
        elif regime <= 40:
            recommendations.append(
                "Risk-off regime detected; raise cash buffer and prioritize capital preservation."
            )
        else:
            recommendations.append(
                "Neutral regime; maintain strategic allocation and rebalance drift above 3%."
            )

        low_esg_assets = [a.ticker for a in self.analytics.assets if a.esg_score < 40]
        if low_esg_assets:
            joined = ", ".join(low_esg_assets)
            recommendations.append(
                f"Consider ESG improvement: review low-scoring assets ({joined})."
            )

        return recommendations

    def summary(self) -> Dict[str, float]:
        return {
            "expected_return": self.analytics.expected_return(),
            "volatility": self.analytics.volatility(),
            "sharpe_ratio": self.analytics.sharpe_ratio(),
            "var_95_daily": self.analytics.var_95(),
            "esg_score": self.analytics.esg_score(),
            "concentration_index": self.analytics.concentration_index(),
            "market_regime_score": self.market_regime_score(),
        }


def _format_pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def run_demo() -> None:
    """Run a sample analysis for quick usage."""
    assets = [
        Asset("AAPL", 0.30, 0.14, 0.26, 72),
        Asset("MSFT", 0.25, 0.12, 0.22, 81),
        Asset("BND", 0.25, 0.04, 0.08, 65),
        Asset("XLE", 0.20, 0.09, 0.29, 35),
    ]

    analytics = PortfolioAnalytics(assets, risk_free_rate=0.03)
    advisor = BlackstoneAIAdvisor(analytics)

    print("=== Blackstone AI Portfolio Analytics ===")
    summary = advisor.summary()
    print(f"Expected Return: {_format_pct(summary['expected_return'])}")
    print(f"Volatility: {_format_pct(summary['volatility'])}")
    print(f"Sharpe Ratio: {summary['sharpe_ratio']:.2f}")
    print(f"1-Day VaR (95%): {_format_pct(summary['var_95_daily'])}")
    print(f"ESG Score: {summary['esg_score']:.1f}/100")
    print(f"Concentration Index: {summary['concentration_index']:.3f}")
    print(f"Market Regime Score: {summary['market_regime_score']:.1f}/100")

    print("\nAI Recommendations:")
    for idx, recommendation in enumerate(advisor.rebalance_plan(), start=1):
        print(f"{idx}. {recommendation}")


if __name__ == "__main__":
    run_demo()

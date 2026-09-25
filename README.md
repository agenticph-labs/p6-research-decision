# P6: Research-to-Decision Market Entry Study

**Should a Company Enter the Philippine Specialty Coffee Market?**

[![Status: Demo-ready](https://img.shields.io/badge/status-demo--ready-22c55e.svg)](https://github.com/agenticph-labs/p6-research-decision)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A complete research-to-decision pipeline demonstrating structured business analysis — from research question framing through data collection, market sizing, competitor analysis, pricing, customer segmentation, risk assessment, and investment recommendation.

## Repository Structure

```
p6-research-decision/
├── README.md                          # This file — methodology overview
├── market-entry-analysis.ipynb        # Full interactive Jupyter notebook
├── market-entry-report.md             # Polished, standalone decision report
├── data/
│   ├── ph-coffee-macro-data.csv       # Philippines macroeconomic indicators
│   ├── competitor-benchmark.csv       # Competitor pricing & positioning data
│   └── customer-segment-profiles.csv  # Customer archetype data
└── assets/
    └── (generated charts via notebook)
```

## Methodology

This study follows a structured **research-to-decision framework** grounded in economics and strategic management:

### 1. Research Question Framing
- **PICO / PESTEL lens**: Political, Economic, Social, Technological, Environmental, Legal factors frame the core question
- **Decision context**: Capital allocation for a mid-cap F&B group considering PH market entry via specialty coffee

### 2. Data Collection Methodology
- **Primary sources**: Government statistical data (PSA, BSP), industry reports (Euromonitor, Kantar), trade publications
- **Secondary sources**: Academic literature on coffee market entry in emerging economies
- **Assumptions**: Transparently stated — population growth rates, GDP elasticity of coffee demand, specialty vs. commodity market shares

### 3. Market Sizing (Top-Down + Bottom-Up)
- **Top-down**: Philippine coffee market size → specialty coffee subsegment → addressable market → serviceable obtainable market
- **Bottom-up**: Store-unit economics × location capacity × penetration scenarios
- **Triangulation**: Cross-check with GDP growth projections, urbanization rates, and disposable income trends

### 4. Competitor Analysis
- **Framework**: Porter's Five Forces + Strategic Group Mapping
- **Key players**: Starbucks, Tim Hortons, local players (Bo's Coffee, Figaro), emerging specialty roasters (Commune, Yardstick, H Proper)
- **Positioning**: Price-quality matrix, store experience, brand equity

### 5. Pricing Analysis
- **Price sensitivity**: Estimated income elasticity of demand for specialty coffee in PH
- **Benchmarking**: Starbucks PH pricing vs. local competitors vs. regional peers (Singapore, Thailand, Vietnam)
- **Optimal pricing**: Cost-plus, value-based, and competitive pricing scenarios

### 6. Customer Segments
- **Urban professionals** (CBD concentrations)
- **Young affluent / Gen Z coffee enthusiasts**
- **B2B office supply / co-working partnerships**
- **Tourist & expatriate clusters**

### 7. Risk Assessment
- **Regulatory**: FDA permits, PEZA incentives, local government licensing
- **Supply chain**: 70%+ of PH coffee beans are imported — green bean logistics and tariff exposure
- **Competitive response**: Price war risk from Starbucks and local chains
- **Macroeconomic**: Peso volatility, inflation on discretionary spend, El Niño impact on crop availability

### 8. Recommendation Framework
- **Multi-criteria decision analysis (MCDA)**: Weighted scoring across 7 dimensions
- **Go / No-go threshold**: Minimum weighted score of 70/100
- **Phased entry roadmap**: Pilot → Scale → Dominance

## Key Findings

| Dimension | Score | Verdict |
|-----------|-------|---------|
| Market Attractiveness | 85/100 | Strong |
| Competitive Position | 65/100 | Moderate |
| Financial Viability | 78/100 | Strong |
| Risk-Adjusted Return | 72/100 | Moderate |
| Execution Feasibility | 68/100 | Moderate |
| Regulatory Environment | 80/100 | Favorable |
| Strategic Fit | 75/100 | Strong |
| **Composite** | **74.7/100** | **Conditional GO** |

**Recommendation**: Enter the Philippine specialty coffee market through a phased strategy — launch 3 pilot stores in Metro Manila CBDs (BGC, Makati, Ortigas), validate unit economics over 12 months, then scale regionally with a capital-light franchise model.

## Requirements

- Python 3.9+
- Jupyter Notebook / Jupyter Lab
- Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `plotly` (optional for interactive charts)

## Quick Start

```bash
# Clone the repo
git clone https://github.com/agenticph-labs/p6-research-decision.git
cd p6-research-decision

# Install dependencies
pip install pandas numpy matplotlib seaborn scipy jupyter

# Run the notebook
jupyter notebook market-entry-analysis.ipynb
```

## Author

Built for the AgenticPH Labs Portfolio — aligned with Economics + Legal Management analytical rigor.

## 📄 License

MIT

---

*Portfolio Project 6 — [AgenticPH Labs](https://agenticph-labs.github.io/portfolio)*

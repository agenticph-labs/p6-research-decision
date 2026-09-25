#!/usr/bin/env python3
"""Run the full PH Specialty Coffee Market Entry analysis. Generates charts and prints results."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style='whitegrid', palette='muted', font_scale=1.0)
plt.rcParams.update({
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'font.family': 'sans-serif', 'font.size': 11,
    'axes.titlesize': 13, 'axes.labelsize': 11,
})
COLORS = ['#2E86AB','#A23B72','#F18F01','#C73E1D','#3B1F2E','#44BBA4','#E94F37']
DATA_DIR = Path("data")
CUPS_PER_STORE_DAY = 350

# ---- LOAD DATA ----
macro = pd.read_csv(DATA_DIR / "ph-coffee-macro-data.csv")
competitors = pd.read_csv(DATA_DIR / "competitor-benchmark.csv")
segments = pd.read_csv(DATA_DIR / "customer-segment-profiles.csv")

print("=== Data Loaded ===")
print(macro.head(3))
print(competitors.head(3))
print(segments.head(3))

# ---- MACRO CONTEXT ----
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
ax = axes[0,0]
ax.plot(macro['Year'], macro['GDP_Growth_Pct'], marker='o', color=COLORS[0], linewidth=2.5)
ax.axhline(y=5.0, color='gray', linestyle='--', alpha=0.5, label='5% threshold')
ax.set_title('GDP Growth Rate', fontweight='bold'); ax.set_ylabel('%'); ax.legend()
ax.fill_between(macro['Year'], macro['GDP_Growth_Pct'], alpha=0.15, color=COLORS[0])

ax = axes[0,1]
ax.plot(macro['Year'], macro['GDP_per_Capita_USD'], marker='s', color=COLORS[1], linewidth=2.5)
ax.set_title('GDP per Capita (USD)', fontweight='bold'); ax.set_ylabel('USD')
ax.fill_between(macro['Year'], macro['GDP_per_Capita_USD'], alpha=0.15, color=COLORS[1])

ax = axes[1,0]; ax2 = ax.twinx()
line1 = ax.plot(macro['Year'], macro['Coffee_Consumption_kg_per_cap'], marker='o',
                color=COLORS[2], linewidth=2.5, label='Total coffee (kg/cap)')
line2 = ax2.plot(macro['Year'], macro['Specialty_Coffee_Pct'], marker='D',
                 color=COLORS[3], linewidth=2.5, label='Specialty share (%)')
ax.set_title('Coffee Consumption Trends', fontweight='bold'); ax.set_ylabel('kg per capita')
ax2.set_ylabel('Specialty share (%)')
ax.legend(line1+line2, [l.get_label() for l in line1+line2], loc='upper left')

ax = axes[1,1]
ax.plot(macro['Year'], macro['Urban_Pct'], marker='^', color=COLORS[4], linewidth=2.5)
ax.set_title('Urban Population Share', fontweight='bold'); ax.set_ylabel('%')
ax.fill_between(macro['Year'], macro['Urban_Pct'], alpha=0.15, color=COLORS[4])
plt.tight_layout(); plt.savefig("macro-context.png", dpi=150, bbox_inches='tight'); plt.close()
print("\n=== Macro context chart saved ===")

# ---- MARKET SIZING ----
TOTAL_POP_2025 = 115.9e6; URBAN_PCT_2025 = 0.495; COFFEE_DRINKERS_PCT = 0.35
SPECIALTY_ADDRESSABLE_PCT = 0.18; ANNUAL_SPEND_PER_SPECIALTY = 15000
urban_pop = TOTAL_POP_2025 * URBAN_PCT_2025
coffee_drinkers = urban_pop * COFFEE_DRINKERS_PCT
specialty_tam_consumers = coffee_drinkers * SPECIALTY_ADDRESSABLE_PCT
tam_value = specialty_tam_consumers * ANNUAL_SPEND_PER_SPECIALTY

MM_POP_SHARE = 0.13; SOM_STORES_PCT = 0.008
sam_value = specialty_tam_consumers * MM_POP_SHARE * ANNUAL_SPEND_PER_SPECIALTY
som_value = sam_value * SOM_STORES_PCT

print(f"\nTAM: PHP {tam_value/1e9:.2f}B | SAM: PHP {sam_value/1e9:.2f}B | SOM: PHP {som_value/1e6:.2f}M")

fig, ax = plt.subplots(figsize=(8, 5))
vals = [tam_value/1e9, sam_value/1e9, som_value/1e9]
labels = ['TAM\n(Total)', 'SAM\n(Manila)', 'SOM\n(Phase 1)']
bars = ax.bar(labels, vals, color=[COLORS[0], COLORS[2], COLORS[5]], edgecolor='black', width=0.6)
for bar, val in zip(bars, vals):
    lbl = f'PHP {val:.1f}B' if val > 1 else f'PHP {val*1000:.0f}M'
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, lbl, ha='center', fontweight='bold')
ax.set_ylabel('PHP (Billions)'); ax.set_title('Market Sizing Funnel', fontweight='bold')
plt.tight_layout(); plt.savefig("market-sizing.png", dpi=150, bbox_inches='tight'); plt.close()
print("Market sizing chart saved")

# ---- UNIT ECONOMICS ----
STORES_PHASE1 = 3; AVG_TICKET_PHP = 190; DAYS_PER_YEAR = 365
GROSS_MARGIN_PCT = 0.65; EBITDA_MARGIN_TARGET = 0.20
CAPEX_PER_STORE = 15_000_000; CAPEX_ROASTERY = 35_000_000
rev_per_store = CUPS_PER_STORE_DAY * AVG_TICKET_PHP * DAYS_PER_YEAR
total_rev = rev_per_store * STORES_PHASE1
ebitda_est = total_rev * EBITDA_MARGIN_TARGET
total_capex = CAPEX_PER_STORE * STORES_PHASE1 + CAPEX_ROASTERY
print(f"Unit economics: Rev {total_rev/1e6:.1f}M | EBITDA {ebitda_est/1e6:.1f}M | CAPEX {total_capex/1e6:.1f}M | Payback {total_capex/ebitda_est:.1f}yr")

years = np.arange(1, 6)
store_exp = np.array([3, 5, 8, 12, 18])
rev = store_exp * rev_per_store * (1.05 ** (years - 1))
capex_y = np.array([total_capex, 2*CAPEX_PER_STORE, 3*CAPEX_PER_STORE, 4*CAPEX_PER_STORE, 6*CAPEX_PER_STORE])
ebitda_y = rev * EBITDA_MARGIN_TARGET
cum_cf = np.cumsum(ebitda_y - capex_y)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.bar(years, rev/1e6, color=COLORS[0], alpha=0.85, label='Revenue')
ax1.bar(years, ebitda_y/1e6, color=COLORS[5], alpha=0.85, label='EBITDA')
ax1.set_xlabel('Year'); ax1.set_ylabel('PHP (M)'); ax1.set_title('5-Year Revenue & EBITDA', fontweight='bold'); ax1.legend()
ax2.fill_between(years, cum_cf/1e6, alpha=0.3, color=COLORS[6])
ax2.plot(years, cum_cf/1e6, marker='o', color=COLORS[6], linewidth=2.5)
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax2.set_xlabel('Year'); ax2.set_ylabel('PHP (M)'); ax2.set_title('Cumulative Cash Flow', fontweight='bold')
plt.tight_layout(); plt.savefig("unit-economics.png", dpi=150, bbox_inches='tight'); plt.close()
print("Unit economics chart saved")

# ---- COMPETITOR MAP ----
fig, ax = plt.subplots(figsize=(12, 8))
type_colors = {'International': COLORS[0], 'Local': COLORS[2], 'Local_Specialty': COLORS[3], 'Local_Chain': COLORS[5], 'Budget': COLORS[6]}
type_markers = {'International': 'o', 'Local': 'D', 'Local_Specialty': '^', 'Local_Chain': 'P', 'Budget': 'v'}
for typ in competitors['Type'].unique():
    sub = competitors[competitors['Type'] == typ]
    c = type_colors.get(typ, 'gray'); m = type_markers.get(typ, 'o')
    for _, row in sub.iterrows():
        ax.scatter(row['AvgCupPrice_PHP'], row['QualityScore'],
                  s=row['Stores_PH']*3, c=c, marker=m, alpha=0.75, edgecolors='black', linewidth=0.5, zorder=5)
        label = row['Competitor'].replace('_', ' ')
        ax.annotate(label, (row['AvgCupPrice_PHP'], row['QualityScore']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9 if row['Stores_PH']>50 else 7.5, fontweight='bold' if row['Stores_PH']>50 else 'normal')
ax.axvspan(170, 220, alpha=0.08, color='green', label='Entry price zone')
ax.axhspan(7.5, 9.0, alpha=0.08, color='blue', label='Premium quality')
ax.set_xlabel('Avg Cup Price (PHP)'); ax.set_ylabel('Quality Score')
ax.set_title('Strategic Group Map: PH Coffee Market', fontweight='bold')
from matplotlib.lines import Line2D
handles = [Line2D([0],[0], marker='o', color='w', markerfacecolor=COLORS[0], markersize=8, label='Intl'),
           Line2D([0],[0], marker='D', color='w', markerfacecolor=COLORS[2], markersize=8, label='Local'),
           Line2D([0],[0], marker='^', color='w', markerfacecolor=COLORS[3], markersize=8, label='Local Specialty'),
           Line2D([0],[0], marker='P', color='w', markerfacecolor=COLORS[5], markersize=8, label='Chain'),
           Line2D([0],[0], marker='v', color='w', markerfacecolor=COLORS[6], markersize=8, label='Budget')]
ax.legend(handles=handles, loc='upper left')
plt.tight_layout(); plt.savefig("competitor-map.png", dpi=150, bbox_inches='tight'); plt.close()
print("Competitor map saved")

# ---- PRICE BENCHMARK ----
fig, ax = plt.subplots(figsize=(10, 6))
sorted_c = competitors.sort_values('AvgCupPrice_PHP')
bar_colors = [COLORS[3] if t in ('Local_Specialty','International') else COLORS[0] for t in sorted_c['Type']]
bars = ax.barh([c.replace('_',' ') for c in sorted_c['Competitor']], sorted_c['AvgCupPrice_PHP'], color=bar_colors, edgecolor='black', linewidth=0.5)
ax.axvspan(175, 210, alpha=0.12, color='green', label='Entry PHP 175-210')
ax.set_xlabel('Avg Cup Price (PHP)'); ax.set_title('Price Positioning', fontweight='bold'); ax.legend()
for bar, p in zip(bars, sorted_c['AvgCupPrice_PHP']):
    ax.text(p+2, bar.get_y()+bar.get_height()/2, f'PHP {p:.0f}', va='center', fontsize=9)
plt.tight_layout(); plt.savefig("pricing-benchmark.png", dpi=150, bbox_inches='tight'); plt.close()
print("Pricing benchmark saved")

# ---- CUSTOMER SEGMENTS ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
colors_seg = [COLORS[0], COLORS[3], COLORS[2], COLORS[5], COLORS[6], COLORS[1], COLORS[4]]
axes[0].pie(segments['Pct_of_Market'], labels=[s.replace('_',' ') for s in segments['Segment']],
            autopct='%1.0f%%', colors=colors_seg, startangle=90, explode=[0.04]*7)
axes[0].set_title('Market Segment Share', fontweight='bold')
seg_s = segments.sort_values('Monthly_Coffee_Spend_PHP')
bars = axes[1].barh([s.replace('_',' ') for s in seg_s['Segment']], seg_s['Monthly_Coffee_Spend_PHP'], color=colors_seg)
axes[1].set_xlabel('Monthly Spend (PHP)'); axes[1].set_title('Spend by Segment', fontweight='bold')
for bar, v in zip(bars, seg_s['Monthly_Coffee_Spend_PHP']):
    axes[1].text(v+50, bar.get_y()+bar.get_height()/2, f'PHP {v:,}', va='center', fontsize=9)
plt.tight_layout(); plt.savefig("customer-segments.png", dpi=150, bbox_inches='tight'); plt.close()
print("Customer segments saved")

# ---- RISK HEATMAP ----
risks = pd.DataFrame([
    ['Supply Chain', 'Bean price volatility (arabica)', 7, 6, 42, 'Multi-year contracts, futures hedging, 3-month buffer stock'],
    ['Regulatory', 'FDA and LGU permit delays', 4, 8, 32, 'Regulatory consultant; parallel applications; 6-month lead'],
    ['Competitive', 'Price war from Starbucks/Tim Hortons', 8, 4, 32, 'Differentiate on quality; loyalty; avoid price competition'],
    ['Macroeconomic', 'Peso depreciation vs USD (imported beans)', 6, 5, 30, 'FX hedging; local supplier development; pass-through pricing'],
    ['Real Estate', 'CBD prime location competition', 7, 5, 35, '10-year leases; explore non-traditional formats (kiosks)'],
    ['Talent', 'Shortage of skilled baristas', 5, 6, 30, 'In-house training academy; above-market pay; career path'],
    ['Brand Reputation', 'Quality inconsistency across stores', 6, 7, 42, 'Centralized roasting; strict SOPs; mystery shoppers; training'],
    ['Climate', 'El Nino impact on arabica supply', 5, 4, 20, 'Diversify sourcing (Vietnam, Colombia); buffer stock'],
    ['Technology', 'POS/delivery platform disruption', 3, 5, 15, 'API-first architecture; multi-platform; own app + CRM'],
], columns=['Risk', 'Description', 'L', 'I', 'Score', 'Mitigation'])
risks['Severity'] = pd.cut(risks['Score'], bins=[0, 20, 35, 50], labels=['Low','Medium','High'])

fig, ax = plt.subplots(figsize=(10, 6))
sc = ax.scatter(risks['L'], risks['I'], s=risks['Score']*20, c=risks['Score'], cmap='RdYlGn_r', alpha=0.7, edgecolors='black', linewidth=0.5)
for _, r in risks.iterrows():
    ax.annotate(r['Risk'], (r['L'], r['I']), xytext=(3,3), textcoords='offset points', fontsize=8)
ax.set_xlabel('Likelihood'); ax.set_ylabel('Impact'); ax.set_title('Risk Heatmap', fontweight='bold')
ax.axhline(y=5, color='gray', linestyle='--', alpha=0.3); ax.axvline(x=5, color='gray', linestyle='--', alpha=0.3)
plt.colorbar(sc, ax=ax, label='Risk Score')
plt.tight_layout(); plt.savefig("risk-heatmap.png", dpi=150, bbox_inches='tight'); plt.close()
print("Risk heatmap saved")

# ---- MCDA ----
criteria = ['Market Attractiveness', 'Competitive Position', 'Financial Viability',
            'Risk-Adjusted Return', 'Execution Feasibility', 'Regulatory Environment', 'Strategic Fit']
weights = [0.20, 0.15, 0.20, 0.15, 0.15, 0.05, 0.10]
scores_dict = {
    'Market Attractiveness': (85, 'TAM PHP 75+B growing 8-12% CAGR; median age 25; urbanization >50%'),
    'Competitive Position': (65, 'Gap in mid-premium specialty tier, but Starbucks + locals + new roasters create crowding risk'),
    'Financial Viability': (78, 'Strong unit economics (65% GM, ~3.5yr payback); growing revenue trajectory'),
    'Risk-Adjusted Return': (72, 'Bean price/FX manageable via hedging; competitive risk mitigable via differentiation'),
    'Execution Feasibility': (68, 'Talent and real estate binding constraints; 12-18mo timeline realistic but tight'),
    'Regulatory Environment': (80, 'FDI-friendly (PEZA); straightforward permitting; foreign ownership OK via JV'),
    'Strategic Fit': (75, 'Good fit for F&B group with SEA presence; complements existing beverage portfolio'),
}
composite = sum(weights[i] * scores_dict[c][0] for i, c in enumerate(criteria))
print(f"\nMCDA SCORE: {composite:.1f}/100 | THRESHOLD: 70 | VERDICT: {'GO' if composite>=70 else 'NO-GO'}")

fig = plt.figure(figsize=(14, 6))
N = len(criteria); angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist() + [0]
sv = [scores_dict[c][0] for c in criteria] + [scores_dict[criteria[0]][0]]
ax1 = fig.add_subplot(121, polar=True)
ax1.plot(angles, sv, 'o-', linewidth=2, color=COLORS[0], markersize=6)
ax1.fill(angles, sv, alpha=0.25, color=COLORS[0])
ax1.set_xticks(angles[:-1]); ax1.set_xticklabels(criteria, fontsize=9)
ax1.set_ylim(0, 100); ax1.set_title('MCDA Score Radar', fontweight='bold', pad=20)
ax1.axhline(y=70, color='red', linestyle='--', linewidth=1, alpha=0.5)

w_contrib = [weights[i]*scores_dict[c][0] for i, c in enumerate(criteria)]
ax2 = fig.add_subplot(122)
bar_colors = [COLORS[0] if scores_dict[c][0]>=70 else COLORS[6] for c in criteria]
bars = ax2.barh(criteria, w_contrib, color=bar_colors, edgecolor='black', linewidth=0.5)
ax2.axvline(x=composite/10, color='red', linestyle='--', linewidth=1.5, label=f'Composite: {composite:.1f}/100')
ax2.set_xlabel('Weighted Contribution'); ax2.set_title('Weighted Contribution', fontweight='bold'); ax2.legend()
for bar, s in zip(bars, [scores_dict[c][0] for c in criteria]):
    ax2.text(0.3, bar.get_y()+bar.get_height()/2, f'{s}/100', va='center', fontsize=8,
            color='white' if s<70 else 'black', fontweight='bold')
plt.tight_layout(); plt.savefig("mcda-scoring.png", dpi=150, bbox_inches='tight'); plt.close()
print("MCDA charts saved")

print("\n===== ALL CHARTS GENERATED =====")
print("Files: macro-context.png, market-sizing.png, unit-economics.png, competitor-map.png, pricing-benchmark.png, customer-segments.png, risk-heatmap.png, mcda-scoring.png")

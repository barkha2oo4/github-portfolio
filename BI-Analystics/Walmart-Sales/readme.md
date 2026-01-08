# Walmart Sales Dashboard

A Power BI dashboard that analyzes Walmart sales performance across branches, product lines, payment modes and customer segments. The dashboard summarizes revenue, profitability, customer behavior, hourly/monthly trends, and contains actionable recommendations for improving margin, customer experience and digital engagement.

Source PBIX: [WalmartSales.pbix](https://github.com/barkha2oo4/powerbi/blob/0a9b73504beec08d914c249fd4dfcc3752d536ab/WalmartSales/WalmartSales.pbix)

---

## Table of contents
- Overview
- Key metrics & insights (summary)
- Dashboard pages & features
- How to open & use the PBIX
- Important measures (DAX samples)
- Suggested actions & recommendations
- How to extend or customize
- Project author & license

---

## Overview
This dashboard visualizes Walmart sales data to provide a concise picture of revenue growth, category performance, branch-level contribution, customer demographics, payment adoption trends, and time-of-day/month patterns. It is designed for operational and marketing stakeholders who need quick insights and concrete recommendations.

---

## Key metrics (snapshot)
- Total Revenue: ₹155.08K  
- Gross Income: ₹7.38K (Gross margin ≈ 5%)  
- Total Units Sold: 3K  
- Customer Count: 499  
- Average Rating: 6.98  
- Projected Revenue (model): ₹277.75K (Actual exceeded projection: ₹322.97K)

Top branch: Mandalay (Branch C) — highest revenue (₹110.57K) and gross income (₹15.38K).  
Top product categories: Food & Beverages, Sports & Travel, Electronic Accessories (balanced distribution).  
Payment mix: Cash, Credit Card, and E-Wallet are all significant; digital payments rising.

---

## Top insights & quick recommendations
- Gross margin is low (~5%) — immediate opportunity to increase profitability.
  - Negotiate supplier discounts, reduce costly SKUs, or adjust pricing for high-demand items.
- Mandalay (Branch C) is outperforming — replicate successful promotions/inventory mix elsewhere.
- Balanced product-line performance — run targeted cross-sell / combo offers for top categories.
- Average rating (6.98) indicates moderate satisfaction — implement post-purchase feedback and incentives for reviews.
- Digital payments are being adopted — use cashback or small discounts via e-wallets/credit cards to accelerate adoption and increase basket size.
- Peak hours: 1 PM–8 PM (3–5 PM especially) — concentrate staffing and promotions during these windows.

---

## Dashboard pages & features
- Overview / Executive Summary — KPIs, trend spark lines, gross margin callout
- Branch Performance — revenue, gross income, units sold, branch-level drill-throughs
- Product Line Analysis — revenue by product line, top SKUs and category share
- Customer Insights — gender split, customer type (member vs normal), average rating
- Payment Modes — revenue and share by payment type
- Time Intelligence — hourly heatmap, monthly trend, forecast visuals
- Settings / Filters — dynamic slicers for Branch, City, Product Line, Date, Payment Mode

---

## How to open & use
1. Install Power BI Desktop (recommended version: at least the version compatible with the PBIX creation date).
2. Download the PBIX: WalmartSales/WalmartSales.pbix (link above).
3. Open the PBIX in Power BI Desktop to view the report pages, data model, and DAX measures.
4. To publish the report to Power BI Service:
   - File → Publish → Select your workspace.
   - Configure scheduled refresh if your dataset is connected to a live data source.

Notes:
- If data sources are local (CSV/Excel), you may need to re-point queries in Power Query Editor.
- For best performance, keep visuals and measures optimized (avoid overly complex row-level calculated columns; prefer measures).

---

## Important measures (example DAX)
These representative DAX measures help reproduce the dashboard’s core KPIs.

Total Revenue
```dax
TotalRevenue = SUM(Sales[Revenue])
```

Gross Income
```dax
GrossIncome = SUM(Sales[GrossIncome])
```

Gross Margin %
```dax
GrossMarginPct = 
DIVIDE([GrossIncome], [TotalRevenue], 0)
```

Average Rating
```dax
AvgRating = AVERAGE(Feedback[Rating])
```

Projected Revenue (example using simple FORECAST)
```dax
-- Example: using built-in analytics (Power BI visual forecast) is recommended.
-- If using time-series forecasting in DAX (simple trend projection):
AvgMonthlyRevenue = AVERAGEX(VALUES(Date[Month]), [TotalRevenue])
ProjectedNextQuarter = [AvgMonthlyRevenue] * 3
```

Tip: Use the built-in Forecast option on line charts (Analytics pane) or integrate Azure ML / Python/R for advanced forecasting.

---

## Data model notes
- Star schema recommended: FactSales table + dimension tables (Date, Branch, ProductLine, Customer, PaymentMode).
- Use measures instead of calculated columns for aggregations to maintain performance.
- Enable/verify relationships: FactSales → Date (1:N), FactSales → Branch (1:N), etc.

---

## Suggested next steps / roadmap
- Improve gross margin:
  - Supplier renegotiations; margin by product/SKU analysis; price elasticity testing.
- Boost customer satisfaction:
  - Implement post-purchase NPS and incentivize review submissions.
- Increase digital transactions:
  - Launch targeted campaigns with e-wallet/credit-card incentives.
- Advanced forecasting:
  - Integrate seasonality-aware models (Azure ML, Prophet) for more accurate revenue projections.
- Dashboard enhancements:
  - Add MoM/YoY KPIs, exportable executive PDF, branch-level drillthroughs, and role-level security (RLS) where appropriate.

---

## Contributing
- To contribute: open an issue with improvement suggestions or create a PR with updated PBIX, documentation, or data connectors.
- Include: description of the change, screenshots of updated visuals, and DAX queries if new measures are added.

---

## Credits
Prepared by Barkha (barkha2oo4). Dashboard created with:
- Power BI Desktop (visualization & report)
- DAX (measures & calculated metrics)
- Power Query (ETL and data shaping)

---

## Contact
For help, questions or collaboration:
- GitHub: https://github.com/barkha2oo4
- Email: (add your preferred contact email)

---

## License
Specify a license (e.g., MIT) or company policy. If unsure, add a LICENSE file or state: "Proprietary — do not distribute without permission."


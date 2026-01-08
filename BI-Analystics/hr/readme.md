# HR Presence Insights Dashboard

A dashboard to visualize and analyze employee presence, Work-from-Home (WFH) and Sick Leave (SL) patterns to support workforce management and data-driven HR decisions.

---

## Table of contents
- [Project overview](#project-overview)
- [Key features](#key-features)
- [Data sources & schema](#data-sources--schema)
- [Calculations & transformation logic](#calculations--transformation-logic)
- [Visualizations included](#visualizations-included)
- [How to open / run the dashboard](#how-to-open--run-the-dashboard)
- [Example SQL / Pandas / Power BI (DAX) snippets](#example-sql--pandas--power-bi-dax-snippets)
- [Potential improvements & roadmap](#potential-improvements--roadmap)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [License & contact](#license--contact)

---

## Project overview
This dashboard surfaces employee attendance trends: presence percentage, WFH percentage, and sick leave percentage across individuals and the organization. It helps HR and managers:
- Monitor attendance trends over time
- Identify employees or days with anomalous absence patterns
- Support decisions such as staffing, remote-work policies, or wellness interventions

---

## Key features
- Summary KPIs: Total Presence %, Total WFH %, Total SL %
- Employee-level table showing presence / WFH / SL % across a selected period
- Time-series trend charts (by date/month)
- Day-of-week analysis (average presence / WFH / SL by weekday)
- Month and presence-type filters
- Drill-down capability (date granularity) when supported by BI tool

---

## Data sources & schema
The dashboard expects attendance-level data, typically coming from an HRIS, attendance database, or CSV export.

Suggested minimal schema (CSV / table):
- EmployeeID (string/integer)
- EmployeeName (string)
- Date (date)
- Status (string) — values like `P` (Present), `WFH` or `W` (Work from Home), `SL` (Sick Leave), `HPL`, `FFL`, `A` (Absent) etc.
- Department (optional)
- Location (optional)
- Role / Team (optional)

Example rows:
| EmployeeID | EmployeeName | Date       | Status |
|------------|---------------|------------|--------|
| 1001       | Alice Sharma  | 2022-04-01 | P      |
| 1002       | Bob Kumar     | 2022-04-01 | WFH    |
| 1003       | Priya Singh   | 2022-04-01 | SL     |

Notes:
- `Status` must be normalised/consistent. Consider mapping synonyms (e.g., `WFH`, `Home`, `W`) into a canonical value.
- Exclude weekends or non-working days if the analysis should cover only working days.

---

## Calculations & transformation logic
Core idea: compute counts per category (Present / WFH / SL) and divide by total working days in the period (per employee or aggregated).

Common transformations:
- Normalize `Status` into categories: Present, WFH, SL, Other.
- Filter to the analysis period and to working days as needed.

Key measures:
- TotalWorkingDays(employee) = COUNT(DISTINCT Date) or COUNT rows for period filtered to working days
- PresentDays(employee) = COUNT rows where Status = 'P'
- WFHDays(employee) = COUNT rows where Status IN ('WFH', 'W')
- SLDays(employee) = COUNT rows where Status IN ('SL', 'SICK')

Percentages:
- Presence% = PresentDays / TotalWorkingDays
- WFH% = WFHDays / TotalWorkingDays
- SL% = SLDays / TotalWorkingDays

Edge cases:
- Use safe division (handle zeros) and define treatment for employees with zero working days in a period.

---

## Visualizations included
- KPI cards showing aggregated Presence %, WFH %, SL %
- Employee-level table with sortable columns: Presence %, WFH %, SL %, TotalWorkingDays
- Line charts:
  - Presence % by Date (trend)
  - WFH % by Date
  - SL % by Date
- Heatmap or bar chart: Day-of-week analysis for Presence / WFH / SL
- Filters: Month, Department, Employee, Presence status

Design tips:
- Use consistent color coding (e.g., green for presence, blue for WFH, red/orange for SL).
- Add tooltips that show counts behind percentages.
- Display sample counts next to percentages for transparency (e.g., 92% (46/50)).

---

## How to open / run the dashboard
This dashboard can be built in common BI tools (Power BI, Tableau, Qlik, Looker):

Power BI:
1. Open Power BI Desktop.
2. Get Data -> CSV / Excel / Database and connect to attendance table.
3. In Power Query, normalize `Status`, filter working days, and create a Date table (for time intelligence).
4. Create measures (see DAX examples below).
5. Build KPIs and visualizations; add filters (slicers).

Tableau:
1. Connect to data source.
2. Perform data prep (status mapping) in Tableau Prep or within Tableau calculated fields.
3. Build calculated fields for counts and percentages and create required sheets/dashboards.

If your repo contains exported .pbix (Power BI) or .twb/.twbx (Tableau) file, open it in the corresponding desktop app.

---

## Example SQL / Pandas / Power BI (DAX) snippets

SQL (presence %, aggregated by employee for a period):
```sql
SELECT
  EmployeeID,
  EmployeeName,
  COUNT(*) AS total_days,
  SUM(CASE WHEN Status = 'P' THEN 1 ELSE 0 END) AS present_days,
  SUM(CASE WHEN Status IN ('WFH','W') THEN 1 ELSE 0 END) AS wfh_days,
  SUM(CASE WHEN Status IN ('SL','SICK') THEN 1 ELSE 0 END) AS sl_days,
  ROUND(100.0 * SUM(CASE WHEN Status = 'P' THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0),2) AS presence_pct
FROM attendance
WHERE Date BETWEEN '2022-04-01' AND '2022-06-30'
GROUP BY EmployeeID, EmployeeName;
```

Pandas:
```python
import pandas as pd
df = pd.read_csv('attendance.csv', parse_dates=['Date'])

# Normalize status
df['Status'] = df['Status'].str.upper().replace({'W':'WFH','SICK':'SL'})

period_df = df[(df['Date'] >= '2022-04-01') & (df['Date'] <= '2022-06-30')]
agg = period_df.groupby(['EmployeeID','EmployeeName']).agg(
    total_days=('Date','count'),
    present_days=('Status', lambda s: (s=='P').sum()),
    wfh_days=('Status', lambda s: s.isin(['WFH']).sum()),
    sl_days=('Status', lambda s: s.isin(['SL']).sum()),
)
agg['presence_pct'] = 100 * agg['present_days'] / agg['total_days']
```

Power BI (DAX) measures:
```
TotalWorkingDays = DISTINCTCOUNT(Attendance[Date])

PresentDays = CALCULATE(COUNTROWS(Attendance), Attendance[Status] = "P")

Presence% = DIVIDE([PresentDays], [TotalWorkingDays], 0)
```

Adjust the context (per employee / overall) using visuals and filters.

---

## Potential improvements & roadmap
- Add department / location breakdowns
- Implement role-based access to protect PII
- Add automated alerts when presence % drops below thresholds
- Integrate with HRIS for near real-time updates
- Mobile-optimized dashboard layout
- Statistical anomaly detection (sudden drop in presence)
- Add tenure, shift type, or overtime data for deeper insights

---

## Project structure (suggested)
- data/ — sample CSVs or data extracts
- docs/ — design notes, screenshots
- powerbi/ — optional .pbix file if used
- tableau/ — optional .twbx file if used
- scripts/ — ETL scripts (SQL / Python)
- README.md — this file

---

## Contributing
Contributions welcome. Please:
1. Open an issue describing the feature or bug.
2. Fork the repo and create a branch for your change.
3. Submit a pull request with clear description and screenshots (if UI change).

---

## License & contact
- License: Choose an appropriate license (e.g., MIT). Add a LICENSE file.
- Contact: Maintainer — barkha2oo4 (GitHub)

---

If you'd like, I can:
- Draft a sample Power BI measure set or a small Power Query transformation script,
- Create a sample CSV with synthetic data to test the dashboard,
- Produce a one-page printable project summary for stakeholders.

Which would you like next?

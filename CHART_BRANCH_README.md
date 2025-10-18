# Insurance Chart Components - Chart Branch

## Overview
This branch contains interactive chart components for visualizing insurance plan data. The charts are built using **Chart.js** and **react-chartjs-2** to provide dynamic, interactive visualizations.

## What's Been Implemented

### 📊 Chart Components (Modular & Conflict-Free)

All chart components are in `src/components/charts/` directory:

1. **InsurancePremiumChart.jsx** - Bar chart showing monthly premiums across different tiers
2. **InsuranceCoverageChart.jsx** - Bar chart comparing deductibles and out-of-pocket maximums
3. **InsuranceCopayChart.jsx** - Doughnut chart showing copay percentage distribution
4. **InsuranceMaxCoverageChart.jsx** - Line chart displaying maximum coverage limits

### 📄 Data Structure

Sample data is located in `src/data/insurancePlans.json` with the following schema:

```json
{
  "tier_name": "string",
  "premium_monthly": number,
  "deductible_annual": number,
  "coverage_max": number,
  "copay_percentage": number,
  "out_of_pocket_max": number,
  "benefits": ["string"],
  "exclusions": ["string"],
  "age_min": number,
  "age_max": number,
  "family_coverage": boolean,
  "network_type": "string"
}
```

### 🎨 Main Dashboard

`InsuranceChartsPage.jsx` - Main component that:
- Loads data from JSON file
- Displays all charts in a responsive grid layout
- Provides a plan selector to view detailed information
- Shows benefits and exclusions for each plan

## Running the Application

```bash
# Install dependencies (already done)
npm install

# Start development server
npm run dev
```

Visit: http://localhost:5173/

## Design Decisions (For Merge Safety)

1. **Separate Directory Structure**: All chart components are in `src/components/charts/` to avoid conflicts
2. **Modular Components**: Each chart is a separate, self-contained component
3. **JSON Data Source**: Using JSON file instead of hardcoded data for easy updates
4. **Minimal App.jsx Changes**: Only imports the main page component
5. **No Routing**: Simple single-page display to avoid router conflicts

## Future Enhancements (To Be Added)

- [ ] Add user personal info (income, expenses, marital status)
- [ ] PDF parsing for plan details
- [ ] Personalized recommendations based on user profile
- [ ] More interactive features (filters, comparisons)
- [ ] Responsive design improvements for mobile

## Dependencies Added

```json
{
  "chart.js": "^latest",
  "react-chartjs-2": "^latest"
}
```

## File Structure

```
src/
├── components/
│   ├── charts/
│   │   ├── InsurancePremiumChart.jsx
│   │   ├── InsuranceCoverageChart.jsx
│   │   ├── InsuranceCopayChart.jsx
│   │   └── InsuranceMaxCoverageChart.jsx
│   └── InsuranceChartsPage.jsx
├── data/
│   └── insurancePlans.json
└── App.jsx (modified)
```

## Notes

- All changes are isolated to the chart branch
- No modifications to existing main branch files (except App.jsx for demo)
- Ready to be merged or kept separate as needed
- JSON structure matches the requirements exactly

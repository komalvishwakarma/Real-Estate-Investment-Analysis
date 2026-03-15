# Real Estate Investment Advisor

## Project Overview
This project develops a data analytics solution to help investors evaluate property investment opportunities. The system predicts the future value of properties and identifies whether a property is a good investment.

The solution combines **data analysis, rule-based modeling, and an interactive Streamlit application** to provide actionable insights for real estate investors.

---

## Business Use Case
- Identify high-return property investments
- Support buyers in making data-driven decisions
- Automate investment evaluation for real estate listings

---

## Tools & Technologies
- Python
- Pandas
- NumPy
- Streamlit
- Data Visualization

---

## Key Features
- Predict **future property value after 5 years**
- Classify properties as **Good Investment or Not**
- Explore real estate market trends using data analysis
- Interactive **Streamlit dashboard**

---

## Methodology

### Future Price Prediction
Future property price is estimated using compound growth:

Future Price = Current Price × (1 + r)^t

Where:
- r = 8% annual growth
- t = 5 years

---

### Investment Classification
A property is considered a **Good Investment** if:

Current Price ≤ Median Price of its locality

This identifies **undervalued properties within their market area**.

---

## Key Insights
- Location has the strongest influence on property value.
- Larger properties tend to have a lower price per square foot.
- Access to infrastructure like schools, hospitals, and public transport increases property value.

---

## Application
The final system was deployed as an interactive **Streamlit application**, allowing users to:

- Evaluate property investment potential
- Predict future property value
- Explore market trends

---

## Full Project Documentation
Detailed project explanation available here:

[Project Documentation](Project Documentation.docx)

---

## Dashboard Preview
![Dashboard](dashboard.png)

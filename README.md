# 📊 Enterprise Sales Analytics & GenAI Insights Platform

- An end-to-end enterprise sales analytics project demonstrating data engineering, business analysis, SQL analytics, interactive dashboards, and optional GenAI-powered narrative insights.
- This project showcases two complementary analytics workflows:
- Python + Streamlit + GenAI for rapid exploratory analysis and conversational insights
- PostgreSQL + Power BI for production-grade reporting and executive dashboards

## 🔍 Project Overview
The goal of this project is to transform raw enterprise sales data into actionable business insights using industry-standard analytics tools.

The project covers:
- Data cleaning and exploratory analysis in Python
- Business-driven SQL analytics in PostgreSQL
- Interactive Power BI dashboards for stakeholders
- Optional GenAI layer for natural-language insight generation
- Production-ready structure suitable for enterprise environments

## 📁 Dataset Overview
> The dataset represents multi-year enterprise sales transactions, including:
- Time dimension (Year)
- Geography (Country, Market, State, Territory)
- Product hierarchy (Product Segment, Group, Line)
> Sales metrics:
- Trade Sales Dollars
- Trade Sales Gallons
- Trade Sales Quantity
- Engineered Fields
- Price per Gallon
- Sale Type (Revenue vs Adjustment)
- Market Classification (USA / Canada / International)
- Product Segment Category (Premium, Commercial/Commodity, Primers, Others)

## 🧰 Tools & Technologies
- Programming             :  Python (Pandas, NumPy, Matplotlib)
- Database	              :  PostgreSQL
- BI & Visualization	    :  Power BI
- Web App	                :  Streamlit
- GenAI	                  :  OpenAI API (optional insight layer)
- IDEs	                  :  VS Code, pgAdmin
- Version Control	        : Git, GitHub
## 🔄 Analytics Workflow
### 1️⃣ Python EDA & Data Preparation

- Data ingestion and validation
- Handling missing values and anomalies
- Feature engineering (pricing, categories, sale types)
- Exploratory data analysis and trend identification
📂 python_streamlit/

### 2️⃣ SQL Business Analysis (PostgreSQL)

- Business questions were translated into SQL queries, including:
- Revenue trends by year
- Top states and markets by revenue and volume
- Pricing analysis by product segment
- Year-over-year growth using window functions
- Identification of premium vs volume-driven segments
📂 sql/
### 3️⃣ Power BI Dashboard
An executive-ready Power BI dashboard was built on top of PostgreSQL, featuring:
### Key KPIs
- Total Revenue
- Transaction Count
- Average Price per Gallon
#### Visuals
- Revenue by Market (Donut Chart)
- Revenue & Volume by Product Category
- Revenue by State
- Sales Volume (Gallons) by State
#### Interactive slicers for:
- Year
- Sale Type
- Product Segment Category
📂 powerbi/

📸 Dashboard Preview


### 4️⃣ GenAI Insight Layer (Optional)
A GenAI layer was added to generate natural-language summaries on top of deterministic analytics.
#### Design Principle
- All calculations are deterministic and performed in Python or SQL.
- GenAI is used only for explanation and storytelling.
#### Benefits
- Executive-friendly summaries
- Safe and explainable outputs
- Graceful fallback to rule-based summaries if API is unavailable
📂 python_streamlit/genai/

## 📊 Key Business Insights
- Revenue is heavily concentrated in the USA market
- Premium and Super Premium segments generate high revenue with lower volume
- Certain states drive high volume but lower effective pricing
- Clear differentiation between volume-driven and margin-driven product segments
- Pricing varies significantly across regions and product categories

### ▶️ How to Run This Project
- Option 1: 
<img width="861" height="466" alt="image" src="https://github.com/user-attachments/assets/5a3044e1-a7a6-4db2-b17a-4b6726eb69f8" />
- Option 2: PostgreSQL + Power BI
1. Load cleaned dataset into PostgreSQL
2. Run SQL scripts in /sql/
3. Connect Power BI to PostgreSQL
4. Open sales_dashboard.pbix

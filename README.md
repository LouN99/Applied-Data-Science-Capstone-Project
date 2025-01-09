# SpaceX Launch Records Analysis and Prediction

This repository contains the code and analysis for my capstone project: **SpaceX Launch Records Analysis and Prediction**. The project aims to explore SpaceX's rocket launches, analyze success factors, and predict launch outcomes using machine learning models.

## 🚀 Project Overview
SpaceX is known for its innovative approach to reducing the cost of space exploration through reusable rocket technology. By analyzing launch records, we can gain insights into factors influencing successful landings and predict outcomes for future launches. 

The project includes:
- Data collection from the **SpaceX REST API** and Wikipedia.
- Exploratory data analysis (EDA) using **SQL** and **Python libraries**.
- Interactive visualizations with **Plotly Dash** and **Folium**.
- Machine learning models to predict rocket landing success.

---

## 📂 Repository Structure
- **`data/`**: Contains processed datasets used for analysis.
- **`notebooks/`**: Jupyter Notebooks with step-by-step data analysis and modeling.
- **`dash_app/`**: Dash application to visualize launch site success rates and payload correlations.
- **`models/`**: Scripts for building and evaluating machine learning models.
- **`README.md`**: This documentation file.

---

## 🛠️ Technologies Used
- **Programming Languages**: Python (Pandas, NumPy, Scikit-learn)
- **Visualization**: Plotly, Matplotlib, Seaborn, Folium
- **Web Framework**: Dash
- **Database Querying**: SQL
- **Web Scraping**: BeautifulSoup

---

## 📊 Key Findings
1. **Success Rate Trends**:
   - SpaceX's success rate has increased over time, with a significant improvement since 2013.
   - Orbits like ES-L1, GEO, HEO, and SSO have a 100% success rate.

2. **Launch Site Insights**:
   - The **KSC LC-39A** launch site has the highest success rate, with 77% of launches achieving success.
   - All launch sites are near coastlines, reducing risk to urban areas.

3. **Payload Correlation**:
   - Higher payload masses are more successful with specific orbits (LEO, ISS, PO).
   - GTO orbit presents mixed success for payloads.

4. **Machine Learning Results**:
   - The **Decision Tree model** performed best with 86% accuracy.
   - All models (Logistic Regression, SVM, Decision Tree, KNN) performed similarly with 83% accuracy on the test dataset.

---

## 🌐 Interactive Dash Application
Explore the insights interactively using the Dash application:
- **Pie Charts**: View launch success counts by site.
- **Scatter Plots**: Explore correlations between payload mass and launch success.
- **Interactive Maps**: Analyze launch site proximity to railways, highways, and coastlines.

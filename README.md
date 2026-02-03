# Football Scout Recommender

### [🚀 Click here to launch the Football Scout Recommender](https://flashdash101.github.io/football-suggest/)

## 📖 Overview
The **Football Scout Recommender** is an advanced machine learning tool designed to make football analytics easier. It assists scouts and enthusiasts in identifying players who fit specific tactical needs and playing styles.

Moving beyond basic stats, this application uses unsupervised learning to uncover players who perform statistically similar to specific archetypes, whether you need a ball-playing center-back , a high-pressing forward or a really creative midfielder, we've got it all.

## 🧠 Core Algorithm
The recommendation logic is powered by the `AdvancedPlayerRecommender` class. This Python module implements a hybrid unsupervised learning and weighted scoring system to surface player insights.

**Key Technical Components:**
*   **Weighted K-Means Clustering:** Automatically infers player sub-roles (e.g., Ball-Playing Defender vs. Stopper) based on feature density.
*   **Percentile-Based Filtering:** Implements dynamic thresholds (90th/70th/60th percentiles) across specific metrics (xG, Progressive Carries) to enforce "Playing Style" requirements.
*   **Monte Carlo Simulation:** Utilizes controlled stochastic sampling to ensure diversity in results while maintaining statistical relevance.
*   **Composite Scoring:** Calculates similarity using a weighted Euclidean distance matrix adjusted for tactical preferences.

[📂 **View the Algorithm Source Code**](https://github.com/flashdash101/football-suggest/blob/master/Algorithms/Recommend(1).py)



## ✨ Key Features

*   **Massive Dataset:** Analyses over **1,000 professional players** from the **Top 5 European Leagues**, utilizing **68 distinct statistical features** (including xG, progressive carries, tackles, and successful take-ons).
*   **Intelligent Clustering:** Utilises automated subcategory inference via **Weighted K-Means clustering**, categorizing players into **8 distinct position-specific roles** rather than generic labels.
*   **Bias Elimination:** Engineers a percentile-based filtering system with **per-90 normalisation**. This implements tiered thresholds (90th/70th/60th percentiles) to ensure statistically robust candidate selection and eliminate "minutes played" bias.
*   **Composite Scoring Engine:** Recommendations are generated via a complex algorithm combining:
    *   Role-specific feature weighting (0.5–1.1×).
    *   Additive style bonuses.
    *   Percentile-rank normalisation.
    *   Controlled stochastic sampling to balance recommendation quality with result diversity.

## 🛠 Technical Architecture


This project is built as a full-stack application with a focus on reproducibility and performance.

*   **Frontend:** React (Vite) for a responsive, fast user interface.
*   **Backend:** FastAPI (Python) deployed on Render.
*   **Machine Learning:**
    *   **Scikit-learn:** Used for K-Means clustering and `RobustScaler` preprocessing.
    *   **Pandas/Numpy:** Utilized for vectorized per-90 calculations and data manipulation.
*   **DevOps:** Docker containerisation ensures reproducible ML workflows across environments.

## 🚀 How It Works

1.  **Data Ingestion:** The pipeline processes raw data, performing per-90 normalisation to standardize stats regardless of game time.
2.  **Clustering & Classification:** The ML model runs weighted K-Means to assign players to sub-roles based on their statistical output.
3.  **User Input:** You select a **Main Role**, a **Sub Role**, and a desired **Playing Style**.
4.  **Algorithmic Scoring:** The backend calculates a composite score based on the weighted importance of specific stats for your chosen role (e.g., passing is weighted higher for a Deep Lying Playmaker).
5.  **Recommendation:** The system returns a list of players that statistically match your criteria, achieving sub-second response times.

## 💻 Usage

1.  Visit the [Live Website](https://flashdash101.github.io/football-suggest/).
2.  Select a position (e.g., Midfielder).
3.  Select a specific sub-role (e.g., Defensive ).
4.  Choose a playing style (e.g., Creative).
5.  Click **"Get Recommendations"** to see the scout report.

## 🔜 Future Enhancements
*   Integration with real-time API feeds for match-day updates.
*   Comparison tool to visualize two players head-to-head.
*   Historical data analysis for longitudinal performance tracking.

## 📄 License
Open Source

## 📧 Contact
For inquiries regarding the engineering behind this project or collaboration opportunities, please contact:
**adesina0202@gmail.com**

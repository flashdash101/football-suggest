# Football Scout Recommender

## Overview
This Football Scout Recommender is an advanced tool designed to assist in identifying and recommending players based on specific tactical needs and playing styles. Whether you're looking for a possession-minded defensive midfielder or any other specialized role, this program provides data-driven recommendations to support your scouting process.

## Features
- **Comprehensive Database**: Analyzes data from over 1,000 professional players across top European leagues.
- **Weighted Feature System**: Utilizes a sophisticated weighting system that accounts for the varying importance of statistics across different playing positions and styles.
- **Flexible Player Classification**: Employs KMeans clustering for player sub-role inference, allowing for nuanced categorization of players who may not fit traditional positional stereotypes.
- **Advanced Recommendation Algorithm**: Uses Monte Carlo simulations to generate robust and reliable player recommendations.

## How It Works
1. **Data Collection and Processing**: The system aggregates and normalizes data from various sources covering 1,000+ players.
2. **Feature Weighting**: Different attributes are weighted based on their importance for specific roles and playing styles.
3. **Clustering**: KMeans clustering algorithm categorizes players into sub-roles, providing a more nuanced view of player types.
4. **Monte Carlo Simulation**: Multiple simulations are run to account for variability and provide consistent recommendations.
5. **Results Generation**: The system outputs a list of recommended players based on the specified criteria.

## Usage
You choose a main role, a sub role and a playing style and click get recommendations, it's as simple as that!

## Technical Details
- **Backend**: Python
- **Machine Learning Libraries**: scikit-learn for KMeans clustering, SHAP and Numpy
- **Data Processing**: Pandas for data manipulation
- **Frontend**: [React.js, JSX]
- **API**: [FastAPI]

## Future Enhancements
- Integration with real-time player performance data


## License
Open Source

## Contact
Here is my email for any inquiries: adesina0202@gmail.com

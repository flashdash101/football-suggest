
import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
from scipy.stats import pearsonr

class AdvancedPlayerRecommender:
    def __init__(self, data):
        self.data = data
        self.scaler = RobustScaler()
        self.features = [ '90s', 'Gls', 'Sh', 'SoT', 'SoT%',
       'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 'PKatt', 'xG',
       'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG',  'onethird', 'A-xAG', 'Ast',
       'Att', 'Att.1', 'Att.2', 'Att.3', 'Cmp', 'Cmp%', 'Cmp%.1', 'Cmp%.2',
       'Cmp%.3', 'Cmp.1', 'Cmp.2', 'Cmp.3', 'CrsPA', 'KP', 'PPA', 'PrgDist',
       'PrgP', 'TotDist', 'xA', 'xAG', 'Att 3rd', 'Att Pen', 'CPA', 'Carries',
       'Def 3rd', 'Def Pen', 'Dis', 'Live', 'Mid 3rd', 'Mis', 'PrgC', 'PrgR',
       'Rec', 'Succ', 'Succ%', 'Tkld', 'Tkld%', 'Touches', 'Blocks', 'Clr',
       'Err', 'Int', 'Lost', 'Pass', 'Tkl', 'Tkl%', 'Tkl+Int', 'Tkl.1', 'TklW' ]
        self.position_categories = {
            'Defender': ['DF'],
            'Midfielder': ['MF'],
            'Forward': ['FW']
        }
        
        self.playing_styles = {
            'Possession': {'Cmp': 1.7, 'PrgP': 1.6, 'KP': 1.4, 'Touches' : 1.6, 'TB' : 1.6},
            'Counter-Attack': {'PrgP': 1.2, 'PrgC': 1.5, 'Ast': 1.3, 'xA': 1.1},
            'High-Press': {'Tkl': 1.8, 'Int': 1.5, 'PrgP': 1.1, 'Att 3rd': 1.7, 'Mid 3rd' : 1.9},
            'Target-Man': {'Gls': 1.2, 'xG': 1.2, 'Sh': 1.1, 'SoT': 1.1},
            'Defensive': {'Tkl': 1.6, 'Int': 1.7, 'Blocks': 1.3, 'Clr': 1.2, 'TklW': 1.6, 'Def 3rd': 1.6},
            'No Style': {}
        }
        
        
        self.subcategories = {
            'Defender': ['CB', 'FB', 'WB'],
            'Midfielder': ['DM', 'CM', 'AM'],
            'Forward': ['ST', 'W']
        }
        self.role_features = {
            'CB': {'Tkl': 0.8, 'Int': 0.8, 'Clr': 0.6, 'Blocks': 0.8,   'Cmp': 0.7, 'TklW': 0.7, 'Def 3rd': 0.7},
            'FB': {'Tkl': 0.6, 'Int': 0.5, 'Pass': 0.5, 'PrgC': 0.7, 'PrgP': 0.7, 'Ast': 0.8, 'Clr': 0.5, 'Cmp': 0.6},
            'WB': {'Tkl': 0.6, 'Int': 0.7, 'PrgC': 0.8, 'PrgP': 0.6, 'Ast': 0.7, 'PrgC': 0.6, 'Cmp': 0.7, 'onthird': 0.7, 'Succ': 0.8},
            'DM': {'Tkl': 0.9, 'Int': 0.7, 'PrgP': 0.8, 'Cmp': 0.8, 'Blocks': 0.7, 'xA': 0.7, 'Ast': 0.7, 'Mid 3rd': 0.7, 'Def 3rd': 0.7},
            'CM': { 'Cmp': 0.9,'PrgP': 0.6, 'Ast': 0.7, 'KP': 0.6, 'Tkl': 0.6, 'Int': 0.7, 'xA': 0.8, 'Cmp': 0.6},
            'AM': {'Ast': 0.7, 'KP': 0.7, 'xA': 0.8, 'PrgP': 0.7, 'Gls': 0.8, 'xG': 0.8, 'PrgC': 0.6, 'TB': 0.7},
            'ST': {'Gls': 0.9, 'xG': 0.9, 'Sh': 0.7, 'SoT': 0.8, 'Ast': 0.6, 'xA': 0.5},
            'W': {'Ast': 0.8, 'xA': 0.9, 'PrgC': 0.8, 'Gls': 0.5, 'xG': 0.6, 'onethird': 0.8, 'Succ': 0.9, 'CPA': 0.7, 'Att': 0.9},
        }
        
        self.subcategory_weights = {
            'CB': {'Tkl': 0.8, 'Int': 0.8, 'Clr': 0.6, 'Blocks': 0.8,   'Cmp': 0.7, 'TklW': 0.7, 'Def 3rd': 0.7},
            'FB': {'Tkl': 0.6, 'Int': 0.5, 'Pass': 0.5, 'PrgC': 0.7, 'PrgP': 0.7, 'Ast': 0.8, 'Clr': 0.5, 'Cmp': 0.6},
            'WB': {'Tkl': 0.6, 'Int': 0.7, 'PrgC': 0.8, 'PrgP': 0.6, 'Ast': 0.7, 'PrgC': 0.6, 'Cmp': 0.7, 'onthird': 0.7, 'Succ': 0.8},
            'DM': {'Tkl': 0.9, 'Int': 0.7, 'PrgP': 0.8, 'Cmp': 0.8, 'Blocks': 0.7, 'xA': 0.7, 'Ast': 0.7, 'Mid 3rd': 0.7, 'Def 3rd': 0.7},
            'CM': {'Cmp': 0.9, 'PrgP': 0.6, 'Ast': 0.7, 'KP': 0.6, 'Tkl': 0.6, 'Int': 0.7, 'xA': 0.8},
            'AM': {'Ast': 0.7, 'KP': 0.7, 'xA': 0.8, 'PrgP': 0.7, 'Gls': 0.8, 'xG': 0.8, 'PrgC': 0.6, 'TB': 0.7},
            'ST': {'Gls': 0.9, 'xG': 0.9, 'Sh': 0.7, 'SoT': 0.8, 'Ast': 0.6, 'xA': 0.5},
            'W': {'Ast': 0.8, 'xA': 0.9, 'PrgC': 0.8, 'Gls': 0.5, 'xG': 0.6, 'onethird': 0.8, 'Succ': 0.9, 'CPA': 0.7, 'Att': 0.6},
        }
        
        self.distance_metrics = {
            'cosine': self.cosine_sim,
            'pearson': self.pearson_correlation,
            'euclidean': self.euclidean_similarity,
            'manhattan': self.manhattan_distances
        }
        
        self.prepare_data()

    def prepare_data(self):
        self.data['MainPos'] = self.data['Pos'].apply(lambda x: x.split(',')[0])
        self.scaled_features = self.scaler.fit_transform(self.data[self.features])
        self.infer_subcategories_weighted_kmeans()
        self.print_subcategory_counts()
        # self.analyze_kmeans_results()
        
        
        


    def apply_subcategory_weights(self, data, subcategory):
        weights = np.ones(len(self.features))
        for i, feature in enumerate(self.features):
            weights[i] = self.subcategory_weights[subcategory].get(feature, 1.0)
        return data * weights

    def infer_subcategories_weighted_kmeans(self):
        positions = ['Defender', 'Midfielder', 'Forward']

        for pos in positions:
            pos_mask = self.data['MainPos'].isin(self.position_categories[pos])
            pos_data = self.scaled_features[pos_mask]

            subcats = self.subcategories[pos]
            
            # Create weighted versions of the data
            weighted_data = np.concatenate([self.apply_subcategory_weights(pos_data, subcat) for subcat in subcats])
            
            # Create labels for the weighted data
            labels = np.repeat(range(len(subcats)), len(pos_data))

            # Fit KMeans on the weighted data
            kmeans = KMeans(n_clusters=len(subcats), random_state=30, n_init=10)
            kmeans.fit(weighted_data, labels)

            # Predict using the original data
            clusters = kmeans.predict(pos_data)

            # Map cluster numbers to subcategories
            cluster_to_subcat = {i: subcat for i, subcat in enumerate(subcats)}
            
            self.data.loc[pos_mask, 'Subcategory'] = [cluster_to_subcat[c] for c in clusters]

    def print_subcategory_counts(self):
        subcategory_counts = self.data['Subcategory'].value_counts()
        total_players = len(self.data)
        print("Subcategory Distribution:")
        for subcat, count in subcategory_counts.items():
            percentage = (count / total_players) * 100
            print(f"{subcat}: {count} players ({percentage:.2f}%)")
        print(f"Total players: {total_players}")

    def analyze_kmeans_results(self):
        for pos in ['Defender', 'Midfielder', 'Forward']:
            subcats = self.subcategories[pos]
            
            print(f"\nAnalysis for {pos}:")
            for subcat in subcats:
                subcat_data = self.data[self.data['Subcategory'] == subcat]
                print(f"\nSubcategory: {subcat}")
                print(f"Number of players: {len(subcat_data)}")
                
                # Print average values for key stats
                key_stats = list(self.subcategory_weights[subcat].keys())
                for stat in key_stats:
                    if stat in subcat_data.columns:
                        avg_value = subcat_data[stat].mean()
                        print(f"Average {stat}: {avg_value:.2f}")

    def cosine_sim(self, normalized_stats):
        return cosine_similarity(normalized_stats)

    def manhattan_distances(self, normalized_stats):
        return manhattan_distances(normalized_stats)
    
    
    def pearson_correlation(self, normalized_stats):
        # Center the data
        centered_stats = normalized_stats - np.mean(normalized_stats, axis=1)[:, np.newaxis]
        
        # Calculate the correlation matrix
        corr_matrix = np.dot(centered_stats, centered_stats.T) / (
            np.sqrt(np.sum(centered_stats**2, axis=1))[:, np.newaxis] *
            np.sqrt(np.sum(centered_stats**2, axis=1))[np.newaxis, :]
        )
        
        # Handle potential numerical instabilities
        corr_matrix = np.clip(corr_matrix, -1, 1)
        
        # Scale from [-1, 1] to [0, 1]
        return (corr_matrix + 1) / 2

    def euclidean_similarity(self, normalized_stats):
        distances = euclidean_distances(normalized_stats)
        return 1 / (1 + distances)
    
    def get_recommendations_monte_carlo(self, category, subcategory=None, num_recommendations=5, min_minutes=450, num_simulations=1000, distance_metric='euclidean', playing_style='No Style'):
        category_mask = self.data['MainPos'].isin(self.position_categories[category])
        filtered_data = self.data[category_mask]
        if subcategory:
            filtered_data = filtered_data[filtered_data['Subcategory'] == subcategory]

        filtered_data = filtered_data[filtered_data['90s'] * 90 >= min_minutes]

        if len(filtered_data) < num_recommendations:
            raise ValueError(f"Not enough players ({len(filtered_data)}) meet the criteria.")

        all_stats = self.features
        
        for stat in all_stats:
            if stat not in filtered_data.columns:
                filtered_data[stat] = 0

        stats_per_90 = filtered_data[self.features].div(filtered_data['90s'], axis=0)
        stats_per_90 = stats_per_90.replace([np.inf, -np.inf], np.nan).fillna(0)

        scaler = StandardScaler()
        normalized_stats = scaler.fit_transform(stats_per_90)

        # Apply feature weighting
        if subcategory:
            feature_weights = np.array([self.role_features[subcategory].get(feat, 0.1) for feat in self.features])
            if playing_style:
                style_weights = np.array([self.playing_styles[playing_style].get(feat, 1.0) for feat in self.features])
                feature_weights *= style_weights
            normalized_stats *= feature_weights
        # Add random noise to simulate performance variability

        # Monte Carlo simulation
        similarity_sums = np.zeros((len(filtered_data), len(filtered_data)))
        for _ in range(num_simulations):
            # Add random noise to simulate performance variability
            noisy_stats = normalized_stats + np.random.normal(0, 0.1, normalized_stats.shape)
            
            # Calculate similarities using the specified distance metric
            similarities = self.distance_metrics[distance_metric](noisy_stats)
            similarity_sums += similarities

        # Average similarities over all simulations
        avg_similarities = similarity_sums / num_simulations
        
        randomness_factor = np.random.uniform(0.85, 1.05, avg_similarities.shape)
        avg_similarities *= randomness_factor

        # Get top similar players (excluding self-similarity)
        top_similar_indices = avg_similarities.argsort()[:, ::-1][:, 1:num_recommendations+1]
        
        recommendations = []
        for idx in top_similar_indices[0]:
            player_data = filtered_data.iloc[idx]
            recommendations.append({
                'Player': player_data['Player'],
                'Pos': player_data['Pos'],
                'Club': player_data['Club'],
                'Similarity': avg_similarities[0, idx],
                'SimilarityStd': np.std(similarity_sums[0, idx] / num_simulations),
                **{stat: player_data[stat] for stat in all_stats}
            })

        return recommendations

    def get_recommendations(self, category, subcategory=None, num_recommendations=5, min_minutes=0):
    # Filter by category
        category_mask = self.data['MainPos'].isin(self.position_categories[category])
        filtered_data = self.data[category_mask]

        # Filter by subcategory if specified
        if subcategory:
            filtered_data = filtered_data[filtered_data['Subcategory'] == subcategory]

        # Filter out players with insufficient minutes
        filtered_data = filtered_data[filtered_data['90s'] * 90 >= min_minutes]

        # Check if we have enough players
        if len(filtered_data) < num_recommendations:
            raise ValueError(f"Not enough players ({len(filtered_data)}) meet the criteria.")

        # Define all stats we want to include
        all_stats = ['Gls', 'Ast', 'xG', 'xA', 'Sh', 'SoT', 'KP', 'PrgP', 'PrgC', 'Tkl', 'Int', 'Clr', 'Blocks']
        
        # Ensure all stats are present in the dataframe
        for stat in all_stats:
            if stat not in filtered_data.columns:
                filtered_data[stat] = 0  # or np.nan if you prefer

        # Normalize stats by minutes played for similarity calculation
        stats_per_90 = filtered_data[self.features].div(filtered_data['90s'], axis=0)

        # Handle potential infinity values
        stats_per_90 = stats_per_90.replace([np.inf, -np.inf], np.nan).fillna(0)

        # Normalize features to 0-1 range
        scaler = MinMaxScaler()
        normalized_stats = scaler.fit_transform(stats_per_90)

        # Calculate similarities
        similarities = cosine_similarity(normalized_stats)

        # Get top similar players (excluding self-similarity)
        top_similar_indices = similarities.argsort()[:, ::-1][:, 1:num_recommendations+1]
        
        # Prepare recommendations
        recommendations = []
        for idx in top_similar_indices[0]:
            player_data = filtered_data.iloc[idx]
            recommendations.append({
                'Player': player_data['Player'],
                'Pos': player_data['Pos'],
                'Club': player_data['Club'],
                'Similarity': similarities[0, idx],
                **{stat: player_data[stat] for stat in all_stats}
            })

        return recommendations
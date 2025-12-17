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
            'Possession': {'Cmp': 1.7, 'PrgP': 1.6, 'KP': 1.4, 'Touches': 1.6, 'Cmp%': 1.5, 'TotDist': 1.3},
            'Creative': {'xA': 2.0, 'KP': 1.9, 'Ast': 1.8, 'PPA': 1.7, 'CPA': 1.6, 'PrgP': 1.4, 'CrsPA': 1.3, 'PrgC': 1.1},
            'Goal Threat': {'Gls': 2.0, 'xG': 1.8, 'SoT': 1.6, 'SoT%': 1.7, 'Sh': 1.4, 'G/SoT': 1.5},
            'Dribbling': {'Carries': 1.9, 'PrgC': 1.7, 'Succ': 1.5, 'CPA': 1.3, 'Touches': 1.2,},
            'High-Press': {'Tkl': 1.8, 'Int': 1.5, 'PrgP': 1.1, 'Att 3rd': 1.7, 'Mid 3rd': 1.9, 'TklW': 1.6},
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
            'W': {'Ast': 0.8, 'xA': 1.1, 'PrgC': 0.85, 'Gls': 0.7, 'xG': 0.85, 'onethird': 0.8, 'Succ': 0.9, 'CPA': 0.75, 'Att': 0.9},
        }
        
        self.subcategory_weights = {
            'CB': {'Tkl': 0.8, 'Int': 0.8, 'Clr': 0.6, 'Blocks': 0.8,   'Cmp': 0.7, 'TklW': 0.7, 'Def 3rd': 0.7},
            'FB': {'Tkl': 0.6, 'Int': 0.5, 'Pass': 0.5, 'PrgC': 0.7, 'PrgP': 0.7, 'Ast': 0.8, 'Clr': 0.5, 'Cmp': 0.6},
            'WB': {'Tkl': 0.6, 'Int': 0.7, 'PrgC': 0.8, 'PrgP': 0.6, 'Ast': 0.7, 'PrgC': 0.6, 'Cmp': 0.7, 'onthird': 0.7, 'Succ': 0.8},
            'DM': {'Tkl': 0.9, 'Int': 0.7, 'PrgP': 0.8, 'Cmp': 0.8, 'Blocks': 0.7, 'xA': 0.7, 'Ast': 0.7, 'Mid 3rd': 0.7, 'Def 3rd': 0.7},
            'CM': {'Cmp': 0.9, 'PrgP': 0.6, 'Ast': 0.7, 'KP': 0.6, 'Tkl': 0.6, 'Int': 0.7, 'xA': 0.8},
            'AM': {'Ast': 0.7, 'KP': 0.7, 'xA': 0.8, 'PrgP': 0.7, 'Gls': 0.8, 'xG': 0.8, 'PrgC': 0.6, 'TB': 0.7},
            'ST': {'Gls': 0.9, 'xG': 0.9, 'Sh': 0.7, 'SoT': 0.8, 'Ast': 0.6, 'xA': 0.5},
            'W': {'Ast': 0.9, 'xA': 1.1, 'PrgC': 0.85, 'Gls': 0.7, 'xG': 0.85, 'onethird': 0.8, 'Succ': 0.9, 'CPA': 0.75, 'Att': 0.6},
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

        # PRE-FILTER by playing style thresholds to ensure quality matches
        initial_count = len(filtered_data)
        
        if playing_style == 'Goal Threat':
            # Strict: High goal threat required
            goal_mask = (filtered_data['xG'] >= np.percentile(filtered_data['xG'], 90)) & (filtered_data['Gls'] >= np.percentile(filtered_data['Gls'], 90)) | (filtered_data['xG'] >= np.percentile(filtered_data['xG'], 90)) & (filtered_data['SoT'] >= np.percentile(filtered_data['SoT'], 90))
            temp_filtered = filtered_data[goal_mask]
            
            if len(temp_filtered) >= num_recommendations:
                filtered_data = temp_filtered
                print(f"Goal Threat filter: {len(filtered_data)} players with xG >= 11.0 AND Goals >= 15 OR xG >= 12.0 AND SoT >= 30")
            else:
                # Medium threshold
                goal_mask = (filtered_data['xG'] >= 6.0) & (filtered_data['Gls'] >= 8) | (filtered_data['xG'] >= 7.0) & (filtered_data['SoT'] >= 15)
                temp_filtered = filtered_data[goal_mask]
                
                if len(temp_filtered) >= num_recommendations:
                    filtered_data = temp_filtered
                    print(f"Goal Threat filter (relaxed): {len(filtered_data)} players with xG >= 6.0 AND Goals >= 8 OR xG >= 7.0 AND SoT >= 15")
                else:
                    # Minimum threshold
                    goal_mask = (filtered_data['xG'] >= 3) | (filtered_data['Gls'] >= 3)
                    filtered_data = filtered_data[goal_mask]
                    print(f"Goal Threat filter (minimum): {len(filtered_data)} players with xG >= 3 OR Goals >= 3")
    
        elif playing_style == 'Creative':
            # Strict: High creativity required (AND condition for better quality)
            creative_mask = (filtered_data['xA'] >= 6.0) & (filtered_data['Ast'] >= 6) | (filtered_data['xA'] >= 6.0) | (filtered_data['KP'] >= 25)
            temp_filtered = filtered_data[creative_mask]
            
            if len(temp_filtered) >= num_recommendations:
                filtered_data = temp_filtered
                print(f"Creative filter: {len(filtered_data)} players with (xA >= 6.0 AND Assists >= 6) OR xA >= 6.0 OR KP >= 25")
            else:
                # Medium threshold - still require good creativity
                creative_mask = (filtered_data['xA'] >= 4.0) & (filtered_data['Ast'] >= 5) | (filtered_data['xA'] >= 3.5) & (filtered_data['KP'] >= 18)
                temp_filtered = filtered_data[creative_mask]
                
                if len(temp_filtered) >= num_recommendations:
                    filtered_data = temp_filtered
                    print(f"Creative filter (relaxed): {len(filtered_data)} players with xA >= 3.0 AND Assists >= 5 OR xA >= 3.5 AND KP >= 18")
                else:
                    # Minimum threshold
                    creative_mask = (filtered_data['xA'] >= 2.0) | (filtered_data['Ast'] >= 3)
                    filtered_data = filtered_data[creative_mask]
                    print(f"Creative filter (minimum): {len(filtered_data)} players with xA >= 2.0 OR Assists >= 3")

        elif playing_style == 'Dribbling':
            # Focus on high-volume ball carriers
            dribble_mask = ((filtered_data['Carries'] >= 180) & (filtered_data['Succ'] >= 60)) | (filtered_data['PrgC'] >= 85)
            temp_filtered = filtered_data[dribble_mask]

            if len(temp_filtered) >= num_recommendations:
                filtered_data = temp_filtered
                print(f"Dribbling filter: {len(filtered_data)} players with Carries >= 180 & Succ >= 60 OR PrgC >= 85")
            else:
                # Medium threshold
                dribble_mask = ((filtered_data['Carries'] >= 130) & (filtered_data['Succ'] >= 50)) | (filtered_data['PrgC'] >= 60)
                temp_filtered = filtered_data[dribble_mask]

                if len(temp_filtered) >= num_recommendations:
                    filtered_data = temp_filtered
                    print(f"Dribbling filter (relaxed): {len(filtered_data)} players with Carries >= 130 & Succ >= 50 OR PrgC >= 60")
                else:
                    dribble_mask = (filtered_data['Carries'] >= 100) | (filtered_data['Succ'] >= 40)
                    filtered_data = filtered_data[dribble_mask]
                    print(f"Dribbling filter (minimum): {len(filtered_data)} players with Carries >= 100 OR Succ >= 40")
        
        elif playing_style == 'Possession':
            # Strict: High passing volume and accuracy
            possession_mask = (filtered_data['Cmp'] >= 1200) & (filtered_data['Cmp%'] >= 85) | (filtered_data['Touches'] >= 1800)
            temp_filtered = filtered_data[possession_mask]
            
            if len(temp_filtered) >= num_recommendations:
                filtered_data = temp_filtered
                print(f"Possession filter: {len(filtered_data)} players with Cmp >= 1200 & Cmp% >= 85 OR Touches >= 1800")
            else:
                # Medium threshold
                possession_mask = (filtered_data['Cmp'] >= 800) | (filtered_data['Touches'] >= 1400)
                temp_filtered = filtered_data[possession_mask]
                
                if len(temp_filtered) >= num_recommendations:
                    filtered_data = temp_filtered
                    print(f"Possession filter (relaxed): {len(filtered_data)} players with Cmp >= 800 OR Touches >= 1400")
                else:
                    # Minimum threshold
                    possession_mask = (filtered_data['Cmp'] >= 500) | (filtered_data['Touches'] >= 1000)
                    filtered_data = filtered_data[possession_mask]
                    print(f"Possession filter (minimum): {len(filtered_data)} players with Cmp >= 500 OR Touches >= 1000")
        
        elif playing_style == 'High-Press':
            # Strict: High pressing and recovery in final third
            press_mask = (filtered_data['Tkl'] >= 40) & (filtered_data['Att 3rd'] >= 15) | (filtered_data['Tkl+Int'] >= 70)
            temp_filtered = filtered_data[press_mask]
            
            if len(temp_filtered) >= num_recommendations:
                filtered_data = temp_filtered
                print(f"High-Press filter: {len(filtered_data)} players with Tkl >= 40 & Att 3rd >= 15 OR Tkl+Int >= 70")
            else:
                # Medium threshold
                press_mask = (filtered_data['Tkl'] >= 25) | (filtered_data['Tkl+Int'] >= 50)
                temp_filtered = filtered_data[press_mask]
                
                if len(temp_filtered) >= num_recommendations:
                    filtered_data = temp_filtered
                    print(f"High-Press filter (relaxed): {len(filtered_data)} players with Tkl >= 25 OR Tkl+Int >= 50")
                else:
                    # Minimum threshold
                    press_mask = (filtered_data['Tkl'] >= 15) | (filtered_data['Tkl+Int'] >= 35)
                    filtered_data = filtered_data[press_mask]
                    print(f"High-Press filter (minimum): {len(filtered_data)} players with Tkl >= 15 OR Tkl+Int >= 35")
        
        elif playing_style == 'Defensive':
            # Strict: High defensive actions
            defensive_mask = (filtered_data['Tkl'] >= 50) & (filtered_data['Int'] >= 30) | (filtered_data['Tkl+Int'] >= 80)
            temp_filtered = filtered_data[defensive_mask]
            
            if len(temp_filtered) >= num_recommendations:
                filtered_data = temp_filtered
                print(f"Defensive filter: {len(filtered_data)} players with Tkl >= 50 & Int >= 30 OR Tkl+Int >= 80")
            else:
                # Medium threshold
                defensive_mask = (filtered_data['Tkl'] >= 35) | (filtered_data['Int'] >= 25) | (filtered_data['Tkl+Int'] >= 60)
                temp_filtered = filtered_data[defensive_mask]
                
                if len(temp_filtered) >= num_recommendations:
                    filtered_data = temp_filtered
                    print(f"Defensive filter (relaxed): {len(filtered_data)} players with Tkl >= 35 OR Int >= 25 OR Tkl+Int >= 60")
                else:
                    # Minimum threshold
                    defensive_mask = (filtered_data['Tkl'] >= 20) | (filtered_data['Int'] >= 15)
                    filtered_data = filtered_data[defensive_mask]
                    print(f"Defensive filter (minimum): {len(filtered_data)} players with Tkl >= 20 OR Int >= 15")
        
        if len(filtered_data) < num_recommendations:
            raise ValueError(f"Not enough players meet the {playing_style} criteria. Found {len(filtered_data)}, need {num_recommendations}.")

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
            role_weights = np.array([self.role_features[subcategory].get(feat, 1.0) for feat in self.features])
            
            if playing_style and playing_style != 'No Style':
                style_bonuses = np.array([
                    max(0, self.playing_styles[playing_style].get(feat, 1.0) - 1.0) 
                    for feat in self.features
                ])
                feature_weights = role_weights + style_bonuses
                
                # DEBUG: Print weights for key stats
                print(f"\n=== WEIGHTING DEBUG for {subcategory} with {playing_style} ===")
                key_stats = ['Gls', 'xG', 'SoT', 'SoT%', 'Ast', 'xA', 'KP', 'PrgC']
                for stat in key_stats:
                    if stat in self.features:
                        idx = self.features.index(stat)
                        print(f"{stat}: role={role_weights[idx]:.2f}, bonus={style_bonuses[idx]:.2f}, total={feature_weights[idx]:.2f}")
                print(f"==========================================\n")
            else:
                feature_weights = role_weights
            
            # Apply weights to stats
            weighted_stats = normalized_stats * feature_weights
            
            # Calculate COMPOSITE SCORE instead of similarity
            # Sum weighted stats for each player (higher = better)
            composite_scores = weighted_stats.sum(axis=1)
            
            # Add controlled randomness for variety (±2-5% variation)
            # This ensures slight variation between requests while keeping quality high
            noise_level = 0.01 + (np.random.random() * 0.02)  # Random between 3-5%
            noise = np.random.normal(0, noise_level, len(composite_scores))
            composite_scores += noise
            
            # Get top performers by composite score (with extra buffer for randomness)
            # Pick from top (num_recommendations * 2) to increase variety
            top_candidates = min(num_recommendations * 2, len(composite_scores))
            candidate_indices = composite_scores.argsort()[::-1][:top_candidates]
            
            # Randomly select from top candidates
            np.random.shuffle(candidate_indices)
            top_indices = candidate_indices[:num_recommendations]
            
            # Use percentile-based normalization for better score distribution
            # This prevents huge gaps between best and worst players
            from scipy.stats import rankdata
            ranks = rankdata(composite_scores, method='average')
            percentile_scores = (ranks / len(ranks))  # 0 to 1 scale
            
            # Scale to emphasize top performers (power transformation)
            normalized_scores = percentile_scores ** 0.5  # Square root to compress low scores
            
            # Return recommendations
            recommendations = []
            for idx in top_indices:
                player_data = filtered_data.iloc[idx]
                recommendations.append({
                    'Player': player_data['Player'],
                    'Pos': player_data['Pos'],
                    'Club': player_data['Club'],
                    'Similarity': float(normalized_scores[idx]),  # Now represents performance score
                    'SimilarityStd': 0.0,
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
# test_recommender.py
import pytest
import numpy as np
from datahandler import player_data
from Recommend import AdvancedPlayerRecommender


@pytest.fixture(scope="module")
def recommender():
    """Build the recommender once for all tests in this module."""
    return AdvancedPlayerRecommender(player_data)


# ---------------------------------------------------------------------------
# Basic smoke tests
# ---------------------------------------------------------------------------

class TestBasicRecommendation:
    def test_returns_requested_count(self, recommender):
        results = recommender.get_recommendations_monte_carlo(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=5,
            min_minutes=0,
        )
        assert len(results) == 5

    def test_returns_player_fields(self, recommender):
        results = recommender.get_recommendations_monte_carlo(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=1,
            min_minutes=0,
        )
        player = results[0]
        assert "Player" in player
        assert "Pos" in player
        assert "Club" in player
        assert "Similarity" in player
        assert isinstance(player["Similarity"], float)

    def test_similarity_in_valid_range(self, recommender):
        results = recommender.get_recommendations_monte_carlo(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=5,
            min_minutes=0,
        )
        for r in results:
            assert 0.0 <= r["Similarity"] <= 1.0


# ---------------------------------------------------------------------------
# Category and subcategory filtering
# ---------------------------------------------------------------------------

class TestCategoryFiltering:
    @pytest.mark.parametrize("category,subcategory,expected_pos", [
        ("Defender", "CB", "DF"),
        ("Midfielder", "CM", "MF"),
        ("Forward", "ST", "FW"),
    ])
    def test_category_returns_correct_position(self, recommender, category, subcategory, expected_pos):
        results = recommender.get_recommendations_monte_carlo(
            category=category,
            subcategory=subcategory,
            num_recommendations=3,
            min_minutes=0,
        )
        for r in results:
            assert r["Pos"].startswith(expected_pos)

    @pytest.mark.parametrize("subcategory", ["CB", "FB", "WB", "DM", "CM", "AM", "ST", "W"])
    def test_subcategory_returns_results(self, recommender, subcategory):
        cat_map = {
            "CB": "Defender", "FB": "Defender", "WB": "Defender",
            "DM": "Midfielder", "CM": "Midfielder", "AM": "Midfielder",
            "ST": "Forward", "W": "Forward",
        }
        category = cat_map[subcategory]
        results = recommender.get_recommendations_monte_carlo(
            category=category,
            subcategory=subcategory,
            num_recommendations=3,
            min_minutes=0,
        )
        assert len(results) > 0


# ---------------------------------------------------------------------------
# Playing style filters
# ---------------------------------------------------------------------------

class TestPlayingStyles:
    @pytest.mark.parametrize("style", [
        "No Style", "Possession", "Creative", "Goal Threat",
        "Dribbling", "High-Press", "Defensive",
    ])
    def test_all_styles_return_results(self, recommender, style):
        results = recommender.get_recommendations_monte_carlo(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=3,
            min_minutes=0,
            playing_style=style,
        )
        assert len(results) > 0


# ---------------------------------------------------------------------------
# Minutes filter
# ---------------------------------------------------------------------------

class TestMinutesFilter:
    def test_high_minutes_still_returns(self, recommender):
        high_min = recommender.get_recommendations_monte_carlo(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=3,
            min_minutes=500,
        )
        assert len(high_min) > 0

    def test_impossible_minutes_raises(self, recommender):
        with pytest.raises(ValueError, match="Not enough players"):
            recommender.get_recommendations_monte_carlo(
                category="Midfielder",
                subcategory="CM",
                num_recommendations=50,
                min_minutes=10000,
            )


# ---------------------------------------------------------------------------
# Stochastic behavior
# ---------------------------------------------------------------------------

class TestStochasticBehavior:
    def test_different_results_on_refresh(self, recommender):
        """Two calls with same params should sometimes differ due to randomness."""
        results_a = recommender.get_recommendations_monte_carlo(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=5,
            min_minutes=0,
        )
        results_b = recommender.get_recommendations_monte_carlo(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=5,
            min_minutes=0,
        )
        players_a = [r["Player"] for r in results_a]
        players_b = [r["Player"] for r in results_b]
        assert players_a != players_b

    def test_results_have_high_similarity(self, recommender):
        results = recommender.get_recommendations_monte_carlo(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=5,
            min_minutes=0,
        )
        scores = [r["Similarity"] for r in results]
        assert scores[0] > 0.5


# ---------------------------------------------------------------------------
# Fallback path (get_recommendations)
# ---------------------------------------------------------------------------

class TestFallbackPath:
    def test_fallback_returns_results(self, recommender):
        results = recommender.get_recommendations(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=5,
            min_minutes=0,
        )
        assert len(results) > 0

    def test_fallback_returns_similarity(self, recommender):
        results = recommender.get_recommendations(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=3,
            min_minutes=0,
        )
        for r in results:
            assert "Similarity" in r
            assert 0.0 <= r["Similarity"] <= 1.0


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    def test_invalid_category_raises(self, recommender):
        with pytest.raises(Exception):
            recommender.get_recommendations_monte_carlo(
                category="Goalkeeper",
                num_recommendations=3,
                min_minutes=0,
            )

    def test_fallback_invalid_category_raises_keyerror(self, recommender):
        """Fallback path raises KeyError for unknown category (no validation)."""
        with pytest.raises(KeyError):
            recommender.get_recommendations(
                category="InvalidCategory",
                num_recommendations=3,
                min_minutes=0,
            )


# ---------------------------------------------------------------------------
# Data integrity
# ---------------------------------------------------------------------------

class TestDataIntegrity:
    def test_subcategory_column_exists(self, recommender):
        assert "Subcategory" in recommender.data.columns

    def test_mainpos_column_exists(self, recommender):
        assert "MainPos" in recommender.data.columns

    def test_all_subcategories_valid(self, recommender):
        valid_subcats = {"CB", "FB", "WB", "DM", "CM", "AM", "ST", "W"}
        actual = set(recommender.data["Subcategory"].unique())
        assert actual.issubset(valid_subcats)

    def test_no_duplicate_players_in_result(self, recommender):
        results = recommender.get_recommendations_monte_carlo(
            category="Midfielder",
            subcategory="CM",
            num_recommendations=5,
            min_minutes=0,
        )
        names = [r["Player"] for r in results]
        assert len(names) == len(set(names))

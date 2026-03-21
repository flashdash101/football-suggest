from fastapi import FastAPI, HTTPException
try:
    from .datahandler import player_data
    from .Recommend import AdvancedPlayerRecommender
    from .Models import RecommendationRequest, RecommendationResponse, PlayerRecommendation, PlayerStats
except ImportError:
    from datahandler import player_data
    from Recommend import AdvancedPlayerRecommender
    from Models import RecommendationRequest, RecommendationResponse, PlayerRecommendation, PlayerStats

app = FastAPI()

recommender = AdvancedPlayerRecommender(player_data)

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    try:
        recs = recommender.get_recommendations(
            request.category,
            request.subcategory,
            request.num_recommendations
        )
        return RecommendationResponse(
            recommendations=[
                PlayerRecommendation(
                    player=rec['Player'],
                    position=rec['Pos'],
                    club=rec['Club'],
                    similarity=rec['Similarity'],
                    stats=PlayerStats(**{
                        key: value for key, value in rec.items()
                        if key in PlayerStats.__fields__ and key not in ['Player', 'Pos', 'Club', 'Similarity']
                    })
                ) for rec in recs  # Changed from recs.iterrows()
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
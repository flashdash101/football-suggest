from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datahandler import player_data
from Recommend import AdvancedPlayerRecommender
from Models import RecommendationRequest, RecommendationResponse, PlayerRecommendation, PlayerStats

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #Allow all origins for simplicity; adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = AdvancedPlayerRecommender(player_data)

subcategory_mapping = {
    'Fullback': 'FB',
    'Wingback': 'WB',
    'Centreback': 'CB',
    'Defensive Midfielder': 'DM',
    'Central Midfielder': 'CM',
    'Attacking Midfielder': 'AM',
    'Winger': 'W',
    'Attacker': 'ST'
}

@app.post("/get_recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    try:
        mapped_subcategory = subcategory_mapping.get(request.subcategory, request.subcategory)
        recs = recommender.get_recommendations_monte_carlo(
            request.category,
            mapped_subcategory,
            request.num_recommendations,
            distance_metric='cosine',
            playing_style=request.playing_style
        )
        return RecommendationResponse(
            recommendations=[
                PlayerRecommendation(
                    player=rec['Player'],
                    position=rec['Pos'],
                    club=rec['Club'],
                    similarity=rec['Similarity'],
                    stats=PlayerStats(
                        Gls=rec.get('Gls'),
                        Ast=rec.get('Ast'),
                        xG=rec.get('xG'),
                        xA=rec.get('xA'),
                        Sh=rec.get('Sh'),
                        SoT=rec.get('SoT'),
                        KP=rec.get('KP'),
                        PrgP=rec.get('PrgP'),
                        PrgC=rec.get('PrgC'),
                        Tkl=rec.get('Tkl'),
                        Int=rec.get('Int'),
                        Clr=rec.get('Clr'),
                        Blocks=rec.get('Blocks'),
                        Pass = rec.get('Pass'),
                        CPA = rec.get('CPA'),
                        Att = rec.get('Att'),
                        Succ = rec.get('Succ'),
                        onethird = rec.get('onethird'),
                        Cmp = rec.get('Cmp'),
                        TklW = rec.get('TklW'),
                        minutes_played=rec.get('90s') * 90 if rec.get('90s') is not None else None
                        
                    )
                ) for rec in recs
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
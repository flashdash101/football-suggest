from pydantic import BaseModel, Field
from typing import List, Optional, Dict


#Create the model which stores the features.
class PlayerStats(BaseModel):
    goals: Optional[int] = Field(alias='Gls', default=None)
    shots: Optional[int] = Field(alias='Sh', default=None)
    shots_on_target: Optional[int] = Field(alias='SoT', default=None)
    xG: Optional[float] = None
    xA: Optional[float] = None
    assists: Optional[int] = Field(alias='Ast', default=None)
    key_passes: Optional[int] = Field(alias='KP', default=None)
    progressive_passes: Optional[int] = Field(alias='PrgP', default=None)
    progressive_carries: Optional[int] = Field(alias='PrgC', default=None)
    tackles: Optional[int] = Field(alias='Tkl', default=None)
    interceptions: Optional[int] = Field(alias='Int', default=None)
    blocks: Optional[int] = Field(alias='Blocks', default=None)
    clearances: Optional[int] = Field(alias='Clr', default=None)
    Passes: Optional[int] = Field(alias='Pass', default=None)
    CPA: Optional[int] = Field(alias='CPA', default=None)
    Att: Optional[int] = Field(alias='Att', default=None)
    Succ : Optional[int] = Field(alias='Succ', default=None)
    onethird: Optional[float] = Field(alias='onethird', default=None)
    cmp: Optional[int] = Field(alias='Cmp', default=None)
    TklW: Optional[int] = Field(alias='TklW', default=None)

    class Config:
        populate_by_name = True

class PlayerRecommendation(BaseModel):
    player: str
    position: str
    club: str
    similarity: float
    stats: PlayerStats

class RecommendationRequest(BaseModel):
    category: str
    subcategory: Optional[str] = None
    num_recommendations: int = 5
    playing_style: Optional[str] = None
    min_minutes: int = 0
    distance_metric: str = 'pearson'
class RecommendationResponse(BaseModel):
    recommendations: List[PlayerRecommendation]
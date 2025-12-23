from pydantic import BaseModel,Field

class PredictionResponce(BaseModel):
    predicted_category: str = Field(...,description="The predicted category for are customers are likely to be expensive",example="high")
    probability_high_risk : float = Field(...,description="Confidance score for more like to be predicted_category (range: 0 to 1)")
    threshold_used: float = Field(...,description="threshold for set boundery or set rule",example=0.3)

class responce(BaseModel):
    predicted_category: int= Field(...,description="The predicted category for are customers are likely to be expensive",example= 0)







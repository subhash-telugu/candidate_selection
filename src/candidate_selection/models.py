from pydantic import BaseModel


class candidate(BaseModel):
    id:int
    name:str
    email:str
    bio:str
    skills:str


class candidateScore(BaseModel):
    id:int
    score:int
    reason:str


class scoredcandidate(BaseModel):
    id:int
    name:str
    email:str
    bio:str
    skills:str
    score:int
    reason:str
        



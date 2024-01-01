from pydantic import BaseModel
    
class Cat(BaseModel):
    id: str
    url: str 
    width: int
    height: int   
    breed_id: str
    
class Breed(BaseModel):
    id: str
    name: str
    cfa_url: str
    vetstreet_url: str
    vcahospitals_url: str
    temperament: str
    origin: str
    country_codes: str
    description: str
    life_span: str
    indoor: int
    lap: int
    alt_names: str
    adaptability: int
    affection_level: int
    child_friendly: int
    dog_friendly: int
    energy_level: int
    grooming: int
    health_issues: int
    intelligence: int
    shedding_level: int
    social_needs: int
    stranger_friendly: int
    vocalisation: int
    experimental: int
    hairless: int
    natural: int
    rare: int
    rex: int
    suppressed_tail: int
    short_legs: int
    wikipedia_url: str
    hypoallergenic: int
    reference_image_id: str
    imperial: str
    metric: str   
    
class Category(BaseModel):
    id: int
    name: str 
    
class CatRespone(BaseModel):
    id: str
    url: str 

    class Config:
        orm_model = True
    
class CategoryRespone(BaseModel):
    name: str

    class Config:
        orm_model = True      
        
class BreedResponse(BaseModel):
    id: str
    name: str
    temperament: str
    description: str
    
    class Config:
        orm_model = True        
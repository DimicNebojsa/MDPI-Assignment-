from fastapi import FastAPI, Depends, status, HTTPException, Response
import requests
import models
from models import Post
from database import engine, get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
import extract


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str  
    published: bool = True
    
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

#extract.update_sql(1, verbose=True)


@app.post("/cat", status_code=status.HTTP_201_CREATED)
def create_cat(cat: Cat, db: Session = Depends(get_db)):
    #new_post = models.Cat(id=cat.id, 
    #                      url=cat.url, 
    #                      width=cat.width,
    #                      height=cat.height, 
    #                      breed_id=cat.breed_id)

    new_post = models.Cat(**cat.dict())
    db.add(new_post)
    db.commit()
    #db.refresh(new_post)
    return {"data": new_post}

@app.post("/category", status_code=status.HTTP_201_CREATED)
def create_breed(category: Category, db: Session = Depends(get_db)):

    new_post = models.Category(**category.dict())
    db.add(new_post)
    db.commit()
    #db.refresh(new_post)
    return {"data": new_post}


@app.get("/breed/get/{breed}")
def get_breed(breed:str, db: Session=Depends(get_db)):
    breed = db.query(models.Breed).filter(models.Breed.id == breed).all()
    
    if not breed:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return {"breed": breed}

@app.get("/category/{category}")
def get_category(category:str, db: Session=Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category).all()
    
    if not category:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return {"category": category}

@app.get("/cat/{id}")
def get_cat(id:str, db: Session=Depends(get_db)):
    cat = db.query(models.Cat).filter(models.Cat.id == id).all()
    
    if not cat:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return {"cat": cat}

@app.delete("/cat/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(id: str, db: Session = Depends(get_db)) -> None:
    cat = db.query(models.Cat).filter(models.Cat.id == id)      
    
    if cat.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cat with id: {id} does not exist")
    cat.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)    

@app.delete("/category/delete/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(name: str, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.name == name)      
    
    if category.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with name: {name} does not exist")
    category.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)  
 
@app.delete("/breed/delete/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_breed(name: str, db: Session = Depends(get_db)):
    breed = db.query(models.Breed).filter(models.Breed.id == name)      
    
    if breed.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Breed with name: {name} does not exist")
    breed.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)    

@app.delete("/cat_category/delete/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat_category(cat_id: str, db: Session = Depends(get_db)):
    cat_category = db.query(models.Cat_Category).filter(models.Cat_Category.cat_id == cat_id)      
    
    if cat_category.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cat_Category with name: {cat_id} does not exist")
    cat_category.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@app.put("/cat/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_cat(id: str, updated_cat: Cat, db: Session = Depends(get_db)):
    update_query = db.query(models.Cat).filter(models.Cat.id == id)
    post = update_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cat with id: {id} does not exist")
        
    update_query.update(updated_cat.dict(), synchronize_session=False)    
    
    db.commit()
    
    return {"message": "success"} 

@app.put("/category/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_category(id: int, updated_category: Category, db: Session = Depends(get_db)):
    update_query = db.query(models.Category).filter(models.Category.id == id)
    post = update_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {id} does not exist")
    
    aaa = updated_category.dict()
    print(aaa)
        
    update_query.update(updated_category.dict(), synchronize_session=False)    
    
    db.commit()
    
    return {"message": "success"} 


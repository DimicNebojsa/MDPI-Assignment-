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

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    
    return {"data": posts}  

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM Posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(cat: Cat, db: Session = Depends(get_db)):
    #new_post = models.Cat(id=cat.id, 
    #                      url=cat.url, 
    #                      width=cat.width,
    #                      height=cat.height)

    new_post = models.Cat(**cat.dict())
    print(new_post)
    db.add(new_post)
    db.commit()
    #db.refresh(new_post)
    return {"data": new_post}

#####
@app.get("/breed/{breed}")
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

#####

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.published == True).all()
    print(post)
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)) -> None:
    post = db.query(models.Post).filter(models.Post.id == id)      
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)) ->None:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    post_query.update(updated_post.dict(), synchronize_session=False)    
    
    db.commit()
    
    return {"message": "success"}   

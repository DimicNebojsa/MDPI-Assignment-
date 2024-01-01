from fastapi import FastAPI, Depends, status, HTTPException, Response
import models
from database import engine, get_db
from sqlalchemy.orm import Session
import schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#extract.update_sql(1, verbose=True)


@app.post("/cat", status_code=status.HTTP_201_CREATED, response_model=schemas.CatRespone)
def create_cat(cat: schemas.Cat, db: Session = Depends(get_db)):
    #new_post = models.Cat(id=cat.id, 
    #                      url=cat.url, 
    #                      width=cat.width,
    #                      height=cat.height, 
    #                      breed_id=cat.breed_id)

    new_post = models.Cat(**cat.dict())
    db.add(new_post)
    db.commit()
    #db.refresh(new_post)
    return new_post

@app.post("/category", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryRespone)
def create_category(category: schemas.Category, db: Session = Depends(get_db)):

    new_post = models.Category(**category.dict())
    db.add(new_post)
    db.commit()
    #db.refresh(new_post)
    return new_post


@app.get("/breed/get/{breed}", response_model = schemas.BreedResponse)
def get_breed(breed: str, db: Session=Depends(get_db)):
    breed = db.query(models.Breed).filter(models.Breed.id == breed).all()
    
    if not breed:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return breed[0]

@app.get("/category/{category}", response_model=schemas.CategoryRespone)
def get_category(category: str, db: Session=Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category).all()
    
    if not category:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return category[0]

@app.get("/cat/{id}", response_model=schemas.CatRespone)
def get_cat(id: str, db: Session=Depends(get_db)):
    cat = db.query(models.Cat).filter(models.Cat.id == id).all()
    
    if not cat:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return cat[0]

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


@app.put("/cat/update/{id}", response_model=schemas.CatRespone)
def update_cat(id: str, updated_cat: schemas.Cat, db: Session = Depends(get_db)):
    update_query = db.query(models.Cat).filter(models.Cat.id == id)
    post = update_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cat with id: {id} does not exist")
        
    update_query.update(updated_cat.dict(), synchronize_session=False)    
    
    db.commit()
    
    return post

@app.put("/category/update/{id}", response_model=schemas.CategoryRespone)
def update_category(id: int, updated_category: schemas.Category, db: Session = Depends(get_db)):
    update_query = db.query(models.Category).filter(models.Category.id == id)
    post = update_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {id} does not exist")
    
        
    update_query.update(updated_category.dict(), synchronize_session=False)    
    
    db.commit()
    
    return post


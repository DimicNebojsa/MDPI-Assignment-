"""Examples of CRUD operations using FastAPI.

Author: Nebojsa Dimic
Date: 1/2/2024
"""

from fastapi import FastAPI, Depends, status, HTTPException, Response
import models
from database import engine, get_db
from sqlalchemy.orm import Session
import app.schemas as schemas
from create_tables import CreateTables
from extract_class import Extract


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

URL_TEST = "https://api.thecatapi.com/v1/images/search?limit=100&api_key="
API_KEY_TEST = "live_LeTQOlg1Yf7kbymctS8792u6PliZpvMVMlRATtIONbuDIZ1MU0UANifkDzCGuzeU"

createTables = CreateTables()
extract_class = Extract(URL_TEST, API_KEY_TEST, createTables)
extract_class.update_sql(1, verbose=True)


@app.post("/cat", status_code=status.HTTP_201_CREATED, response_model=schemas.CatRespone)
def create_cat(cat: schemas.Cat, db: Session = Depends(get_db)) -> models.Cat:
    """Performs insert into Cat table."""
    """
        Args:
            cat (Cat): Pydantic Cat object.
                
        Excpetions:
            None

        Returns:
            Pydantic CatResponse object.
    """  

    new_post = models.Cat(**cat.dict())
    db.add(new_post)
    db.commit()
    return new_post

@app.post("/category", status_code=status.HTTP_201_CREATED, 
          response_model=schemas.CategoryRespone)
def create_category(category: schemas.Category, 
                    db: Session = Depends(get_db)) -> models.Category:
    """Performs insert into Category table."""
    """
        Args:
            cat (Cat): Pydantic Cat object.
                
        Excpetions:
            None

        Returns:
            Pydantic Category object.
    """ 

    new_post = models.Category(**category.dict())
    db.add(new_post)
    db.commit()
    #db.refresh(new_post)
    return new_post


@app.get("/breed/get/{breed}", response_model = schemas.BreedResponse)
def get_breed(breed: str, db: Session=Depends(get_db)) -> models.Breed:
    """Performs select from Breed table by supplied breed name."""
    """
        Args:
            breed (str): Name of breed.
                
        Excpetions:
            None

        Returns:
            Pydantic Breed object.
    """ 
    
    breed = db.query(models.Breed).filter(models.Breed.id == breed).all()
    
    if not breed:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return breed[0]

@app.get("/category/{category}", response_model=schemas.CategoryRespone)
def get_category(category: str, db: Session=Depends(get_db)) -> models.Category:
    """Performs select from Category table by supplied category id."""
    """
        Args:
            category (str): Category id.
                
        Excpetions:
            None

        Returns:
            Pydantic Category object.
    """ 
    category = db.query(models.Category).filter(models.Category.id == category).all()
    
    if not category:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return category[0]

@app.get("/cat/{id}", response_model=schemas.CatRespone)
def get_cat(id: str, db: Session=Depends(get_db)) -> models.Cat:
    """Performs select from Cat table by supplied cat id."""
    """
        Args:
            cat (str): cat id.
                
        Excpetions:
            None

        Returns:
            Pydantic Cat object.
    """ 
    cat = db.query(models.Cat).filter(models.Cat.id == id).all()
    
    if not cat:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return cat[0]

@app.delete("/cat/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(id: str, db: Session = Depends(get_db)) -> None:
    """Performs delete from Cat table by supplied cat id."""
    """
        Args:
            cat (Cat): cat id.
                
        Excpetions:
            None

        Returns:
            None
    """ 
    cat = db.query(models.Cat).filter(models.Cat.id == id)      
    
    if cat.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cat with id: {id} does not exist")
    cat.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)    

@app.delete("/category/delete/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(name: str, db: Session = Depends(get_db)) -> None:
    """Performs delete from Category table by supplied category id."""
    """
        Args:
            category (str): category id.
                
        Excpetions:
            None

        Returns:
            None
    """ 
    category = db.query(models.Category).filter(models.Category.name == name)      
    
    if category.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with name: {name} does not exist")
    category.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)  
 
@app.delete("/breed/delete/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_breed(name: str, db: Session = Depends(get_db)) -> None:
    """Performs delete from Breed table by supplied breed id."""
    """
        Args:
            breed (str): breed id.
                
        Excpetions:
            None

        Returns:
            None
    """ 
    breed = db.query(models.Breed).filter(models.Breed.id == name)      
    
    if breed.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Breed with name: {name} does not exist")
    breed.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)    

@app.delete("/cat_category/delete/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat_category(cat_id: str, db: Session = Depends(get_db)) -> None:
    """Performs delete from Cat_Category table by supplied cat id."""
    """
        Args:
            cat_id (str): cat id.
                
        Excpetions:
            None

        Returns:
            None
    """ 
    cat_category = db.query(models.Cat_Category).filter(
        models.Cat_Category.cat_id == cat_id)      
    
    if cat_category.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cat_Category with name: {cat_id} does not exist")
    cat_category.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@app.put("/cat/update/{id}", response_model=schemas.CatRespone)
def update_cat(id: str, updated_cat: schemas.Cat, 
               db: Session = Depends(get_db)) -> models.Cat:
    """Updates Cat table by supplied cat id."""
    """
        Args:
            id (str): cat id.
                
        Excpetions:
            None

        Returns:
            None
    """ 
    update_query = db.query(models.Cat).filter(models.Cat.id == id)
    post = update_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cat with id: {id} does not exist")
        
    update_query.update(updated_cat.dict(), synchronize_session=False)    
    
    db.commit()
    
    return post

@app.put("/category/update/{id}", response_model=schemas.CategoryRespone)
def update_category(id: int, updated_category: schemas.Category, 
                    db: Session = Depends(get_db)) -> models.Category:
    """Performs update to Category table by supplied category id."""
    """
        Args:
            id (str): category id.
                
        Excpetions:
            None

        Returns:
            None
    """ 
    update_query = db.query(models.Category).filter(models.Category.id == id)
    post = update_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {id} does not exist")
    
        
    update_query.update(updated_category.dict(), synchronize_session=False)    
    
    db.commit()
    
    return post


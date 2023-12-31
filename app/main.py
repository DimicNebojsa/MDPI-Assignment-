from fastapi import FastAPI, Depends, status, HTTPException, Response
import requests
import models
from models import Post
from database import engine, get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
import extract

GECKO_COIN_URL = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd"
STAR_WARS_URL = "https://swapi.dev/api/"

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

extract.update_sql(10, verbose=True)

@app.get("/starwars")
def get_star_wars_data():
    result = []
    count = 1

    for i in range(17,18):
        star_wars_data = requests.get(STAR_WARS_URL + "people/" + str(i) + "/").json()
        print(STAR_WARS_URL + "people/" + str(i) + "/")
        result.append((count, star_wars_data))
        count += 1
    return result

#result = get_star_wars_data()
#print(result)
#print(len(result))

URL =  "https://api.thecatapi.com/v1/breeds"
URL_SEARCH = "https://api.thecatapi.com/v1/images/search?limit=10&breed_ids={}&api_key="
API_KEY = "live_LeTQOlg1Yf7kbymctS8792u6PliZpvMVMlRATtIONbuDIZ1MU0UANifkDzCGuzeU "
cat_data = requests.get(URL).json()

#breeds = []
#for i in range(len(cat_data)):
#    breeds.append(cat_data[i]["id"])
    
def breed_search(breed: str, limit: int) -> list[dict]:
    breed_id = "breed_ids=" + breed
    limit_size = "limit=" + str(limit)
    URL = "https://api.thecatapi.com/v1/images/search?" + limit_size + "&" + breed_id + "&api_key="
    #URL_TEST = "https://api.thecatapi.com/v1/images/search?limit=200&breed_ids=beng&page=100&api_key=live_LeTQOlg1Yf7kbymctS8792u6PliZpvMVMlRATtIONbuDIZ1MU0UANifkDzCGuzeU"
    search_result = requests.get(URL + API_KEY).json()
    return search_result, URL

def search_all_breeds(breeds: list[str]) ->list[list[dict]]:
    result = []
    counter = 1
    for breed in breeds:
        print(str(counter) + " " + breed)
        result.append(breed_search(breed, 1000))
        counter += 1
    return result    

#aaa, URL = breed_search("abys", 100)
#aaa = search_all_breeds(breeds)

#print(aaa[14])
#print(breeds)
   
   
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
#@app.post("/posts", status_code=status.HTTP_201_CREATED)
#def create_posts(post: Post, db: Session = Depends(get_db)):
    #new_post = models.Post(title=post.title, 
    #                       content=post.content, 
    #                       published=post.published)
#    new_post = models.Post(**post.dict())
#    db.add(new_post)
#    db.commit()
#    db.refresh(new_post)
#    return {"data": new_post}

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

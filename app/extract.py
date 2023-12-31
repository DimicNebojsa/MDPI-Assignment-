import requests
from sqlalchemy import insert, Table, MetaData, Column, Integer, String
from database import engine


URL_TEST = "https://api.thecatapi.com/v1/images/search?limit=100&api_key="
API_KEY_TEST = "live_LeTQOlg1Yf7kbymctS8792u6PliZpvMVMlRATtIONbuDIZ1MU0UANifkDzCGuzeU"

def create_Cat_Table(table_name: str) -> Table:
    
    metadata_obj = MetaData()
    cat_table = Table(table_name, metadata_obj, 
                      Column("id", String, primary_key=True, nullable=False),
                      Column("url", String, nullable=False),
                      Column("width", Integer, nullable=False),
                      Column("height", Integer, nullable=False),
                      Column("breed_id", String, nullable=True))
    return cat_table

def create_Category_Table(table_name: str) -> Table:
    
    metadata_obj = MetaData()
    category_table = Table(table_name, metadata_obj, 
                      Column("id", Integer, primary_key=True, nullable=False),
                      Column("name", String, nullable=False))
    return category_table   

def create_Cat_Category_Table(table_name: str) -> Table:
    
    metadata_obj = MetaData()
    category_table = Table(table_name, metadata_obj, 
                      Column("cat_id", String, primary_key=True, nullable=False),
                      Column("category_id", Integer, primary_key=True, nullable=False))
    return category_table  

def create_Breed_Table(table_name: str) -> Table:
    
    metadata_obj = MetaData()
    breed_table = Table(table_name, metadata_obj, 
                           Column("id", String, primary_key=True, nullable=True), 
                           Column("name", String, nullable=True), 
                           Column("cfa_url", String, nullable=True), 
                           Column("vetstreet_url", String, nullable=True), 
                           Column("vcahospitals_url", String, nullable=True),
                           Column("temperament", String, nullable=True),
                           Column("origin", String, nullable=True),
                           Column("country_codes", String, nullable=True),
                           Column("description", String, nullable=True), 
                           Column("life_span", String, nullable=True),
                           Column("indoor", Integer, nullable = True),
                           Column("lap", Integer, nullable=True), 
                           Column("alt_names", String, nullable=True), 
                           Column("adaptability", Integer, nullable=True),
                           Column("affection_level", Integer, nullable=True),
                           Column("child_friendly", Integer, nullable=True), 
                           Column("dog_friendly", Integer, nullable=True), 
                           Column("energy_level", Integer, nullable=True), 
                           Column("grooming", Integer, nullable=True),
                           Column("health_issues", Integer, nullable=True),
                           Column("intelligence" , Integer, nullable=True),
                           Column("shedding_level", Integer, nullable=True),
                           Column("social_needs", Integer, nullable=True),
                           Column("stranger_friendly", Integer, nullable=True),
                           Column("vocalisation", Integer, nullable=True),
                           Column("experimental", Integer, nullable=True),
                           Column("hairless", Integer, nullable=True),
                           Column("natural", Integer, nullable=True),
                           Column("rare", Integer, nullable=True),
                           Column("rex", Integer, nullable=True),
                           Column("suppressed_tail", Integer, nullable=True),
                           Column("short_legs", Integer, nullable=True),
                           Column("wikipedia_url", String, nullable=True),
                           Column("hypoallergenic", Integer, nullable=True),
                           Column("reference_image_id", String, nullable=True),
                           Column("imperial", String, nullable=True),
                           Column("metric", String, nullable=True))
    return breed_table  
 

cat_table = create_Cat_Table("Cat")
category_table = create_Category_Table("Category")
cat_category_table = create_Cat_Category_Table("Cat_Category")
breed_table = create_Breed_Table("Breed")


def get_batch(url: str, api_key: str) -> list[dict]:
    """test_function does blah blah blah.

    :param p1: describe about parameter p1
    :param p2: describe about parameter p2
    :param p3: describe about parameter p3
    :return: describe what it returns
    """ 
    try:
        search_result = requests.get(url + api_key).json()
    except:
        print("SKIPPING...")    
        return None
    return search_result

def unpack_batch(batch: list[dict], target_list: list[dict]) ->list[dict]:
    for idx in range(len(batch)):
        target_list.append(batch[idx])
    return target_list    


def get_raw_data(number_of_batches: int, url: str, api_key: str, verbose: bool) ->list[dict]:
    raw_data = []
    counter = 0
    for idx in range(number_of_batches):
        result = get_batch(url, api_key)
        if result is not None:
            unpack_batch(result, raw_data)
        
        counter += 1
        if counter % 100 == 0:
            if verbose:
                print(f"Batch number {idx} is downloaded...") 
                   
            
    return raw_data    

def extract_cat(cat: dict) ->dict:
    id = cat["id"]
    url = cat["url"]
    width = cat["width"]
    height = cat["height"]   
    return {"id": id, "url": url, "width": width, "height": height}

def extract_category(cat: dict) ->dict:
    if cat.get("categories",0) != 0:
        category = cat["categories"][0]
        id = category["id"]
        name = category['name']
        return {"id": id, "name": name}    
    else:
        return None    
    
def extract_cat_category(cat: dict) ->dict:
    if cat.get("categories",0) != 0:
        category = cat["categories"][0]
        category_id = category["id"]     
        cat_id = cat["id"]
        return {"cat_id": cat_id, "category_id": category_id}
    else:
        return None


def extract_breed(breed: dict) -> dict:
    
    attributes = ["id", "name", "cfa_url", "vetstreet_url", "vcahospitals_url", "temperament", "origin", \
                 "country_codes", "description", "life_span", "indoor", "lap", "alt_names", \
                 "adaptability", "affection_level", "child_friendly", "dog_friendly", "energy_level", \
                 "grooming", "health_issues", "intelligence", "shedding_level", "social_needs", \
                 "stranger_friendly", "vocalisation", "experimental", "hairless", "natural", "rare", \
                 "rex", "suppressed_tail", "short_legs", "wikipedia_url", "hypoallergenic", \
                 "reference_image_id"]

    result = {}
    for attr in attributes:
        result[attr] = 0
            
    breeds = breed['breeds']
    if len(breeds) > 0:
        
        weight = breeds[0]["weight"]
        result["imperial"] = weight['imperial']
        result['metric'] = weight['metric']
    
        for attr in attributes:
            if breeds[0].get(attr, 0) != 0:
                result[attr] = breeds[0][attr]
        return result        
    else:
        return None      
    
def cat_housekeeping(housekeeping: dict, cat: dict):
    if cat['id'] not in housekeeping:
        housekeeping[cat["id"]] = 1 
    return housekeeping    
                               

def update_sql(iter: int, verbose: bool) ->None:
    print("STARTING.....")
    
    housekeeping = {}
    
    raw_data = get_raw_data(iter, URL_TEST, API_KEY_TEST, verbose=verbose)
     
    counter = 0
    breed_counter = 0 
    cat_counter = 0
    cat_category_counter = 0
    
    for data in raw_data:
         
        cat = extract_cat(data)
        category = extract_category(data)
        cat_category = extract_cat_category(data)
        breed = extract_breed(data)
        if breed is not None:
            cat["breed_id"] = breed["id"]
        else:
            cat["breed_id"] = "None"    

        if counter % 1000 == 0:
            print(counter)   
          
        try:
            with engine.connect() as conn: 
                _ = conn.execute(insert(cat_table), cat, ) 
                if breed is not None:
                    _ = conn.execute(insert(breed_table), breed, )
                    breed_counter += 1 
                if category is not None:
                    _ = conn.execute(insert(category_table), category, )
                if cat_category is not None:
                    _ = conn.execute(insert(cat_category_table), cat_category, )    
                    cat_category_counter += 1
                conn.commit()   
                housekeeping = cat_housekeeping(housekeeping, cat) 
        except:
            #print("Issue with writing to SQL base...") 
            #del housekeeping[str(cat["id"])]
            #print(f"Cat with id {cat["id"]} deleted")
            pass
                
        counter += 1     
    print("Cat counter is: " + str(len(housekeeping)))
    print("Breed counte is: " + str(breed_counter))  
    print("Cat_Category counter is: " + str(cat_category_counter))
    print("Counter is: " + str(counter))
    
    print('END....')
    
#update_sql(5, verbose=True)


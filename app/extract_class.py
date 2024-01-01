import requests
from sqlalchemy import insert, Table, MetaData, Column, Integer, String
from database import engine
from create_tables import CreateTables

class Extract:
    def __init__(self, url: str, api_key: str, createTables: CreateTables):
        self.__url = url
        self.__api_key = api_key
        self.cat_table = createTables.create_Cat_Table("Cat")
        self.category_table = createTables.create_Category_Table("Category")
        self.cat_category_table = createTables.create_Cat_Category_Table("Cat_Category")
        self.breed_table = createTables.create_Breed_Table("Breed")

    def __get_batch(self, url: str, api_key: str) -> list[dict]:
        """test_function does blah blah blah.

        :param p1: describe about parameter p1
        :param p2: describe about parameter p2
        :param p3: describe about parameter p3
        :return: describe what it returns
        """ 
        try:
            search_result = requests.get(url + api_key).json()
        except:
            #print("SKIPPING...")    
            return None
        return search_result

    def __unpack_batch(self, batch: list[dict], target_list: list[dict]) ->list[dict]:
        for idx in range(len(batch)):
            target_list.append(batch[idx])
        return target_list    


    def __get_raw_data(self, number_of_batches: int, url: str, api_key: str, verbose: True) ->list[dict]:
        raw_data = []
        counter = 0
        print("   Sending requests to CatAPI")
        for idx in range(number_of_batches):
            result = self._Extract__get_batch(url, api_key)
            if result is not None:
                self._Extract__unpack_batch(result, raw_data)
        
            counter += 1
            if counter % 5 == 0 and verbose:
                print(f"        Batch number {idx+1} is downloaded...") 
                   
            
        return raw_data    

    def __extract_cat(self, cat: dict) ->dict:
        id = cat["id"]
        url = cat["url"]
        width = cat["width"]
        height = cat["height"]   
        return {"id": id, "url": url, "width": width, "height": height}

    def __extract_category(self, cat: dict) ->dict:
        if cat.get("categories",0) != 0:
            category = cat["categories"][0]
            id = category["id"]
            name = category['name']
            return {"id": id, "name": name}    
        else:
            return None    
    
    def __extract_cat_category(self, cat: dict) ->dict:
        if cat.get("categories",0) != 0:
            category = cat["categories"][0]
            category_id = category["id"]     
            cat_id = cat["id"]
            return {"cat_id": cat_id, "category_id": category_id}
        else:
            return None


    def __extract_breed(self, breed: dict) -> dict:
    
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
    
    def __cat_housekeeping(self, housekeeping: dict, cat: dict):
        if cat['id'] not in housekeeping:
            housekeeping[cat["id"]] = 1 
        return housekeeping    
                               

    def update_sql(self, iter: int, verbose: bool) ->None:
        print("STARTING.....")
    
        housekeeping = {}
    
        raw_data = self._Extract__get_raw_data(iter, self.__url, self.__api_key, verbose=verbose)
     
        counter = 0
        breed_counter = 0 
        cat_counter = 0
        cat_category_counter = 0
    
        print("   Raw data are extracted...")
        print("   Processing data and inserting into PostgreSQL tables...")
        for data in raw_data:
         
            cat = self._Extract__extract_cat(data)
            category = self._Extract__extract_category(data)
            cat_category = self._Extract__extract_cat_category(data)
            breed = self._Extract__extract_breed(data)
            if breed is not None:
                cat["breed_id"] = breed["id"]
            else:
                cat["breed_id"] = "None"     
          
            try:
                with engine.connect() as conn: 
                    _ = conn.execute(insert(self.cat_table), cat, ) 
                    if breed is not None:
                        _ = conn.execute(insert(self.breed_table), breed, )
                        breed_counter += 1 
                    if category is not None:
                        _ = conn.execute(insert(self.category_table), category, )
                    if cat_category is not None:
                        _ = conn.execute(insert(self.cat_category_table), cat_category, )    
                        cat_category_counter += 1
                    conn.commit()   
                    housekeeping = self._Extract__cat_housekeeping(housekeeping, cat) 
            except:
                #print("Issue with writing to SQL base...") 
                #del housekeeping[str(cat["id"])]
                #print(f"Cat with id {cat["id"]} deleted")
                pass
                
            counter += 1     
        
        print('END....')
        
        print()
        print("Extract, transform and load procedure is done. Check SQL relations, it shoud have following unique instances:")        
        print("   Cat instances: " + str(len(housekeeping)))
        print("   Breed instances: " + str(breed_counter))  
        print("   Cat_Category instances: " + str(cat_category_counter))
        print("   Total calls to CatAPI: " + str(counter))

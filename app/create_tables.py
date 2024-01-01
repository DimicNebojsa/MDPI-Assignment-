from sqlalchemy import insert, Table, MetaData, Column, Integer, String

class CreateTables:
    def __init__(self):
        print("Creating SQLAlchemy tables...")
    
    
    def create_Cat_Table(self, table_name: str) -> Table:
    
        metadata_obj = MetaData()
        cat_table = Table(table_name, metadata_obj, 
                          Column("id", String, primary_key=True, nullable=False),
                          Column("url", String, nullable=False),
                          Column("width", Integer, nullable=False),
                          Column("height", Integer, nullable=False),
                          Column("breed_id", String, nullable=True))
        return cat_table    
    
    def create_Category_Table(self, table_name: str) -> Table:
    
        metadata_obj = MetaData()
        category_table = Table(table_name, metadata_obj, 
                               Column("id", Integer, primary_key=True, nullable=False),
                               Column("name", String, nullable=False))
        return category_table   

    def create_Cat_Category_Table(self, table_name: str) -> Table:
    
        metadata_obj = MetaData()
        category_table = Table(table_name, metadata_obj, 
                         Column("cat_id", String, primary_key=True, nullable=False),
                         Column("category_id", Integer, primary_key=True, nullable=False))
        return category_table  

    def create_Breed_Table(self, table_name: str) -> Table:
    
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
        
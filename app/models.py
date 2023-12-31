from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base

class Post(Base):
    __tablename__ = "Post"
     
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  
     
     
class Cat(Base):
    __tablename__ = "Cat"
    id = Column(String, primary_key=True, nullable=False)
    url = Column(String, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    breed_id = Column(String, nullable=True)
    
class Category(Base):
    __tablename__ = "Category"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)    

class Cat_Category(Base):
    __tablename__ = "Cat_Category"
    cat_id = Column(String, ForeignKey("Cat.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    category_id = Column(Integer, ForeignKey("Category.id", ondelete="CASCADE"), primary_key=True, nullable=False)

class Breed(Base):
    __tablename__ = "Breed"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=True)
    cfa_url = Column(String, nullable=True)
    vetstreet_url = Column(String, nullable=True)
    vcahospitals_url = Column(String, nullable=True)
    temperament = Column(String, nullable=True)
    origin = Column(String, nullable=True)
    country_codes = Column(String, nullable=True)
    description = Column(String, nullable=True)
    life_span = Column(String, nullable=True)
    indoor = Column(Integer, nullable = True)
    lap = Column(Integer, nullable=True) 
    alt_names = Column(String, nullable=True) 
    adaptability = Column(Integer, nullable=True)
    affection_level = Column(Integer, nullable=True)
    child_friendly = Column(Integer, nullable=True) 
    dog_friendly = Column(Integer, nullable=True) 
    energy_level = Column(Integer, nullable=True)
    grooming =  Column(Integer, nullable=True)
    health_issues = Column(Integer, nullable=True)
    intelligence = Column(Integer, nullable=True)
    shedding_level = Column(Integer, nullable=True)
    social_needs = Column(Integer, nullable=True)
    stranger_friendly = Column(Integer, nullable=True)
    vocalisation = Column(Integer, nullable=True)
    experimental = Column(Integer, nullable=True)
    hairless = Column(Integer, nullable=True)
    natural = Column(Integer, nullable=True)
    rare = Column(Integer, nullable=True)
    rex = Column(Integer, nullable=True)
    suppressed_tail = Column(Integer, nullable=True)
    short_legs = Column(Integer, nullable=True)
    wikipedia_url = Column(String, nullable=True)
    hypoallergenic = Column(Integer, nullable=True)
    reference_image_id = Column(String, nullable=True)
    imperial = Column(String, nullable=True) 
    metric = Column(String, nullable=True)
  
         


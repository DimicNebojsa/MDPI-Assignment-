<<<<<<< HEAD
## Assignment API

Assignment API is designed to connect to public CatAPI (https://thecatapi.com). 
Data are collected, transformed, and inserted into PostgreSQL database.

### CatAPI data structure

Data in CatAPI are stored in non-relational database. Major documents in this design are:
<br>
<br>**Cat**
    <br>id: str 
	<br>url: str
    <br>width: int
    <br>heigh: int
    <br>Breed : [] 	// can be empty or Breed document
    <br>Category: [] 	//can be empty or Category document
<br>
<br>**Category**
<br>Id: int
<br>Name: string
<br>
<br>**Breed**
<br>[id, name, cfa_url, vetstreet_url, vcahospitals_url, temperament, origin, country_code, description, life_span, indoor, lap, alt_names, adaptability, affection_level, child_friendly, dog_friendly, energy_level, grooming, health_issues, intelligence, shedding_level, social_needs, stranger_friendly, vocalization, experimental, hairless, natural, rare, suppressed_tail, short_legs, wikipedia_url, hypoallergenic, reference_image_id, imperial, metric]
<br> ***for brevity for Breed table I have put just attribute names***    
<br>
<br>Majority of instances will not have Category or Breed document inside Cat document. 
<br>
<br>CatAPI provides random instances from database with maximum number of 100 instances in one batch. Since our target database is relation model, duplicated instances are not inserted into database. 

### Description of files 
Files in this project are:
<br>
<br><li>  <mark>main.py</mark> – FastAPI routes for CRUD operations are defined. Additionally, method for extract, transform and insert to PostgreSQL is called from this file.
<br><li> <mark>databse.py</mark> – file which defines SQL Alchemy engine, Session and dependency
<br><li> <mark>models.py</mark> – file which defines DB schema in SQL Alchemy
<br><li> <mark>schemas.py</mark> – file which defines Pydantic objects 
<br><li> <mark>extract_class.py</mark> – file that defines calls to CatApi, transforms data and inserts data in PostgreSQL relations. 
<br><li> <mark>SQLAlchemy_CRUD.py</mark> – examples of CRUD operations in SQL Alchemy framework
<br><li> <mark>pandas_examples.py</mark> – examples of data loading, transformation and joining in pandas framework
<br><li> <mark>tests.py</mark> – test cases
<br>


### SQL schema

Relational model used in our API is modeled as following:
<br><li>Relations:
<br> <mark>Cat, Breed, Category </mark>
<br> We will have many-to-many relationship between Cat and Category, so we needed to design junction table <mark>Cat_Category</mark>. 


#### Final SQL schema is:

<br>**CAT**
<br>**id**: str - Primary Key, not null
<br>**url**: str - not null
<br>**width**: int - not null
<br>**height**: int - not null
<br>**breed_id** - not null
<br>
<br>**CATEGORY**
<br>**id**: int - Primary Key, not null
<br>**Name**: str - not null

<br>**BREED**:
<br>**id**:str - Primary Key, not null
<br>...
<br> ***for brevity and visibility I have ommited other attributes. Full list of attribites is in file <mark>'models.py'</mark>.    
    
<br>**CAT_CATEGORY**
<br>**cat_id**: str	 - Primary Key,  not null, Foreign Key on Cat.id
<br>**category_id**: int - Primary Key, not null, Foreign Key on Category.id
<br>
<br>Finally, control table has been added in design to control number of unique instances in Cat, Breed and Category relation. It is used for testing purposes.
<br>
<br>**CONTROL**
<br>**cat_counter**: int - Primary Key, not null
<br>**breed_counter**:int 
<br>**cat_category_counter**:int

ORM database design is in file <mark>'database.py'</mark> .



    
### FastAPI

CRUD Routes are defined in main.py file.

<br>**Create routes**
	<li>http://localhost:8000/cat        	for creating CAT instance
	<li>http://localhost:8000/category  	for creating Category instance

To test API routes, I was using Postman platform. Requests to FastAPI are sent in JSON format (e.g. for creating CAT instance we should sent following JSON using Postman PUT request {“id: “test123”, “url”: ”www.cat123.com”, “width”: 400, “height”: 640}

<br>**Read routes:**
	<li>http://localhost:8000/breed/{breed}             for getting instance of specific breed id
	<li>http://localhost:8000/category/{category}   for getting instance of specific category id
	<li>http://localhost:8000/cat/{id} 	             for getting instance of specific cat id

<br>**Delete routes:**
	<li>http://localhost:8000/breed/delete/{name} 
	<li>http://localhost:8000/category/delete/{cat_id}
	<li>http://localhost:8000/cat/delete/{id}

<br>**Update routes:**
	<li>http://localhost:8000/cat/update/{id}
	<li>http://localhost:8000/category/update/{id}   


### Pydantic

<br>Pydantic schemas for Cat, Category, Breed objects are in file <mark>'schemas.py'</mark>

<br>All objects have Input and Response schemas defined.

<br>Pydantic Input and Responses objects were tested using Postman platform.
 

### SQLAlchemy 

<br>SQLAlchemy table objects are defined in file <mark>'extract_tables.py'</mark>


### Extract, Transform and Load

<br>ETL operations are defined in extract_class.py

<br>This class is designed to get raw batch of 100 instances from CatAPI, transform data in format that Cat, Category and Breed object requires and performs insert operations PostgreSQL database. 

<br>Since CatAPI provides random instances, we are facing situation that same instance can be inserted in PostgreSQL. In case that SQL constraints are breached (PK or FK constraints) insert operation will not be performed.

<br>To have 6000 – 8000 unique instances in PostgreSQL database, we will need to have 30 000 – 50 000 calls to CatAPI. By testing batch size, conclusion is that most optimal batch size is 100 instances (in regards of time and number of failed insert operations due to unique PK constraint in SQL relations).


### SQLAlchemy CRUD operations

<br>SQL Alchemy CRUD operations are defined in file SQLAlchemy_CRUD.py

<br>This file defines select, insert, and join operation by in SQL Alchemy framework.


### Pandas
<br>Examples of using pandas framework are in file pandas_example.py

<br>This file defines read operation from database and same join operations as they are defined in SQLAlchemy_CRUD.py file for comparison purposes.



### How to start:

**Step 1. Run docker container with PostgreSQL image.**

```
docker run --rm -it -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=mdpi -d -p 5432:5432 postgres
```

I was using PGAdmin as client to connect to PostgreSQL database.

<br>**Step2. To start FastAP in folder .app/app run:**

```
uvicorn main:app –-reload
```

If there are no tables created in PostgreSQL database, SQLAlchemy will first create them and them it will run method “update_sql” from class_extract.py in order to fill Db with instances. 

Default set up is 5 bathes which should be 500 calls to CatAPI. This should be enough call to have instance in all tables (Cat, Breed and Category)


CRUD operations using FastAPi can be checked using API platform (e.g. Postman) with providing data in line with table structures in JSON format. 


**SQL Alchemy CRUD operations**

To run defined SQL Alchemy CRUD operations FastAPI should be stopped and we simple run SQLAlchemy_CRUD.py file 

```
python3 SQLAlcehmy_CRUD.py
```

I have chosen this solution not to clutter output while using FastAPI in main.py


**Pandas**

In order to run pandas framework, we can use 

```
python3 pandas_example.py
```

Examples given in this file are made with purpose of showing basic pandas operations and joins between different tables. 

**Tests**

Test are run with pytest by: 

```
pytest ./test/tests.py
```
Test are made to check for consistency of SQL relations and equality between SQL Alchemy queries with native SQL queries, as well as equality between panda joins and SQL Alchemy join queries.


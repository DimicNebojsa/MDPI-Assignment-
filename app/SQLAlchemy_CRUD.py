"""Examples of CRUD operations using SQLAlchemy.

Author: Nebojsa Dimic
Date: 1/2/2024
"""

from sqlalchemy import Select, Table, Insert, Update, Delete
from create_tables import CreateTables
from extract_class import Extract
from database import engine

URL = "https://api.thecatapi.com/v1/images/search?limit=100&api_key="
API_KEY = "live_LeTQOlg1Yf7kbymctS8792u6PliZpvMVMlRATtIONbuDIZ1MU0UANifkDzCGuzeU"

createTables = CreateTables()
extract_class = Extract(URL, API_KEY, createTables)     

cat_table = extract_class.cat_table
breed_table = extract_class.breed_table
cat_category_table = extract_class.cat_category_table
category_table = extract_class.category_table


def select(table: Table, attribute: str, condition: str= None) -> None:
    """Performs 'SELECT * from Table WHERE attribute = condition."""
    """
        Args:
            table (Table): ORM Table name.
            attribute (str): attribute of relation.
            condition (str): conditon to look at
                
        Excpetions:
            HTTP exceptions    

        Returns:
            Nothing
    """    
    
    stmt = Select(table).where(table.columns[attribute] == condition)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)

def join(table1: Table, 
         table2: Table, 
         attribute1: str, 
         attribute2: str, 
         limit: int) -> None:
    """Performs INNER join between Table1 and Table2."""
    """
        Args:
            table1 (Table): ORM Table name.
            table2 (Table): ORM Table name.
            attribute1 (str): attribute of relation Table1.
            attribute2 (str): attribute of relation Table2
                
        Excpetions:
            HTTP exceptions    

        Returns:
            Nothing
    """  
    stmt = Select(table1).join(table2, 
                               table1.columns[attribute1] == table2.
                               columns[attribute2]).limit(limit)

    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)
            
#join(cat_table, breed_table, "breed_id", "id")            
            
def insert(table: Table, input_dict: dict) -> None:
    """Performs 'INSERT INTO Table' query."""
    """
        Args:
            table (Table): ORM Table name.
            input_dict (dict): dictionary of instance 
                
        Excpetions:
            HTTP exceptions    

        Returns:
            Nothing
    """  
    assert(len(table.columns) == len(input_dict))
    
    values_temp = {}
    for column, value in zip(table.columns, input_dict.values()):
        values_temp[str(column)] = value
        
    keys = values_temp.keys()  
    
    values = {}
    for key in keys:
        values[str(key.split(".")[1])] = values_temp[key]
        
    #print(values)    
        
    insert_stmt = Insert(table).values(values)
    
    try:
        with engine.connect() as conn:
            conn.execute(insert_stmt)
            conn.commit()
    except:
        print("PK exists...")   
 
def update(table: Table, 
           input_dict: dict, 
           condition_column: str, 
           condition_value: str) -> None:
    """Performs update sql query on given Table."""
    """
        Args:
            table (Table): ORM Table name.
            input_dict (dict): dictionary of instance for update
            condition_column (str): column of relation 
            condition _value (str): conditon to look at in relation
                
        Excpetions:
            HTTP exceptions    

        Returns:
            Nothing
    """  
    assert(len(table.columns) == len(input_dict))
    
    values_temp = {}
    for column, value in zip(table.columns, input_dict.values()):
        values_temp[str(column)] = value
        
    keys = values_temp.keys()  
    
    values = {}
    for key in keys:
        values[str(key.split(".")[1])] = values_temp[key]
    
    #print(values)    
    
    stmt = Update(table).where(
        table.columns[condition_column] == condition_value).values(values)
    try:
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
    except:
        print("Problems with writing to PostgreSQL....")   
        
   

def delete(table: Table, 
           input_dict: dict, 
           condition_column: str, 
           condition_value: str) -> None:
    """Performs delete sql query on given Table."""
    """
        Args:
            table (Table): ORM Table name.
            input_dict (dict): dictionary of instance for deleting
            condition_column (str): column of relation 
            condition _value (str): conditon to look at in relation
                
        Excpetions:
            HTTP exceptions    

        Returns:
            Nothing
    """  
    
    assert(len(table.columns) == len(input_dict))
    
    values_temp = {}
    for column, value in zip(table.columns, input_dict.values()):
        values_temp[str(column)] = value
        
    keys = values_temp.keys()  
    
    values = {}
    for key in keys:
        values[str(key.split(".")[1])] = values_temp[key]
    
    #print(values)    
     
    stmt = Delete(table).where(
        table.columns[condition_column] == condition_value)

    try:
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
    except:
        print("Problems with deleting from PostgreSQL....")   
        
#insert(cat_table, input_dict)         
#delete(cat_table, input_dict, "id", "165ok6ESN")

def run_SQLAlchemy_queries() -> None:
    """Performs queries from this SQLAlchemy_CRUD class."""
    """
        Args:
            None
        
        Excpetions:
            None  

        Returns:
            Nothing
    """  
    #run select query 
    stmt = Select(cat_table)
    with engine.connect() as conn:
        cat = conn.execute(stmt)
    cat = cat.fetchall()    
    print()
    print(f"INSTANCE OF CAT RELATION WHERE ID IS: {cat[0][0]}")
    select(cat_table, "id", cat[0][0])  
    
    # run join query 
    print()
    print("RESULT OF INNER JOIN BETWEEN CAT AND BREED TABLE, LIMIT IS SET TO 10")
    join(cat_table, breed_table, "breed_id", "id", 10)   
    
    # define test cases for input, update, delete
    input_dict = {"id": "165ok6ESN", 
                "url": "www.carworld.com", 
                "width": 1000, 
                "height": 1200, 
                "breed_id": "None"}
    input_dict1 = {"id": "165ok6ESN", 
                "url": "www.carworld.com", 
                "width": 1, 
                "height": 2, 
                "breed_id": "None"}
    #input_dict2 = {"id": 100, "name": "test_test"}
    #input_dict3 = {"cat_id": "165ok6ESN", "category_id": 100}
    
    print()
    print("INSERTING NEW INSTANCE TO CAT TABLE")
    print(f"instance is {input_dict}")
    insert(cat_table, input_dict)  
    print()
    print(f"CHECKING IF INSTANCE WITH ID {input_dict["id"]} EXISTS:")
    select(cat_table, "id", input_dict["id"])
    print()
    print(f"UPDATING INSTANCE WITH ID {input_dict1["id"]}")
    update(cat_table, input_dict1, "id", input_dict1["id"])  
    print(f"CHECKING IF INSTANCE WITH ID {input_dict1["id"]} IS UPDATED:") 
    select(cat_table, "id", input_dict1["id"])
    print()
    print(f"DELETING INSTANCE WITH ID {input_dict["id"]}")
    delete(cat_table, input_dict, "id", input_dict["id"])

run_SQLAlchemy_queries()
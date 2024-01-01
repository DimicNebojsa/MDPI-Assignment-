from sqlalchemy import Select, Table, Insert, Update, Delete
import extract
from database import engine

cat_table = extract.cat_table
breed_table = extract.breed_table
cat_category_table = extract.cat_category_table
category_table = extract.category_table


def select(table: Table, attribute: str, condition: str):
    """
        SELECT * FROM table WHERE table.attribute == condition
    """
    #stmt = Select(cat_table).where(cat_table.c.id == "165ok6ESN")
    
    stmt = Select(table).where(table.columns[attribute] == condition)
    print(stmt)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)
            
#select(extract.cat_table, "id", "165ok6ESN")   


def join(table1: Table, table2: Table, attribute1: str, attribute2: str):
    """
        SELECT * FROM Table1 
        INNER JOIN Table2
            ON Table1.attribute1 = Table2.attribute2
    """
    stmt = Select(table1).join(table2, 
                               table1.columns[attribute1] == table2.columns[attribute2])
    #print(type(stmt))
    #print(cat_table.c.id)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)
            
#join(cat_table, breed_table, "breed_id", "id")            
            
def insert(table: Table, input_dict: dict):
    """
        INSERT INTO Table VALUES (value1, value2, ..., valueN)
    """
    
    assert(len(table.columns) == len(input_dict))
    
    values_temp = {}
    for column, value in zip(table.columns, input_dict.values()):
        values_temp[str(column)] = value
        
    keys = values_temp.keys()  
    
    values = {}
    for key in keys:
        values[str(key.split(".")[1])] = values_temp[key]
        
    print(values)    
        
    insert_stmt = Insert(table).values(values)
    
    try:
        with engine.connect() as conn:
            conn.execute(insert_stmt)
            conn.commit()
    except:
        print("PK exists...")   


input_dict = {"id": "165ok6ESN", "url": "www.carworld.com", "width": 1000, "height": 1200, "breed_id": "None"}
input_dict2 = {"id": 100, "name": "test_test"}
input_dict3 = {"cat_id": "165ok6ESN", "category_id": 100}

#insert(cat_table, input_dict)    
#insert(category_table, input_dict2)
#insert(cat_category_table, input_dict3)
 
 
def update(table: Table, input_dict: dict, condition_column: str , condition_value):
    assert(len(table.columns) == len(input_dict))
    
    values_temp = {}
    for column, value in zip(table.columns, input_dict.values()):
        values_temp[str(column)] = value
        
    keys = values_temp.keys()  
    
    values = {}
    for key in keys:
        values[str(key.split(".")[1])] = values_temp[key]
    
    #print(values)    
    
    stmt = Update(table).where(table.columns[condition_column] == condition_value).values(values)
    try:
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
    except:
        print("Problems with writing to PostgreSQL....")   
        
#update(cat_table, input_dict, "id", "165ok6ESN")      

def delete(table: Table, input_dict: dict, condition_column: str , condition_value):
    assert(len(table.columns) == len(input_dict))
    
    values_temp = {}
    for column, value in zip(table.columns, input_dict.values()):
        values_temp[str(column)] = value
        
    keys = values_temp.keys()  
    
    values = {}
    for key in keys:
        values[str(key.split(".")[1])] = values_temp[key]
    
    #print(values)    
     
    stmt = Delete(table).where(table.columns[condition_column] == condition_value)

    try:
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
    except:
        print("Problems with deleting from PostgreSQL....")   
        
#insert(cat_table, input_dict)         
delete(cat_table, input_dict, "id", "165ok6ESN")

"""Extraction data from SQL relation and simple joinery.

Data ara collected from already formed SQL relations.
Simple joineries are perfomed using Pandas package.

Author: Nebojsa Dimic
Date: 1/2/2024
"""



from database import engine
from sqlalchemy import select
from create_tables import CreateTables
from sqlalchemy import Table
import pandas as pd


class Pds:
    """Extracts relations from SQL and does joineries in Pandas.

    Attributes:
    ----------
    None

    Methods:
    -------
    __validate_table_name(table_name: str) -> Table
        Private method that creates SQLAlchemy table 
        for later queries
        
    pandas_select_table(table_name: str, 
                        columns: list = None) -> pd.DataFrame:    
        Public method that select all instances from table_name
        
    test_breed() -> pd.DataFrame
        Tests 'SELECT * FROM Breed' query    
        
    test_cat() -> pd.DataFrame: 
        Tests 'SELECT * FROM Cat' query      
        
    test_category() -> pd.DataFrame   
        Tests 'SELECT * FROM Category' query   
        
    test_cat_category()
        Tests 'SELECT * FROM Cat_Category' query  
    
    """
    
    def __init__(self) -> None:
        pass

    def __validate_table_name(self, table_name: str) -> Table:
        
        createTables = CreateTables()
    
        if table_name == "Breed":
            table = createTables.create_Breed_Table(table_name)
        elif table_name == "Cat":
            table = createTables.create_Cat_Table(table_name)
        elif table_name == "Category":
            table = createTables.create_Category_Table(table_name)
        elif table_name == "Cat_Category":  
            table = createTables.create_Cat_Category_Table(table_name)
        else:
            print("Please provide correct table name.")
            print("Options are: 'Cat', 'Breed', 'Category' or 'Cat_Category'")
        
        return table    

        
        
    def pandas_select_table(self, table_name: str, 
                            columns: list = None) -> pd.DataFrame:
        """Perfoms SQL equivalent of SELECT * FROM Table."""
        """
            Args:
                table_name (str): Name of table in SQL database
                columns (list): List of strings with column names.
                
            Excpetions:
                None

            Returns:
                Pandas Dataframe of equivalent SQL table
        """
    
    
        table = self._Pds__validate_table_name(table_name)
        if table is None: 
            return 
    
        stmt = select(table)

        try:
            with engine.connect() as conn: 
                result = conn.execute(stmt)
                    
        except:
            pass

        df = pd.DataFrame(result)
    
        if columns is not None:
            df = df[columns]
    
        return df
    
    def test_breed(self) -> pd.DataFrame:
        """Performs test on Breed table."""
        """
            Args:
               None
                
            Excpetions:
                None  

            Returns:
                Pandas Dataframe equivalent to Breed relation in SQL DB
        """
        breed_result = pds.pandas_select_table("Breed", 
                                               ["id", "name", "description"])
        return breed_result
    
    def test_cat(self) -> pd.DataFrame:
        """Performs test on Cat table."""
        """
            Args:
               None
                
            Excpetions:
                None  

            Returns:
                Pandas Dataframe equivalent to Cat relation in SQL DB
        """
        cat_result = pds.pandas_select_table("Cat", ["id", "breed_id"])
        return cat_result
    
    def test_category(self) -> pd.DataFrame:
        """Performs test on Category table."""
        """
            Args:
               None
                
            Excpetions:
                None  

            Returns:
                Pandas Dataframe equivalent to Category relation in SQL DB
        """
        category_result = pds.pandas_select_table("Category")
        return category_result
    
    def test_cat_category(self) -> pd.DataFrame:
        """Performs test on Cat_Category table."""
        """
            Args:
               None
                
            Excpetions:
                None  

            Returns:
                Pandas Dataframe equivalent to Cat_Category relation in SQL DB
        """
        cat_category_result = pds.pandas_select_table("Cat_Category")
        return cat_category_result
        

pds = Pds()

breed_result = pds.test_breed()
print(breed_result)

cat_result = pds.test_cat()
print(cat_result)

category_result = pds.test_category()
print(category_result)

cat_category_result = pds.test_cat_category()
print(cat_category_result)


# Examples of simple joinery using Pandas
merge_cat_breed = cat_result.merge(breed_result, 
                                   how='inner', 
                                   left_on='breed_id', 
                                   right_on='id')
print(merge_cat_breed)

merge_cat_category = cat_result.merge(cat_category_result, 
                                      how = "inner", 
                                      left_on = "id", 
                                      right_on="cat_id").merge(
                                          category_result, 
                                          how = "inner", 
                                          left_on = "category_id", 
                                          right_on = "id")
merge_cat_category.columns = ["cat_id", 
                              "breed_id", 
                              "cat_id", 
                              "category_id", 
                              "id", 
                              "name"]

merge_cat_category = merge_cat_category[["cat_id", "category_id", "name"]]
print(merge_cat_category)




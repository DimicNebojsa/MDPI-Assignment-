"""Class for testing.

Author: Nebojsa Dimic
Date: 1/2/2024
"""

from sqlalchemy import Select
from app.database import engine
from app.create_tables import CreateTables
from app.extract_class import Extract


class TestClass:
    """A class with test cases.

    Attributes:
    ----------
        None

    Methods:
    -------
        test1(): -> None
        This test compares number of instances in PostgreSQL
        with housekeeping counters in Extract class
    """
    
    def test_1(self) -> None:    
        """Test that compares housekeeping counters with control tables."""
        """
            Args:
                None

            Returns:
                None
        """        
        
        URL = "https://api.thecatapi.com/v1/images/search?limit=100&api_key="
        API_KEY = "live_LeTQOlg1Yf7kbymctS8792u6PliZpvMVMlRATtIONbuDIZ1MU0UANifkDzCGuzeU"
        createTables = CreateTables()
        extract_class = Extract(URL, API_KEY, createTables)     

        stmt = Select(extract_class.control_table)
        with engine.connect() as conn:
            result = conn.execute(stmt)
        result = result.fetchall()    
  
        stmt_count_cat = Select(extract_class.cat_table)
        cat_counter = 0
        with engine.connect() as conn:
            for row in conn.execute(stmt_count_cat):
                cat_counter += 1        
    
        stmt_count_breed = Select(extract_class.breed_table)
        breed_counter = 0
        with engine.connect() as conn:
            for row in conn.execute(stmt_count_breed):
                breed_counter += 1
    
        stmt_count_cat_category = Select(extract_class.cat_category_table)
        cat_category_counter = 0
        with engine.connect() as conn:
            for row in conn.execute(stmt_count_cat_category):
                cat_category_counter += 1
    
        assert result[0][0] == cat_counter
        assert result[0][1] == breed_counter
        assert result[0][2] == cat_category_counter
    
    def __helper_pk_dict(self, table_name: str) -> bool:
        
        URL = "https://api.thecatapi.com/v1/images/search?limit=100&api_key="
        API_KEY = "live_LeTQOlg1Yf7kbymctS8792u6PliZpvMVMlRATtIONbuDIZ1MU0UANifkDzCGuzeU"
        createTables = CreateTables()
        extract_class = Extract(URL, API_KEY, createTables)     
        
        if table_name == "Cat":
            stmt = Select(extract_class.cat_table)
        elif table_name == "Breed":
            stmt = Select(extract_class.breed_table)
        elif table_name == "Category":
            stmt = Select(extract_class.category_table)    
        
        with engine.connect() as conn:
            result = conn.execute(stmt)
        result = result.fetchall()  
        
        pk_dict ={}
        
        for instance in result:
            if instance[0] not in pk_dict:
                pk_dict[str(instance[0])] = 1
            else:
                pk_dict[str(instance[0])] +=1 
                
        result = True
        
        for key, value in pk_dict.items():
            if value > 1:
                result = result and False
        return result        
        
    
    def test_PK_constraint_cat(self) -> bool:
        """Test uniqueness of Primary Key in relation Cat."""
        """
            Args:
                None

            Returns:
                True if all PKs are unique, False otherwise
        """        
        
        result = self.__helper_pk_dict("Cat")        
        assert result is True                   
            
            
    def test_PK_constraint_breed(self) -> bool:
        """Test uniqueness of Primary Key in relation Breed."""
        """
            Args:
                None

            Returns:
                True if all PKs are unique, False otherwise
        """ 
                
        result = self.__helper_pk_dict("Breed")        
        assert result is True         
    
    def test_PK_constraint_category(self) -> bool:
        """Test uniqueness of Primary Key in relation Category."""
        """
            Args:
                None

            Returns:
                True if all PKs are unique, False otherwise
        """ 
                
        result = self.__helper_pk_dict("Category")        
        assert result is True              
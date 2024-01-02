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
    

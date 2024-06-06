#!/usr/bin/python

from datetime import datetime
import uuid
import re

class Amenity():
    """
    Amenity class
    """
    
    def __init__(self, *args, **kwargs):
     """Constructor"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = ""
    
    if kwargs:
        for key, value in kwargs.items():
            if key == "place_id" or key == "user_id":
                self.name = value
    
    # --- Getters and Setters ---
    @property
    def name(self):
    """Getter for private prop name"""
        return self.name

@name.setter
def name(self, value):
    """Setter for private prop name"""

# ensure that the value is not spaces-only and is alphabets + spaces only
    is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z ]+$", value)
    if is_valid_name:
        self.__name = value
    else:
        raise ValueError("Invalid amenity name specified: {}".format(value))

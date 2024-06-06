#!/usr/bin/python

from datetime import datetime
import uuid
import re

class Review():
    """Representation of a review"""
    
    #Constructor
    def __init__(self, *args, **kwargs):
        
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        # Setattr - only allow place_id, user_id, text
        if kwargs:
            for key, value in kwargs.items():
                if key == "place_id" or key == "user_id" or key == "text":
                    setattr(self, key, value)

    @property
    def place_id(self):
        """Getter for private prop place_id"""
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        """Setter for private prop place_id"""
        self.__place_id = value

    @property
    def user_id(self):
        """Getter for private prop user_id"""
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        """Setter for private prop user_id"""
        self.__user_id = value

    @property
    def text(self):
        """Getter for private prop text"""
        return self.__text

    @text.setter
    def text(self, value):
        """Setter for private prop text"""
        self.__text = value
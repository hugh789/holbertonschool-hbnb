#!/usr/bin/python

from datetime import datetime
import uuid
import re
from data import country_data

class Place():
    """Representation of a place"""
    def __init__(self, *args, **kwargs):
        """Initialization of a place"""

        
        #Constructor
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.__name = ""
        self.__city_id = ""
        self.__description = ""


        # Setattr - only allow name, city-id, description
        if kwargs:
            for key, value in kwargs.items():
                if key == "name" or key == "city_id" or key == "description":
                    setattr(self, key, value)


    @property
    def name(self):
        """Getter for private prop name"""
        return self.__name
    
    @name.setter
    def name(self, value):
        """Setter for private prop name"""
        #Ensure that the value is not spaces-only and is alpahabets + spaces only
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z ]+$", value)
        if is_valid_name:
            self.__name = value
        else:
            raise ValueError("Invalid place name specified: {}".format(value))
    
    @property
    def city_id(self):
        """Getter for private prop city_id"""
        return self.__city_id
    
    @city_id.setter
    def city_id(self, value):
        """Setter for private prop city_id"""
        self.__city_id = value
        #Ensure city id exists? against city data source
    
    @property
    def description(self):
        """Getter for private prop description"""
        return self.__description
    
    @description.setter
    def description(self, value):
        """Setter for private prop description"""
        #No validation needed for description, can be anything
        self.__description = value

    @property
    def address(self):
        """Getter for private prop address"""
        return self.__address
    
    @address.setter
    def address(self, value):
        """Setter for private prop address"""
        self.__address = value

    @property
    def latitude(self):
        """Getter for private prop latitude"""
        return self.__latitude
    
    @latitude.setter
    def latitude(self, value):
        """Setter for private prop latitude"""
        #float or int check?
        self.__latitude = value

    @property
    def longitude(self):
        """Getter for private prop longitude"""
        return self.__longitude
    
    @longitude.setter
    def longitude(self, value):
        """Setter for private prop longitude"""
        #float or int check?
        self.__longitude = value

    @property
    def number_rooms(self):
        """Getter for private prop number_rooms"""
        #INT check?
        return self.__number_rooms
    
    @number_rooms.setter
    def number_rooms(self, value):
        """Setter for private prop number_rooms"""
        self.__number_rooms = value

    @property
    def number_of_bathrooms(self):
        """Getter for private prop number_bathrooms"""
        return self.__number_bathrooms
    
    @number_of_bathrooms.setter
    def number_of_bathrooms(self, value):
        """Setter for private prop number_bathrooms"""
        self.__number_bathrooms = value
    
    @property
    def price_per_night(self):
        """Getter for private prop price_by_night"""
        return self.__price_per_night
    
    @price_per_night.setter
    def price_per_night(self, value):
        """Setter for private prop price_by_night"""
        self.__price_per_night = value

    @property
    def max_guest(self):
        """Getter for private prop max_guest"""
        return self.__max_guest
    
    @max_guest.setter
    def max_guest(self, value):
        """Setter for private prop max_guest"""
        self.__max_guest = value
#!/usr/bin/python3

from datetime import datetime
import uuid
import re
from data import place_data, user_data, city_data, amenity_data, review_data


class Amenity():
    """"Representation of an amenity"."""

    def __init__(self, *args, **kwargs):
        """ constructor """

        # defaults
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = self.created_at
        self.__number_of_rooms = None
        self.__bathrooms = None
        self.__price_per_night = None
        self.__max_guests = None

        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    raise ValueError(f"Invaild item: {key}")

    @property
    def number_of_rooms(self):
        """Getter for private number_of_rooms"""
        return self.__number_of_rooms

    @number_of_rooms.setter
    def number_of_rooms(self, value):
        """Setter for private number_of_rooms"""
        # ensure that the value is positive int

        if isinstance(value, int) and value > 0:
            self.__number_of_rooms = value
        else:
            raise ValueError(
                f"Invalid number_of_rooms specified: {value}.\nNumber of room(s) must be a positive integer")

    @property
    def price_per_night(self):
        """Getter for private price_per_night"""
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, value):
        """Setter for private longitude"""
        # ensure that the value is 0 or positive int or float
        if isinstance(value, (float, int)) and value >= 0:
            self.__price_per_night = float(value)
        else:
            raise ValueError(
                f"Invalid price_per_night specified: {value}.\nPrice per night must be a non-negative integer")

    @property
    def max_guests(self):
        """Getter for private max_guests"""
        return self.__max_guests

    @max_guests.setter
    def max_guests(self, value):
        """Setter for private max_guests"""
        # ensure that the value is positive int only

        if isinstance(value, int) and value > 0:
            self.__max_guests = value
        else:
            raise ValueError(
                f"Invalid max_guests specified: {value}.\nGuest(s) must be a positive integer.")

    @property
    def bathrooms(self):
        """Getter for private bathrooms"""
        return self.__bathrooms

    @bathrooms.setter
    def bathrooms(self, value):
        """Setter for private bathrooms"""
        # ensure that the value is positive int or 0

        if isinstance(value, int) and value >= 0:
            self.__bathrooms = value
        else:
            raise ValueError(
                f"Invalid bathrooms specified: {value}.\nBathrooms must be a non-negative integer.")

    def update_amenity(self, **kwargs):
        """update existing amenity"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid item: {key}")
        self.updated_at = datetime.now().timestamp()
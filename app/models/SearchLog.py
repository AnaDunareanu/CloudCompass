from config.__init__ import search_collection
import datetime


class SearchLog:
    def __init__(self, user_id, origin, destination, date, airline, price):
        self.user_id = user_id
        self.origin = origin
        self.destination = destination
        self.date = date
        self.airline = airline
        self.price = price
        self.timestamp = datetime.datetime.now()  # Add a timestamp for when the search was made

    def save(self):
        search_collection.insert_one(self.__dict__)



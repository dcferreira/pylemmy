from enum import Enum


class SortType(Enum):
    Active = "Active"
    Hot = "Hot"
    MostComments = "MostComments"
    New = "New"
    NewComments = "NewComments"
    Old = "Old"
    TopAll = "TopAll"
    TopDay = "TopDay"
    TopMonth = "TopMonth"
    TopWeek = "TopWeek"
    TopYear = "TopYear"


class ListingType(Enum):
    All = "All"
    Community = "Community"
    Local = "Local"
    Subscribed = "Subscribed"

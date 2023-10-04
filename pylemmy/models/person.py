"""Implements the Person class."""

import pylemmy
from pylemmy import api


class Person:
    """A class for Persons."""

    def __init__(
        self,
        lemmy: "pylemmy.Lemmy",
        counts: api.person.PersonAggregates,
        person: api.person.Person,
    ):
        """Initialize a Person instance.

        :param lemmy: A Lemmy instance.
        :param person: A [PersonView](
        https://join-lemmy.org/api/interfaces/PersonView.html).
        """
        self.lemmy = lemmy
        self.counts = counts
        self.safe = person

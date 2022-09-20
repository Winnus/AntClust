# Inside this file the distance objects, which will be used inside the
# AntClust class are defined.
# A similarity object should always inherit from the
# informal interface "similarity_interface".
# The similarity function should only return values between 0 and 1
# These similarity objects can then be instantiated and provided to AntClust.

# imports
import math


# Informal Interface
class similarity_interface:
    def similarity(self, d_0, d_1):
        """
        Computes the similarity/distance between two data vectors d_0 and d_1.
        This distance/similarity between the two objects should be expressed as
        a range between 0.0 and 1.0, where 1.0 means the objects are similar,
        0.0 is returned if the objects are completely anti-similar.
        I.e. if d_0 == d_1 it should return 1.0
        """
        raise NotImplementedError


class similarity_euclid2d(similarity_interface):
    """
    Implements the euclidean distance for 2D vectors
    """

    def __init__(self, min, max):
        """
        min: the minimal value a vector can have
        max: the maximal value a vector can have
        """
        self.min = min
        self.max = max

    def similarity(self, a, b):
        # Calculate eclidean distance for 2D vectors.
        # Normalize between 0 and 1 and invert.
        return 1 - (math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)/abs(self.min-self.max))


class similarity_1d(similarity_interface):
    """
    Implements the 1d numeric distance measure
    """

    def __init__(self, min, max):
        """
        min: the minimal numeric value an object can have
        max: the maximal numeric value an object can have in the data set
        """
        self.min = min
        self.max = max

    def similarity(self, d_0, d_1):
        """
        Inverted distance between two numbers, normalized between 0 and 1.
        Meaning if two numbers are equal they are completely similar => sim(2,2) = 1
        """
        return 1 - (abs(d_0 - d_1)/abs(self.min - self.max))

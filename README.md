# ANTCLUST

This project is a Python build of ANTCLUST, a clustering algorithm based on the chemical recognition system of ants which was developed by Nicolas Labroche et al. [0].

# similarity functions
Data sets can have very different features with different data types. The clustering algorithm has to calculate distances based on these features and this is done by using a similarity function. Since each tuple may contain different features which can be of a different data type, there is the need for different similarity functions that are applicable to the different features - e.g an image will have a different similarity function as a two dimensional numerical vector - . Finding the correct similarity function can be a non trivial task and therefore AntClust expects the user to define its own similarity functions for each feature inside a data tuple. To be sure the user defined a similarity function AntClust can handle a lazy interface was used. The user has to provide a Python object which inherits from the similarity interface class. Inside this object he has to define a function called similarity(d0, d1) which computes the similarity/distance between the two data vectors d0 and d1. This distance/similarity between the two objects should be expressed as a range between 0.0 and 1.0, where 1.0 means the objects are similar and 0.0 is returned if the objects are completely anti-similar. I.e. if d0 == d1 1.0 should be returned.
A very simplistic example would be

```
# class inherits from the similarity_interface
class similarity_1d(similarity_interface):
    """
    Implements the 1d numeric distance measure
    """

    def __init__(self, min, max):
        """
        min: the minimal numeric value
             an object can have
        max: the maximal numeric value
             an object can have in the dataset
        """
        self.min = min
        self.max = max

    def similarity(self, d_0, d_1):
        """
        Inverted distance between two numbers,
        normalized between 0 and 1.
        I.e. if two numbers are equal they are
        completely similar => sim(2,2) = 1
        """
        dist = abs(d_0 - d_1)
        scaled = dist/abs(self.min - self.max)
        inverted = 1 - dist_scaled
        return inverted```
```
# rule set
The rule set for AntClust can be changed. The ruleset used in [0] is already implemented and can be used. However if a new ruleset should be created then it should inherit from the rule_interface and implement the function apply_rules(). An example on how to achieve this can be seen when looking into the rules.py file, where the Labroche rules are defined and an explanation is given.


# Usage example
A very simplistic usage example would look as follows.
```
# ----------------------
#       imports
# ----------------------
# import AntClust
from AntClust import AntClust

# import the self defined similarity functions
from distance_classes import similarity_1d
from distance_classes import similarity_euclid2d

# import the rule set
from rules import labroche_rules


# ----------------------
#       data
# ----------------------
# Define a very simple data set
# This set contains 8 data tuples, each
# having 2 features, where the first is 
# a numeric feature and the second one a
# vector in the 2Dimensional space.
# Therefore every feature needs
# a different similarity function.
data = [[ 0.1,  [1,1] ],
        [ 0.2,  [1,2] ],
        [ 0.11, [2,1] ],
        [ 0.13, [2,2] ],
        [ 0.9,  [8,9] ],
        [ 0.98, [9,9] ],
        [ 0.87, [9,10]],
        [ 0.7,  [10,9]]]


# ----------------------
#       AntClust
# ----------------------
# define a different similarity function per feature
f_sim = [similarity_1d(0,1),
         similarity_euclid2d(0,14)]

# rules
rules = labroche_rules()

# AntClust
ant_clust = AntClust(data,
                    f_sim,
                    rules)
                    
# find clusters
ant_clust.find_clusters()

# get the clustering result
clusters_found =  ant_clust.get_clusters()

```





# sources
[0] https://www.researchgate.net/publication/2551128_A_New_Clustering_Algorithm_Based_on_the_Chemical_Recognition_System_of_Ants

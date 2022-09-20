import numpy as np
import threading


class Ant:
    """
    Ant's will hold the data frames of the data set as their genetic.
    """

    def __init__(self, genetic, index):
        # saves the label i.e. the colony == cluster to which this ant belongs
        self.label = -1

        # the template of this Ant
        self.template = 0

        # m is an estimator which is reflecting how successful this ant is
        # during its meetings with other ants
        self.m = 0

        # m_p measures how well accepted this ant is inside his nest
        self.m_p = 0

        # age of the ant, updated during a change in acceptance threshold
        self.age = 0

        # estimators of the max and mean similarity observed during meetings
        # sim_mean is computed via sim_sum/age
        self.sim_max = 0
        self.sim_sum = 0
        # self.sim_mean = 0

        # the genetic of this Ant
        self.gene = np.array(genetic)

        # store the index of the genetic
        # i.e. index of this data frame inside the data set and inside AntClut
        self.index = index

        # locker for multithreading
        self.lock = threading.Lock()

    def update_template(self, similarity):
        """Updates age, max and mean similarity's and template of this ant """
        # lock Ant object
        self.lock.acquire()
        # update age
        self.age += 1
        # update mean_sim
        self.sim_sum += similarity
        # update max_sim?
        if similarity > self.sim_max:
            self.sim_max = similarity
        # update template
        self.template = ((self.sim_sum/self.age) + self.sim_max) / 2
        # release lock
        self.lock.release()

    # -----------------
    #       getter
    # -----------------
    def get_label(self):
        self.lock.acquire()
        value = self.label
        self.lock.release()
        return value

    def get_m(self):
        self.lock.acquire()
        value = self.m
        self.lock.release()
        return value

    def get_m_p(self):
        self.lock.acquire()
        value = self.m_p
        self.lock.release()
        return value

    # -----------------
    #      setter
    # -----------------
    def set_label(self, label):
        self.lock.acquire()
        self.label = label
        self.lock.release()

    def set_m(self, m):
        self.lock.acquire()
        self.m = m
        self.lock.release()

    def set_m_p(self, m_p):
        self.lock.acquire()
        self.m_p = m_p
        self.lock.release()

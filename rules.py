# Informal rule Interface
# The function apply_rules will need to be implemented 
# and will be called by AntClust to perform the rules.
class rule_interface:
    def apply_rules(self, ant_i, ant_j, AntClust):
        """
        Will apply all rules the rules inside the ruleset of this class.
        ant_i: one ant
        ant_j: another ant
        AntClust: reference to the AntClust instance

        You will have acess to the following things:
            - Ant attributes:
                - get_label(): which is thhe label for the cluster this ant
                  belongs to. If not yet assigned it will be -1
                - get_m(): m is an estimator which is reflecting how sucessfull
                  this ant is during its meetings with other ants, is an
                  estimator of the size of the nest
                - get_m_p: m_p measures how well accpeted this ant is inside
                   his nest

            - AntClust attributes:
                - get_acceptance(ant_i, ant_j): true or false depending if
                  the ant accept each other or not
        """
        raise NotImplementedError


# standard rule set as in Labroche et.al
# In the very beginning all ants are initialized
# with no label - i.e. label ← 0. Thus when two ants meet in
# the beginning, mostly R1 will be applied. This will create a
# lot of little clusters containing only two ants. Once more and
# more ants have got a label assigned trough R1, it becomes
# more likely that R2 is applied and thus the initial formed
# clusters begin to grow. If two ants belong to the same cluster
# there are two cases: they accept each other or they do not.
# In the first case R3 will be applied which will increase the
# cluster size estimator M and the colony integrity estimator
# M + which makes sense since it seems that the colony is quite
# big if two randomly chosen ants belong to the same colony,
# accepting each other means that the colony is still in a good
# integrity state. In the second case R4 will be applied as the
# colony mates do not accept each other. This will increase the
# colony size estimator since the colony must be relatively big
# if two randomly chosen ants belong to the same colony and
# decrease the integrity estimator M + since the two ants did not
# accept each other but belong to the same colony, suggesting
# the integration of colony members is relatively low. If two
# ants meet that do no belong to the same colony but accept
# each other then R5 is applied which will, over time, lead to
# the ability that smaller colonies - where many of these are
# initially formed in the beginning via R1 - getting integrated
# into the bigger colony’s. For all other cases the default rule is
# applied and thus nothing ha
class labroche_rules(rule_interface):
    def __init__(self):
        # list of all created labels
        self.labels = []

        # label counter, will be increased for every new label creation
        self.label_counter = 0

    def apply_rules(self, ant_i, ant_j, AntClust):
        # get the ants acceptance
        acceptance = AntClust.get_acceptance(ant_i, ant_j)

        # ---------------------------------------------------------
        # R1 New nest creation:
        # ---------------------------------------------------------
        if (ant_i.get_label() == -1) and (ant_j.get_label() == -1):
            if acceptance:
                # create and assign new label if both ants do not have a label
                # and accept each other
                # use label and create new one by updating the label_counter
                new_label = self.label_counter
                self.labels.append(new_label)
                self.label_counter += 1  # update label counter

                # assign label to ants
                ant_i.set_label(new_label)
                ant_j.set_label(new_label)
            else:
                # if no acceptance then no other rule is applied
                return

        # ---------------------------------------------------------
        # R2 Adding an ant with no label to an existing nest:
        # ---------------------------------------------------------
        if (ant_i.get_label() == -1) and (ant_j.get_label() != -1) and acceptance:
            ant_i.set_label(ant_j.get_label())

        if (ant_j.get_label() == -1) and (ant_i.get_label() != -1) and acceptance:
            ant_j.set_label(ant_i.get_label())

        # ---------------------------------------------------------
        # R3 "Positive" meeting between two nestmates:
        # ---------------------------------------------------------
        # FIXME: ant_i,j label can not be -1 here because it is catched inside
        #  the if from rule 1, you do not need to check here. Are you sure?
        if (ant_i.get_label() == ant_j.get_label()) and (ant_i.get_label() != -1) and (ant_j.get_label() != -1) and acceptance:
            # increase their meeting estimators m and m_p
            # m:
            ant_i.set_m(self.increase_estimator_variable(ant_i.get_m()))
            ant_j.set_m(self.increase_estimator_variable(ant_j.get_m()))

            # m_p
            ant_i.set_m_p(self.increase_estimator_variable(ant_i.get_m_p()))
            ant_j.set_m_p(self.increase_estimator_variable(ant_j.get_m_p()))

        # ---------------------------------------------------------
        # R4 "Negative" meeting between two nestmates:
        # ---------------------------------------------------------
        # FIXME: ant_i,j label can not be -1 here because it is catched inside
        #  the if from rule 1, you do not need to check here. Are you sure?
        if (ant_i.get_label() == ant_j.get_label()) and (ant_i.get_label() != -1) and (ant_j.get_label() != -1) and acceptance == False:
            # increase m_j,i and decrease m_p_i,j
            # m:
            ant_i.set_m(self.increase_estimator_variable(ant_i.get_m()))
            ant_j.set_m(self.increase_estimator_variable(ant_j.get_m()))

            # m_p:
            ant_i.set_m_p(self.decrease_estimator_variable(ant_i.get_m_p()))
            ant_j.set_m_p(self.decrease_estimator_variable(ant_j.get_m_p()))

            # The ant x (x=i, x=j) which poseeses the worst integration
            # in the nest loses its label
            # FIXME: what if both ants have the same acceptance inside the nets?
            # m_p is the estimator how well accepted the ant is inside her nest
            m_p_i = ant_i.get_m_p()
            m_p_j = ant_j.get_m_p()

            # ant_i looses its label i.e. is not as good accepted as ant_j
            if m_p_i < m_p_j:
                ant_i.set_label(-1)
                ant_i.set_m(0)
                ant_i.set_m_p(0)

            # ant_j looses its label i.e. is not as good accepted as ant_i
            if m_p_j < m_p_i:
                ant_j.set_label(-1)
                ant_j.set_m(0)
                ant_j.set_m_p(0)

        # ---------------------------------------------------------
        # R5 meeting between two ants of different nests:
        # ---------------------------------------------------------
        if (ant_i.get_label() != ant_j.get_label()) and acceptance:
            # decrease m
            # the ant with the lowest Mx changes its nest

            # m:
            ant_i.set_m(self.decrease_estimator_variable(ant_i.get_m()))
            ant_j.set_m(self.decrease_estimator_variable(ant_j.get_m()))

            # M:
            if ant_i.get_m() < ant_j.get_m():
                # ant_i is inside the smaller cluster and will be absorbed
                ant_i.set_label(ant_j.get_label())
            else:
                # ant_j is inside the smaller cluster and will be absorbed
                ant_j.set_label(ant_i.get_label())

        # ---------------------------------------------------------
        # R6 If no other rule applies nothing happens:
        # ---------------------------------------------------------
        return

    def increase_estimator_variable(self, x, alpha=0.2):
        return (1 - alpha) * x + alpha

    def decrease_estimator_variable(self, x, alpha=0.2):
        return (1 - alpha) * x

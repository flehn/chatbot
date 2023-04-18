class State:
    """ Defines a single state """

    def __init__(self, name):
        self.name = name

    def get_name(self):
        """ Retrieve the name of the state """

        return self.name
# Imports
from classes.State import *
from config import labels as labels
from config import settings as settings 


class StateMachine:
    """ An architecture to manipulate states """

    def __init__(self):
        self.current_state = State("welcome")

    def get_current_state(self):
        """ Retrieve the current state """

        return self.current_state

    def update_current_state(self, next_state):
        """ Update current state """
        self.current_state = next_state

    @staticmethod
    def state_transition(state_machine, user):
        """ State transition function based on dialog acts """

        # Keep the same state
        if user.get_last_dialog_act() in [labels.REPEAT, labels.NUL, labels.AFFIRM]:
            next_state = state_machine.get_current_state()

        if user.get_last_dialog_act() in [labels.BYE, labels.THANKYOU]:
            next_state = State("end")

        # When the user wants to completely reset the system  
        if user.get_last_dialog_act() == labels.RESTART:
            # No restarts allowed 
            if settings.NO_RESTARTS:
                next_state = state_machine.get_current_state()

            else:
                user.update_area_pref(None)
                user.update_pricerange_pref(None)
                user.update_food_pref(None)
                user.update_additional_requirements(None)
                user.reset_possible_restaurants()
                next_state = State("welcome")

        if user.get_last_dialog_act() == labels.HELLO:
            next_state = State("area")

        if user.get_last_dialog_act() in [labels.INFORM, labels.ACK, labels.NEGATE]:

            # Make sure all preferences are known before making a recommendation
            if not user.get_area_pref():
                next_state = State("area")
                state_machine.update_current_state(next_state)
                return

            if not user.get_pricerange_pref():
                next_state = State("pricerange")
                state_machine.update_current_state(next_state)
                return

            if not user.get_food_pref():
                next_state = State("food")
                state_machine.update_current_state(next_state)
                return

            if not user.get_additional_requirements():
                next_state = State("requirements")
            
            else:
                next_state = State("recommend")

        if user.get_last_dialog_act() == labels.CONFIRM:
            next_state = State("check")

        if user.get_last_dialog_act() == labels.REQMORE:
            next_state = State("more")

        if user.get_last_dialog_act() == labels.REQUEST:
            next_state = State("request")

        if user.get_last_dialog_act() == labels.DENY:
            next_state = State("correction")

        if user.get_last_dialog_act() == labels.REQALTS:
            next_state = State("recommend")

        state_machine.update_current_state(next_state)


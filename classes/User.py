# Imports
import pandas as pd
import config.settings as settings

class User:
    """ Architecture to keep track of a user's preferences, most recent answer, and possible recommendations """

    def __init__(self, possible_restaurants):
        self.food = None
        self.pricerange = None
        self.area = None
        self.utterance = None
        self.dialog_act = None
        self.possible_restaurants = possible_restaurants
        self.last_recommendation = None
        self.additional_requirements = None

    def get_food_pref(self):
        """ Retrieve food preference """

        return self.food

    def get_pricerange_pref(self):
        """ Retrieve price range preference """

        return self.pricerange

    def get_area_pref(self):
        """ Retrieve area preference """

        return self.area

    def update_food_pref(self, pref):
        """ Update food preference """ 

        self.food = pref

    def update_area_pref(self, pref):
        """ Update area preference """

        self.area = pref

    def update_pricerange_pref(self, pref):
        """ Update price range preference """

        self.pricerange = pref

    def get_last_utterance(self):
        """ Retrieve most recent utterance """

        return self.utterance

    def get_last_dialog_act(self):
        """ Retrieve most recent dialog act """

        return self.dialog_act

    def update_last_utterance(self, utterance):
        """ Update most recent utterance """

        self.utterance = utterance

    def update_last_dialog_act(self, act):
        """ Update most recent dialog act """

        self.dialog_act = act

    def get_possible_restaurants(self):
        """ Retrieve possible recommendations """

        return self.possible_restaurants

    def get_last_recommendation(self):
        """ Retrieve most recent recommendation """

        return self.last_recommendation

    def update_last_recommendation(self, recommendation):
        """ Update most recent recommendation """

        self.last_recommendation = recommendation

    def get_additional_requirements(self):
        """ Retrieve additional requirements set by user """

        return self.additional_requirements

    def update_additional_requirements(self, requirements):
        """ Set requirements given by user """

        self.additional_requirements = requirements

    def delete_possible_restaurant(self, restaurant_name):
        """ Delete restaurant from possible recommendations """

        self.possible_restaurants = self.get_possible_restaurants()[
            (self.get_possible_restaurants().restaurantname != restaurant_name)]

    def update_possible_restaurants(self, data):
        """ Narrow down possible recommendations based on preferences and requirements"""

        # The preferences 
        if self.get_area_pref() and self.get_area_pref() != "any":
            data = data.loc[(data["area"] == self.get_area_pref())]

        if self.get_pricerange_pref() and self.get_pricerange_pref() != "any":
            data = data.loc[(data["pricerange"] == self.get_pricerange_pref())]

        if self.get_food_pref() and self.get_food_pref() != "any":
            data = data.loc[(data["food"] == self.get_food_pref())]

        # The additional requirements
        if self.get_additional_requirements() and self.get_additional_requirements() != "any":
            if any(item in self.get_additional_requirements() for item in ["romantic", "children", "fancy", "healthy", "groups"]):
                for requirement in [item for item in self.get_additional_requirements() if item in ["romantic", "children", "fancy", "healthy", "groups"]]:
                    data = data.loc[(data[requirement] == True)]

            if any(item in self.get_additional_requirements() for item in ["long", "short", "medium"]):
                for requirement in [item for item in self.get_additional_requirements() if item in ["long", "short", "medium"]]:
                    data = data.loc[(data["length_of_stay"] == requirement)]

            if any(item in self.get_additional_requirements() for item in ["busy", "overcrowded", "empty", "moderate"]):
                for requirement in [item for item in self.get_additional_requirements() if item in ["busy", "overcrowded", "empty", "moderate"]]:
                    data = data.loc[(data["crowdedness"] == requirement)]
            
        self.possible_restaurants = data

    def reset_possible_restaurants(self):
        """ Reset the possible recommendations to all restaurants """

        self.possible_restaurants = pd.read_csv(settings.RESTAURANT_DATABASE_FILE, sep=";")

    def is_frame_empty(self, key):
        """ Returns whether the given frame is empty """

        if key == 'area':
            return not self.area
        elif key == 'food':
            return not self.food
        elif key == 'pricerange':
            return not self.pricerange
        else:
            return False

    def get_preferences_as_string(self):
        """ Returns the preferences as a string """

        return 'Food: ' + str(self.food) + ', Pricerange: ' + str(self.pricerange) + ', Area: ' + str(self.area)

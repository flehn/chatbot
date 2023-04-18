import Levenshtein as lev
import pandas as pd
import random

import config.settings as settings


def identify_topics(utterance, keywords):
    """ Identify which topic(s) the utterance is about (price, area, food, phone number, address and/or postcode) """

    # Look for the keywords in the utterance for each category
    price = [word for word in keywords["pricerange"] if word in utterance]
    area = [word for word in keywords["area"] if word in utterance]
    food = [word for word in keywords["food"] if word in utterance]
    phone = [word for word in keywords["phone"] if word in utterance]
    address = [word for word in keywords["addr"] if word in utterance]
    postcode = [word for word in keywords["postcode"] if word in utterance]

    topics = []

    # Topic is found if there are suitable keywords in the utterance 
    if len(price) > 0:
        topics.append("price")

    if len(area) > 0:
        topics.append("area")

    if len(food) > 0:
        topics.append("food")

    if len(phone) > 0:
        topics.append("phone")

    if len(address) > 0:
        topics.append("addr")

    if len(postcode) > 0:
        topics.append("postcode")

    return topics


def extract_keywords(df):
    """ Make lists of keywords for each category using the restaurant data for the preference and topic extraction"""

    keywords = {}

    # Extract keywords from data
    price_keywords = [keyword for keyword in df["pricerange"].unique() if not pd.isnull(keyword)]
    area_keywords = [keyword for keyword in df["area"].unique() if not pd.isnull(keyword)]
    food_keywords = [keyword for keyword in df["food"].unique() if not pd.isnull(keyword)]

    # Also add "don't care" keywords
    keywords["pricerange"] = price_keywords
    keywords["pricerange"] = keywords["pricerange"] + ["moderately", "any price", "any price range"]
    keywords["area"] = area_keywords
    keywords["area"] = keywords["area"] + ["any area", "any part of town", "anywhere"]
    keywords["food"] = food_keywords
    keywords["food"] = keywords["food"] + ["any food", "any type", "any restaurant"]

    keywords["addr"] = ["where", "address"]
    keywords["postcode"] = ["postcode"]
    keywords["phone"] = ["phone", "phone number", "number"]

    keywords["any"] = ["any", "don't care", "don't mind", "any preference"]

    keywords["requirements"] = ["romantic", "children", "fancy", "healthy", "groups", 
                                "long", "short", "medium", "busy", "overcrowded", 
                                "empty", "moderate", "no", "not"]

    return keywords


def update_user_preferences(user):
    """
    Update preferences to match data set instances

    :param user:
    :return:
    """

    if user.get_pricerange_pref() == "moderately":
        user.update_pricerange_pref("moderate")

    if user.get_pricerange_pref() in ["any price", "any price range"]:
        user.update_pricerange_pref("any")

    if user.get_area_pref() in ["any area", "any part of town", "anywhere"]:
        user.update_area_pref("any")

    if user.get_food_pref() in ["any food", "any type", "any restaurant", "any kind"]:
        user.update_food_pref("any")

    if user.get_additional_requirements() in ["no", "anything", "any requirements", "not"]:
        user.update_additional_requirements("any")


def extract_preferences(state_machine, user, keywords):
    """ Extract preferences and requirements from the user's most recent utterance without using Levenshtein distance"""

    utterance = user.get_last_utterance()

    # Look for the keywords in the utterance for each category
    price_pref = [word for word in keywords["pricerange"] if word in utterance]
    area_pref = [word for word in keywords["area"] if word in utterance]
    food_pref = [word for word in keywords["food"] if word in utterance]

    # For the requirements
    requirements_pref = [word for word in keywords["requirements"] if word in utterance]

    # Check if keyword matches have been found
    if len(price_pref) > 0:
        user.update_pricerange_pref(max(price_pref, key=len))

    if len(area_pref) > 0:
        user.update_area_pref(max(area_pref, key=len))

    if len(food_pref) > 0:
        user.update_food_pref(max(food_pref, key=len))

    # For the requirements
    if len(requirements_pref) > 0:
        extract_requirements(state_machine, user, keywords)

    # Check for "don't care" keywords that don't contain info about category (price, food, etc)
    for any_keyword in keywords["any"]:

        # Determine category belonging to keyword based on state
        if any_keyword in utterance:

            if state_machine.get_current_state().get_name() == "area":
                user.update_area_pref("any")

            if state_machine.get_current_state().get_name() == "pricerange":
                user.update_pricerange_pref("any")

            if state_machine.get_current_state().get_name() == "food":
                user.update_food_pref("any")

            if state_machine.get_current_state().get_name() == "requirements":
                user.update_additional_requirements("any")

    # Update preferences to match data set instances 
    update_user_preferences(user)


def find_best_match(key, keyword_dict, user):
    """ Finds closest preference keyword that matches the users utterance using Levenshtein distance """
    utterance = user.get_last_utterance().split(" ")
    best_match = 0

    # Initialize really large distance
    current_distance = 100000

    # Compare all keywords to all words from utterance
    for keyword in keyword_dict[key]:
        for word in utterance:

            # When it is the first comparison or better match, update
            if best_match == 0 or lev.distance(keyword, word) < current_distance:
                best_match = keyword
                current_distance = lev.distance(keyword, word)

            # When it is an equally good match
            elif lev.distance(keyword, word) == current_distance:
                best_match = random.choice([keyword, best_match])

    # Threshold for true match
    if current_distance <= settings.LEVENSHTEIN_THRESHOLD:
        return best_match

    # No true match found
    else:
        return 0


def extract_preferences_lev(state_machine, user, keywords):
    """ Preference extraction using Levenshtein distance """

    # First extract preferences (and requirements) without Levenshtein distance
    extract_preferences(state_machine, user, keywords)

    # Check for each category if preferences can be extracted 
    if state_machine.get_current_state().get_name() == 'pricerange':
        
        # Only try if there isnt already a preference extracted
        if not user.get_pricerange_pref():

            # Check for possible closest match 
            match = find_best_match("pricerange", keywords, user)
            if match:
                user.update_pricerange_pref(match)
            
            # If no match is found check for "don't care" match
            else:
                match = find_best_match("any", keywords, user)
                if match:
                    user.update_pricerange_pref(match)


    if state_machine.get_current_state().get_name() == 'area':
        # Only try if there isnt already a preference extracted
        if not user.get_area_pref():

            # Check for possible closest match 
            match = find_best_match("area", keywords, user)
            if match:
                user.update_area_pref(match)

            # If no match is found check for "don't care" match
            else:
                match = find_best_match("any", keywords, user)
                if match:
                    user.update_pricerange_pref(match)

    if state_machine.get_current_state().get_name() == 'food':
        
        # Only try if there isnt already a preference extracted
        if not user.get_food_pref():

            # Check for possible closest match 
            match = find_best_match("food", keywords, user)
            if match:
                user.update_food_pref(match)
            
            # If no match is found check for "don't care" match
            else:
                match = find_best_match("any", keywords, user)
                if match:
                    user.update_pricerange_pref(match)

        else:
            # Determine category belonging to keyword based on state
            match = find_best_match("any", keywords, user)
            if match:
                if state_machine.get_current_state().get_name() == "area":
                    user.update_area_pref("any")

                if state_machine.get_current_state().get_name() == "pricerange":
                    user.update_pricerange_pref("any")

                if state_machine.get_current_state().get_name() == "food":
                    user.update_food_pref("any")

    # Update preferences to match data set instances
    update_user_preferences(user)


def extract_requirements(state_machine, user, keywords):
    """ Extracts (multiple) additional requirements from the most recent user utterance if any """

    # Requirements are extracted after asking and also if the user specifies them in an inform dialogue act
    if state_machine.get_current_state().get_name() in ["requirements", "recommend"] :
        utterance = user.get_last_utterance()

        if user.get_last_dialog_act() == "negate":
            user.update_additional_requirements("any") 

        # Look for the keywords in the utterance 
        requirements = [word for word in keywords["requirements"] if word in utterance]

        # No additional requirements found
        if len(requirements) == 0:
            return
        
        # Update if there are additional requirements 
        user.update_additional_requirements(requirements)
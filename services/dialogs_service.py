from tqdm import tqdm
import time
import random
import pyttsx3

# Custom modules
from services.utterence_decoding_service import identify_topics
import config.settings as settings
import config.labels as labels


def print_loading_bar(range_time=400):
    for i in tqdm(range(range_time),
                  desc="Thinking…",
                  ascii=False, ncols=75):
        time.sleep(0.01)


def _print(sentence):
    """
    Custom print function that overrides the default one
    Also includes the text to speech component

    :param sentence:
    :return:
    """

    # Output all capital restriction
    if settings.OUTPUT_ALL_CAPS:
        print(sentence.upper())
    else:
        print(sentence)

    # Text to speech restriction
    if settings.TEXT_TO_SPEECH:
        engine = pyttsx3.init()
        engine.say(sentence)
        engine.runAndWait()



def ask_food():
    """ Display message to the screen to ask for food type """

    sentence = ["What kind of food would you like?", 
                "What food type do you have in mind?",
                "What type of food do you prefer?"]

    _print(random.choice(sentence))


def ask_area():
    """ Display message to the screen to ask for area """

    sentence = ["What part of town do you have in mind?",
                "In which part of the town are you looking for a restaurant?",
                "Should the restaurant be located in the east, west, north, south or center part of the city?"]
    _print(random.choice(sentence))


def ask_pricerange():
    """ Display message to the screen to ask for the price-range """

    sentence = ["Would you like something in the cheap , moderate or expensive price range?",
                "What is the price category you are looking for?",
                "Should I look for cheap, moderate or expensive restaurants?"]
    _print(random.choice(sentence))



def say_hello():
    """ Display welcome message """

    sentence = ["Hello, welcome to the restaurant recommendation system of Team 3! You can ask for restaurants by area, price range or food type. How may I help you?",
                "Hello! I am helping you to find the perfect restaurant! How may I help you?",
                "Hi! You are looking for a restaurant? I can help you, tell me what you have in mind!"]
    _print(random.choice(sentence))


def say_bye():
    """ Display goodbye message """

    sentence = ["Have a nice day, bye!",
                "I hope you found a place to eat, bye!",
                "Bye!"]
    _print(random.choice(sentence))


def suggest_restaurant(restaurant):
    """ Display restaurant suggestion """

    sentence = ["I found a restaurant named {}", 
                "What do you think of {}", 
                "I think {} is a pretty good choice"]

    # Loading restriction
    if settings.DELAYED_RESPONSES:
        print_loading_bar(400)
        _print(random.choice(sentence).format(restaurant))
    else:
        time.sleep(4)
        _print(random.choice(sentence).format(restaurant))



def say_no_restaurants_found():
    """ Display no suitable restaurant found message """

    sentence = ["Hm, sorry I can´t find any good restaurants, maybe adjust your preferences a little bit",
                "Sorry I couldn't find a restaurant that suits your wishes. I might be able to find something if you change your preferences",
                "Sorry I couldn't find any suitable restaurants, you need to adjust your preferences if you want to find a place to eat"]

    # Loading restriction
    if settings.DELAYED_RESPONSES:
        print_loading_bar(400)
        _print(random.choice(sentence))
    else:
        time.sleep(4)
        _print(random.choice(sentence))
        

def suggest_other_restaurant(restaurant):
    """ Display another restaurant suggestion """

    sentence = ["I found another restaurant named {}", 
                "What do you think of {} instead", 
                "I think {} is also pretty good choice"]

    # Loading restriction
    if settings.DELAYED_RESPONSES:
        print_loading_bar(400)
        _print(random.choice(sentence).format(restaurant))
    else:
        time.sleep(4)
        _print(random.choice(sentence).format(restaurant))


def answer_request(requests, answers):
    """ Answer the address/postcode/phone number request of the user """

    # Convert data set column labels to words that fit a sentence
    requests_insentence = []
    for request in requests:
        if request == "addr":
            requests_insentence.append("address")

        if request == "phone":
            requests_insentence.append("phone number")

        else:
            requests_insentence.append(request)

    # The user requested one thing
    if len(requests) == 1:
        sentence = ["Here you go, the {} is {}",
                    "I looked the {} up for you: {}",
                    "The {} is {}"]

        _print(random.choice(sentence).format(requests_insentence[0], answers[0]))
        return 

    # The user requested two things
    if len(requests) == 2:
        sentence = ["Here you go, the {} and {} are {} and {}",
                    "I looked the {} and {} up for you: {}, {}",
                    "The {} and {} are {} and {}"]

        _print(random.choice(sentence).format(requests_insentence[0], requests_insentence[1], answers[0], answers[1]))
        return 
    
    # The user requested three things
    if len(requests) == 3:
        sentence = ["Here you go, the {}, {} and {} are {}, {} and {}",
                    "I looked the {}, {} and {} up for you: {}, {}, {}",
                    "The {}, {} and {} are {}, {} and {}"]

        _print(random.choice(sentence).format(requests_insentence[0], requests_insentence[1], requests_insentence[2], answers[0], answers[1], answers[2]))
        return

def say_affirmative():
    """ Display a confirmation message """

    sentence = ["Yes, that's right",
                "Yes, indeed",
                "That's correct"]

    _print(random.choice(sentence))


def say_negative(pricerange, area, food):
    """ Display a negating message """

    sentence = ["No it is a {} restaurant in the {} that serves {} food",
                "The restaurant is {}, is in the {} area of town and it serves {} food",
                "No the restaurant I recommended is {}, is located in the {} part of town and serves {} food"]

    _print(random.choice(sentence).format(pricerange, area, food))


def ask_additional_requirements():
    """ Ask for additional requirements such as romantic etc """

    sentence = ["Do you have any additional requirements?",
                "Are there any more requirements?",
                "Any additional requirements?"]

    _print(random.choice(sentence))

def say_cannot_help():
    "Used when the system cannot handle the user's response"

    sentence = ["Sorry I can't help you with that",
                "I don't understand",
                "I don't recognize what you want"]

    _print(random.choice(sentence))

def generate_system_utterance(state_machine, user, keywords):
    """ Display a message based on the current state """

    if state_machine.get_current_state().get_name() == "welcome":
        say_hello()
        return

    if state_machine.get_current_state().get_name() == "end":
        say_bye()
        return

    if state_machine.get_current_state().get_name() == "area":
        ask_area()
        return

    if state_machine.get_current_state().get_name() == "food":
        ask_food()
        return

    if state_machine.get_current_state().get_name() == "pricerange":
        ask_pricerange()
        return

    if state_machine.get_current_state().get_name() == "requirements":
        ask_additional_requirements()
        return

    if state_machine.get_current_state().get_name() in ["recommend", "reqmore"]:

        # Repeat previous recommendation
        if user.get_last_dialog_act() in [labels.REPEAT, labels.NUL, labels.AFFIRM]:
            suggest_restaurant(user.get_last_recommendation().iloc[0]["restaurantname"])
            return 

        # There are no possible recommendations for the user
        if len(user.get_possible_restaurants()) == 0:
            say_no_restaurants_found()
            return

        # Sample a recommendation randomly
        recommendation = user.get_possible_restaurants().sample()

        if state_machine.get_current_state().get_name() == "recommend":
            suggest_restaurant(recommendation.iloc[0]["restaurantname"])

        if state_machine.get_current_state().get_name() == "reqmore":
            suggest_other_restaurant(recommendation.iloc[0]["restaurantname"])

        # Delete recommendatrepeation from possibilities and update most recent recommendation
        user.delete_possible_restaurant(recommendation.iloc[0]["restaurantname"])
        user.update_last_recommendation(recommendation)

        return

    # The user wants to correct the registered preferences
    if state_machine.get_current_state().get_name() == "correction":

        # Identify which preference should be corrected 
        correction_pref = identify_topics(user.get_last_utterance(), keywords)

        if len(correction_pref) == 0:
            say_cannot_help()
            return

        # Delete preference and ask again
        if "area" in correction_pref:
            user.update_area_pref(None)

            ask_area()
            return

        if "food" in correction_pref:
            user.update_food_pref(None)

            ask_food()
            return

        else:
            user.update_pricerange_pref(None)

            ask_pricerange()
            return

    # User requested address, phone number or postcode
    if state_machine.get_current_state().get_name() == "request":

        # Identify what the request is
        requests = identify_topics(user.get_last_utterance(), keywords)
        answers = []

        # Retrieve answer(s) from data
        for i, request in enumerate(requests):
            answers.append(user.get_last_recommendation().iloc[0][requests[i]])

        answer_request(requests, answers)
        return 

    # User wants to check if a preference is correctly registered
    if state_machine.get_current_state().get_name() == "check":

        # Identify which preference should be checked 
        to_check = identify_topics(user.get_last_utterance(), keywords)
        
        if len(to_check) == 0:
            say_cannot_help()
            return

        # Check if the registered preferences matches the user's utterance 
        if "area" in to_check:
            if user.get_area_pref() in user.get_last_utterance().split():
                to_check.remove("area")

        if "food" in to_check:
            if user.get_food_pref() in user.get_last_utterance().split():
                to_check.remove("food")

        if "price" in to_check:
            if user.get_pricerange_pref() in user.get_last_utterance().split():
                to_check.remove("price")

        # Everything matched
        if len(to_check) == 0:
            say_affirmative()
            return

        # Registered preferences and user's utterance don't match 
        else:
            food = user.get_last_recommendation().iloc[0]["food"]
            area = user.get_last_recommendation().iloc[0]["area"]
            pricerange = user.get_last_recommendation().iloc[0]["pricerange"]
            say_negative(pricerange, area, food)
            return 


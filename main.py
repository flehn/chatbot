# Modules
from helpers.file_manager import load_model
from services.add_preferences_service import addPreferences
from classes.StateMachine import *
from classes.User import *
from helpers.arguments_parser import parse_arguments
from services.classifiers_service import *
from services.dialogs_service import *
from services.utterence_decoding_service import *
from services.baselines_service import * 
import string
import os 

def dialog_system():

    # Get model !!!give True as input if you get version warnings or when using program for the first time!!!
    clf, vectorizer = create_dialog_prediction_model()

    # Initializations
    dialog = StateMachine()
    all_restaurants = pd.read_csv(settings.RESTAURANT_DATABASE_FILE, sep=";")
    
    # Apply inference rules and add features to the data set 
    addPreferences(all_restaurants)

    user = User(all_restaurants)
    keywords = extract_keywords(all_restaurants)

    # Dialog loop
    while True:
        # Show system utterance
        generate_system_utterance(dialog, user, keywords)

        # End dialog
        if dialog.get_current_state().get_name() == "end":
            break

        # Get user input
        user_input = input("user: ")
        for char in user_input:
            if char in ["!", ".", ",", "?"]:
                user_input = user_input.replace(char, " ")

        # Update user's most recent utterance 
        user.update_last_utterance(user_input.lower())

        # Classify dialog act of most recent utterance and update most recent dialog act
        if settings.BASELINE_2:
            dialog_act = baseline_2(user.get_last_utterance(), labels.COUNTS)
        else:
            dialog_act = predict_dialog_act(clf, vectorizer, [user.get_last_utterance()])

        user.update_last_dialog_act(dialog_act)
    
        # Extract and update preferences
        if user.get_last_dialog_act() in [labels.INFORM, labels.NEGATE, labels.REQALTS]:
            if settings.USE_LEVENSHTEIN == True:
                extract_preferences_lev(dialog, user, keywords)
            else:
                extract_preferences(dialog, user, keywords)

            # Update possible recommendations
            user.update_possible_restaurants(all_restaurants)
        
        # Go to next state 
        StateMachine.state_transition(dialog, user)
        
def clear_screen(): 
    _ = os.system("cls" if os.name == "nt" else "clear") 


if __name__ == '__main__':
    parse_arguments()
    dialog_system()
    clear_screen()
    

""" Holds the filename of the dataset was given raw and unedited from blackboard """
INPUT_FILE = 'dialog_acts.dat'

""" Holds the filename of the dataset that is used for training and testing """
INPUT_WORKING_FILE = 'dialog_acts.csv'

""" Holds the filename of the dataset that is used for restaurant recommendations """
RESTAURANT_DATABASE_FILE = 'restaurant_info_with_extra_properties.csv'

""" Holds the filename for the trained model """
MODEL_FILE = 'trained_model.mod'

""" Sets whether the output should be in caps """
OUTPUT_ALL_CAPS = False

""" Configures whether to use Levenshtein distance """
USE_LEVENSHTEIN = False 

""" Configures the levenshtein distance threshold """
LEVENSHTEIN_THRESHOLD = 3

""" Sets whether the dialog will have delayed responses """
DELAYED_RESPONSES = False 

""" Sets whether the system will use text to speech """
TEXT_TO_SPEECH = False 

""" Sets whether the system will use the baseline 2 or logistic regression classifier """
BASELINE_2 = False

""" Sets whether dialogue restarts are allowed """
NO_RESTARTS = False

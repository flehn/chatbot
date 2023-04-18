# :books: Table of contents

- How to run the program
- Project structure

# :bicyclist: How to run the program

Default parameters

```python main.py```

List all possible confiruable parameters

```python main.py --help```

Running with configurable parameter (eg. using levenshtein method)

```python main.py --use-levenshtein=true```

NOTE: if you are running the program for the first time, set retrain to true in the create_dialog_prediction_model in main.py

# :file_folder: Project structure

The main idea of this project was to be able to have a small main file and a good organization in seperate files for each class, type and services. Thus the project is split in the following folders:

- classes
- config
- custom_types
- helpers
- services

## Classes

Contains the classes State, StateMachine and User. The StateMachine is the one used for the state transition functionality that the chatbot has. The User class contains functions and properties that differ for each user. Hence, the User class contains properties that represent user's preferences (like area, pricerange...) and at the same time the class has functions similar to getters and setters. Since, the recommended restaurants differ for each user, the User class contains as well functions that deal with the restaurants that are recommended to the user. 

## Config

Contains two important files:
- settings.py

Holds all the configurable variables such as levenshtein method activeness, whether the output will be in all capitals and more. In addition, this file contains the filenames that are being used in this project

- labels.py

Contains the names of the labels, meaning the dialogue act classifications. 

## Custom types

Contains the label_dict file which in return contains a small list of keywords for each label. It generates a label dictionary that maps the keywords to each class for the machine learning baseline 2

## Helpers

The helpers folder contains two files that are responsible for the smooth operation of this chatbot. 

- File manager

Contains functions that help with the creating of a csv file. Additionally, it contains two functions for saving the training model and loading the training model (if exists)

- Arguments parser

Contains the functionality of parsing the arguments from the command line and updating the general settings (it is used mainly for the configurability)

## Services

Each service contains functions responsible for a particular action

- add_preferences

Contains functions to handle the additional requirements

- baselines

Contains 2 baselines for the project and a function to test them

- classifiers

Contains the functionality of training the model. Thus, it includes other helper functions such as converting to a bag of war, training with the decision tree algorithm or logistic regression, creating a prediction model...

- dialogs

Contains the functionality for generating a system utterance. 

-  utterance_deconding_service

Handles the user's input. Responsible for extracting keywords, preferences, updating the user's preferences based on the input, updating the state, extracting requirements and identifying the topic of the sentence








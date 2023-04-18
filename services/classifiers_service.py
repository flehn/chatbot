from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np

from services.baselines_service import test_baseline
import helpers.file_manager as file_manager
import config.settings as settings


def fit_bag_words(data):
    """
    Fit a vectorizer based on input data

    :param x_train:
    :return:
    """

    # Considering both bigrams and unigrams
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 2))
    vectorizer.fit(data)

    return vectorizer


def to_bag_words(data, vectorizer):
    """
    Convert set of utterances into bag of words representation considering both bigrams and unigrams
    
    :param data: 
    :param vectorizer: 
    :param x_test: 
    :return: 
    """

    return vectorizer.transform(data)


def train_decision_tree(train_data, train_labels):
    """
    Train a decision tree classifier

    :param train_data:
    :param train_labels:
    :return:
    """

    # Define classifier
    clf = DecisionTreeClassifier(class_weight='balanced', max_depth=50)

    # Train
    clf.fit(train_data, train_labels)

    return clf


def train_logistic_regression(train_data, train_labels):
    """
    Train a multi-class logistic regression classifier

    :param train_data:
    :param train_labels:
    :return:
    """

    # Define classifier
    clf = LogisticRegression(multi_class='multinomial', class_weight='balanced')

    # Train
    clf.fit(train_data, train_labels)

    return clf


def test_classifier(clf, test_data, test_labels):
    """
    Test a classifier and returns the F1 and Accuracy score

    :param clf:
    :param test_data:
    :param test_labels:
    :return:
    """

    output = clf.predict(test_data)

    return f1_score(test_labels, output, average='macro'), accuracy_score(test_labels, output)


def predict_dialog_act(clf, vectorizer, utterance):
    """
    Predicts dialog act for a given utterance (represented as list in lower case)

    :param clf:
    :param vectorizer:
    :param utterance:
    :return:
    """

    bag_words = vectorizer.transform(utterance)

    return clf.predict(bag_words)[0]


def create_dialog_prediction_model(retrain=False):
    """
    Creates a dialog prediction model
    If there is already a saved model then the function returns the save model.
    However, if the retrain parameter is specified to True then the model is retrained even if
    a saved model exists

    :param retrain:
    :return:
    """
    # Firstly, load the model if it is saved
    if retrain is False:
        clf, vectorizer = file_manager.load_model()
        if clf is not None and vectorizer is not None:
            return clf, vectorizer

    # At this point, the model needs to be trained
    print('Training model...')

    # Load dataset
    file_manager.create_csv_file(settings.INPUT_FILE, settings.INPUT_WORKING_FILE)
    df = pd.read_csv(settings.INPUT_WORKING_FILE)

    # Convert string class labels into categorical variables
    df["ACT"] = pd.Categorical(df["ACT"])

    # Split data into train, dev, test
    x = df["UTTERANCE"]
    y = df["ACT"]

    label_counts = df.groupby('ACT').size()

    #baseline_1 = []
    #baseline_2 = []
    #tree_train = []
    #tree_test = []
    log_train = []
    log_test = []

    # Test performance 10 times and take mean
    for i in range(10):
        # Split data and convert utterances into bag of words representation
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

        # Fit vocabulary 
        vectorizer = fit_bag_words(x_train)

        # Test baselines (no bag of words needed)
        #baseline_1.append(test_baseline(x_test, y_test, 1, label_counts))
        #baseline_2.append(test_baseline(x_test, y_test, 2, label_counts))

        # Convert data into bag of words 
        x_train = to_bag_words(x_train, vectorizer)
        x_test = to_bag_words(x_test, vectorizer)

        # Train ML classifiers
        clf_log = train_logistic_regression(x_train, y_train)
        #clf_tree = train_decision_tree(x_train, y_train)

        # Test classifiers (decision tree is deactivated due to inferior performance)
        #tree_train.append(test_classifier(clf_tree, x_train, y_train))
        #tree_test.append(test_classifier(clf_tree, x_test, y_test))
        log_train.append(test_classifier(clf_log, x_train, y_train))
        log_test.append(test_classifier(clf_log, x_test, y_test))

    
    #print("Baseline model 1 F1 and accuracy:", [sum(item) / len(baseline_1) for item in zip(*baseline_1)])
    #print("Baseline model 2 F1 and accuracy:", [sum(item) / len(baseline_2) for item in zip(*baseline_2)])

    #print("Decision Tree training F1 and accuracy:", [sum(item) / len(tree_train) for item in zip(*tree_train)])
    #print("Decision Tree testing F1 and accuracy:", [sum(item) / len(tree_test) for item in zip(*tree_test)])

    print("Logistic Regression training F1 and accuracy:", [sum(item) / len(log_train) for item in zip(*log_train)])
    print("Logistic Regression testing F1 and accuracy:", [sum(item) / len(log_test) for item in zip(*log_test)])

    # Save model for future purposes
    file_manager.save_model(clf_log, vectorizer)
    return clf_log, vectorizer

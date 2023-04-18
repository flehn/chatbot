# Import libraries
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer

# Modules
import config.labels as labels
import custom_types.label_dict as label_dict


def baseline_1(input_data):
    """
    Baseline model 1: Returns the majority class

    :param input_data:
    :return: Majority class
    """
    return labels.INFORM


def baseline_2(input_data, label_counts):
    """
    Baseline 2 model: keyword search

    :param input_data: string
    :param label_counts:
    :return:
    """
    current_overlap = 0

    # Intialize best match as majority class
    best_match = "inform"

    # Search through all classes
    for key, value in label_dict.get().items():

        # Find overlap between class keywords and an utterance
        utterance_list = input_data.split(" ")
        overlap = len(list(set(utterance_list).intersection(set(value))))

        # Keep track of class that has most overlap with utterance
        if overlap > current_overlap:
            current_overlap = overlap
            best_match = key

        # If current class has the same overlap as previous, choose the class most common in the training data
        elif overlap == current_overlap & overlap != 0:
            if label_counts[key] > label_counts[best_match]:
                best_match = key

    return best_match


def test_baseline(data, labels, model, label_counts):
    """
    Tests the baseline models

    :param data:
    :param labels:
    :param model:
    :param label_counts:
    :return:
    """

    pred = []

    for utterance, label in zip(data, labels):
        # Majority class baseline
        if model == 1:
            output = baseline_1(utterance)
        
        # Keyword search baseline
        else:
            output = baseline_2(utterance, label_counts)

        pred.append(output)

    return f1_score(labels, pred, average='macro'), accuracy_score(labels, pred)

# Libraries
import csv
import pickle
from os.path import exists

# Modules
import config.settings as settings


def create_csv_file(filename, output_filename):
    """
    Creates a new CSV file that has the data in the format
    that is easier for us to work with

    :param output_filename:
    :param filename:
    :return:
    """
    # Separate labels from utterances and store in list
    data = [line.strip().split(" ", 1) for line in open(filename).readlines()]

    # Writing data to csv file
    with open(output_filename, 'w') as my_file:
        writer = csv.writer(my_file)
        writer.writerow(["ACT", "UTTERANCE"])

        # for each row append it to our CSV file
        for row in data:

            # replacing null label with nul to avoid mistakes with NULL
            if "null" in row:
                row = ["nul", row[1]]
            writer.writerow(row)


def save_model(model, vectorizer):
    """
    Saves the trained model into a file

    :param model:
    :return:
    """
    with open(settings.MODEL_FILE, 'wb') as fh:
        pickle.dump(model, fh)
        pickle.dump(vectorizer, fh)


def load_model():
    """
    Loads and returns the trained model iff the model file exists
    The model file is specified in the configuration settings

    :return:
    """

    if exists(settings.MODEL_FILE):
        with open(settings.MODEL_FILE, 'rb') as f:
            clf = pickle.load(f)
            vectorizer = pickle.load(f)

        return clf, vectorizer
    else:
        return None, None


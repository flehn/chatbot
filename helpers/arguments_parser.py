import argparse
import config.settings as settings


def init_parser():
    """
    Initializes the parser with the available command line arguments

    :return:
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-all-caps",
                        help="sets whether the output should be in caps",
                        default=settings.OUTPUT_ALL_CAPS,
                        type=bool)
    parser.add_argument("--use-levenshtein",
                        help="sets whether the levenshtein distance should be used",
                        default=settings.USE_LEVENSHTEIN,
                        type=bool)
    parser.add_argument("--levenshtein-threshold",
                        help="sets the threshold (value) of the levenshtein distance",
                        default=settings.LEVENSHTEIN_THRESHOLD,
                        type=int)
    parser.add_argument("--use-delayed-responses",
                        help="sets whether should use a delay before showing system responses",
                        default=settings.DELAYED_RESPONSES,
                        type=bool)
    parser.add_argument("--text-to-speech",
                        help="lets the system speak in addition to displayed responses",
                        default=settings.TEXT_TO_SPEECH,
                        type=bool)
    parser.add_argument("--baseline-2",
                        help="lets the system use baseline 2 instead of logistic regression for classification",
                        default=settings.BASELINE_2,
                        type=bool)
    parser.add_argument("--no-restarts",
                        help="system does not allow restarts if True",
                        default=settings.NO_RESTARTS,
                        type=bool)
    return parser


def update_settings_from_arguments(args):
    """
    Updates the global constant settings-variables based on the arguments

    :param args:
    :return:
    """

    settings.OUTPUT_ALL_CAPS = args.output_all_caps
    settings.USE_LEVENSHTEIN = args.use_levenshtein
    settings.LEVENSHTEIN_THRESHOLD = args.levenshtein_threshold
    settings.DELAYED_RESPONSES = args.use_delayed_responses
    settings.TEXT_TO_SPEECH = args.text_to_speech
    settings.BASELINE_2 = args.baseline_2
    settings.NO_RESTARTS = args.no_restarts


def parse_arguments():
    """
    Initialize the available command line options and parses the given arguments
    by using the appropriate functions

    :return:
    """

    args = init_parser().parse_args()
    update_settings_from_arguments(args)


def print_settings():
    """
    Prints the configurable settings to the screen
    (To be used only for debugging purposes)

    :return:
    """
    print('OUTPUT_ALL_CAPS', settings.OUTPUT_ALL_CAPS)
    print('USE_LEVENSHTEIN', settings.USE_LEVENSHTEIN)
    print('LEVENSHTEIN_THRESHOLD', settings.LEVENSHTEIN_THRESHOLD)
    print('DELAYED_RESPONSES', settings.DELAYED_RESPONSES)
    print('TEXT_TO_SPEECH', settings.TEXT_TO_SPEECH)
    print('BASELINE_2', settings.BASELINE_2)
    print('RESTARTS', settings.NO_RESTARTS)



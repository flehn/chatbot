import config.labels as labels


def get():
    """
    Generates a label dictionary that maps the keywords
    to each class for the machine learning baseline 2
    """

    return {
        labels.ACK: ["okay"],
        labels.AFFIRM: ["yes"],
        labels.BYE: ["bye"],
        labels.CONFIRM: ["does", "is"],
        labels.DENY: ["dont", "no", "wrong"],
        labels.HELLO: ["hi", "hello"],
        labels.INFORM: ["looking", "for", "want", "food"],
        labels.NEGATE: ["no"],
        labels.NUL: ["noise", "unintelligible", "sil"],
        labels.REPEAT: ["back", "repeat"],
        labels.REQALTS: ["else", "other", "how", "what", "about"],
        labels.REQMORE: ["more"],
        labels.REQUEST: ["whats", "what", "is", "i", "can", "address", "phone", "number"],
        labels.RESTART: ["start", "reset"],
        labels.THANKYOU: ["thank", "thanks"]
    }


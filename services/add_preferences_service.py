# Imports 
import pandas 

"""
Implementation of the inference rules for additional requirements of the user.
romantic = Not busy and long stay
suitable for children = not long stay
fancy = very good and long stay
healthy = very good or good and busy or overcrowded
groups = long stay and empty or moderate crowdedness
"""

def isRomantic(row):
    return row["crowdedness"] != "busy" and row["length_of_stay"] == "long"


def isSuitableForChildren(row):
    return row["length_of_stay"] != "long"


def isFancy(row):
    return row["length_of_stay"] == "long" and row["food_quality"] == "very good"


def isHealthy(row):
    return row["crowdedness"] in ["busy", "overcrowded"] and row["food_quality"] in ["good", "very good"]


def isSuitableForGroups(row):
    return row["crowdedness"] in ["empty", "moderate"] and row["length_of_stay"] == "long"


def addPreferences(data):
    """Applies the defined inference rules to the data and adds the results to the data"""
    data.loc[(data['pricerange'] == "cheap") & (data['food_quality'] == "good"), ['crowdedness']] = "busy"  #rule 1
    data.loc[data['food'] == "spanish", ['length_of_stay']] = "long"                                        #rule 2
    data.loc[data['crowdedness'].isin(["busy", "overcrowded"]) , ['length_of_stay']] = "long"               #rule 3
    data['romantic'] = data.apply(lambda row: isRomantic(row), axis=1)                                      #rule 5&6
    data['children'] = data.apply(lambda row: isSuitableForChildren(row), axis=1)                           #rule 4
    data['fancy'] = data.apply(lambda row: isFancy(row), axis=1)
    data['healthy'] = data.apply(lambda row: isHealthy(row), axis=1)
    data['groups'] = data.apply(lambda row: isSuitableForGroups(row), axis=1)

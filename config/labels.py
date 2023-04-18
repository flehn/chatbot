import pandas as pd
from config.settings import *

ACK = 'ack'
AFFIRM = 'affirm'
BYE = 'bye'
CONFIRM = 'confirm'
DENY = 'deny'
HELLO = 'hello'
INFORM = 'inform'
NEGATE = 'negate'
NUL = 'nul'
REPEAT = 'repeat'
REQALTS = 'reqalts'
REQMORE = 'reqmore'
REQUEST = 'request'
RESTART = 'restart'
THANKYOU = 'thankyou'

# Count occurrences of each class 
df = pd.read_csv(INPUT_WORKING_FILE)
df["ACT"] = pd.Categorical(df["ACT"])
COUNTS = df.groupby('ACT').size()

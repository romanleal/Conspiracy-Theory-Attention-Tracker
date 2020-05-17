import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

# Importing and cleaning the data.
data = pd.read_csv('subreddit_data_set.csv')
df = pd.DataFrame(data, columns=['timestamp', 'comms_word_count', 'classifier', 'fixed_timestamp'])
trimmed_timestamp = df["timestamp"].str[6:].astype(str)
fixed_timestamp = trimmed_timestamp.str.replace("-", "/")
df['fixed_timestamp'] = fixed_timestamp
sorted_df = df.sort_values(by=['fixed_timestamp'])
political_threads = sorted_df.loc[(df['classifier'] == 0)]
conspiracy_threads = sorted_df.loc[(df['classifier'] == 1)]

# Plotting the data
plt.style.use('fivethirtyeight')
plt.title("Words Commented")
plt.plot(conspiracy_threads['fixed_timestamp'], political_threads['comms_word_count'], label='r/Politics')
plt.plot(conspiracy_threads['fixed_timestamp'], conspiracy_threads['comms_word_count'], color='g', label='r/conspiracy')
plt.show()


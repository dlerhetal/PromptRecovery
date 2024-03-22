# install tiktoken if necessary
# !pip install tiktoken

# import dependencies
import pandas as pd
import tiktoken

# count tokens like Gemma does
def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))

# read the texts
data = pd.read_csv('data.csv')

# add a column for token counts
data['token_count'] = data['text'].apply(count_tokens)

# append the token_count column as the third column in 'data.csv' so that 'data.csv' now has three columns: id, text, and token_count.
data[['id', 'text', 'token_count']].to_csv('data.csv', index=False, header=True)
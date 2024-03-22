import pandas as pd
import tiktoken

def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))

data = pd.read_csv('data.csv')

data['token_count'] = data['text'].apply(count_tokens)

# prompt: append the token_count column as the third column in 'data.csv' so that 'data.csv' now has three columns: id, text, and token_count. please make sure the column headings id, text, and token_count remain in place

data[['id', 'text', 'token_count']].to_csv('data.csv', index=False, header=True)
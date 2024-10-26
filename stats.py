from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud

import emoji


extract = URLExtract()


def fetchstats(selected_user, df):

    # if the selected user is a specific user,then make changes in the dataframe,else do not make any changes

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # counting the number of media files shared

    mediaommitted = df[df['Message'] == '<Media omitted>']

    # number of links shared

    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), mediaommitted.shape[0], len(links)


# most busy users {group level}

def fetchbusyuser(df):

    df = df[df['User'] != 'Group Notification']
    count = df['User'].value_counts().head()

    newdf = pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    return count, newdf


def createwordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Convert all messages to strings
    df['Message'] = df['Message'].astype(str)

    # Check if there are any messages left
    if df['Message'].str.strip().str.len().sum() == 0:
        # Return None or an empty WordCloud
        return None

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    df_wc = wc.generate(df['Message'].str.cat(sep=" "))

    return df_wc




# get most common words,this will return a dataframe of
# most common words

def getcommonwords(selecteduser, df):

    # getting the stopwords

    file = open('stop_hinglish.txt', 'r')
    stopwords = file.read()
    stopwords = stopwords.split('\n')

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    temp = df[(df['User'] != 'Group Notification') | (df['Message'] != '<Media omitted>')]


    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    mostcommon = pd.DataFrame(Counter(words).most_common(20))
    return mostcommon


def getemojistats(selected_user, df):
    # Create a DataFrame to store emoji counts
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    emoji_count = {}
    
    for message in df['Message']:
        emojis = [c for c in message if c in emoji.EMOJI_DATA]
        for e in emojis:
            if e in emoji_count:
                emoji_count[e] += 1
            else:
                emoji_count[e] = 1

    # Convert emoji_count dictionary to DataFrame
    emoji_df = pd.DataFrame(list(emoji_count.items()), columns=['Emoji', 'Count'])
    return emoji_df


def monthtimeline(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    temp = df.groupby(['Year', 'Month_num', 'Month']).count()[
        'Message'].reset_index()

    time = []
    for i in range(temp.shape[0]):
        time.append(temp['Month'][i]+"-"+str(temp['Year'][i]))

    temp['Time'] = time

    return temp


def monthactivitymap(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    return df['Month'].value_counts()


def weekactivitymap(selecteduser, df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    return df['Day_name'].value_counts()

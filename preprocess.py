import streamlit as st
import numpy as np
import pandas as pd
import re

def gettimeanddate(string):
    string = string.split(',')
    date, time = string[0], string[1]
    time = time.split('-')[0].strip()  # Keep the time clean by removing unnecessary parts
    return date + " " + time

def getstring(text):
    return text.split('\n')[0]

def preprocess(data):
    # Regular expression pattern to match WhatsApp message entries
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[apm]{2}\s-\s'
    
    # Split the data into messages and dates
    messages = re.split(pattern, data)[1:]  # Exclude the first entry which is empty
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})

    # Format the date string into a datetime object
    df['message_date'] = df['message_date'].apply(lambda text: gettimeanddate(text))
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1].strip())  # User's name
            messages.append(entry[2])  # Message content
        else:
            users.append('Group Notification')  # For system messages
            messages.append(entry[0])

    df['User'] = users
    df['Message'] = messages

    df['Message'] = df['Message'].apply(lambda text: getstring(text))  # Clean message

    # Drop unnecessary columns and add new ones
    df = df[['Message', 'date', 'User']]
    df['Only date'] = pd.to_datetime(df['date']).dt.date
    df['Year'] = pd.to_datetime(df['date']).dt.year
    df['Month_num'] = pd.to_datetime(df['date']).dt.month
    df['Month'] = pd.to_datetime(df['date']).dt.month_name()
    df['Day'] = pd.to_datetime(df['date']).dt.day
    df['Day_name'] = pd.to_datetime(df['date']).dt.day_name()
    df['Hour'] = pd.to_datetime(df['date']).dt.hour
    df['Minute'] = pd.to_datetime(df['date']).dt.minute

    return df

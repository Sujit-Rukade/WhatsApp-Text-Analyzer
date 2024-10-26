import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import preprocess
import stats
import os

st.sidebar.title("WhatsApp Chat Analyzer")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt", "json", "csv", "xlsx"])

if uploaded_file is not None:
    # Read the file based on its type
    file_extension = os.path.splitext(uploaded_file.name)[1]
    
    if file_extension == ".txt":
        # Handle text file
        data = uploaded_file.read().decode("utf-8")
    elif file_extension in [".csv", ".json", ".xlsx"]:
        # Handle other file types
        try:
            if file_extension == ".csv":
                data = pd.read_csv(uploaded_file)
            elif file_extension == ".json":
                data = pd.read_json(uploaded_file)
            elif file_extension == ".xlsx":
                data = pd.read_excel(uploaded_file)
            st.success("File loaded successfully.")
        except Exception as e:
            st.error(f"Error reading the file: {e}")
            data = None
    else:
        st.error("Unsupported file type. Please upload a text, CSV, JSON, or Excel file.")
        data = None

    if data is not None:
        df = preprocess.preprocess(data)
        st.dataframe(df) 

        user_list = df['User'].unique().tolist()
        
        user_list = [user for user in user_list if user != 'Group Notification']
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

        st.title(f"WhatsApp Chat Analysis for {selected_user}")

        if st.sidebar.button("Show Analysis"):
            # Get stats for selected user
            num_messages, num_words, media_omitted, links = stats.fetchstats(selected_user, df)

            # Basic stats display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total No. of Words")
                st.title(num_words)
            with col3:
                st.header("Media Shared")
                st.title(media_omitted)
            with col4:
                st.header("Total Links Shared")
                st.title(links)

            # Busiest users
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                busycount, newdf = stats.fetchbusyuser(df)
                fig, ax = plt.subplots()
                col1, col2 = st.columns(2)
                with col1:
                    ax.bar(busycount.index, busycount.values, color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(newdf)

            # Word Cloud
            st.title('Word Cloud')
            df_img = stats.createwordcloud(selected_user, df)
            if df_img is not None:
                st.image(df_img.to_array(), use_column_width=True)
            else:
                st.write("No words available to generate a word cloud.")

            # Most common words
            most_common_df = stats.getcommonwords(selected_user, df)
            if not most_common_df.empty:
                fig, ax = plt.subplots()
                ax.barh(most_common_df[0], most_common_df[1], color='skyblue')
                plt.xticks(rotation='vertical')
                st.title('Most Common Words')
                st.pyplot(fig)
            else:
                st.write("No common words found.")

            # Emoji Analysis
            emoji_df = stats.getemojistats(selected_user, df)
            if not emoji_df.empty:
                emoji_df.columns = ['Emoji', 'Count']
                st.title("Emoji Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    emojicount = list(emoji_df['Count'])
                    total_count = sum(emojicount)
                    emoji_df['Percentage Use'] = [(i / total_count) * 100 for i in emojicount]
                    st.dataframe(emoji_df)

            # Monthly Timeline
            st.title("Monthly Timeline")
            time = stats.monthtimeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(time['Time'], time['Message'], color='green')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

            # Activity maps
            st.title("Activity Maps")
            col1, col2 = st.columns(2)

            with col1:
                st.header("Most Busy Day")
                busy_day = stats.weekactivitymap(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='purple')
                plt.xticks(rotation='vertical')
                plt.tight_layout()
                st.pyplot(fig)

            with col2:
                st.header("Most Busy Month")
                busy_month = stats.monthactivitymap(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation='vertical')
                plt.tight_layout()
                st.pyplot(fig)

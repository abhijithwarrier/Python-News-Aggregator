# Programmer - python_scripts (Abhijith Warrier)

# PYTHON SCRIPT FOR AGGREGATING AND FETCHING THE NEWS BASED ON SENTIMENTS

# News can be classified into 3 types (All-NEUTRAL, Good-POSITIVE, Bad-Negative)
# The AYLIEN News API is the most powerful way of sourcing, searching, and syndicating
# analyzed and enriched news content. It is accessed by sending HTTP requests to server,
# which return JSON data in response

# Get 14-Days Trial AYLIEN News API License Key From
# https://newsapi.aylien.com/

# The Python Client for AYLIEN News API can be installed by pip install aylien_news_api
# It is compatible with Python 2.7 and 3.4+

# Importing the necessary packages
import tkinter as tk
import aylien_news_api
from tkinter import *
from aylien_news_api.rest import ApiException

# Defining the CreateWidgets() to create necessary widgets for the news aggregator
def CreateWidgets():
    searchLabel = Label(root, text="SEARCH FOR : ", bg="turquoise4", font=('Helvetica',10))
    searchLabel.grid(row=0, column=1, padx=5, pady=5)

    searchText = Entry(root, width=50, textvariable=searchnews)
    searchText.grid(row=0, column=2, padx=5, pady=5)

    searchButton = Button(root, width = 20, text="SEARCH", command=SearchNews)
    searchButton.grid(row=0, column=3, padx=5, pady=5)

    # Creating 3 Radiobuttons to select the type of the news
    allRadioBtn = Radiobutton(text="ALL", variable=s, value='neutral',bg="turquoise4",
                              font=('Helvetica',10))
    allRadioBtn.grid(row=1, column=1, padx=5, pady=5)

    goodRadioBtn = Radiobutton(text="GOOD NEWS", variable=s, value='positive', bg="turquoise4",
                               font=('Helvetica',10))
    goodRadioBtn.grid(row=1, column=2, padx=5, pady=5)

    badRadioBtn = Radiobutton(text="BAD NEWS", variable=s, value='negative', bg="turquoise4",
                              font=('Helvetica',10))
    badRadioBtn.grid(row=1, column=3, padx=5, pady=5)

    # Setting the default selection for the RadioButton
    s.set('neutral')

    root.newsResults = Text(root, width=70, height=30)
    root.newsResults.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

# Defining the SearchNews() for searching and fetching the news based on sentiments
def SearchNews():
    # Retrieving and storing user-input (News to be searched and type of news)
    searchFor = searchnews.get()
    newsType = s.get()

    # Storing aylien_news_api license keys
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = "YOUR ID"
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = "YOUR KEY"

    # Creating an instance of API Class
    api_instance = aylien_news_api.DefaultApi()

    # Parameters for fetching the news
    # Title, Language, Type of news(Sentiment), Published Time and
    # many more parameters can be specifed as well
    opts = {
        'title': searchFor,
        'language': ['en'],
        'sentiment_title_polarity' : newsType,
        'published_at_start': 'NOW-7DAYS',
        'published_at_end': 'NOW',
    }

    # Trying to Search and Fetch the News(stories)
    try:
        # List stories
        count = 1
        api_response = api_instance.list_stories(**opts)

        # Looping over the fetched News (stories)
        for news in api_response.stories:
            storyTitle = news.title
            storySource = news.source.name
            storyBody = news.body
            storyDate = news.published_at

            displayNews = "\n\n"+str(count)+". "+storyTitle+"\n\nSOURCE : "+storySource+\
                          "| PUBLISHED ON : "+str(storyDate)+"\n\n"+storyBody

            # Printing the fetched news
            root.newsResults.insert('1.0', displayNews)

            count = count + 1

    # Catching the API Exception if it occurs
    except ApiException as e:
        print("Exception when calling DefaultApi->list_stories: %sn" % e)

# Creating object root of tk
root = tk.Tk()

# Setting the title, background color, size of the window
# and disabling the resizing property
root.title("PyNewsAggregator")
root.resizable(False, False)
root.config(bg = "turquoise4")
root.geometry("590x575")

# Creating the tkinter StringVar() variables
searchnews = StringVar()
s = StringVar()

# Calling the CreateWidgets() function
CreateWidgets()

# Defining infinite loop to run application
root.mainloop()

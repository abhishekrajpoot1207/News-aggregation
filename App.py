import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import geocoder
import nltk
nltk.download('punkt')

st.set_page_config(page_title='News_Aggregation_System: A Summarised News📰 Portal', page_icon='./Meta/newspaper.ico')

def get_user_location():
    g = geocoder.ip('me')
    return g.city

def fetch_news_search_topic(topic):
    site = 'https://news.google.com/rss/search?q={}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        st.image(image, use_column_width=True)
    except:
        image = Image.open('./Meta/no_image.jpg')
        st.image(image, use_column_width=True)


def display_news(list_of_news, news_quantity):
    c = 0
    for news in list_of_news:
        c += 1
        # st.markdown(f"({c})[ {news.title.text}]({news.link.text})")
        st.write('**({}) {}**'.format(c, news.title.text))
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            st.error(e)
        fetch_news_poster(news_data.top_image)
        with st.expander(news.title.text):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}"</h6>'''.format(news_data.summary),
                unsafe_allow_html=True)
            st.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text))
        st.success("Published Date: " + news.pubDate.text)
        if c >= news_quantity:
            break


def run():


    st.title("News Aggregation System:📰")
    image = Image.open('./Meta/newspaper.png')
    

    col1, col2, col3 = st.columns([3, 5, 3])

    with col1:
        st.write("")

    with col2:
        st.image(image, use_column_width=False)

    with col3:
        st.write("")

    category = ['Local news','Location based search', 'Trending🔥 News', 'Favourite💙 Topics', 'Search🔍 Topic','Event wise news']
    cat_op = st.sidebar.selectbox('Select your Category', category)
    

    if cat_op == category[0]:
        user_location = get_user_location()
        st.text(f"Your location: {user_location}")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)

        if  user_location != '':
            user_topic_pr = user_location.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_location.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(user_location))
        else:
            st.warning("Please wait")
    elif cat_op == category[1]:
        user_topic = st.text_input("Enter Location")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=15, step=1)

        if st.button("Search") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(user_topic))
        else:
            st.warning("Please write Event name")


    elif cat_op == category[2]:
        st.subheader("✅ Here is the Trending🔥 news for you")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
        news_list = fetch_top_news()
        display_news(news_list, no_of_news)
    elif cat_op == category[3]:
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE',
                     'HEALTH']
        st.subheader("Choose your favourite Topic")
        chosen_topic = st.selectbox("Choose your favourite Topic", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Please Choose the Topic")
        else:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news(chosen_topic)
            if news_list:
                st.subheader("✅ Here are the some {} News for you".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(chosen_topic))
    

    elif cat_op == category[4]:
        user_topic = st.text_input("Enter your Topic🔍")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=15, step=1)

        if st.button("Search") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(user_topic))
        else:
            st.warning("Please write Topic Name to Search🔍")
    elif cat_op == category[5]:
        rad = st.sidebar.radio("Event Wise News",["BIHU","4th Grade Job Assam","Manipur Violence","Margherita rape case","Guwahati Child Abuse","Porn star in jorhat"]) 
        if rad == "BIHU":
          user_topic = 'bihu'
          no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
          
          if  user_topic != '':
             user_topic_pr = user_topic.replace(' ', '')
             news_list = fetch_news_search_topic(topic=user_topic_pr)
             if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
             else:
                st.error("No News found for {}".format(user_topic))
          else:
            st.warning("Please wait")
        if rad == "Margherita rape case":
          user_topic = 'Margherita'
          no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
          
          if  user_topic != '':
             user_topic_pr = user_topic.replace(' ', '')
             news_list = fetch_news_search_topic(topic=user_topic_pr)
             if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
             else:
                st.error("No News found for {}".format(user_topic))
          else:
            st.warning("Please wait")

        if rad == "4th Grade Job Assam":
          user_topic = 'AssamRecruitment'
          no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
          
          if  user_topic != '':
             user_topic_pr = user_topic.replace(' ', '')
             news_list = fetch_news_search_topic(topic=user_topic_pr)
             if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
             else:
                st.error("No News found for {}".format(user_topic))
          else:
            st.warning("Please wait")
    
        if rad == "Manipur Violence":
          user_topic = 'ManipurViolence'
          no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
          
          if  user_topic != '':
             user_topic_pr = user_topic.replace(' ', '')
             news_list = fetch_news_search_topic(topic=user_topic_pr)
             if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
             else:
                st.error("No News found for {}".format(user_topic))
          else:
            st.warning("Please wait")
    
        if rad == "Guwahati Child Abuse":
          user_topic = 'GuwahatiChildAbuse'
          no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
          
          if  user_topic != '':
             user_topic_pr = user_topic.replace(' ', '')
             news_list = fetch_news_search_topic(topic=user_topic_pr)
             if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
             else:
                st.error("No News found for {}".format(user_topic))
          else:
            st.warning("Please wait")
        if rad == "Porn star in jorhat":
          user_topic = 'jorhatViral'
          no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
          
          if  user_topic != '':
             user_topic_pr = user_topic.replace(' ', '')
             news_list = fetch_news_search_topic(topic=user_topic_pr)
             if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
             else:
                st.error("No News found for {}".format(user_topic))
          else:
            st.warning("Please wait")

run()

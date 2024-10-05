from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup

# Initialize the web driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
url = 'https://inflact.com/tools/profile-analyzer/'
driver.get(url)

# Define lists to store the extracted data
post_per_day = []
posts_per_week = []
post_per_month = []
total_posts = []
Engagement_rate = []
total_followers = []
Avg_user_activity = []

# Loop through each influencer username
for i, username in enumerate (null_user_name_to_scrape):
    # Wait until the input field for username is present
    username_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profileanalyzerform-username"]')))

    # Enter the username in the input field
    username_input.send_keys(username)

    # Wait until the search button is present and click it
    submit_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="account-form"]/div[2]/div[2]/button')))
    submit_button.click()

    
    # Wait for the page to load
    user= input("username") # I did this to monitor manually the oytcome after clicking because while using time.sleep() sometimes it's an issue with the internet and I dont get my values 
    

    # Get the HTML source code of the page a queastion will rise here why we do this and we are not using beautifulsoap directly ?
    #for this website I need to pass the username to get search results so we use selenum to do this then scrape the data using beautiful soap for shorter codr running time
    html_source = driver.page_source

    # Pass the HTML source to Beautiful Soup for parsing
    soup = BeautifulSoup(html_source, 'html.parser')

    # Extract the desired metrics using Beautiful Soup
    #for the bar charts we have there numbers we need so we will get a list of all desired numbers in bar charts then extract the data from it
    #create a list to store the data and scrape the bar charts
    # Bar elements
    bar_chart_data = soup.find_all("div", class_="pa-chart-data-number")


    #note: we are using try except becouse sometimes the list is empty due to a private account or whatever and we don't want our code to crash
    try:
        number_of_posts_per_day = bar_chart_data[0].get_text(strip=True)
        post_per_day.append(number_of_posts_per_day)
    except IndexError:
        post_per_day.append("")

    try:
        number_of_posts_per_week = bar_chart_data[1].get_text(strip=True)
        posts_per_week.append(number_of_posts_per_week)
    except IndexError:
        posts_per_week.append("")

    try:
        number_of_posts_per_month = bar_chart_data[2].get_text(strip=True)
        post_per_month.append(number_of_posts_per_month)
    except IndexError:
        post_per_month.append("")



    # Extract the desired metrics using Beautiful Soup
    #for the boxes we have four numbers we need so we will get a list of all desired numbers in boxes then extract the data from it
    #create a list to store the data and scrape the bar charts
    bar_chart_data =[]

    box_values_data = soup.find_all("div", class_="pa-number-value")
    # Box elements
    box_elements = soup.find_all("div", class_="pa-number-value")

    #note: we are using try except becouse sometimes the list is empty due to a private account or whatever and we don't want our code to crash
    try:
        number_of_post = box_values_data[0].get_text(strip=True)
        total_posts.append(number_of_post)
    except IndexError:
        total_posts.append("")

    try:
        Engagmentrate = box_values_data[1].get_text(strip=True)
        Engagement_rate.append(Engagmentrate)
    except IndexError:
        Engagement_rate.append("")

    try:
        numberof_followers = box_values_data[2].get_text(strip=True)
        total_followers.append(numberof_followers)
    except IndexError:
        total_followers.append("")

    try:
        avg_activity = box_values_data[3].get_text(strip=True)
        Avg_user_activity.append(avg_activity)
    except IndexError:
        Avg_user_activity.append("")

    # Re-locate the input field for the next iteration
    username_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profileanalyzerform-username"]')))

    #add the new data 
    df.loc[df['Username'] == username, 'Posts per Day'] = post_per_day[i]
    df.loc[df['Username'] == username, 'Posts per Week'] = posts_per_week[i]
    df.loc[df['Username'] == username, 'Posts per Month'] = post_per_month[i]
    df.loc[df['Username'] == username, 'Total Posts'] = total_posts[i]
    df.loc[df['Username'] == username, 'Engagement Rate'] = Engagement_rate[i]
    df.loc[df['Username'] == username, 'Total Followers'] = total_followers[i]
    df.loc[df['Username'] == username, 'Average User Activity'] = Avg_user_activity[i]

    # Clear the input field for the next username
    username_input.clear()
    time.sleep(5)
import requests
from bs4 import BeautifulSoup
import csv
import streamlit as st
import pandas as pd
import time
import os
st.title('Mobile Price Scraper and Filter App')
placeholder=st.empty()
def scrap():
    base_url = "https://priceoye.pk/mobiles"
    page = 1
    all_products = []
    counter=0

    placeholder.write("started scraping mobiles")
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        mobiles=soup.find_all("div",class_="p-title bold h5")
        prices=soup.find_all("div", class_="price-box p1")
        for mobile,price in zip(mobiles,prices):
            all_products.append([mobile.get_text(strip=True), int(price.get_text(strip=True)[2:].replace(',',''))])
        
        next_button = soup.find("a", id="next-button")
        if not next_button:
            break
        
        page += 1
        counter+=1
        placeholder.text(f"scrapped page: {counter}")
    time.sleep(1)
    placeholder.write("finished scraping")
    time.sleep(1)
    placeholder.write("writing data to exel file")
    time.sleep(1)
    with open("mobiles.csv","w",newline="",encoding="utf-8") as file:
        writer=csv.writer(file)
        writer.writerow(["Mobile","Price"])
        writer.writerows(all_products)
    placeholder.write("done")
    time.sleep(1)
    placeholder.empty()


if st.button("update data"):
    scrap()
    
brands=set()
if os.path.exists("mobiles.csv"):
    df=pd.read_csv("mobiles.csv")
    
    df = pd.read_csv("mobiles.csv")
    df['Brand'] = df['Mobile'].apply(lambda x: x.split()[0])
    df.to_csv("mobiles.csv", index=False) 
    
    
    
    search=st.text_input("search mobile") # SEARCH BAR
    if search:
        search_filter=df[df['Mobile'].str.contains(search,na=False,case=False) ]
    else:
        search_filter=df
    
    price=st.number_input("price less than")  # price flter
    if price:
        search_filter=search_filter[search_filter['Price']<=price]
    
    brands=search_filter['Brand'].unique()   # BRAND FILTER
    selected_brand = st.selectbox("Filter by mobile", ['All'] + list(brands))
    if selected_brand!="All":
        search_filter=search_filter[search_filter['Brand']==selected_brand]
    
    
    
    st.dataframe(search_filter,use_container_width=True)
else:
    placeholder.text("Data doesnot exist")
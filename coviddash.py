# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 13:29:38 2020

@author: Ben George
"""

import streamlit as st
import altair as alt
import pandas as pd 



st.cache(persist=True)
def load_data():
    covid=pd.read_csv("data.csv")
    covid["Date"]=pd.to_datetime(covid["Date"],format="%d-%m-%Y")
    latest=covid[covid["Date"] == "2020-09-30"][["Country","Confirmed","Recovered","Deaths","Active"]]
    return covid,latest
covid,latest= load_data()



st.title('🦠 Covid-19 Dashborad 🦠 ')
st.sidebar.markdown('🦠 **Covid-19 Dashborad** 🦠 ')
st.sidebar.markdown(''' 
This app is to give insights about Covid-19 Infections around the world.

The data considerd for this analysis for 8 Months starting from 01-02-2020 to 30-09-2020

Select the different options to vary the Visualization

All the Charts are interactive. 

Scroll the mouse over the Charts to feel the interactive features like Tool tip, Zoom, Pan
                    

Designed by: 
**Ben George**  ''')  

st.header("Select the Country to Visualize the Covid-19 Cases")
    
cty = st.selectbox("Select country",covid["Country"][:186])



st.header(f"View Daily New Cases/Recoveries/Deaths for {cty}")
daily = st.selectbox("Select the option",('Daily New Cases', 'Daily New Recoveries','Daily New Deaths'))
typ = st.radio("Select the type of Chart",("Line Chart","Scatter Chart"))

ca = alt.Chart(covid[covid["Country"]==cty]).encode(
    x="Date",
    y="New cases",
    tooltip=["Date","Country","New cases"]
).interactive()

re = alt.Chart(covid[covid["Country"]==cty]).encode(
    x="Date",
    y="New recovered",
    tooltip=["Date","Country","New recovered"]
).interactive()

de = alt.Chart(covid[covid["Country"]==cty]).encode(
    x="Date",
    y="New deaths",
    tooltip=["Date","Country","New deaths"]
).interactive()

cas= alt.Chart(covid[covid["Country"]==cty],title="Scatter Chart",width=500,height=400).mark_circle(color='green').encode(
    x="Date",
    y="New cases",
    size="New deaths",
    color="New recovered",
    tooltip=["Date","Country","New cases","New deaths","New recovered"]
).interactive()




if daily =='Daily New Cases':
    if typ == "Line Chart":
        st.altair_chart(ca.mark_line(color='firebrick'))
    else:
        st.altair_chart(ca.mark_circle(color='firebrick'))
elif daily =='Daily New Recoveries':
    if typ == "Line Chart":
        st.altair_chart(re.mark_line(color='green'))
    else:
        st.altair_chart(re.mark_circle(color='green'))
elif daily =='Daily New Deaths':
    if typ == "Line Chart":
        st.altair_chart(de.mark_line(color='purple'))
    else:
        st.altair_chart(de.mark_circle(color='purple'))

"Visualizing Daily New Cases, recoveries and deaths in a Single Chart"
"In Scatter Chart, Circle represent daily new cases, size of the circle shows the daily deaths and the color variation shows the daily recoveries"
st.altair_chart(cas)

a= alt.Chart(covid[covid["Country"]==cty],width=500,height=400).mark_bar().encode(
    x="day(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

b=alt.Chart(covid[covid["Country"]==cty],width=500,height=400).mark_text().encode(
    x="day(Date):O",
    y="month(Date):O",
    text="sum(New deaths)" 
)

c= alt.Chart(covid[covid["Country"]==cty],width=500,height=100).mark_bar().encode(
    x="day(Date):O",
   # y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

d=alt.Chart(covid[covid["Country"]==cty],width=500,height=100).mark_text().encode(
    x="day(Date):O",
    #y="month(Date):O",
    text="sum(New deaths)" 
)
st.header(f"View deaths for {cty} by Month/Day/Date")

e= alt.Chart(covid[covid["Country"]==cty],width=900,height=300).mark_bar().encode(
    x="date(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

f=alt.Chart(covid[covid["Country"]==cty],width=900,height=300).mark_text(angle=270).encode(
    x="date(Date):O",
    y="month(Date):O",
    text="sum(New deaths)" 
)

g= alt.Chart(covid[covid["Country"]==cty],width=900,height=100).mark_bar().encode(
    x="date(Date):O",
   # y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

h=alt.Chart(covid[covid["Country"]==cty],width=900,height=100).mark_text(angle=270).encode(
    x="date(Date):O",
    #y="month(Date):O",
    text="sum(New deaths)" 
)



op = st.radio("Select the option",('Day and Month', 'Day','Date and Month','Date'))

if op == 'Day and Month':
     st.altair_chart(a+b)
elif op == 'Day':
    st.altair_chart(c+d)
elif op == 'Date and Month':
    st.altair_chart(e+f)
elif op == 'Date':
    st.altair_chart(g+h)



st.header(f"View Total Confirmed vs Total Recovered cases for {cty}")

con=alt.Chart(covid[covid["Country"]==cty]).mark_area(color="purple").encode(
    x="Date",
    y="Confirmed",
    tooltip=["Date","Confirmed"]
    
).interactive()

rec=alt.Chart(covid[covid["Country"]==cty]).mark_area(color="green").encode(
    x="Date",
    y="Recovered",
    tooltip=["Date","Recovered"]
    
).interactive()

opt = st.radio(
     "Select the option",
     ('Confirmed', 'Recovered','Confirmed and Recovered'))

if opt == 'Confirmed':
     st.altair_chart(con)
elif opt == 'Recovered':
    st.altair_chart(rec)
else:
     st.altair_chart(con+rec)


st.header(f"Summary of Covid-19 infections in {cty}")
"From 01-02-2020 to 30-09-2020"
tot = latest[latest["Country"]==cty]['Confirmed'].sum()

#st.subheader(f"Total Confirmed cases in {cty} = {tot}")

reco = latest[latest["Country"]==cty]['Recovered'].sum()

#st.subheader(f"Total Recovered in {cty} = {reco}")

act = latest[latest["Country"]==cty]['Active'].sum()

#st.subheader(f"Total Active cases in {cty} = {act}")

dths = latest[latest["Country"]==cty]['Deaths'].sum()

#st.subheader(f"Total Deaths occured in {cty} = {dths}")
infsing = covid[covid["Country"]==cty]['New cases'].max()

deasing = covid[covid["Country"]==cty]['New deaths'].max()

recsing = covid[covid["Country"]==cty]['New recovered'].max()

tab = {"Category":["Total Confirmed Cases","Total Recovered","Total Active Cases","Total Deaths","Maximum Cases on a Single Day","Maximum Deaths on a Single Day","Maximum Recoveries on a Single Day"],
       "Total Count":[tot,reco,act,dths,infsing,deasing,recsing]}

stat = pd.DataFrame(tab)
st.table(stat)



st.header(f"Daily New Cases and Total Cases for Selected Countries")


options = st.multiselect(
    'Select Multiple Countries',
     covid["Country"][:186])


fire=alt.Chart(covid[covid["Country"].isin(options)],width=500,height=300).mark_circle().encode(
    x="Date",
    y="Country",
    tooltip=["Date","Country","New cases"],
    color="Country",
    size="New cases"
).interactive()

bar1 = alt.Chart(covid[covid["Country"].isin(options)]).mark_bar().encode(
    y="sum(New cases)",
    x=alt.X("Country",sort="-y"),
    color="Country",
    tooltip = "sum(New cases)"
).interactive()

st.altair_chart(fire | bar1)

texchart=alt.Chart(covid[covid["Country"].isin(options)],width=800,height=400).mark_text().encode(
    x=alt.X('sum(New cases)',axis=None),
    y=alt.Y("Country",axis=None),
    size=alt.Size("sum(New cases)",scale=alt.Scale(range=[10, 150]),legend=None),
    text="Country",
    color=alt.Color("Country",legend=None),
    tooltip=["Country","sum(New cases)"]
).configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
st.markdown("### World Cloud representing total confirmed cases for the selected countries")
st.altair_chart(texchart)

confirm = latest.sort_values("Confirmed",ascending=False)[["Country","Confirmed"]].head()

confirm.reset_index(inplace = True,drop = True)

bar2 = alt.Chart(confirm).mark_bar().encode(
    x="Confirmed",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Confirmed"
).interactive()


death = latest.sort_values("Deaths",ascending=False)[["Country","Deaths"]].head()

death.reset_index(inplace = True,drop = True)

bar3 = alt.Chart(death).mark_bar().encode(
    x="Deaths",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Deaths"
).interactive()



deathper=latest["Deaths"] / latest["Confirmed"] * 100
lat = latest.copy()
lat["Death Percentage"] = deathper
deathp = lat.sort_values("Death Percentage",ascending=False)[["Country","Death Percentage"]].head()

deathp.reset_index(inplace = True,drop = True)

bar4 = alt.Chart(deathp).mark_bar().encode(
    x="Death Percentage",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Death Percentage"
).interactive()


recover = latest.sort_values("Recovered",ascending=False)[["Country","Recovered"]].head()

recover.reset_index(inplace = True,drop = True)

bar5 = alt.Chart(recover).mark_bar().encode(
    x="Recovered",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Recovered"
).interactive()


recper=latest["Recovered"] / latest["Confirmed"] * 100
lat = latest.copy()
lat["Recovered Percentage"] = recper
recp = lat.sort_values("Recovered Percentage",ascending=False)[["Country","Recovered Percentage"]].head()

recp.reset_index(inplace = True,drop = True)

bar6 = alt.Chart(recp).mark_bar().encode(
    x="Recovered Percentage",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Recovered Percentage"
).interactive()




st.header(f"Do you want to know the Top 5 countries")
top = st.selectbox("Select your option",["Confirmed Cases","Deaths","Death Percentage","Recovered","Recovered Percentage"])
if top == "Confirmed Cases":
    st.altair_chart(bar2)
elif top == "Deaths":
    st.altair_chart(bar3)
elif top == "Death Percentage":
    st.altair_chart(bar4)
elif top == "Recovered":
    st.altair_chart(bar5)
else:
    st.altair_chart(bar6)
    

st.header(f"View Covid-19 details by Date")
import datetime
ddd = st.date_input(
     "Select the Date",value = datetime.date(2020, 2, 1),min_value = datetime.date(2020, 2, 1), max_value= datetime.date(2020, 9, 30) )
#st.write('The selected date is:', ddd)
#covid[covid["Date"]==ddd]
#st.dataframe(covid.iloc[[covid[covid["Date"] == dd]["New cases"].idxmax()]][["Country","Date","New cases"]].reset_index(drop=True))
ques = st.selectbox("Select the option to know details",["Maximum Cases","Maximum Recovered","Maximum Deaths"])

if ques == "Maximum Cases":
    st.dataframe(covid.iloc[[covid[covid["Date"] == pd.Timestamp(ddd)]["New cases"].idxmax()]][["Country","Date","New cases"]].reset_index(drop=True))
elif ques == "Maximum Recovered":
    st.dataframe(covid.iloc[[covid[covid["Date"] == pd.Timestamp(ddd)]["New recovered"].idxmax()]][["Country","Date","New recovered"]].reset_index(drop=True))
elif ques == "Maximum Deaths":
    st.dataframe(covid.iloc[[covid[covid["Date"] == pd.Timestamp(ddd)]["New deaths"].idxmax()]][["Country","Date","New deaths"]].reset_index(drop=True))



st.header(f"View Covid-19 Country Standings")

ques2 = st.radio("Select the option to know details",["Total Confirmed Cases","Total Recovered","Total Deaths","Total Active Cases"])

if ques2 == "Total Confirmed Cases":
    dff = latest.sort_values(by="Confirmed",ascending=False)[["Country","Confirmed"]].reset_index(drop=True)
    dff.index+=1
    st.dataframe(dff)
elif ques2 == "Total Recovered":
    dff = latest.sort_values(by="Recovered",ascending=False)[["Country","Recovered"]].reset_index(drop=True)
    dff.index+=1
    st.dataframe(dff)
elif ques2 == "Total Deaths":
    dff = latest.sort_values(by="Deaths",ascending=False)[["Country","Deaths"]].reset_index(drop=True)
    dff.index+=1
    st.dataframe(dff)
else:
    dff = latest.sort_values(by="Active",ascending=False)[["Country","Active"]].reset_index(drop=True)
    dff.index+=1
    st.dataframe(dff)


st.header(f"View the Dataset by Month")

if st.checkbox("Click to View the Dataset",False):
    "Select the Month from Slider"
    nc = st.slider("Month",2,9,2,1)
    covid = covid[covid["Date"].dt.month ==nc]
    "data", covid
    






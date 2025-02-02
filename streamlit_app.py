import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import altair as alt
import pydeck as pdk

st.set_page_config(layout="wide")

st.markdown(
        "<h1 style='font-size: 62px; text-align: center;'>Data Analysis of AB \"Šiaulių Energija\"</h1>",
        unsafe_allow_html=True
    )
sidebar = st.sidebar
sidebar.header("Settings")
res_side = sidebar.selectbox("Select category", ("Heat, kWh", "Hot water, m³"), placeholder="Heat", key=48)
lang = sidebar.selectbox("Language / Kalba", ("English", "Lietuvių"), placeholder="English", key=47)
tab1, tab2, tab3, tab4 = st.tabs(["Overall Consumption Trends", "Trends by building function", "Rooms data", "Machine Learning Predictions"])
with tab1:
    st.markdown(
    "<h1 style='text-align: center;'>Energy Consumption Trends</h1>",
    unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)
    
    
    with col1:
        #_---------------------------------------------
        # Monthly trend data
        st.markdown(
            "<h3 style='text-align: center;'>Monthly</h1>",
            unsafe_allow_html=True
        )
        monthly_trend = pd.read_csv("monthly_trend.csv")
        monthly_trend["Date"] = pd.to_datetime(monthly_trend["month"])
        
        opt = {
            'Heat, kWh': 'Šiluma',
            'Hot water, m³': 'Karštas vanduo'
        }
        res_lt = opt[res_side]
        st.line_chart(monthly_trend, x="Date", y=res_lt, y_label=res_side)
        
    with col2:
        st.markdown(
            "<h3 style='text-align: center;'>Yearly</h1>",
            unsafe_allow_html=True
        )
        #_---------------------------------------------
        # Yearly trend data
        monthly_trend = pd.read_csv("yearly_trend.csv")
        opt = {
            'Heat, kWh': 'Šiluma',
            'Hot water, m³': 'Karštas vanduo'
        }
        res_lt = opt[res_side]
        st.bar_chart(monthly_trend, x="year", y=res_lt, y_label=res_side)
        #------------------------------------------------
    st.markdown(
    "<h1 style='text-align: center;'>Number Of Provided Services Trends</h1>",
    unsafe_allow_html=True
    )
    col3, col4 = st.columns(2)
    with col3:
        # Contracts monthly trend
        contract_trend = pd.read_csv("contract_trend.csv")
        st.markdown(
            "<h3 style='text-align: center;'>Monthly</h1>",
            unsafe_allow_html=True
        )
        st.line_chart(contract_trend, x="month", y="0")
    with col4:
        #------------------------------------------------
        # Contracts yearly trend
        contract_trend = pd.read_csv("contract_trend_yearly.csv")
        st.markdown(
            "<h3 style='text-align: center;'>Yearly</h1>",
            unsafe_allow_html=True
        )
        st.bar_chart(contract_trend, x="year", y="0")
        #----------------------------------------------
    st.markdown(
    "<h1 style='text-align: center;'>Consumption Heatmap</h1>",
    unsafe_allow_html=True
    )
    opt = {
        'Heat, kWh': "geo_amount_heat.csv",
        'Hot water, m³': "geo_amount_wat.csv"
    }
    res_lt = opt[res_side]

    date_range = pd.date_range(start="2019-01-01", end="2023-12-31", freq='MS').to_pydatetime().tolist()

    # Create the slider with the list of dates as options
    res_date = st.select_slider("Datetime to view", options=date_range, value=datetime(2019, 1, 1))
    res_date = str(res_date.date())
    geo_amount = pd.read_csv(res_lt)
    geo_amount_filtered = geo_amount[geo_amount["month"] == res_date]
    st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=55.9192288419136,
            longitude=23.29157347671509,
            zoom=11.6,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HeatmapLayer",
                data=geo_amount_filtered,
                get_position="[x_grid, y_grid]",
                get_weight="amount",
                radiusPixels=80,
                intensity=1,
                threshold=0.1,
            )
            
        ],
    )
    
    )
    
with tab2:
    
    col5, col6 = st.columns(2)
    # Building funcs
    with col5:
        st.markdown(
            "<h3 style='text-align: center;'>Number of rooms by building function</h1>",
            unsafe_allow_html=True
        )
        rooms = pd.read_csv("rooms.csv")
        func_val_counts = rooms["building_func"].value_counts()
        st.table(func_val_counts)
    with col6:
        st.markdown(
            "<h3 style='text-align: center;'>Consumption Efficiency by function</h1>",
            unsafe_allow_html=True
        )
        func_df = pd.read_csv("func_df.csv")
        bar_chart = alt.Chart(func_df).mark_bar().encode(
        y=alt.Y('building_func:N', sort='-x', title='Building Function'),
        x=alt.X('eff:Q')
        ).properties(height=635
        )
        st.altair_chart(bar_chart, use_container_width=True)
    #------------------------------------------------
    # Yearly consumption by building func
    heat_cons_by_func = pd.read_csv("heat_cons_by_func.csv")
    wat_cons_by_func = pd.read_csv("wat_cons_by_func.csv")
    st.write("### Yearly Consumption trend by building function")

    opt = {
        'Heat, kWh': heat_cons_by_func,
        'Hot water, m³': wat_cons_by_func
    }
    res_lt = opt[res_side]

    df_melted = res_lt.melt(id_vars=['year'], var_name='Category', value_name='Value')

    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X('year:O', title='Year', scale=alt.Scale(zero=False)),
        y=alt.Y('sum(Value):Q', title='Total Value', scale=alt.Scale(zero=False)),
        color='Category:N',
        order=alt.Order('Value', sort="descending")
    ).properties(
        width=600,
        height=400).interactive()
    st.altair_chart(chart, use_container_width=True)

    
with tab3:

    col7, col8 = st.columns(2)
    with col7:
        st.markdown(
        "<h1 style='font-size: 48px; text-align: center;'>No. Unique rooms</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        "<h1 style='font-size: 72px; text-align: center;'>44900</h1>",
        unsafe_allow_html=True
    )
        area_df = pd.read_csv("area_df.csv")
        st.header("Average heat consumption per square meter against area size")

        chart = alt.Chart(area_df).mark_bar().encode(
            x=alt.X("area_bins:N", sort="-y"),
            y="eff:Q",
        )
        st.altair_chart(chart, use_container_width=True)
    with col8:
        st.markdown(
        "<h1 style='font-size: 48px; text-align: center;'>No. Unique buildings</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        "<h1 style='font-size: 72px; text-align: center;'>1421</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        "<h1 style='font-size: 48px; text-align: center;'>Average room area</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        "<h1 style='font-size: 72px; text-align: center;'>71.6 m^2</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        "<h1 style='font-size: 48px; text-align: center;'>Biggest room area</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        "<h1 style='font-size: 72px; text-align: center;'>40760 m^2</h1>",
        unsafe_allow_html=True
    )
    st.write("### Number of rooms per buyer, top 20")
    buyer_rooms = pd.read_csv("buyer_rooms.csv")
    st.bar_chart(buyer_rooms["room_id"])

    #-------------------------------------------
    # Consumption by building year

    heat_by_build_year = pd.read_csv("heat_by_build_year.csv")
    st.header("Heat consumption per square meter by building build year")
    st.write("Over time we can see that heat consumption decreases as buildings get younger, which can be attributed to better technology, heat insulation maybe")
    st.bar_chart(heat_by_build_year, x="build_year", y="eff")
    #------------------------------------------------------------------
    st.write("# Oldest building was built in -- 1849")
    st.write("# Most frequent build year -- 1970 (1924 buildings)")

    st.write("## Geospatial building age heatmap")

    geo_build = pd.read_csv("geo_build.csv")
    geo_build = geo_build[geo_build["build_year"] > 1900]
    st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=55.9192288419136,
            longitude=23.29157347671509,
            zoom=11.6,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HeatmapLayer",
                data=geo_build,
                get_position="[x_coord, y_coord]",
                get_weight="build_year",
                radiusPixels=80,
                intensity=1,
                threshold=0.1,
                colorRange=[
                        [0, 128, 128, 255],  # Teal
                        [64, 160, 160, 255],  # Intermediate teal
                        [128, 192, 192, 255],  # Light teal
                        [144, 238, 144, 255]  # Light green
                    ]
            )
            
        ],
    )
    )
    st.write("# Median amount of floors per building -- 5 Floors")
    st.write("# Highest building -- 15 floors")

    st.write("## Geospatial building floors heatmap")

    geo_floors = pd.read_csv("geo_floors.csv")
    st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=55.9192288419136,
            longitude=23.29157347671509,
            zoom=11.6,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HeatmapLayer",
                data=geo_floors,
                get_position="[x_coord, y_coord]",
                get_weight="building_floors",
                radiusPixels=80,
                color_domain=[1, 15],
                intensity=1,
                threshold=0.1,
            )
            
        ],
    )
    )

with tab4:
    st.write("br")
    
    
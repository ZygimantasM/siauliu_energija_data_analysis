import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import altair as alt
import pydeck as pdk


st.header('Data Analysis of AB "Siauliu Energija"')

sidebar = st.sidebar
sidebar.header("Settings")

tab1, tab2, tab3, tab4 = st.tabs(["Overall Consumption Trends", "Trends by building function", "Rooms data", "Geospatial Data"])
with tab1:
    #_---------------------------------------------
    # Monthly trend data
    monthly_trend = pd.read_csv("monthly_trend.csv")
    monthly_trend["Date"] = pd.to_datetime(monthly_trend["month"])
    st.write("### Monthly Energy Consumption Trends")
    res = st.selectbox("Select category", ("Heat, kWh", "Hot water, m³"), placeholder="Heat")
    opt = {
        'Heat, kWh': 'Šiluma',
        'Hot water, m³': 'Karštas vanduo'
    }
    res_lt = opt[res]
    st.line_chart(monthly_trend, x="Date", y=res_lt, y_label=res)
    #_---------------------------------------------
    # Yearly trend data
    monthly_trend = pd.read_csv("yearly_trend.csv")
    st.write("### Yearly Energy Consumption Trends")
    res = st.selectbox("Select category", ("Heat, kWh", "Hot water, m³"), placeholder="Heat", key=42)
    opt = {
        'Heat, kWh': 'Šiluma',
        'Hot water, m³': 'Karštas vanduo'
    }
    res_lt = opt[res]
    st.bar_chart(monthly_trend, x="year", y=res_lt, y_label=res)
    #------------------------------------------------
    # Contracts monthly trend
    contract_trend = pd.read_csv("contract_trend.csv")
    st.write("### Monthly trend of Number Of Provided Services")
    st.line_chart(contract_trend, x="month", y="0")
    #------------------------------------------------
    # Contracts yearly trend
    contract_trend = pd.read_csv("contract_trend_yearly.csv")
    st.write("### Yearly trend of Number Of Provided Services")
    st.bar_chart(contract_trend, x="year", y="0")
    #----------------------------------------------
with tab2:
    # Building funcs
    rooms = pd.read_csv("rooms.csv")
    func_val_counts = rooms["building_func"].value_counts()
    st.table(func_val_counts)
    #------------------------------------------------
    # Yearly consumption by building func
    heat_cons_by_func = pd.read_csv("heat_cons_by_func.csv")
    wat_cons_by_func = pd.read_csv("wat_cons_by_func.csv")
    st.write("### Yearly Heat Consumption trend by building function")

    res = st.selectbox("Select category", ("Heat, kWh", "Hot water, m³"), placeholder="Heat", key=43)
    opt = {
        'Heat, kWh': heat_cons_by_func,
        'Hot water, m³': wat_cons_by_func
    }
    res_lt = opt[res]

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

    st.header("Average monthly heat consumption by building function")
    func_df = pd.read_csv("func_df.csv")
    bar_chart = alt.Chart(func_df).mark_bar().encode(
    y=alt.Y('building_func:N', sort='-x', title='Building Function'),
    x=alt.X('eff:Q', title='Average Monthly Heat Consumption')
    ).properties(
    title='Average Monthly Heat Consumption by Building Function'
    )
    st.altair_chart(bar_chart, use_container_width=True)
with tab3:
    #-------------------------------------------------
    # rooms per buyer
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
    area_df = pd.read_csv("area_df.csv")
    st.header("Average heat consumption per square meter against area size")

    st.bar_chart(area_df, x="area_bins", y="eff")
with tab4:
    st.header("Geospatial consumption heatmap")
    res = st.selectbox("Select category", ("Heat, kWh", "Hot water, m³"), placeholder="Heat", key=44)
    opt = {
        'Heat, kWh': "geo_amount_heat.csv",
        'Hot water, m³': "geo_amount_wat.csv"
    }
    res_lt = opt[res]

    date_range = pd.date_range(start="2019-01-01", end="2023-12-31", freq='MS').to_pydatetime().tolist()

    # Create the slider with the list of dates as options
    res_date = st.select_slider("Datetime to view", options=date_range, value=datetime(2019, 1, 1))
    res_date = str(res_date.date())
    geo_amount = pd.read_csv(res_lt)
    geo_amount_filtered = geo_amount[geo_amount["month"] == res_date]
    st.write(len(geo_amount_filtered))
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
    st.header("Geospatial building age heatmap")

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
    st.markdown(
        """
        <style>
        .legend {
            background-color: white;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            position: absolute;
            bottom: 20px;
            left: 20px;
            z-index: 1000;
            color: black; 
        }
        .legend div {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }
        .legend div div {
            width: 20px;
            height: 20px;
            margin-right: 5px;
        }
        </style>

        <div class="legend">
            <b>Legend</b><br>
            <div>
                <div style="background-color: rgba(0, 128, 128, 1);"></div>Old
            </div>
            <div>
                <div style="background-color: rgba(144, 238, 144, 1);"></div>New
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("Geospatial building floors heatmap")

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

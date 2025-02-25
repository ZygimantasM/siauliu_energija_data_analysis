import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import altair as alt
import pydeck as pdk
from helper_funcs import get_prediction
from streamlit_folium import st_folium
import folium

st.set_page_config(layout="wide")

sidebar = st.sidebar
sidebar.header("Settings / Nustatymai")

lang = sidebar.selectbox("Language / Kalba", ("English", "Lietuvių"), placeholder="English", key=47)

lt_mappings = {
    "Data Analysis of AB \"Šiaulių Energija\"": "Duomenų Analizė AB \"Šiaulių Energija\"",
    "Select Category": "Pasirink Kategorija",
    "Overall Consumption Trends": "Bendrosios Energijos Vartojimo Tendencijos",
    "Trends By Building Function": "Energijos Vartojimas Pagal Pastatų Funkcijas",
    "Rooms Data": "Patalpų Duomenys",
    "Machine Learning Predictions": "Dirbtinio intelekto prognozavimas",
    "Energy Consumption Trends": "Energijos Vartojimo Tendencijos",
    "Monthly": "Kas mėnesį",
    "Yearly": "Kas Metus",
    "Number Of Provided Services": "Kiekis Teiktų Paslaugų",
    "Consumption Heatmap": "Energijos Vartojimo Šiluminis Žemėlapis",
    "## Select date to view": "## Pasirinkite laikotarpį",
    "Number of Rooms by Building Function": "Skaičius patalpų pagal pastato funkciją",
    "Average Monthly Heat Consumption / m² by Function": "Vidutinis mėnesinis šilumos suvartojimas / m² pagal pastato funkciją",
    "### Yearly Consumption trend by building function": "### Metinės vartojimo tendencijos pagal pastato funkciją",
    "No. Unique rooms": "Skaičius unikalių patalpų",
    "Average Heat Consumption / m² against Room Area": "Vidutinis Šilumos suvartojimas / m² lyginant su patalpos plotu",
    "No. Unique buildings": "Skaičius unikalių pastatų",
    "Average room area": "Vidutinis patalpos plotas",
    "Biggest room area": "Didžiausias patalpos plotas",
    "## Number of Rooms per buyer, Top 20 buyers": "## Skaičius Patalpų priklausančių kiekvienam pirkėjui, Top 20 pirkėjų",
    "## Average Heat Consumption / m² by buildings build year": "## Vidutinis Šilumos suvartojimas / m² pagal pastato statybos metus",
    "Over time we can see that heat consumption decreases as buildings get younger, which can be attributed to better construction and insulation technology. Specifically buildings built after 1940 and then 2000 have lower consumption heat consumption on average": "Laikui bėgant, matome, kad šilumos suvartojimas mažėja, kai pastatai tampa naujesni, o tai galima priskirti geresnei statybos ir izoliacijos technologijai. Konkrečiai, pastatai, pastatyti po 1940 m. ir tada po 2000 m., vidutiniškai turi mažesnį šilumos suvartojimą.",
    "# Oldest building was built in -- 1849": "# Seniausias pastatas buvo pastatytas -- 1849 m.",
    "# Most frequent build year -- 1970 (1924 buildings)": "# Dažniausiai pasidorantys statybos metai -- 1970 m. (1924 Pastatų)",
    "## Geospatial building age heatmap": "## Geografinis pastatų amžiaus šiluminis žemėlapis",
    "# Median amount of floors per building -- 5 Floors": "# Vidutinis aukštų skaičius pastate -- 5 aukštai (Mediana)",
    "# Highest building -- 15 floors": "# Aukščiausias pastatas -- 15 aukštų",
    "## Geospatial building floors heatmap": "## Geografinis pastatų aukštų šiluminis žemėlapis",
    "Heat, kWh": "Šiluma, kWh",
    "Hot water, m³": "Karštas vanduo, m³",
    "Date": "Data",
    "Year": "Metai",
    "No. Services": "Skaičius paslaugų",
    "Building Function": "Pastato funkcija",
    "Room Area, m²": "Patalpos Plotas, m²",
    "Individual buyers": "Individualūs pirkėjai",
    "No. Rooms": "Skaičius patalpų",
    "Build Year": "Statybos metai"

}

def trans(text, lang=lang):
    if lang == "English":
        return text
    else:
        return lt_mappings[text]

res_side = sidebar.selectbox(trans("Select Category"), (trans("Heat, kWh"), trans("Hot water, m³")), placeholder="Heat", key=48)

st.markdown(
        f"<h1 style='font-size: 62px; text-align: center;'>{trans("Data Analysis of AB \"Šiaulių Energija\"")}</h1>",
        unsafe_allow_html=True
    )










tab1, tab2, tab3, tab4 = st.tabs([trans("Overall Consumption Trends"), trans("Trends By Building Function"), trans("Rooms Data"), trans("AI Consumption Estimation Tool")])
with tab1:
    st.markdown(
    f"<h1 style='text-align: center;'>{trans("Energy Consumption Trends")}</h1>",
    unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)
    
    
    with col1:
        #_---------------------------------------------
        # Monthly trend data
        st.markdown(
            f"<h3 style='text-align: center;'>{trans("Monthly")}</h1>",
            unsafe_allow_html=True
        )
        monthly_trend = pd.read_csv("monthly_trend.csv")
        monthly_trend["Date"] = pd.to_datetime(monthly_trend["month"])
        
        opt = {
            'Heat, kWh': 'Šiluma',
            'Hot water, m³': 'Karštas vanduo',
            "Šiluma, kWh": "Šiluma",
            "Karštas vanduo, m³": "Karštas vanduo"
        }
        res_lt = opt[res_side]
        st.line_chart(monthly_trend, x="Date", y=res_lt, y_label=res_side, x_label = trans("Date"), color="#fcaa01")
        
    with col2:
        st.markdown(
            f"<h3 style='text-align: center;'>{trans("Yearly")}</h1>",
            unsafe_allow_html=True
        )
        #_---------------------------------------------
        # Yearly trend data
        monthly_trend = pd.read_csv("yearly_trend.csv")
        res_lt = opt[res_side]
        st.bar_chart(monthly_trend, x="year", y=res_lt, y_label=res_side, x_label=trans("Year"),color= "#fcaa01")
        #------------------------------------------------
    st.markdown(
    f"<h1 style='text-align: center;'>{trans("Number Of Provided Services")}</h1>",
    unsafe_allow_html=True
    )
    col3, col4 = st.columns(2)
    with col3:
        # Contracts monthly trend
        contract_trend = pd.read_csv("contract_trend.csv")
        contract_trend["month"] = pd.to_datetime(contract_trend["month"])
        st.markdown(
            f"<h3 style='text-align: center;'>{trans("Monthly")}</h1>",
            unsafe_allow_html=True
        )
        st.line_chart(contract_trend, x="month", y="0", y_label=trans("No. Services"), x_label=trans("Date"), color="#fcaa01")
    with col4:
        #------------------------------------------------
        # Contracts yearly trend
        contract_trend = pd.read_csv("contract_trend_yearly.csv")
        st.markdown(
            f"<h3 style='text-align: center;'>{trans("Yearly")}</h1>",
            unsafe_allow_html=True
        )
        st.bar_chart(contract_trend, x="year", y="0", x_label=trans("Year"), y_label=trans("No. Services"), color="#fcaa01")
        #----------------------------------------------
    st.markdown(
    f"<h1 style='text-align: center;'>{trans("Consumption Heatmap")}</h1>",
    unsafe_allow_html=True
    )

    opt_csv = {
            'Heat, kWh': 'geo_amount_heat.csv',
            'Hot water, m³': 'geo_amount_wat.csv',
            "Šiluma, kWh": 'geo_amount_heat.csv',
            "Karštas vanduo, m³": 'geo_amount_wat.csv'
        }
    res_csv = opt_csv[res_side]

    date_range = pd.date_range(start="2019-01-01", end="2023-12-31", freq='MS').to_pydatetime().tolist()

    # Create the slider with the list of dates as options
    st.write(trans("## Select date to view"))
    res_date = st.select_slider(" ", options=date_range, value=datetime(2019, 1, 1))
    res_date = str(res_date.date())
    geo_amount = pd.read_csv(res_csv)
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
            f"<h3 style='text-align: center;'>{trans("Number of Rooms by Building Function")}</h1>",
            unsafe_allow_html=True
        )
        rooms = pd.read_csv("rooms.csv")
        func_val_counts = rooms["building_func"].value_counts()
        st.table(func_val_counts)
    with col6:
        st.markdown(
            f"<h3 style='text-align: center;'>{trans("Average Monthly Heat Consumption / m² by Function")}</h1>",
            unsafe_allow_html=True
        )
        func_df = pd.read_csv("func_df.csv")
        bar_chart = alt.Chart(func_df).mark_bar().encode(
        y=alt.Y('building_func:N', sort='-x', title=trans('Building Function')),
        x=alt.X('eff:Q', title="kWh / m²"),
        color=alt.value("#fcaa01")
        ).properties(height=600
        )
        st.altair_chart(bar_chart, use_container_width=True)
    #------------------------------------------------
    # Yearly consumption by building func
    heat_cons_by_func = pd.read_csv("heat_cons_by_func.csv")
    wat_cons_by_func = pd.read_csv("wat_cons_by_func.csv")
    st.write(trans("### Yearly Consumption trend by building function"))
    opt_csv = {
            'Heat, kWh': heat_cons_by_func,
            'Hot water, m³': wat_cons_by_func,
            "Šiluma, kWh": heat_cons_by_func,
            "Karštas vanduo, m³": wat_cons_by_func
        }
    res_lt = opt_csv[res_side]

    df_melted = res_lt.melt(id_vars=['year'], var_name='Category', value_name='Value')

    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X('year:O', title='Year', scale=alt.Scale(zero=False)),
        y=alt.Y('sum(Value):Q', title=res_side, scale=alt.Scale(zero=False)),
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
        f"<h1 style='font-size: 48px; text-align: center;'>{trans("No. Unique rooms")}</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        "<h1 style='font-size: 72px; text-align: center;'>44900</h1>",
        unsafe_allow_html=True
    )
        area_df = pd.read_csv("area_df.csv")
        st.header(trans("Average Heat Consumption / m² against Room Area"))

        chart = alt.Chart(area_df).mark_bar().encode(
            x=alt.X("area_bins:N", sort="-y", title=trans("Room Area, m²")),
            y=alt.Y("eff:Q", title="kWh / m²"),
            color=alt.value("#fcaa01")
        )
        st.altair_chart(chart, use_container_width=True)
    with col8:
        st.markdown(
        f"<h1 style='font-size: 48px; text-align: center;'>{trans("No. Unique buildings")}</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        "<h1 style='font-size: 72px; text-align: center;'>1421</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        f"<h1 style='font-size: 48px; text-align: center;'>{trans("Average room area")}</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        "<h1 style='font-size: 72px; text-align: center;'>71.6 m²</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        f"<h1 style='font-size: 48px; text-align: center;'>{trans("Biggest room area")}</h1>",
        unsafe_allow_html=True
    )
        st.markdown(
        "<h1 style='font-size: 72px; text-align: center;'>40760 m²</h1>",
        unsafe_allow_html=True
    )
    st.write(trans("## Number of Rooms per buyer, Top 20 buyers"))
    buyer_rooms = pd.read_csv("buyer_rooms.csv")
    st.bar_chart(buyer_rooms["room_id"], x_label=trans("Individual buyers"), y_label=trans("No. Rooms"), color="#fcaa01")

    #-------------------------------------------
    # Consumption by building year

    heat_by_build_year = pd.read_csv("heat_by_build_year.csv")
    st.write(trans("## Average Heat Consumption / m² by buildings build year"))
    st.write(trans("Over time we can see that heat consumption decreases as buildings get younger, which can be attributed to better construction and insulation technology. Specifically buildings built after 1940 and then 2000 have lower consumption heat consumption on average"))
    st.bar_chart(heat_by_build_year, x="build_year", y="eff", y_label="kWh / m²", x_label=trans("Build Year"), color="#fcaa01")
    #------------------------------------------------------------------
    st.write(trans("# Oldest building was built in -- 1849"))
    st.write(trans("# Most frequent build year -- 1970 (1924 buildings)"))

    st.write(trans("## Geospatial building age heatmap"))

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
    st.write(trans("# Median amount of floors per building -- 5 Floors"))
    st.write(trans("# Highest building -- 15 floors"))

    st.write(trans("## Geospatial building floors heatmap"))

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
    # Initialize features in Session State if not already present
    if "features" not in st.session_state:
        st.session_state.features = {
            "legal_entity": False,
            "month": 1,
            "room_area": 50.0,
            "build_year": 1971,
            "building_floors": 5,
            "building_func": 'Gyvenamasis (trijų ir daugiau butų - daugiaaukštis pastatas)',
            "x_coord": 456969.719985,
            "y_coord": 6199673.340395
        }

    features = st.session_state.features
    # Title of the web app
    st.title("AI Energy consumption estimation tool")
    st.markdown("### How to use the tool?")
    st.markdown("Use the displayed sliders and input boxes to select the various metrics of the room, which helps the AI model give an accurate prediction. In order to select the coordinates of where the room is located, simply click on the map on the location of the relevant building, the map can be dragged around and zoomed in/out. The month of the year field specifies for which month of the year to predict energy consumption. If the number `6` is supplied, the energy consumption will be calculated for the month of june. Lastly, in order to get an estimation simply click the button below that says `Predict Energy Consumption`. After waiting a second for the model to finish calculations, a field should appear below the button, with the predictions for heat and hot water consumed for that month. More information about the AI model is at the bottom of the page")
    # Input fields using columns for a more compact layout
    st.markdown("### Please enter the required information")
    col1, col2, col3 = st.columns(3)

    with col1:
        features["legal_entity"] = st.checkbox("Is the buyer a legal entity?")
        features["building_floors"] = st.slider("Number of floors in the building", min_value=1, max_value=15, step=1, value=5)
        features["room_area"] = st.number_input(
            "Room area, m²", 
            min_value=0.0, 
            max_value=40000.0, 
            value=50.0,  # Default value from session state
            step=10.0, 
            format="%.1f"  # Display with 1 decimal place
        )

        

    with col2:
        features["build_year"] = st.number_input("Year that the building was built", min_value=1849, step=1, value=1970)
        features["month"] = st.number_input("Month of the year (1-12)", min_value=1, max_value=12, step=1)
        features["building_func"] = st.selectbox("Building function", ['Transporto','Maitinimo','Gyvenamasis (individualus pastatas)','Gydymo',
'Religinės' ,'Kita' ,'Administracinė', 'Kultūros' ,'Gamybos' ,'Gyvenamasis (trijų ir daugiau butų - daugiaaukštis pastatas)', 'Prekybos', 'Sporto', 'Komercinės paskirties', 'Mokslo' ,'Viešbučių', 'Sandėliavimo'])

    with col3:
        from pyproj import Transformer
        transformer = Transformer.from_crs('epsg:4326', 'epsg:3346', always_xy=True)
        st.subheader("Select Coordinates")
        map_center = [55.9292, 23.3102]
        map = folium.Map(location=map_center, zoom_start=12)
        #-
        marker = folium.Marker(location=map_center)
        map.add_child(marker)

        click = folium.LatLngPopup()
        map.add_child(click)

        map_data = st_folium(map, height=300, width=300)

        x_coord, y_coord = map_center[0], map_center[1]
        if map_data and 'last_clicked' in map_data and map_data['last_clicked']:
            x_coord, y_coord = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
            x_coord, y_coord = transformer.transform(y_coord, x_coord)
            features["x_coord"] = x_coord
            features["y_coord"] = y_coord
    
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            height: 3em;
            width: 100%;
            font-size: 20px;
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Center the button and make prediction
    if st.button("Predict Energy Consumption"):
        preds_heat = get_prediction([features.values()])
        preds_wat = get_prediction([features.values()], "xgb_wat_v1.sav", "column_transformer_wat.pkl")
        
        # Display results in a styled container
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px;'>
                <h3 style='color: #2c3e50;'>Prediction Results</h3>
                <div style='display: flex; justify-content: space-between;'>
                    <div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; width: 48%;'>
                        <h4 style='color: #2ecc71; margin: 0;'>Heat Consumption</h4>
                        <p style='font-size: 24px; color: #2ecc71; margin: 5px 0 0 0;'>{:.2f} kWh / month</p>
                    </div>
                    <div style='background-color: #e3f2fd; padding: 15px; border-radius: 8px; width: 48%;'>
                        <h4 style='color: #3498db; margin: 0;'>Water Consumption</h4>
                        <p style='font-size: 24px; color: #3498db; margin: 5px 0 0 0;'>{:.2f} m³ / month</p>
                    </div>
                </div>
            </div>
        """.format(float(preds_heat), float(preds_wat)), unsafe_allow_html=True)
    st.markdown("### Technical description of the AI model")
    st.markdown("""
    ### 1. The data
    The data used to train the model was procured from
    """)

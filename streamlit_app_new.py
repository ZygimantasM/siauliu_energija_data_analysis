from datetime import datetime
import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
import folium
from streamlit_folium import st_folium
from helper_funcs import get_prediction

# Initialize session state for coordinates with default values
if "x_coord" not in st.session_state:
    st.session_state.x_coord = 456969.719985  # Default X coordinate
if "y_coord" not in st.session_state:
    st.session_state.y_coord = 6199673.340395  # Default Y coordinate

# Set page configuration
st.set_page_config(layout="wide")

# Sidebar setup
sidebar = st.sidebar
sidebar.header("Settings / Nustatymai")

# Language selection
lang = sidebar.selectbox("Language / Kalba", ("English", "Lietuvių"), key=47)


# Lithuanian translations dictionary
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
    "# Most frequent build year -- 1970 (1924 buildings)": "# Dažniausiai pasirodantys statybos metai -- 1970 m. (1924 Pastatų)",
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
    "Build Year": "Statybos metai",
    "AI Consumption Estimation Tool": "DI Energijos suvartojimo įrankis",
    "Heat Consumption Forecast Using SARIMA": "Šilumos suvartojimo prognozė naudojant SARIMA",
    """In this analysis, we employ a sophisticated statistical tool known as SARIMA—Seasonal Autoregressive Integrated Moving Average—to forecast the trajectory of heat consumption over the next three years. This model allows us to capture both seasonal patterns and long-term trends in the data, providing a reliable prediction of how heat consumption might evolve.
        The regions shaded in red on the graph illustrate the upper and lower bounds of the prediction error for the forecast.
        These areas represent the range within which the actual heat consumption values are likely to fall.""": "Šioje analizėje mes naudojame sudėtingą statistinį įrankį, vadinamą SARIMA (Seasonal Autoregressive Integrated Moving Average), kad prognozuotume šilumos suvartojimo tendencijas per ateinančius trejus metus. Šis modelis leidžia mums užfiksuoti tiek sezoninius dėsningumus, tiek ilgalaikes duomenų tendencijas, teikdamas patikimą prognozę apie tai, kaip gali kisti šilumos vartojimas. Grafike raudonai pažymėtos sritys iliustruoja prognozės klaidos viršutines ir apatines ribas. Šios sritys rodo diapazoną, kuriame tikėtina, kad bus faktinės šilumos suvartojimo vertės.",
    "Red color - Higher consumption area, Yellow - Lower consumption area": "Raudona spalva - Didesnio suvartojimo sritis, Geltona - Mažesnio suvartojimo sritis",
    "From the graph above we can see that as the room area increases the average heat consumption per square meter actually decreases, meaning it is more efficient to provide heating for larger rooms rather than smaller ones.": "Iš grafiko aukščiau matome, kad didėjant kambario plotui, vidutinis šilumos suvartojimas kvadratiniam metrui iš tikrųjų mažėja, tai reiškia, kad efektyviau yra šildyti didesnius kambarius, o ne mažesnius.",
    "From this bar chart, we can see that a few buyers possess hundreds of rooms, but we can’t identify who they are because the data about the buyers in the dataset is anonymized.": "Iš šio stulpelinio diagramos matome, kad keli pirkėjai turi šimtus kambarių, tačiau mes negalime nustatyti, kas jie yra, nes pirkėjų duomenys duomenų rinkinyje yra anonimizuoti.",
    "Green color means newer buildings, blue is older buildings": "Žalia spalva reiškia naujesnius pastatus, mėlyna - senesnius pastatus.",
    "Red color means higher buildings with more floors, blue are lower buildings with less floors": "Raudona spalva reiškia aukštesnius pastatus su daugiau aukštų, mėlyna - žemesnius pastatus su mažiau aukštų.",
    "AI Energy consumption estimation tool": "DI Energijos suvartojimo įrankis",
    "How to use the tool?": "Kaip nauduoti šį įrankį?",
    "Use the displayed sliders and input boxes to select the various metrics of the room, which helps the AI model give an accurate prediction. In order to select the coordinates of where the room is located, simply click on the map on the location of the relevant building, the map can be dragged around and zoomed in/out. The month of the year field specifies for which month of the year to predict energy consumption. If the number `6` is supplied, the energy consumption will be calculated for the month of june. Lastly, in order to get an estimation simply click the button below that says `Predict Energy Consumption`. After waiting a second for the model to finish calculations, a field should appear below the button, with the predictions for heat consumed for that month. More information about the AI model is at the bottom of the page": "Naudokite rodiklius rodančius slankiklius ir įvesties laukelius, kad pasirinktumėte įvairius kambario parametrus, kas padės AI modeliui pateikti tikslią prognozę. Norėdami pasirinkti koordinates, kur yra kambarys, tiesiog spustelėkite žemėlapį atitinkamo pastato vietoje, žemėlapį galima vilkti ir priartinti/tolinti. Metų mėnesio laukas nurodo, kuriam mėnesiui prognozuoti energijos suvartojimą. Jei įvedamas skaičius `6`, energijos suvartojimas bus apskaičiuotas birželio mėnesiui. Galiausiai, norėdami gauti apskaičiavimą, tiesiog spustelėkite žemiau esantį mygtuką, kuris sako `Prognozuoti energijos suvartojimą`. Palaukus sekundę, kol modelis baigs skaičiavimus, po mygtuku turėtų atsirasti laukas su šilumos suvartojimo prognozėmis tam mėnesiui. Daugiau informacijos apie DI modelį yra puslapio apačioje.",
    "<strong>Note:</strong> The AI predicts heat consumption in kWh with an average error of about 100 kWh, based on historical data. Results may vary depending on real-world conditions.": "<strong>Pastaba:</strong> DI prognozuoja šilumos suvartojimą kWh su vidutine klaida apie 100 kWh, remiantis istoriniais duomenimis. Rezultatai gali skirtis priklausomai nuo realių sąlygų.",
    "Please enter the required information": "Prašome įvesti reikiamą informaciją",
    "Number of floors in the building": "Aukštų skaičius pastate",
    "Room area, m²": "Kambario plotas, m²",
    "Year that the building was built": "Pastato statybos metai",
    "Building function": "Pastato funkcija",
    "Select Coordinates": "Pasirinkti koordinates",
    "Is the buyer a legal entity?": "Ar pirkėjas yra juridinis asmuo?",
    "Predict Energy Consumption": "Prognozuoti energijos suvartojimą",
    "Month of the year (1-12)": "Metų mėnuo (1-12)",
    "Prediction Results": "Prognozės rezultatai",
    "Heat Consumption": "Šilumos suvartojimas",
    "Hot Water Consumption": "Karšto vandens suvartojimas",
    "month": "mėn",
    "Technical description of the AI model": "Techninis DI modelio aprašymas",
    "The data": "Duomenys",
    "The model": "DI modelis",
    "Evaluation": "DI modelio įvertinimas",
    "The data used to train the model was sourced from Lithuania's open data portal, data.gov.lt, and includes records up to 2025. Preparing the data for modeling required extensive preprocessing. For instance, geographical coordinates needed to be converted from one system to another. Additionally, the dataset contained multiple records for the same room and time period under a specific service category, such as 'heat', though another column provided more detailed classifications. Since these records shared the same units, I aggregated them by summing their values. This reduced, for example, five separate entries for a single room and time period into one consolidated figure, which the model then predicts.": "Modeliui mokyti naudoti duomenys buvo gauti iš Lietuvos atvirų duomenų portalo data.gov.lt ir apima įrašus iki 2025 metų. Ruošiant duomenis modeliavimui, reikėjo atlikti išsamią išankstinį duomenų apdorojimą. Pavyzdžiui, geografines koordinatės reikėjo konvertuoti iš vienos sistemos į kitą. Be to, duomenų rinkinyje buvo daug įrašų apie tą patį kambarį ir laikotarpį pagal tam tikrą paslaugų kategoriją, pavyzdžiui, 'šiluma', nors kitame stulpelyje buvo pateikiami išsamesnės kategorijos. Kadangi šie įrašai buvo pateikti tokiais pačiais vienetais, aš juos sujungiau, sudėdamas jų reikšmes. Tai leido, pavyzdžiui, penkis atskirus įrašus apie vieną kambarį ir laikotarpį sujungti į vieną konsoliduotą skaičių, kurį prognozavo modelis.",
    "For this tool, I employed an XGBoost model, which leverages Gradient Boosted Decision Trees. While I considered alternative models, my experience—particularly from data science competitions on Kaggle—has shown that libraries like XGBoost and CatBoost often deliver top-tier performance for tabular datasets. This made XGBoost a confident choice. The model is both efficient and lightweight. During training, its hyperparameters were optimized using Optuna, a widely recognized industry-standard library.": "Šiam įrankiui naudojau XGBoost modelį, kuris naudoja (GBDT) algoritmą. Nors svarsčiau alternatyvius modelius, mano patirtis iš duomenų mokslų varžybų Kaggle platformoje parodė, kad bibliotekos, tokios kaip XGBoost ir CatBoost, dažnai suteikia aukščiausio lygio našumą dirbant su duomeninimis lentelės formatu. Tai padarė XGBoost patikimu pasirinkimu. Modelis yra tiek efektyvus, tiek mažas. Mokymosi metu modelio parametrai buvo optimizuoti naudojant Optuna -- plačiai pripažintą biblioteką.",
    "The model’s performance was assessed using two metrics: Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE). Across the test set, the MAE for heat consumption is 140 kWh, indicating an average prediction error of about 140 kWh. However, this figure is somewhat inflated by extreme values where the model’s predictions deviate significantly. For most samples, the average error is closer to 90 kWh, with some predictions as accurate as 15, 30, or 50 kWh off. Generally, larger predicted values correlate with larger errors, likely due to the scarcity of high-energy-consumption samples in the dataset. This skews the heat consumption feature heavily. While these high values could be considered outliers, they are not errors, so I opted to retain them. The RMSE, at around 800 kWh, confirms that the model struggles more with outliers, as expected.": "Modelio našumas buvo vertinamas naudojant dvi metrikas: vidutinę absoliučią klaidą (MAE) ir kvadratinės vidutinės klaidos šaknį (RMSE). Testo rinkinyje šilumos suvartojimui vidutinė absoliuti klaida (MAE) yra 140 kWh, kas parodo jog modelis vidutiniškai klysta apie 140 kWh. Tačiau šis skaičius yra šiek tiek padidintas dėl ekstremalių reikšmių, dėl kurių modelio prognozės reikšmingai nukrypsta. Daugeliui mėginių vidutinė klaida yra artimesnė 90 kWh, kai kurioms prognozėms, model klysta tik 15, 30 ar 50 kWh. Paprastai didesnės prognozuojamos reikšmės koreliuoja su didesne paklaida, greičiausiai dėl trūkumo aukšto energijos suvartojimo pavyzdžių duomenų rinkinyje. Nors šias aukštas vertes būtų galima laikyti nukrypusiais duomenų taškais, jos nėra klaidos, todėl nusprendžiau jas palikti. Kvadratinės vidutinės klaidos šaknis (RMSE) yra maždaug 800 kWh. Tai patvirtina, kad modeliui yra sunkiau tiksliai nuspėti aukštesnes vertes",
    "The model excels at predicting heat consumption in kWh but performs poorly with hot water consumption. Its MAE for hot water prediction is approximately 1 m³, meaning it errs by about 1 cubic meter on average. This larger error makes sense, as hot water consumption is inherently harder to predict than heat consumption. Given this limitation, I’d advise against deploying the model for hot water predictions in a production environment.": "Modelis puikiai prognozuoja šilumos suvartojimą kWh, tačiau prastai veikia su karšto vandens suvartojimo prognozę. Modelio paklaida karšto vandens prognozėms yra maždaug 1 m³, tai reiškia, kad vidutiniškai jis klysta apie 1 kubinį metrą. Ši didesnė klaida nenustebina, nes karšto vandens suvartojimą numatyti iš esmės yra sunkiau nei šilumos suvartojimą. Atsižvelgiant į šį apribojimą, rekomenduočiau nenaudoti modelį karšto vandens prognozėms gamybos aplinkoje.",
    "Below is a sample from the test set used to evaluate the model. It compares actual values from the dataset with the AI’s predictions, showcasing impressive results, especially for heat consumption. In some cases, the model is off by 300 kWh or 50 kWh, while in others, it’s spot-on with a difference of 0 kWh. The Actual column reflects the real values the AI aims to match, the Preds column displays the AI’s predictions, and the Diff column indicates the difference between them, revealing the model’s error in units.": "Žemiau pateiktas pavyzdys iš testo rinkinio, kuris buvo naudojamas modelio vertinimui. Jis lygina faktines reikšmes iš duomenų rinkinio su DI prognozėmi. Iš šio pavyzdžio matosi įspūdingi rezultatai, ypač šilumos suvartojimo atveju. Kai kuriais atvejais modelis klaidingai nukrypsta 300 kWh arba tik 50 kWh, o kitais atvejais jis visiškai tiksliai progrnozuoja su beveik 0 kWh nuokrypa. Stulpelis „Actual“ atspindi realias reikšmes, kurias DI siekia atspėti, stulpelis „Preds“ rodo DI prognozes, o stulpelis „Diff“ rodo skirtumą tarp prognozės ir tiesos, parodantis kiek nuklydo modelis vienetais",
    "Socials": "Socialiniai tinklai",
    "What does this tool do?": "Ką šis įrankis daro?",
    """Armed with specific data and metrics about a room, this sophisticated AI tool can precisely forecast the monthly consumption of heat for that space. Applications include: efficient energy management in residential and commercial buildings, optimizing heating schedules to reduce costs and environmental impact, assisting in the design of energy-efficient homes and buildings""": """
    Turėdamas konkrečius duomenis ir matavimus patalpos, šis išmanusis DI įrankis gali tiksliai prognozuoti mėnesinį šilumos suvartojimą toje erdvėje. Naudojimo sritys: efektyvus energijos valdymas gyvenamuosiuose ir komerciniuose pastatuose, šildymo grafikų optimizavimas siekiant sumažinti išlaidas ir poveikį aplinkai, pagalba projektuojant energiją taupančius namus ir pastatus
    """,
    "About": "Apie",
    "Quick How-to": "Kaip naudotis puslapiu?",
    "Purpose": "Projekto prasmė",
    "Technical Skills Used": "Naudoti techniniai įgūdžiai",
    "Challenges": "Iššūkiai",
    "Improvements": "Ka galima patobulinti?",
    "This web app serves as a data analytics and data science project, exploring energy consumption data in Šiauliai, Lithuania. The data, collected by AB 'Šiaulių Energija', is publicly available on [data.gov.lt](https://data.gov.lt/datasets/2886/). The app features various graphs, heatmaps, and statistics designed to deliver valuable insights for stakeholders. It also includes an advanced AI tool that estimates energy consumption for rooms, offering practical real-world applications. The project is open-source and available on [GitHub](https://github.com/ZygimantasM/siauliu_energija_data_analysis).": "Ši internetinė programėlė yra duomenų analizės ir duomenų mokslo projektas, tyrinėjantis energijos vartojimo duomenis Šiauliuose. Duomenis, surinktus AB 'Šiaulių Energija', galima rasti viešai [data.gov.lt](https://data.gov.lt/datasets/2886/). Programėlė pateikia įvairius grafikus, šilumos žemėlapius ir statistiką, skirta suteikti vertingų įžvalgų suinteresuotiems asmenims. Programėleje taip pat galima rasti pažangų DI įrankį, kuris apskaičiuoja mėnesinį energijos suvartojimą patalpose, šis įrankis suteikia praktinių realaus pasaulio taikymo galimybių. Projektas yra atvirojo kodo ir prieinamas [GitHub](https://github.com/ZygimantasM/siauliu_energija_data_analysis).",
    "Although I recently began my bachelor’s degree in Data Science and Applied Mathematics, I have a deep passion for self-learning and have been studying data science for nearly two years. To build my skills, I’ve completed numerous courses, read extensively, and participated in data science competitions, all to prepare for a career in this field. Seeking to apply my knowledge, I explored project ideas to strengthen my portfolio. While browsing public data websites, I discovered a dataset on energy consumption in my hometown, Šiauliai. This dataset piqued my interest due to its potential for both data analytics and the creation of practical machine learning (AI) models. To share my findings effectively, I developed this web app to present the results in a user-friendly and accessible way. After roughly 80 hours of effort, I completed the project and am delighted with the outcome.": "Nors neseniai pradėjau duomenų mokslo bakalauro studijas, laisvalaikių mėgstu gilinti savo žinias šioje srityje. Duomenų moksla studijuoju savarankiškai beveik dvejus metus. Siekdamas tobulinti savo įgūdžius, baigiau daugybę kursų, skaičiau knygas ir dalyvavau duomenų mokslo konkursuose, visa tai ruošiantis karjerai šioje srityje. Siekdamas pritaikyti savo žinias, ieškojau projekto idėjų, kad pastiprinčiau savo portfolio. Naršydamas viešų duomenų svetainėse, atradau duomenų rinkinį apie energijos suvartojimą mano mieste -- Šiauliuose. Šis duomenų rinkinys mane sudomino dėl savo potencialo tiek duomenų analizei, tiek praktinių mašininio mokymosi (AI) modelių kūrimui. Siekdamas efektyviai pasidalinti savo atradimais, sukūriau šią internetinę programėlę, kad pateikčiau rezultatus patogia ir prieinama forma. Po maždaug 80 valandų darbo baigiau projektą ir esu labai patenkintas rezultatu.",
    "Get started with these simple steps:": "Pradėkite šiais paprastais žingsniais:",
    "**Open the Sidebar**: Access the sidebar on the left side of the web app.": "**Atidarykite Šoninį Meniu**: Pasiekite šoninį meniu, esantį kairėje internetinės programėlės pusėje.",
    "**Choose Language**: Select your preferred language—English or Lithuanian.": "**Pasirinkite Kalbą**: Pasirinkite norimą kalbą – anglų arba lietuvių.",
    "**Select Data**: Pick the type of data to view (heat consumption or hot water consumption). The website will update automatically based on your choice.": "**Pasirinkite Duomenis**: Pasirinkite, kokio tipo duomenis norite peržiūrėti (šilumos vartojimo ar karšto vandens vartojimo). Svetainė automatiškai atsinaujins pagal jūsų pasirinkimą.",
    "**Explore Tabs**: Click the tabs in the center of the page to navigate through the content.": "**Naršykite Skirtukus**: Spauskite skirtukus puslapio centre, kad naršytumėte turinį.",
    "Most graphs are interactive and can be explored in detail, as can the 3D heatmaps.": "Dauguma grafikų yra interaktyvūs ir gali būti išsamiai tyrinėjami, taip pat ir 3D šilumos žemėlapiai.",
    "To bring this project to life, I drew on my expertise in data science, Python, and a range of data science libraries. My workflow included:": "Siekdamas įgyvendinti šį projektą, remiausi savo duomenų mokslo, Python ir įvairių duomenų mokslo bibliotekų ekspertize. Mano darbo eiga apėmė:",
    "**Environment Setup**: Managing Python environments, Linux VMs, packages, and Jupyter notebooks.": "**Aplinkos Sukūrimas**: Python aplinkų, Linux VM, paketų ir Jupyter notebook valdymas.",
    "**Data Processing**: Using Pandas, NumPy, and Matplotlib to clean, manipulate, and visualize data.": "**Duomenų Apdorojimas**: Pandas, NumPy ir Matplotlib naudojimas duomenų valymui, manipuliavimui ir vizualizavimui.",
    "**Modeling**: Leveraging Scikit-learn and XGBoost for model development and evaluation, with Optuna for optimization to boost performance.": "**Modeliavimas**: Scikit-learn ir XGBoost naudojimas modelių kūrimui ir vertinimui, su Optuna optimizavimui, siekiant pagerinti našumą.",
    "**Web Development**: Learning Streamlit to build the web application.": "**Internetinės Programėlės Kūrimas**: Streamlit naudojimas kuriant internetinę programėlę.",
    "**Version Control**: Utilizing GitHub for tracking changes and deploying the app online.": "**Versijos valdymas**: GitHub naudojimas projektui",
    "These skills enabled me to transform raw data into a functional and insightful tool.": "Šie įgūdžiai leido man paversti paprastus duomenis į funkcionalią ir naudingą priemonę.",
    "The project presented several obstacles, including:": "Projektas susidūrė su keliais sunkumais, įskaitant:",
    "**Hardware Limitations**: Downloading and processing a large dataset on a low-performance computer, which significantly delayed model training and optimization.": "**Aparatinės įrangos apribojimai**: Didelio duomenų kiekio atsisiuntimas ir apdorojimas žemo našumo kompiuteryje, kas irgi labai sulėtino modelio treniravimo procesą ir optimizavimą.",
    "**Translation**: Translating the entire web app into English and Lithuanian, a straightforward but time-intensive task.": "**Vertimas**: Visos internetinės programėlės vertimas į anglų ir lietuvių kalbas – paprasta, bet daug laiko reikalaujanti užduotis.",
    "**Ideation**: Brainstorming ideas for graphs and statistics that would be both relevant and useful to users.": "**Idėjų generavimas**: Teko daug pagalvoti apie grafikus ir statistika, kuri būtų tiek aktuali, tiek naudinga naudotojams.",
    "Overcoming these hurdles required persistence and creative problem-solving.": "Šių kliūčių įveikimas reikalavo atkaklumo ir kūrybiško problemų sprendimo.",
    "While I achieved most of my initial objectives, there’s room for enhancement:": "Nors pasiekiau daugumą savo pradinių tikslų, yra kur tobulėti:",
    "**Data Updates**: An issue with the source website prevented me from obtaining a complete 2024 dataset, leaving some graphs without this year’s data due to its incompleteness.": "**Duomenų atnaujinimai**: Problema su šaltinio svetaine neleido man gauti pilno 2024 metų duomenų rinkinio, todėl kai kurie grafikai neturi šių metų duomenų dėl jų neišsamumo.",
    "**Performance**: The web app could be smoother, with techniques like caching offering potential optimization.": "**Veikimas**: Internetinė programėlė galėtų veikti sklandžiau, pasitelkiant kelis programavimo būdus",
    "These areas provide opportunities for future refinement as I continue to develop the project.": "Šie trūkumai suteikia galimybių patobulinti puslapį ateityje, toliau vystant projektą",
    "Introduction": "Įvadas",
    "Intro": "Įvadas" 
}

building_func_translations = {
    "Transporto": "Transportation",
    "Maitinimo": "Catering",
    "Gyvenamasis (individualus pastatas)": "Residential (individual building)",
    "Gydymo": "Medical",
    "Religinės": "Religious",
    "Kita": "Other",
    "Administracinė": "Administrative",
    "Kultūros": "Cultural",
    "Gamybos": "Industrial",
    "Gyvenamasis (trijų ir daugiau butų - daugiaaukštis pastatas)": "Residential (three or more apartments - multi-story building)",
    "Prekybos": "Commercial",
    "Sporto": "Sports",
    "Komercinės paskirties": "Commercial purpose",
    "Mokslo": "Educational",
    "Viešbučių": "Hotels",
    "Sandėliavimo": "Warehousing"
}

# Translation function with fallback
def trans(text, lang=lang):
    """Translate text based on selected language, default to original if not found."""
    if lang == "English":
        return text
    return lt_mappings.get(text, text)

# Category selection
category_options = (trans("Heat, kWh"), trans("Hot water, m³"))
res_side = sidebar.selectbox(trans("Select Category"), category_options, key=48)

# Sidebar spacer
sidebar.empty().markdown("<div style='height: 25vh;'></div>", unsafe_allow_html=True)

# Social media links
sidebar.title(trans("Socials"))
sidebar.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">',
    unsafe_allow_html=True
)
sidebar.markdown(
    """
    <div style="background-color: #ffffff; border-radius: 15px; padding: 15px; display: flex; flex-direction: column; gap: 10px;">
        <a href="https://x.com/zygimantasmk" target="_blank" style="text-decoration: none; color: #000000;">
            <i class="fa-brands fa-x-twitter"></i> X
        </a>
        <a href="https://github.com/ZygimantasM" target="_blank" style="text-decoration: none; color: #333;">
            <i class="fab fa-github"></i> GitHub
        </a>
        <a href="https://www.linkedin.com/in/zygimantasmickavicius/" target="_blank" style="text-decoration: none; color: #0077B5;">
            <i class="fab fa-linkedin"></i> LinkedIn
        </a>
        <a href="https://www.kaggle.com/zygmuntyt" target="_blank" style="text-decoration: none; color: #20bffe;">
            <i class="fab fa-kaggle"></i> Kaggle
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Main title
st.markdown(
    f"<h1 style='font-size: 62px; text-align: center;'>{trans('Data Analysis of AB \"Šiaulių Energija\"')}</h1>",
    unsafe_allow_html=True
)

# Define tabs
intro, tab1, tab2, tab3, tab4 = st.tabs([
    trans("Intro"),
    trans("Overall Consumption Trends"),
    trans("Trends By Building Function"),
    trans("Rooms Data"),
    trans("AI Consumption Estimation Tool")
])

# Intro tab
with intro:
    st.header(trans("Introduction"))
    st.markdown(f"""
    ## {trans('About')}
    {trans('This web app serves as a data analytics and data science project, exploring energy consumption data in Šiauliai, Lithuania. The data, collected by AB \'Šiaulių Energija\', is publicly available on [data.gov.lt](https://data.gov.lt/datasets/2886/). The app features various graphs, heatmaps, and statistics designed to deliver valuable insights for stakeholders. It also includes an advanced AI tool that estimates energy consumption for rooms, offering practical real-world applications. The project is open-source and available on [GitHub](https://github.com/ZygimantasM/siauliu_energija_data_analysis).')}

    ## {trans('Quick How-to')}
    {trans('Get started with these simple steps:')}

    1. {trans('**Open the Sidebar**: Access the sidebar on the left side of the web app.')}
    2. {trans('**Choose Language**: Select your preferred language—English or Lithuanian.')}
    3. {trans('**Select Data**: Pick the type of data to view (heat consumption or hot water consumption). The website will update automatically based on your choice.')}
    4. {trans('**Explore Tabs**: Click the tabs in the center of the page to navigate through the content.')}

    {trans('Most graphs are interactive and can be explored in detail, as can the 3D heatmaps.')}

    ## {trans('Purpose')}
    {trans('Although I recently began my bachelor’s degree in Data Science and Applied Mathematics, I have a deep passion for self-learning and have been studying data science for nearly two years. To build my skills, I’ve completed numerous courses, read extensively, and participated in data science competitions, all to prepare for a career in this field. Seeking to apply my knowledge, I explored project ideas to strengthen my portfolio. While browsing public data websites, I discovered a dataset on energy consumption in my hometown, Šiauliai. This dataset piqued my interest due to its potential for both data analytics and the creation of practical machine learning (AI) models. To share my findings effectively, I developed this web app to present the results in a user-friendly and accessible way. After roughly 80 hours of effort, I completed the project and am delighted with the outcome.')}

    ## {trans('Technical Skills Used')}
    {trans('To bring this project to life, I drew on my expertise in data science, Python, and a range of data science libraries. My workflow included:')}

    - {trans('**Environment Setup**: Managing Python environments, Linux VMs, packages, and Jupyter notebooks.')}
    - {trans('**Data Processing**: Using Pandas, NumPy, and Matplotlib to clean, manipulate, and visualize data.')}
    - {trans('**Modeling**: Leveraging Scikit-learn and XGBoost for model development and evaluation, with Optuna for optimization to boost performance.')}
    - {trans('**Web Development**: Learning Streamlit to build the web application.')}
    - {trans('**Version Control**: Utilizing GitHub for tracking changes and deploying the app online.')}

    {trans('These skills enabled me to transform raw data into a functional and insightful tool.')}

    ## {trans('Challenges')}
    {trans('The project presented several obstacles, including:')}

    - {trans('**Hardware Limitations**: Downloading and processing a large dataset on a low-performance computer, which significantly delayed model training and optimization.')}
    - {trans('**Translation**: Translating the entire web app into English and Lithuanian, a straightforward but time-intensive task.')}
    - {trans('**Ideation**: Brainstorming ideas for graphs and statistics that would be both relevant and useful to users.')}

    {trans('Overcoming these hurdles required persistence and creative problem-solving.')}

    ## {trans('Improvements')}
    {trans('While I achieved most of my initial objectives, there’s room for enhancement:')}

    - {trans('**Data Updates**: An issue with the source website prevented me from obtaining a complete 2024 dataset, leaving some graphs without this year’s data due to its incompleteness.')}
    - {trans('**Performance**: The web app could be smoother, with techniques like caching offering potential optimization.')}

    {trans('These areas provide opportunities for future refinement as I continue to develop the project.')}
    """)

# Tab 1: Overall Consumption Trends
with tab1:

    @st.cache_data
    def load_monthly_trend():
        df = pd.read_csv("csv_files/monthly_trend.csv")
        df["Date"] = pd.to_datetime(df["month"])
        return df

    @st.cache_data
    def load_yearly_trend():
        return pd.read_csv("csv_files/yearly_trend.csv")

    @st.cache_data
    def load_contract_trend():
        df = pd.read_csv("csv_files/contract_trend.csv")
        df["month"] = pd.to_datetime(df["month"])
        return df

    @st.cache_data
    def load_contract_trend_yearly():
        return pd.read_csv("csv_files/contract_trend_yearly.csv")

    @st.cache_data
    def load_geo_amount(res_side):
        opt_csv = {
            "Heat, kWh": "csv_files/geo_amount_heat.csv",
            "Hot water, m³": "csv_files/geo_amount_wat.csv",
            "Šiluma, kWh": "csv_files/geo_amount_heat.csv",
            "Karštas vanduo, m³": "csv_files/geo_amount_wat.csv"
        }
        return pd.read_csv(opt_csv[res_side])

    st.markdown(
        f"<h1 style='text-align: center;'>{trans('Energy Consumption Trends')}</h1>",
        unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"<h3 style='text-align: center;'>{trans('Monthly')}</h3>",
            unsafe_allow_html=True
        )
        monthly_trend = load_monthly_trend()
        monthly_trend["Date"] = pd.to_datetime(monthly_trend["month"])
        opt = {
            "Heat, kWh": "Šiluma",
            "Hot water, m³": "Karštas vanduo",
            "Šiluma, kWh": "Šiluma",
            "Karštas vanduo, m³": "Karštas vanduo"
        }
        res_lt = opt[res_side]
        st.line_chart(
            monthly_trend,
            x="Date",
            y=res_lt,
            y_label=res_side,
            x_label=trans("Date"),
            color="#fcaa01"
        )

    with col2:
        st.markdown(
            f"<h3 style='text-align: center;'>{trans('Yearly')}</h3>",
            unsafe_allow_html=True
        )
        yearly_trend = load_yearly_trend()
        res_lt = opt[res_side]
        st.bar_chart(
            yearly_trend,
            x="year",
            y=res_lt,
            y_label=res_side,
            x_label=trans("Year"),
            color="#fcaa01"
        )

    st.markdown(
        f"<h1 style='text-align: center;'>{trans('Number Of Provided Services')}</h1>",
        unsafe_allow_html=True
    )
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            f"<h3 style='text-align: center;'>{trans('Monthly')}</h3>",
            unsafe_allow_html=True
        )
        contract_trend = load_contract_trend()
        contract_trend["month"] = pd.to_datetime(contract_trend["month"])
        st.line_chart(
            contract_trend,
            x="month",
            y="0",
            y_label=trans("No. Services"),
            x_label=trans("Date"),
            color="#fcaa01"
        )

    with col4:
        st.markdown(
            f"<h3 style='text-align: center;'>{trans('Yearly')}</h3>",
            unsafe_allow_html=True
        )
        contract_trend_yearly = load_contract_trend_yearly()
        st.bar_chart(
            contract_trend_yearly,
            x="year",
            y="0",
            x_label=trans("Year"),
            y_label=trans("No. Services"),
            color="#fcaa01"
        )

    st.markdown(
        f"<h1 style='text-align: center;'>{trans('Heat Consumption Forecast Using SARIMA')}</h1>",
        unsafe_allow_html=True
    )
    cols1, cols2, cols3 = st.columns([1, 8, 1])
    with cols2:
        st.markdown(trans("""In this analysis, we employ a sophisticated statistical tool known as SARIMA—Seasonal Autoregressive Integrated Moving Average—to forecast the trajectory of heat consumption over the next three years. This model allows us to capture both seasonal patterns and long-term trends in the data, providing a reliable prediction of how heat consumption might evolve.
        The regions shaded in red on the graph illustrate the upper and lower bounds of the prediction error for the forecast.
        These areas represent the range within which the actual heat consumption values are likely to fall."""))
        st.image("images/image.png", use_container_width=True)

    st.markdown(
        f"<h1 style='text-align: center;'>{trans('Consumption Heatmap')}</h1>",
        unsafe_allow_html=True
    )
    opt_csv = {
        "Heat, kWh": "csv_files/geo_amount_heat.csv",
        "Hot water, m³": "csv_files/geo_amount_wat.csv",
        "Šiluma, kWh": "csv_files/geo_amount_heat.csv",
        "Karštas vanduo, m³": "csv_files/geo_amount_wat.csv"
    }
    res_csv = opt_csv[res_side]
    date_range = pd.date_range(start="2019-01-01", end="2023-12-31", freq="MS").to_pydatetime().tolist()
    st.write(trans("## Select date to view"))
    st.write(trans("Red color - Higher consumption area, Yellow - Lower consumption area"))
    res_date = st.select_slider(" ", options=date_range, value=datetime(2019, 1, 1))
    res_date = str(res_date.date())
    geo_amount = load_geo_amount(res_side)
    geo_amount_filtered = geo_amount[geo_amount["month"] == res_date]
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=55.9192288419136,
                longitude=23.29157347671509,
                zoom=11.6,
                pitch=50
            ),
            layers=[
                pdk.Layer(
                    "HeatmapLayer",
                    data=geo_amount_filtered,
                    get_position="[x_grid, y_grid]",
                    get_weight="amount",
                    radiusPixels=80,
                    intensity=1,
                    threshold=0.1
                )
            ]
        )
    )

# Tab 2: Trends By Building Function
with tab2:
    @st.cache_data
    def load_rooms():
        return pd.read_csv("csv_files/rooms.csv")

    @st.cache_data
    def load_func_df():
        return pd.read_csv("csv_files/func_df.csv")

    @st.cache_data
    def load_cons_by_func(res_side):
        if res_side in ["Heat, kWh", "Šiluma, kWh"]:
            return pd.read_csv("csv_files/heat_cons_by_func.csv")
        else:
            return pd.read_csv("csv_files/wat_cons_by_func.csv")
    col5, col6 = st.columns(2)
    with col5:
        st.markdown(
            f"<h3 style='text-align: center;'>{trans('Number of Rooms by Building Function')}</h3>",
            unsafe_allow_html=True
        )
        rooms = load_rooms()
        func_val_counts = rooms["building_func"].value_counts()
        # Translate the index based on language
        if lang == "English":
            func_val_counts.index = func_val_counts.index.map(building_func_translations)
            func_val_counts.name = "Count"  # Explicitly set to "Count" in English
        else:
            func_val_counts.index = func_val_counts.index  # No change needed for Lithuanian index
            func_val_counts.name = "Skaičius"  # Set to "Skaičius" in Lithuanian
        st.table(func_val_counts)

    with col6:
        with col6:
            st.markdown(
                f"<h3 style='text-align: center;'>{trans('Average Monthly Heat Consumption / m² by Function')}</h3>",
                unsafe_allow_html=True
            )
            func_df = load_func_df()
            # Add translated column based on language
            if lang == "English":
                func_df["building_func_trans"] = func_df["building_func"].map(building_func_translations)
            else:
                func_df["building_func_trans"] = func_df["building_func"]
            # Update the chart to use the translated column
            bar_chart = alt.Chart(func_df).mark_bar().encode(
                y=alt.Y("building_func_trans:N", sort="-x", title=trans("Building Function")),
                x=alt.X("eff:Q", title="kWh / m²"),
                color=alt.value("#fcaa01")
            ).properties(height=600)
            st.altair_chart(bar_chart, use_container_width=True)

    st.write(trans("### Yearly Consumption trend by building function"))
    res_lt = load_cons_by_func(res_side)  # Use cached function
    # Create a translated DataFrame based on language
    if lang == "English":
        res_lt_trans = res_lt.rename(columns=building_func_translations)
    else:
        res_lt_trans = res_lt.copy()
    # Melt the translated DataFrame
    df_melted = res_lt_trans.melt(id_vars=["year"], var_name="Category", value_name="Value")
    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X(f"year:O", title=f"{trans('Year')}", scale=alt.Scale(zero=False)),
        y=alt.Y("sum(Value):Q", title=res_side, scale=alt.Scale(zero=False)),
        color=alt.Color("Category:N", scale=alt.Scale(scheme="category20")),  # Add custom color scheme
        order=alt.Order("Value", sort="descending")
    ).properties(width=600, height=800).interactive()
    st.altair_chart(chart, use_container_width=True)

# Tab 3: Rooms Data
with tab3:
    @st.cache_data
    def load_area_df():
        return pd.read_csv("csv_files/area_df.csv")

    @st.cache_data
    def load_buyer_rooms():
        return pd.read_csv("csv_files/buyer_rooms.csv")

    @st.cache_data
    def load_heat_by_build_year():
        return pd.read_csv("csv_files/heat_by_build_year.csv")

    @st.cache_data
    def load_geo_build():
        df = pd.read_csv("csv_files/geo_build.csv")
        return df[df["build_year"] > 1900]  # Pre-filter to cache the result

    @st.cache_data
    def load_geo_floors():
        return pd.read_csv("csv_files/geo_floors.csv")
    col7, col8 = st.columns(2)
    with col7:
        st.markdown(
            f"<h1 style='font-size: 48px; text-align: center;'>{trans('No. Unique rooms')}</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<h1 style='font-size: 72px; text-align: center;'>44900</h1>",
            unsafe_allow_html=True
        )
        area_df = load_area_df()
        st.header(trans("Average Heat Consumption / m² against Room Area"))
        chart = alt.Chart(area_df).mark_bar().encode(
            x=alt.X("area_bins:N", sort="-y", title=trans("Room Area, m²")),
            y=alt.Y("eff:Q", title="kWh / m²"),
            color=alt.value("#fcaa01")
        )
        st.altair_chart(chart, use_container_width=True)

    with col8:
        st.markdown(
            f"<h1 style='font-size: 48px; text-align: center;'>{trans('No. Unique buildings')}</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<h1 style='font-size: 72px; text-align: center;'>1421</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<h1 style='font-size: 48px; text-align: center;'>{trans('Average room area')}</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<h1 style='font-size: 72px; text-align: center;'>71.6 m²</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<h1 style='font-size: 48px; text-align: center;'>{trans('Biggest room area')}</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<h1 style='font-size: 72px; text-align: center;'>40760 m²</h1>",
            unsafe_allow_html=True
        )

    st.write(trans("From the graph above we can see that as the room area increases the average heat consumption per square meter actually decreases, meaning it is more efficient to provide heating for larger rooms rather than smaller ones."))
    st.write(trans("## Number of Rooms per buyer, Top 20 buyers"))
    st.write(trans("From this bar chart, we can see that a few buyers possess hundreds of rooms, but we can’t identify who they are because the data about the buyers in the dataset is anonymized."))
    buyer_rooms = load_buyer_rooms()
    st.bar_chart(
        buyer_rooms["room_id"],
        x_label=trans("Individual buyers"),
        y_label=trans("No. Rooms"),
        color="#fcaa01"
    )

    st.write(trans("## Average Heat Consumption / m² by buildings build year"))
    st.write(trans("Over time we can see that heat consumption decreases as buildings get younger, which can be attributed to better construction and insulation technology. Specifically buildings built after 1940 and then 2000 have lower consumption heat consumption on average"))
    heat_by_build_year = load_heat_by_build_year()
    st.bar_chart(
        heat_by_build_year,
        x="build_year",
        y="eff",
        y_label="kWh / m²",
        x_label=trans("Build Year"),
        color="#fcaa01"
    )

    st.write(trans("# Oldest building was built in -- 1849"))
    st.write(trans("# Most frequent build year -- 1970 (1924 buildings)"))
    st.write(trans("## Geospatial building age heatmap"))
    st.write(trans("Green color means newer buildings, blue is older buildings"))
    geo_build = load_geo_build()
    geo_build = geo_build[geo_build["build_year"] > 1900]
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=55.9192288419136,
                longitude=23.29157347671509,
                zoom=11.6,
                pitch=50
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
            ]
        )
    )

    st.write(trans("# Median amount of floors per building -- 5 Floors"))
    st.write(trans("# Highest building -- 15 floors"))
    st.write(trans("## Geospatial building floors heatmap"))
    st.write(trans("Red color means higher buildings with more floors, blue are lower buildings with less floors"))
    geo_floors = load_geo_floors()
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=55.9192288419136,
                longitude=23.29157347671509,
                zoom=11.6,
                pitch=50
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
                    threshold=0.1
                )
            ]
        )
    )

# Tab 4: AI Consumption Estimation Tool
# Tab 4: AI Consumption Estimation Tool
with tab4:
    from pyproj import Transformer
    transformer = Transformer.from_crs("epsg:4326", "epsg:3346", always_xy=True)

    st.title(trans("AI Consumption Estimation Tool"))
    st.markdown(f"### {trans('What does this tool do?')}")
    st.markdown(trans("""Armed with specific data and metrics about a room, this sophisticated AI tool can precisely forecast the monthly consumption of heat for that space. Applications include: efficient energy management in residential and commercial buildings, optimizing heating schedules to reduce costs and environmental impact, assisting in the design of energy-efficient homes and buildings"""))

    st.markdown(f"### {trans('How to use the tool?')}")
    st.markdown(trans("Use the displayed sliders and input boxes to select the various metrics of the room, which helps the AI model give an accurate prediction. In order to select the coordinates of where the room is located, simply click on the map on the location of the relevant building, the map can be dragged around and zoomed in/out. The month of the year field specifies for which month of the year to predict energy consumption. If the number `6` is supplied, the energy consumption will be calculated for the month of June. Lastly, in order to get an estimation, click the 'Predict Energy Consumption' button after adjusting all inputs. After waiting a second for the model to finish calculations, a field should appear below the button with the predictions for heat consumed for that month. More information about the AI model is at the bottom of the page"))

    st.markdown(
        f"""
        <div style='background-color: #fff3cd; padding: 10px; border-radius: 5px; border: 1px solid #ffeeba; color: #856404;'>
            {trans('<strong>Note:</strong> The AI predicts heat consumption in kWh with an average error of about 100 kWh, based on historical data. Results may vary depending on real-world conditions.')}
        </div>
        """,
        unsafe_allow_html=True
    )

    col10, col20 = st.columns([2, 1])
    
    with col20:
        # Map outside the form for coordinate selection
        st.subheader(trans("Select Coordinates"))
        map_center = [55.9292, 23.3102]  # Default center
        if "map_center" not in st.session_state:
            st.session_state.map_center = map_center
        map_obj = folium.Map(location=st.session_state.map_center, zoom_start=12)
        folium.Marker(location=st.session_state.map_center).add_to(map_obj)
        folium.LatLngPopup().add_to(map_obj)
        map_data = st_folium(map_obj, height=300, width=300)
        if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
            lat, lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
            x_coord, y_coord = transformer.transform(lon, lat)
            st.session_state.x_coord = x_coord
            st.session_state.y_coord = y_coord
            st.session_state.map_center = [lat, lon]  # Update map center to last clicked location

    with col10:
        # Form for other inputs
        st.markdown(f"### {trans('Please enter the required information')}")
        with st.form(key="prediction_form"):
            col1, col2 = st.columns(2)  # Reduced to 2 columns since map is outside

            with col1:
                legal_entity = st.checkbox(trans("Is the buyer a legal entity?"), value=False)
                building_floors = st.slider(
                    trans("Number of floors in the building"),
                    min_value=1,
                    max_value=15,
                    step=1,
                    value=5
                )
                room_area = st.number_input(
                    trans("Room area, m²"),
                    min_value=0.0,
                    max_value=40000.0,
                    value=50.0,
                    step=10.0,
                    format="%.1f"
                )

            with col2:
                build_year = st.number_input(
                    trans("Year that the building was built"),
                    min_value=1849,
                    step=1,
                    value=1970
                )
                month = st.number_input(
                    trans("Month of the year (1-12)"),
                    min_value=1,
                    max_value=12,
                    step=1,
                    value=1
                )
                building_func_options_lt = [
                    "Transporto", "Maitinimo", "Gyvenamasis (individualus pastatas)", "Gydymo",
                    "Religinės", "Kita", "Administracinė", "Kultūros", "Gamybos",
                    "Gyvenamasis (trijų ir daugiau butų - daugiaaukštis pastatas)", "Prekybos",
                    "Sporto", "Komercinės paskirties", "Mokslo", "Viešbučių", "Sandėliavimo"
                ]
                if lang == "English":
                    building_func_options_display = [building_func_translations.get(func, func) for func in building_func_options_lt]
                else:
                    building_func_options_display = building_func_options_lt
                selected_display = st.selectbox(
                    trans("Building function"),
                    building_func_options_display,
                    index=building_func_options_lt.index("Gyvenamasis (trijų ir daugiau butų - daugiaaukštis pastatas)")
                )
                # Map back to Lithuanian for model input
                if lang == "English":
                    building_func = next(
                        key for key, value in building_func_translations.items() if value == selected_display
                    )
                else:
                    building_func = selected_display

            # Submit button
            submit_button = st.form_submit_button(trans("Predict Energy Consumption"))

    # Prediction logic after form submission
    if submit_button:
        if "x_coord" not in st.session_state or "y_coord" not in st.session_state:
            st.error(trans("Please select coordinates on the map."))
        else:
            features = {
                "legal_entity": legal_entity,
                "month": month,
                "room_area": room_area,
                "build_year": build_year,
                "building_floors": building_floors,
                "building_func": building_func,
                "x_coord": st.session_state.x_coord,
                "y_coord": st.session_state.y_coord
            }
            preds_heat = get_prediction([list(features.values())])
            st.markdown(
                f"""
                <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px;'>
                    <h3 style='color: #2c3e50;'>{trans('Prediction Results')}</h3>
                    <div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; width: 100%;'>
                        <h4 style='color: #2ecc71; margin: 0;'>{trans('Heat Consumption')}</h4>
                        <p style='font-size: 24px; color: #2ecc71; margin: 5px 0 0 0;'>{float(preds_heat):.2f} kWh / {trans('month')}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Technical description remains unchanged
    st.markdown(f"### {trans('Technical description of the AI model')}")
    st.markdown(f"""
    ### 1. {trans('The data')}
    {trans("The data used to train the model was sourced from Lithuania's open data portal, data.gov.lt, and includes records up to 2025. Preparing the data for modeling required extensive preprocessing. For instance, geographical coordinates needed to be converted from one system to another. Additionally, the dataset contained multiple records for the same room and time period under a specific service category, such as 'heat', though another column provided more detailed classifications. Since these records shared the same units, I aggregated them by summing their values. This reduced, for example, five separate entries for a single room and time period into one consolidated figure, which the model then predicts.")}
    """)
    st.image("images/explanation.png")
    st.markdown(f"""
    ### 2. {trans('The model')}
    {trans('For this tool, I employed an XGBoost model, which leverages Gradient Boosted Decision Trees. While I considered alternative models, my experience—particularly from data science competitions on Kaggle—has shown that libraries like XGBoost and CatBoost often deliver top-tier performance for tabular datasets. This made XGBoost a confident choice. The model is both efficient and lightweight. During training, its hyperparameters were optimized using Optuna, a widely recognized industry-standard library.')}

    ### 3. {trans('Evaluation')}
    {trans('The model’s performance was assessed using two metrics: Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE). Across the test set, the MAE for heat consumption is 140 kWh, indicating an average prediction error of about 140 kWh. However, this figure is somewhat inflated by extreme values where the model’s predictions deviate significantly. For most samples, the average error is closer to 90 kWh, with some predictions as accurate as 15, 30, or 50 kWh off. Generally, larger predicted values correlate with larger errors, likely due to the scarcity of high-energy-consumption samples in the dataset. This skews the heat consumption feature heavily. While these high values could be considered outliers, they are not errors, so I opted to retain them. The RMSE, at around 800 kWh, confirms that the model struggles more with outliers, as expected.')}

    {trans('The model excels at predicting heat consumption in kWh but performs poorly with hot water consumption. Its MAE for hot water prediction is approximately 1 m³, meaning it errs by about 1 cubic meter on average. This larger error makes sense, as hot water consumption is inherently harder to predict than heat consumption. Given this limitation, I’d advise against deploying the model for hot water predictions in a production environment.')}

    {trans('Below is a sample from the test set used to evaluate the model. It compares actual values from the dataset with the AI’s predictions, showcasing impressive results, especially for heat consumption. In some cases, the model is off by 300 kWh or 50 kWh, while in others, it’s spot-on with a difference of 0 kWh. The Actual column reflects the real values the AI aims to match, the Preds column displays the AI’s predictions, and the Diff column indicates the difference between them, revealing the model’s error in units.')}
    """)
    st.image("images/sample.png")
import pandas as pd
import numpy as np
import pickle

def get_prediction(data_array, model_path='other_files/xgb_v1.sav', col_trans_path = 'other_files/column_transformer.pkl'):
  
    df = pd.DataFrame(data_array, columns=["legal_entity", "month", "room_area", "build_year", "building_floors", "building_func", "x_coord", "y_coord"])
    with open(col_trans_path, 'rb') as file:
        column_transformer = pickle.load(file)
    with open(model_path, 'rb') as file:
        xgb_v1 = pickle.load(file)
    df_proc = column_transformer.transform(df)

    return xgb_v1.predict(df_proc)
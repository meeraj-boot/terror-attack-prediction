#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pickle
import streamlit as st

# Load the trained model
loaded_model = pickle.load(open('trained_model02.sav', 'rb'))

# Reverse mapping dictionaries
attack_type_reverse_mapping = {
    'Shooting': 1,
    'Bombing': 2,
    'Hijacking': 3,
    'Arson': 4,
    'Stabbing': 5,
    'Kidnapping': 6,
    'Assassination': 7,
    'Other': 8
}

perpetrator_reverse_mapping = {
    'Group C': 1,
    'Group A': 2,
    'Group D': 3,
    'Group B': 4
}

target_type_reverse_mapping = {
    'civilians': 1,
    'tourists': 2,
    'government officials': 3,
    'infrastructure': 4,
    'police': 5
}

weapon_used_reverse_mapping = {
    'Blade Weapons': 1,
    'chemical': 2,
    'explosives': 3,
    'firearms': 4,
    'incendiary': 5,
    'melee': 6,
    'unknown': 7
}

Intelligence_Tip_reverse_mapping = {
    'Unknown': 1,
    'Yes': 2,
    'No': 3
}

Motive_reverse_mapping = {
    'Political': 1,
    'Religious': 2,
    'Ethnic': 3,
    'Unknown': 4,
    'Retaliation': 5
}

def map_to_encoded_values(value, reverse_mapping):
    return reverse_mapping.get(value, -1)

def terror_prediction(input_data):

    Attack_Type_encoded = map_to_encoded_values(input_data['Attack_Type'], attack_type_reverse_mapping)
    Perpetrator_encoded = map_to_encoded_values(input_data['Perpetrator'], perpetrator_reverse_mapping)
    Target_Type_encoded = map_to_encoded_values(input_data['Target_Type'], target_type_reverse_mapping)
    Weapon_Used_encoded = map_to_encoded_values(input_data['Weapon_Used'], weapon_used_reverse_mapping)
    Intelligence_Tip_encoded = map_to_encoded_values(input_data['Intelligence_Tip'], Intelligence_Tip_reverse_mapping)
    Motive_encoded = map_to_encoded_values(input_data['Motive'], Motive_reverse_mapping)

    Victims_Injured = input_data['Victims_Injured']
    Victims_Deceased = input_data['Victims_Deceased']

    input_data_reshaped = np.array([
        Attack_Type_encoded,
        Perpetrator_encoded,
        Victims_Injured,
        Victims_Deceased,
        Target_Type_encoded,
        Weapon_Used_encoded,
        Intelligence_Tip_encoded,
        Motive_encoded
    ]).reshape(1, -1)

    prediction = loaded_model.predict(input_data_reshaped)

    if prediction[0] == 0:
        return 'Attack is minor'
    else:
        return 'Attack is major'

def main():

    st.title('Terror Attack Prediction Web App')

    # Input fields
    Attack_Type = st.selectbox('Attack Type', list(attack_type_reverse_mapping.keys()))
    Perpetrator = st.selectbox('Perpetrator', list(perpetrator_reverse_mapping.keys()))
    Victims_Injured = st.number_input('Victims Injured', value=0)
    Victims_Deceased = st.number_input('Victims Deceased', value=0)
    Target_Type = st.selectbox('Target Type', list(target_type_reverse_mapping.keys()))
    Weapon_Used = st.selectbox('Weapon Used', list(weapon_used_reverse_mapping.keys()))
    Intelligence_Tip = st.selectbox('Intelligence Tip', list(Intelligence_Tip_reverse_mapping.keys()))
    Motive = st.selectbox('Motive', list(Motive_reverse_mapping.keys()))

    prediction = ''

    if st.button('Predict'):
        input_data = {
            'Attack_Type': Attack_Type,
            'Perpetrator': Perpetrator,
            'Victims_Injured': Victims_Injured,
            'Victims_Deceased': Victims_Deceased,
            'Target_Type': Target_Type,
            'Weapon_Used': Weapon_Used,
            'Intelligence_Tip': Intelligence_Tip,
            'Motive': Motive
        }
        prediction = terror_prediction(input_data)

    st.success(prediction)

if __name__ == '__main__':
    main()


# In[ ]:





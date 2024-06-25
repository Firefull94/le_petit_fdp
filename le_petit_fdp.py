import streamlit as st
from gtts import gTTS
import base64
import os
import pandas as pd



# Function to generate and play TTS
def text_to_speech(text, lang='fr'):
    tts = gTTS(text, lang=lang)
    tts.save("temp.mp3")
    audio_file = open("temp.mp3", "rb").read()
    audio_bytes = base64.b64encode(audio_file).decode()
    audio_html = f'<audio controls autoplay><source src="data:audio/mp3;base64,{audio_bytes}" type="audio/mp3"></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)
    os.remove("temp.mp3")


st.title("Le Petit FDP")
st.markdown('*Small online dictionnary gathering the most famous words use by french people*')
st.markdown("Made by Katakoda for Pierre Petite-Ile <3")

def reader(path):
    df = pd.read_excel(path)
    df = df.fillna("No data")
    for index, row in df.iterrows():
        st.subheader(row['word'])
        if row['alternative'] != "No data":
            st.markdown("Alternative: " +row['alternative'])
        st.markdown("**Translation**: "+row['translation'])
        st.markdown("**Description**: "+row['description'])
        st.markdown("**Example**: ")
        st.markdown(row['example'])
        st.markdown(row['example_translate'])

        if row['alternative'] == "No data":
            col1, col2 = st.columns([1,5])
            with col2:
                if st.button("🔊 Word ", key = row['word']):
                    text_to_speech(row['word'])
            with col1:
                if st.button("🔊 Example", key = row['example']):
                    text_to_speech(row['example'])
        
        else:
            col1, col2, col3 = st.columns([1,1,3])
            with col2:
                if st.button("🔊 Word ", key = row['word']):
                    text_to_speech(row['word'])
            with col3:
                if st.button("🔊 Alternative", key = row['alternative']):
                    text_to_speech(row['alternative'])
            with col1:
                if st.button("🔊 Example", key = row['example']):
                    text_to_speech(row['example'])

def modify(path):
    df = pd.read_excel(path)
    df = df.fillna("No data")

    
# Define sections of the app
def section_insultes():
    st.markdown('<a id="Serious Insults/侮辱"></a>', unsafe_allow_html=True)
    st.header(":red[Serious Insults/侮辱]")
    st.write("Welcome to the Serious Insult section. In this section you will find all the most finest and popular insults commonly used in the French language !\n")
    
    st.write("Do not hesitate to use the '🔊 Listen' button to hear the pronunciation !")
    st.markdown("**Note: (M) means masculin (to use against men) and (F) stands for feminin (to use against women)**")
   
    reader("lpfdp_insultes.xlsx")
    

def section_swear():
    st.markdown('<a id="about"></a>', unsafe_allow_html=True)
    st.header(":green[Swear words/悪口]")
    st.write("Welcome to the Swear words section. In this section you will find all the most finest and popular bad words commonly used in the French language !\n")
    
    st.write("Do not hesitate to use the '🔊 Listen' button to hear the pronunciation !")
    # st.markdown("**Note: (M) means masculin (to use against men) and (F) stands for feminin (to use against women)**")
   
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    reader("lpfdp_swear.xlsx")

def section_funny():
    st.markdown('<a id="Funny Insults/侮辱"></a>', unsafe_allow_html=True)
    st.header(":orange[Funny Insults/ばか侮辱]")
    st.write("Welcome to the Funny Insult section. Basically insult for fun between friend, nothing serious here. In this section you will find all the most funniest, finest and popular insults commonly used in the French language !\n")
    
    st.write("Do not hesitate to use the '🔊 Listen' button to hear the pronunciation !")
    st.markdown("**Note: (M) means masculin (to use against men) and (F) stands for feminin (to use against women)**")

       #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    reader("lpfdp_funny.xlsx")

def add_your_own():
    st.header("Add your own words !")
    st.markdown('In this section you can add the words yourself with their description, translation and examples !')
    st.markdown('You will be able to complete your own dictionnary without me when you will be in France !')
    
    # Predefined password
    correct_password = st.secrets["password"]

    # Password input
    password = st.text_input("Enter password to access this section", type='password')

    if password == correct_password:
        with st.form(key='add_word_form'):
            cat = st.radio("Select the category", ('insultes', 'funny', 'swear'), key='category')

            filename = "lpfdp_" + cat
            path = filename + ".xlsx"


            df = pd.read_excel(path)
            df = df.fillna("No data")

            word = st.text_input("Word", value="No data")
            alternative = st.text_input("Alternative", value="No data")
            translation = st.text_input("Translation", value="No data")
            description = st.text_area("Description", value="No data")
            example = st.text_area("Example", value="No data")
            example_translate = st.text_area("Example Translated", value="No data")

            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                new_data = {
                    'word': [word],
                    'alternative': [alternative],
                    'translation': [translation],
                    'description': [description],
                    'example': [example],
                    'example_translate': [example_translate]
                }
                df_new = pd.DataFrame(new_data)

                df_combined_excel = pd.concat([df, df_new], ignore_index=True)

                df_combined_excel.to_excel(path, index=False)
                st.success("Data added successfully!")
        with st.form(key='update'):
            cat2 = st.radio("Select the category", ('insultes', 'funny', 'swear'), key='category2')
            filename2 = "lpfdp_" + cat2
            path2 = filename2 + ".xlsx"

            df2 = pd.read_excel(path2)
            df2 = df2.fillna("No data")
            words = df2["word"].tolist()
            select_word = st.selectbox("Select the word to update", options=words, key="select_word" )
            action = st.radio("Select the action", ("Delete, Modify"), key="action")

            word_id = df2[df2["word"]==select_word]
            if action == "Modify":
                altmod = df2["alternative"].iloc[word_id]
                transmod = df2["translation"].iloc[word_id]
                descmod = df2["description"].iloc[word_id]
                exmod = df2["example"].iloc[word_id]
                extransmod = df2["example_translate"].iloc[word_id]

                new_alt = st.text_input("Alternative", value=altmod)
                new_trans = st.text_input("Translation", value=transmod)
                new_desc = st.text_area("Description", value=descmod)
                new_ex = st.text_area("Example", value=exmod)
                new_extrans = st.text_area("Example Translated", value=extransmod)

                
            submit_button_update = st.form_submit_button(label='Update')

            if submit_button_update:
                
                if action == "Modify":
                    df2 = df2.drop(word_id)
                    new_data = {
                        'word': [select_word],
                        'alternative': [new_alt],
                        'translation': [new_trans],
                        'description': [new_desc],
                        'example': [new_ex],
                        'example_translate': [new_extrans]
                    }
                    df_new2 = pd.DataFrame(new_data)

                    df_combined_excel2 = pd.concat([df2, df_new2], ignore_index=True)

                    df_combined_excel2.to_excel(path2, index=False)
                    st.success("Data modified successfully!")

                elif action == "Delete":
                    df2 = df2.drop(word_id)
                    df2.to_excel(path2, index=False)
                    st.success("Data deleted successfully!")





# Mapping section names to their corresponding IDs and functions
sections = {
    "Serious Insults/侮辱": ("Serious Insults/侮辱", section_insultes),
    "Funny Insults": ("Funny Insults", section_funny),
    "Swear words/悪口": ("Swear words/悪口", section_swear),
    "Add your own !": ("Add your own !", add_your_own),
    
}

# Create sidebar for navigation
st.sidebar.title("Table of Contents")
selected_section = st.sidebar.radio("Go to", list(sections.keys()))

# Display the selected section
section_id, section_function = sections[selected_section]
section_function()


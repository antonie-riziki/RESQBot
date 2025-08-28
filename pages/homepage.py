import streamlit as st 

st.title("RESQBOT")
st.subheader("🌍 Stay Safe, Stay Informed with ResQBot 🚀")
st.write('''

	Disasters strike when least expected, but timely response can save lives. ResQBot is your intelligent crisis assistant, designed to provide real-time alerts, safety guidance, and emergency support through an AI-powered chatbot.

	Whether facing floods, fires, or any crisis, we connect you to verified information, emergency contacts, and step-by-step safety measures—all in a fast, reliable, and user-friendly experience.

	💡 Be Prepared. Stay Connected. Act Fast. 💡

	''')

st.image('./src/1729866737051.jpeg', width=900)


def display_example_prompts():
    """Display example prompt buttons"""
    example_prompts = [
        ("Gender Based Violence", "Domestic abuse, workplace harassment, unsafe public spaces"),
        ("Kidnapping & Human Trafficking", "Border crossings, child abductions, illegal labor trade"),
        ("Missing Person", "Natural disasters, crowded events, lost hikers"),
        ("Fire Outbreak", "Electrical faults, unattended flames, industrial accidents"),
        ("Road accident", "Reckless driving, poor weather conditions, vehicle malfunctions"),
        ("Civil Unrest & Riots", "Political protests, economic crises, social movements"),
        ("Terror attacks", "Public gatherings, high-security zones, transportation hubs"),
        ("Power Grid Failures", "Extreme weather, cyberattacks, infrastructure failure"),
        ("Water supply disruptions", "Drought, pipeline damage, contamination"),
        ("Structural collapse", "Poor construction, earthquakes, old infrastructure"),
        ("Explosion", "Gas leaks, industrial mishaps, acts of sabotage"),
        ("Floods", "Heavy rainfall, dam failures, rising sea levels"),
        ("Earthquakes", 'Tectonic shifts, seismic activity, aftershocks'),
        ("Wildfires", "Dry weather, human negligence, lightning strikes"),
        ("Disease outbreak", "Pandemics, foodborne illnesses, bioterrorism"), 
        ("Landslides", "Deforestation, heavy rains, unstable terrain"),
        ("Food & water contamination", "Poor sanitation, industrial waste, supply chain failures"),
        ("Gas & Chemical Leaks", "Factory accidents, pipeline ruptures, hazardous material transport"),
    ]

   

    st.markdown("---")
    st.write("Select an example prompt or enter your own, then **click `Search`** to get recommendations.")

    button_cols_1 = st.columns(3)
    button_cols_2 = st.columns(3)
    button_cols_3 = st.columns(3)
    button_cols_4 = st.columns(3)
    button_cols_5 = st.columns(3)
    button_cols_6 = st.columns(3)

    for i, (movie_type, occasion) in enumerate(example_prompts):
        # col = button_cols_1[i] if i < 3 else button_cols_2[i-3] 
        if i < 3:
        	col = button_cols_1[i]

        elif i > 3 and i < 6:
        	col = button_cols_2[i-3]

        elif i > 6 and i < 9:
        	col = button_cols_3[i-6]

        elif i > 9 and i < 12:
        	col = button_cols_4[i-9]

        elif i > 12 and i < 15:
        	col = button_cols_5[i-12]

        elif i > 15 and i < 18:
        	col = button_cols_6[i-15]

        # else:
        # 	break



        if col.button(f"{movie_type} associated with {occasion}"):
        	st.write(f'This is a sample text for {movie_type}')
            # st.session_state.example_movie_type = movie_type
            # st.session_state.example_occasion = occasion
            # return col.button({movie_type})

        # else:
        # 	break

        # if col.button(f"{movie_type} associated with {occasion}") == "Floods":
        # 	st.file_upload('upload a file')

    return False


display_example_prompts()
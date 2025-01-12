import streamlit as st

# Function to calculate savings
def calculate_savings(num_fixtures, hours_per_year, cost_per_kwh, tube_type, pris_armatur, additional_variable):
    # Tube power data
    old_tube_watts = {"T8_58W": 70, "T8_36W": 43, "T5_49W": 54, "T5_28W": 32}
    new_tube_watts = {"LED_20W": 20, "LED_18W": 18, "LED_25W": 25, "LED_16W": 16}

    # Map old tube types to new LED equivalents
    tube_mapping = {
        "T8_58W": "LED_20W",
        "T8_36W": "LED_18W",
        "T5_49W": "LED_25W",
        "T5_28W": "LED_16W"
    }

    if tube_type not in old_tube_watts or tube_type not in tube_mapping:
        raise ValueError(f"Invalid tube type: {tube_type}")

    old_power_consumption = old_tube_watts[tube_type] * 2
    new_power_consumption = new_tube_watts[tube_mapping[tube_type]] * 2

    old_energy_kwh = (old_power_consumption * hours_per_year) / 1000
    new_energy_kwh = (new_power_consumption * hours_per_year) / 1000

    old_energy_cost = old_energy_kwh * num_fixtures * cost_per_kwh
    new_energy_cost = new_energy_kwh * num_fixtures * cost_per_kwh

    savings = old_energy_cost - new_energy_cost

    break_even = ((pris_armatur * num_fixtures) + new_energy_cost + additional_variable) / old_energy_cost

    total_inpris = (pris_armatur * num_fixtures)

    saving_CO2 = ((num_fixtures * 2) / 100) * 2.5

    totalkostnad = (total_inpris + additional_variable)

    kg_co2_saved = saving_CO2 * 1000  # Convert tons to kg

    trees_required = kg_co2_saved / 21.77  # 1 tree absorbs ~21.77 kg CO2 annually

    return old_energy_cost, new_energy_cost, savings, break_even, total_inpris, saving_CO2, totalkostnad, trees_required


# Streamlit Interface
# Add background image and centering styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://raw.githubusercontent.com/AndersEagle/4EDiodeAB/main/Background_Skyline.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;  /* Full viewport height */
    padding: 0;
    text-align: center;  /* Center the text horizontally */
}

/* Ensure the title text is white */
h1 {
    color: white !important; /* Force white color */
    font-size: 24px;
    font-weight: normal; /* Remove bold */
    text-align: center;
}

[data-testid="stSidebar"] {
    background-color: rgba(248, 247, 247, 0.8); /* Transparent sidebar */
}

div.stTitle {
    color: white;  /* White title text */
    font-size: 24px;
    font-weight: normal;
}

label {
    color: white;  /* Make the labels white */
    font-size: 18px;  /* Increase font size for better readability */
    font-weight: normal;
}

div.stNumberInput label,
div.stMarkdownContainer, div.stSelectbox label, div.stButton button {
    color: white; /* Adjust form text color */
    font-weight: normal;
    font-size: 16px;
}

div.stNumberInput input {
    background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent input background */
    color: black; /* Input text color */
    font-weight: normal;
}

div[data-testid="stToolbar"] {
    visibility: hidden; /* Hide the Streamlit menu */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Center the app content
st.title("4E DIODE AB - Besparingskalkylator")

# User input
num_fixtures = st.number_input("Ange antalet armaturer (2 rör i varje):", min_value=1, value=50)
hours_per_year = st.number_input("Ange antalet driftstimmar/år:", min_value=1, value=4000)
cost_per_kwh = st.number_input("Ange elpriset per kWh:", min_value=0.01, value=0.15, format="%.2f")
tube_type = st.selectbox(
    "Välj lysrörstyp som skall bytas:", 
    ["T8_58W", "T8_36W", "T5_49W", "T5_28W"]
)
pris_armatur = st.number_input("Ange inköpskostnad för armatur:", min_value=1, value=800)
additional_variable = st.number_input("Ange ev. extrakostnad, ex.vis installation:", min_value=1, value=1000)

# Calculate and display results
if st.button("Beräkna besparingen"):
    old_cost, new_cost, savings, break_even, total_inpris, saving_CO2, totalkostnad, trees_required = calculate_savings(
        num_fixtures, hours_per_year, cost_per_kwh, tube_type, pris_armatur, additional_variable
    )

    st.markdown(f"<h3 style='color: white;'>Resultat för {tube_type}:</h3>", unsafe_allow_html=True)

    # Styling for the result boxes
    result_box_style = """
    <style>
    .result-box {
        background-color: white;
        color: black;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        font-size: 16px;
        font-weight: normal;
        text-align: left;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    """
    st.markdown(result_box_style, unsafe_allow_html=True)

    # Display results inside styled boxes
    st.markdown(f"<div class='result-box'>Årlig driftskostnad för de gamla lysrören: <b>SEK {old_cost:.0f}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'>Ny driftskostnad för de nya LED-rören: <b>SEK {new_cost:.0f}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'>Årlig driftsbesparing: <b>SEK {savings:.0f}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'>Inköpspris för ny armatur: <b>SEK {total_inpris:.0f}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'>Inkl. kostnad för installation: <b>SEK {totalkostnad:.0f}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'>Minskat CO2-utsläpp: <b>{saving_CO2:.2f} ton</b></div>", unsafe_allow_html=True)
    
    if break_even > 1:
        st.markdown(f"<div class='result-box'>Tid till breakeven: <b>{break_even:.2f} år</b></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='result-box'>Tid till breakeven: <b>{12 * break_even:.2f} månader</b></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='result-box'>Antal träd som krävs för att kompensera för motsvarande CO2: <b>{trees_required:.0f} träd</b></div>", unsafe_allow_html=True)



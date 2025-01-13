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
    background-image: url("https://raw.githubusercontent.com/AndersEagle/4EDiodeAB/main/Background_Skyline2.jpg");
    background-size: cover !important; /* Ensures the image fully covers the container */
    background-position: center center !important; /* Centers the image horizontally and vertically */
    background-repeat: no-repeat; /* Prevents the image from repeating */
    background-attachment: fixed; /* Locks the image to the viewport */
    position: fixed; /* Fixes the container to the screen */
    top: 0;
    left: 0;
    width: 100vw; /* Full viewport width */
    height: 100vh; /* Full viewport height */
    margin: 0; /* Removes default margin */
    padding: 0; /* Removes default padding */
    overflow: hidden; /* Prevents scrolling issues */
    z-index: -1; /* Moves the background behind the content */
}

/* Adjusts the sidebar for better visibility */
[data-testid="stSidebar"] {
    background-color: rgba(248, 247, 247, 0.8); /* Transparent sidebar */
}

/* Title and form labels styling */
h1 {
    color: white !important; /* Ensure the title is white */
    font-size: 24px;
    font-weight: normal;
    text-align: center; /* Center the title text */
}

label {
    color: white; /* Make labels white for better visibility */
    font-size: 18px;
}

/* Styling input boxes and buttons */
div.stNumberInput input,
div.stButton button {
    background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent input background */
    color: black;
    font-size: 16px;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
}

/* Result box styling */
.result-box {
    background-color: white;
    color: black;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 10px;
    font-size: 16px;
    text-align: left;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
}

/* Remove toolbar */
div[data-testid="stToolbar"] {
    visibility: hidden;
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



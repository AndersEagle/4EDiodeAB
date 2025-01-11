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
# Add background image styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://raw.githubusercontent.com/AndersEagle/4EDiodeAB/main/Background_Skyline.jpg");
    background-size: contain;  /* Ensures the image fits entirely within the container */
    background-position: center center;  /* Centers the image in the container */
    background-attachment: fixed;  /* Ensures the background stays fixed when scrolling */
    height: 100vh;  /* Ensures the background fills the entire viewport height */
}


[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.8);
}

div.stTitle {
    color: white;  /* White title text */
    text-align: center;
}

div.stSubtitle {
    color: white;
    text-align: center;
}

label, div[data-testid="stMarkdownContainer"], .stButton, .stNumberInput {
    color: black; /* Black for better readability */
    font-weight: bold;
    font-size: 16px;
}

div.stNumberInput input {
    background-color: white;
    color: black;
}

div[data-testid="stToolbar"] {
    visibility: hidden;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Display the logos
col1, col2 = st.columns([1, 1])  # Equal width columns
with col1:
    st.image("4EDIODE.png", use_container_width=True)
with col2:
    st.image("Diode_logga.png", use_container_width=True)

# Add some space (optional) before the headline
st.markdown("<br>", unsafe_allow_html=True)
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

if st.button("Beräkna besparingen"):
    old_cost, new_cost, savings, break_even, total_inpris, saving_CO2, totalkostnad, trees_required = calculate_savings(
        num_fixtures, hours_per_year, cost_per_kwh, tube_type, pris_armatur, additional_variable
    )

    st.write(f"### Resultat för {tube_type}:")
    st.write(f"**Årlig driftskostnad för de gamla lysrören:** SEK {old_cost:.0f}")
    st.write(f"**Ny driftskostnad för de nya LED-rören:** SEK {new_cost:.0f}")
    st.write(f"**Årlig driftsbesparing:** SEK {savings:.0f}")
    st.write(f"**Inköpspris för ny armatur:** SEK {total_inpris:.0f}")
    st.write(f"**Inkl. kostnad för installation:** SEK {totalkostnad:.0f}")
    st.write(f"**Minskat CO2-utsläpp:** {saving_CO2:.2f} ton")

    # Calculate break-even output
    if break_even > 1:
        break_even_years = break_even / 1
        st.write(f"**Tid till breakeven:** {break_even_years:.2f} år")
    else:
        break_even_months = 12 * break_even
        st.write(f"**Tid till breakeven:** {break_even_months:.2f} månader")

    st.write(f"**Antal träd som krävs för att kompensera för motsvarande CO2:** {trees_required:.0f} träd")


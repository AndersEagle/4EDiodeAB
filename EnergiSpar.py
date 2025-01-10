import streamlit as st

# Function to calculate savings
def calculate_savings(num_fixtures, hours_per_year, cost_per_kwh, tube_type, pris_armatur, additional_variable):
    old_tube_watts = {"T8_58W": 70, "T8_36W": 43}
    new_tube_watts = {"LED_20W": 20, "LED_18W": 18}

    if tube_type not in old_tube_watts:
        raise ValueError(f"Invalid tube type: {tube_type}")

    old_power_consumption = old_tube_watts[tube_type] * 2

    if tube_type == "T8_58W":
        new_power_consumption = new_tube_watts["LED_20W"] * 2
    elif tube_type == "T8_36W":
        new_power_consumption = new_tube_watts["LED_18W"] * 2

    old_energy_kwh = (old_power_consumption * hours_per_year) / 1000
    new_energy_kwh = (new_power_consumption * hours_per_year) / 1000

    old_energy_cost = old_energy_kwh * num_fixtures * cost_per_kwh
    new_energy_cost = new_energy_kwh * num_fixtures * cost_per_kwh

    savings = old_energy_cost - new_energy_cost

    break_even = ((pris_armatur * num_fixtures) + new_energy_cost) / old_energy_cost

    total_inpris = (pris_armatur * num_fixtures)

    saving_CO2 = ((num_fixtures * 2) / 100) * 2.5

    totalkostnad = (total_inpris + additional_variable)

    return old_energy_cost, new_energy_cost, savings, break_even, total_inpris, saving_CO2, totalkostnad

# Function to calculate trees needed for CO2 offset
def calculate_trees(saving_CO2):
    kg_co2_saved = saving_CO2 * 1000  # Convert tons to kg
    trees_required = kg_co2_saved / 21.77  # 1 tree absorbs ~21.77 kg CO2 annually
    return trees_required

# Streamlit Interface
# Display the logo above the headline
# Create two columns
col1, col2 = st.columns([1, 1])  # Equal width columns

# Display the first logo in the left column
with col1:
    st.image("4EDIODE.png", use_column_width=True)

# Display the second logo in the right column
with col2:
    st.image("Diode_logga.png", use_column_width=True)

# Add some space (optional) before the headline
st.markdown("<br>", unsafe_allow_html=True)
st.title("4E DIODE AB - Besparingskalkylator")

# User input
num_fixtures = st.number_input("Ange antalet armaturer (2 rör i varje):", min_value=1, value=50)
hours_per_year = st.number_input("Ange antalet driftstimmar/år:", min_value=1, value=4000)
cost_per_kwh = st.number_input("Ange elpriset per kWh:", min_value=0.01, value=0.15, format="%.2f")
tube_type = st.selectbox("Välj lysrörstyp som skall bytas:", ["T8_58W", "T8_36W"])
pris_armatur = st.number_input("Ange inköpskostnad för armatur:", min_value=1, value=800)
additional_variable = st.number_input("Ange ev. extrakostnad, ex.vis installation:", min_value=1, value=1000)

if st.button("Beräkna besparingen"):
    old_cost, new_cost, savings, break_even, total_inpris, saving_CO2, totalkostnad = calculate_savings(num_fixtures, hours_per_year, cost_per_kwh, tube_type, pris_armatur, additional_variable)

    st.write(f"### Resultat för {tube_type}:")
    st.write(f"**Årlig driftskostnad för de gamla lysrören:** SEK {old_cost:.0f}")
    st.write(f"**Ny driftskostnad för de nya LED-rören:** SEK {new_cost:.0f}")
    st.write(f"**Årlig driftsbesparing:** SEK {savings:.0f}")
    st.write(f"**Inköpspris för ny armatur:** SEK {total_inpris:.0f}")
    st.write(f"**Ev. extra kostnad för installation:** SEK {additional_variable:.0f}")
    st.write(f"**Minskat CO2-utsläpp:** {saving_CO2:.2f} ton")

    # Calculate break-even output
    if break_even > 1:
        break_even_years = break_even / 1
        st.write(f"**Tid till breakeven:** {break_even_years:.2f} år")
    else:
        break_even_months = 12 * break_even
        st.write(f"**Tid till breakeven:** {break_even_months:.2f} månader")
        
    st.write(f"**Antal träd som krävs för att kompensera för motsvarande CO2:** {trees_required:.0f} träd")

import streamlit as st

st.title("🎃 Giant Pumpkin OTT Weight Calculator")
st.write("Enter your measurements below to calculate your pumpkin's estimated weight.")

# 1. GET INPUTS
dap = st.number_input("Enter DAP (Days After Pollination):", min_value=1, value=30)

side_to_side = st.number_input("Enter Side-to-Side measurement (In Inches):", min_value=0.0, value=100.0)
end_to_end = st.number_input("Enter End-to-End measurement (In Inches):", min_value=0.0, value=100.0)
circumference = st.number_input("Enter Circumference (In Inches):", min_value=0.0, value=150.0)

# 2. THE MATH LOGIC
ott = side_to_side + end_to_end + circumference

if ott > 0:
    weight_lbs = (((12.81 / (1 + 6.87 * 2**(-ott / 97))) ** 3 + (ott / 45.9) ** 3.014) - 10)
    weight_kg = weight_lbs * 0.453592
else:
    weight_lbs = 0.0
    weight_kg = 0.0

# 3. DISPLAY RESULTS
st.markdown("---")
st.subheader("📊 Calculation Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="DAP", value=f"{dap} days")

with col2:
    st.metric(label="Total OTT", value=f"{ott:.2f} in")

with col3:
    st.metric(label="Est. Weight (Lbs)", value=f"{weight_lbs:.2f} lbs")

with col4:
    st.metric(label="Est. Weight (Kg)", value=f"{weight_kg:.2f} kg")

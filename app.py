import streamlit as st
import requests
from collections import defaultdict
from datetime import datetime

# Configure the page layout
st.set_page_config(page_title="Pumpkin Growth Dashboard", page_icon="🎃", layout="wide")

# ==============================================================================
# SIDEBAR NAVIGATION & SHARED INPUTS
# ==============================================================================
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to tool:", ["🎃 Weight Calculator (OTT)", "🌤️ Weather & Risk Dashboard", "📅 16-Day Weather Outlook"])

# ==============================================================================
# TOOL 1: OTT WEIGHT CALCULATOR
# ==============================================================================
if page == "🎃 Weight Calculator (OTT)":
    st.title("🎃 Giant Pumpkin OTT Weight Calculator")
    st.write("Enter your measurements below to calculate your pumpkin's estimated weight.")

    dap = st.number_input("Enter DAP (Days After Pollination):", min_value=1, value=30)
    side_to_side = st.number_input("Enter Side-to-Side measurement (In Inches):", min_value=0.0, value=100.0)
    end_to_end = st.number_input("Enter End-to-End measurement (In Inches):", min_value=0.0, value=100.0)
    circumference = st.number_input("Enter Circumference (In Inches):", min_value=0.0, value=150.0)

    ott = side_to_side + end_to_end + circumference

    if ott > 0:
        weight_lbs = (((12.81 / (1 + 6.87 * 2**(-ott / 97))) ** 3 + (ott / 45.9) ** 3.014) - 10)
        weight_kg = weight_lbs * 0.453592
    else:
        weight_lbs = 0.0
        weight_kg = 0.0

    st.markdown("---")
    st.subheader("📊 Calculation Results")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric(label="DAP", value=f"{dap} days")
    with col2: st.metric(label="Total OTT", value=f"{ott:.2f} in")
    with col3: st.metric(label="Est. Weight", value=f"{weight_lbs:.2f} lbs")
    with col4: st.metric(label="Est. Weight", value=f"{weight_kg:.2f} kg")

# ==============================================================================
# TOOL 2: WEATHER, MILDEW & GROWTH RISK DASHBOARD
# ==============================================================================
elif page == "🌤️ Weather & Risk Dashboard":
    st.title("🌤️ Pumpkin Patch Weather & Risk Dashboard")
    st.write("Analyze growth environments and predict Powdery Mildew risks using live weather forecasting.")

    # Sidebar inputs specifically for weather calculations
    st.sidebar.markdown("---")
    st.sidebar.subheader("Dashboard Inputs")
    zip_code = st.sidebar.text_input("Enter 5-Digit ZIP Code:", value="11951").strip()
    dap_weather = st.sidebar.number_input("Current DAP:", min_value=0, value=30)
    fruit_set = st.sidebar.checkbox("Fruit is Set", value=True)

    # Core algorithmic math functions (unaltered from your notebook logic)
    def growth_stage_multiplier(dap, fruit_set):
        if not fruit_set or dap < 20: return 0.65
        elif dap < 35: return 0.9
        else: return 1.1

    def temp_score(temp_f):
        if temp_f < 50: return 0
        elif temp_f < 60: return 10
        elif temp_f < 68: return 20
        elif temp_f <= 80: return 30
        elif temp_f <= 90: return 20
        elif temp_f < 100: return 10
        else: return 0

    def rh_score(rh):
        if rh < 50: return 2
        elif rh < 65: return 8
        elif rh < 75: return 14
        else: return 20

    def cloud_score(cloud):
        if cloud < 30: return 5
        elif cloud < 70: return 10
        else: return 15

    def wind_score(wind_mph):
        if wind_mph < 2: return 6
        elif wind_mph <= 8: return 10
        elif wind_mph <= 15: return 6
        else: return 3

    def dew_score(dewpoint_f, temp_f):
        spread = temp_f - dewpoint_f
        if spread <= 2: return 5
        elif spread <= 5: return 3
        else: return 1

    def rain_penalty(rain_inches):
        if rain_inches == 0: return 0
        elif rain_inches < 0.10: return 5
        elif rain_inches < 0.25: return 12
        else: return 20

    def powdery_mildew_risk(day, multiplier):
        base_score = (
            temp_score(day["mean_temp"]) +
            rh_score(day["avg_humidity"]) +
            cloud_score(day["avg_cloud_cover"]) +
            wind_score(day["max_wind"]) +
            dew_score(day["dewpoint"], day["mean_temp"]) -
            rain_penalty(day["rain_total"])
        )
        base_score = max(0, min(base_score, 100))
        final_score = base_score * multiplier
        final_score = max(0, min(final_score, 100))

        if final_score < 25: category = "Low"
        elif final_score < 50: category = "Moderate"
        elif final_score < 75: category = "High"
        else: category = "Very High"
        return {"score": round(final_score, 1), "category": category}

    def score_day(day_data):
        score = 100
        reasons = []
        if day_data["low_temp"] < 55:
            score -= 12
            reasons.append("Nighttime temperature is below ideal.")
        if day_data["high_temp"] < 72:
            score -= 8
            reasons.append("Daytime temperature is a bit cool for strong growth.")
        if day_data["high_temp"] > 90: 
            score -= 15
            reasons.append("Daytime temperatures may induce heat stress.")
        if day_data["avg_humidity"] > 80:
            score -= 10
            reasons.append("Humidity is high which may lead to increased disease risk.")
        if day_data["max_wind"] > 20:
            score -= 10
            reasons.append("Wind may cause stress or damage to plant.")
        if day_data["rain_total"] > 0.5:
            score -= 8
            reasons.append("Wet conditions may increase disease pressure.")
        if day_data["avg_cloud_cover"] > 85:
            score -= 5
            reasons.append("Heavy cloud cover may reduce solar energy.")

        if score >= 93: label = "Perfect"
        elif score >= 85: label = "Excellent"
        elif score >= 70: label = "Good"
        elif score >= 55: label = "Okay"
        elif score >= 40: label = "Poor"
        else: label = "Risky"
        return score, label, reasons

    # Efficient Caching for API Functions
    @st.cache_data(ttl=3600)
    def geocode_zip(zip_str):
        if not (zip_str.isdigit() and len(zip_str) == 5):
            return None
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": zip_str, "count": 10, "language": "en", "format": "json", "countryCode": "US"}
        res = requests.get(url, params=params, timeout=10).json()
        results = res.get("results", [])
        if not results: return None
        for result in results:
            if zip_str in result.get("postcodes", []):
                return {"name": result.get("name", "Unknown"), "state": result.get("admin1", ""), "latitude": result["latitude"], "longitude": result["longitude"]}
        r = results[0]
        return {"name": r.get("name", "Unknown"), "state": r.get("admin1", ""), "latitude": r["latitude"], "longitude": r["longitude"]}

    @st.cache_data(ttl=3600)
    def get_forecast(lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat, "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,dewpoint_2m,precipitation_probability,precipitation,wind_speed_10m,cloud_cover",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,precipitation_sum",
            "temperature_unit": "fahrenheit", "wind_speed_unit": "mph", "precipitation_unit": "inch", "timezone": "auto", "forecast_days": 7
        }
        return requests.get(url, params=params, timeout=10).json()

    def summarize_hourly_by_day(hourly):
        grouped = defaultdict(lambda: {"humidity": [], "cloud_cover": [], "precip_prob": [], "temperature": [], "dewpoint": []})
        for t, h, c, p, temp_f, dew_f in zip(hourly["time"], hourly["relative_humidity_2m"], hourly["cloud_cover"], hourly["precipitation_probability"], hourly["temperature_2m"], hourly["dewpoint_2m"]):
            day = t.split("T")[0]
            grouped[day]["humidity"].append(h)
            grouped[day]["cloud_cover"].append(c)
            grouped[day]["precip_prob"].append(p)
            grouped[day]["temperature"].append(temp_f)
            grouped[day]["dewpoint"].append(dew_f)
        
        summary = {}
        for day, values in grouped.items():
            summary[day] = {
                "avg_humidity": round(sum(values["humidity"]) / len(values["humidity"]), 1),
                "avg_cloud_cover": round(sum(values["cloud_cover"]) / len(values["cloud_cover"]), 1),
                "max_precip_prob": max(values["precip_prob"]),
                "mean_temp": round(sum(values["temperature"]) / len(values["temperature"]), 1),
                "dewpoint": round(sum(values["dewpoint"]) / len(values["dewpoint"]), 1),
            }
        return summary

    # Program Execution Interface
    if zip_code:
        location = geocode_zip(zip_code)
        if location:
            st.success(f"📍 Showing patch forecast for: **{location['name']}, {location['state']}**")
            
            # Fetch and process data
            raw_forecast = get_forecast(location["latitude"], location["longitude"])
            hourly_summary = summarize_hourly_by_day(raw_forecast["hourly"])
            daily = raw_forecast["daily"]
            multiplier = growth_stage_multiplier(dap_weather, fruit_set)

            st.write(f"**Growth Stage Multiplier Weight:** `{multiplier}`")
            st.markdown("---")

            # Iterate over the 7 days
            for i in range(len(daily["time"])):
                day_string = daily["time"][i]
                extra = hourly_summary.get(day_string, {})
                
                day_data = {
                    "date": day_string, "high_temp": daily["temperature_2m_max"][i], "low_temp": daily["temperature_2m_min"][i],
                    "mean_temp": extra.get("mean_temp"), "rain_total": daily["precipitation_sum"][i], "rain_chance": daily["precipitation_probability_max"][i],
                    "max_wind": daily["wind_speed_10m_max"][i], "avg_humidity": extra.get("avg_humidity"), "avg_cloud_cover": extra.get("avg_cloud_cover"), "dewpoint": extra.get("dewpoint"),
                }

                dt = datetime.strptime(day_string, "%Y-%m-%d")
                readable_day = dt.strftime("%A, %b %d")

                # Process evaluations
                growth_score, growth_label, growth_reasons = score_day(day_data)
                pm_result = powdery_mildew_risk(day_data, multiplier)

                # Set UI color mapping based on disease category
                color_map = {"Low": "🟢 Low Risk", "Moderate": "🟡 Moderate Risk", "High": "🟠 High Risk", "Very High": "🔴 Very High Risk"}
                pm_badge = color_map.get(pm_result['category'], "💡 Unknown")

                # Render each day in a clean interactive drop-down box
                with st.expander(f"📅 {readable_day} | Growth: **{growth_label}** ({growth_score}/100) | Mildew: **{pm_badge}**"):
                    col_left, col_mid, col_right = st.columns(3)
                    
                    with col_left:
                        st.markdown("**🌡️ Temperatures**")
                        st.write(f"• High: {day_data['high_temp']}°F")
                        st.write(f"• Low: {day_data['low_temp']}°F")
                        st.write(f"• Mean: {day_data['mean_temp']}°F")
                        
                    with col_mid:
                        st.markdown("**💧 Moisture & Wind**")
                        st.write(f"• Rain: {day_data['rain_total']} in ({day_data['rain_chance']}% chance)")
                        st.write(f"• Humidity: {day_data['avg_humidity']}%")
                        st.write(f"• Wind Max: {day_data['max_wind']} mph")

                    with col_right:
                        st.markdown("**🔬 Disease Metrics**")
                        st.write(f"• Dew Point: {day_data['dewpoint']}°F")
                        st.write(f"• Cloud Cover: {day_data['avg_cloud_cover']}%")
                        st.write(f"• Mildew Index Score: `{pm_result['score']}/100`")

                    if growth_reasons:
                        st.markdown("**⚠️ Notes for the Day:**")
                        for reason in growth_reasons:
                            st.info(reason)
        else:
            st.error("Invalid ZIP code or location not found. Please verify input.")


# ==============================================================================
# TOOL 3: 16-DAY WEATHER OUTLOOK
# ==============================================================================
elif page == "📅 16-Day Weather Outlook":
    st.title("📅 16-Day Extended Weather Outlook")
    st.write("Track extended atmospheric data and wind trends for long-term planning.")

    # Sidebar parameters for this tool
    st.sidebar.markdown("---")
    st.sidebar.subheader("Extended Outlook Inputs")
    extended_zip = st.sidebar.text_input("Enter 5-Digit ZIP Code:", value="11951", key="ext_zip").strip()

    # Re-use your updated tracking calculations
    def summarize_hourly_extended(hourly):
        grouped = defaultdict(lambda: {"humidity": [], "cloud_cover": [], "precip_prob": [], "temperature": [], "dewpoint": [], "wind": []})
        for t, h, c, p, temp_f, dew_f, wind_mph in zip(hourly["time"], hourly["relative_humidity_2m"], hourly["cloud_cover"], hourly["precipitation_probability"], hourly["temperature_2m"], hourly["dewpoint_2m"], hourly["wind_speed_10m"]):
            day = t.split("T")[0]
            grouped[day]["humidity"].append(h)
            grouped[day]["cloud_cover"].append(c)
            grouped[day]["precip_prob"].append(p)
            grouped[day]["temperature"].append(temp_f)
            grouped[day]["dewpoint"].append(dew_f)
            grouped[day]["wind"].append(wind_mph)
        
        summary = {}
        for day, values in grouped.items():
            summary[day] = {
                "avg_humidity": round(sum(values["humidity"]) / len(values["humidity"]), 1),
                "avg_cloud_cover": round(sum(values["cloud_cover"]) / len(values["cloud_cover"]), 1),
                "max_precip_prob": max(values["precip_prob"]),
                "mean_temp": round(sum(values["temperature"]) / len(values["temperature"]), 1),
                "dewpoint": round(sum(values["dewpoint"]) / len(values["dewpoint"]), 1),
                "max_wind": max(values["wind"]),
                "avg_wind": round(sum(values["wind"]) / len(values["wind"]), 1)
            }
        return summary

    # Use Streamlit's caching magic so 16-day fetches don't slow down the UI
    @st.cache_data(ttl=3600)
    def get_extended_forecast(lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat, "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,dewpoint_2m,precipitation_probability,precipitation,wind_speed_10m,cloud_cover",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,precipitation_sum",
            "temperature_unit": "fahrenheit", "wind_speed_unit": "mph", "precipitation_unit": "inch", "timezone": "auto", "forecast_days": 16
        }
        return requests.get(url, params=params, timeout=10).json()

    # Re-using the geocoder function you already have configured
    if extended_zip:
        # Calls the function we made earlier
        location = geocode_zip(extended_zip) 
        if location:
            st.success(f"📍 Showing 16-Day Outlook for: **{location['name']}, {location['state']}**")
            
            # Fetch 16 days of data instead of 7
            forecast_data = get_extended_forecast(location["latitude"], location["longitude"])
            extended_summary = summarize_hourly_extended(forecast_data["hourly"])
            daily_data = forecast_data["daily"]

            # Layout the 16 days inside clean interactive expanders
            for i in range(len(daily_data["time"])):
                day_str = daily_data["time"][i]
                info = extended_summary.get(day_str, {})
                
                dt = datetime.strptime(day_str, "%Y-%m-%d")
                readable_date = dt.strftime("%A, %b %d")
                
                with st.expander(f"📅 {readable_date} | High: {daily_data['temperature_2m_max'][i]}°F | Wind Max: {info.get('max_wind')} mph"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**🌡️ Temperature Array**")
                        st.write(f"• High: {daily_data['temperature_2m_max'][i]}°F")
                        st.write(f"• Low: {daily_data['temperature_2m_min'][i]}°F")
                        st.write(f"• Mean Daily: {info.get('mean_temp')}°F")
                        st.write(f"• Avg Dew Point: {info.get('dewpoint')}°F")
                        
                    with col2:
                        st.markdown("**💨 Wind Breakdown**")
                        st.write(f"• Peak Gusts: {info.get('max_wind')} mph")
                        st.write(f"• Sustained Avg: {info.get('avg_wind')} mph")
                        
                    with col3:
                        st.markdown("**☁️ Atmosphere & Moisture**")
                        st.write(f"• Total Rain: {daily_data['precipitation_sum'][i]} in")
                        st.write(f"• Max Rain Chance: {daily_data['precipitation_probability_max'][i]}%")
                        st.write(f"• Avg Humidity: {info.get('avg_humidity')}%")
                        st.write(f"• Avg Cloud Cover: {info.get('avg_cloud_cover')}%")
        else:
            st.error("Invalid ZIP code. Please re-verify.")

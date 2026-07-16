import streamlit as st
import requests
from collections import defaultdict
from datetime import datetime

# Configure the page layout
st.set_page_config(page_title="Pumpkin Growth Dashboard", page_icon="🎃", layout="wide")

# ==============================================================================
# 🌍 GLOBAL HELPER FUNCTIONS (Shared by all pages)
# ==============================================================================
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

def get_air_quality_data(lat, lon):
    """Fetches a 5-day hourly Air Quality Index (US AQI) and PM2.5 forecast."""
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "us_aqi,pm2_5",
        "timezone": "auto"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to tool:", [
    "🏠 Home & Patch Notes",
    "🎃 Weight Calculator (OTT)", 
    "🌤️ Weather & Risk Dashboard", 
    "📅 16-Day Weather Outlook",
    "🐝 Pollination Calculator",
    "🌱 Cell Division Optimizer",
    "Powdery Mildew Risk Center"
])


# ==============================================================================
# DISCLAIMER: SIDE BAR
# ==============================================================================

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="font-size: 0.75rem; color: #888888; line-height: 1.2; text-align: justify;">
        <strong> DISCLAIMER:</strong><br>
        This dashboard is designed to provide agricultural estimations and environmental analysis for informational purposes only.
        Patch management, watering, and chemical application descisions are made at the sole discretion and risk of the grower.
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# PAGE 0: HOME & PATCH NOTES (DEFAULT)
# ==============================================================================
if page == "🏠 Home & Patch Notes":
    st.title("🎃 Giant Pumpkin Copilot")
    st.subheader("Your data-driven patch companion.")
    
    st.markdown("---")
    
    # 📰 Section 1: Patch Notes / Blog (Updates)
    st.markdown("### 📰 Patch Notes & Feature Updates")
    
    # We use st.expander so older updates don't clutter the screen, but are still accessible!
    with st.expander("🚀 Version 1.2 Alpha Update — July 2026 (New Features!)", expanded=True):
        st.markdown("""
        * **🌱 New Tool Added:** The *Cell Division Window Optimizer* is now live! Monitor the critical 10-day post-pollination cellular growth phase.
        * **🐝 Pollination Upgrades:** The Pollination Calculator now automatically pulls live weather data at your exact pollination hour to audit temperature, wind, and humidity.
        * **💨 Wind Metrics:** The 16-Day Weather Outlook now tracks both sustained average wind speeds and maximum gusts.
        """)
        
    with st.expander("🛠️ Version 1.1 Alpha Update — March 2026"):
        st.markdown("""
        * **🌤️ Weather Engine Upgrade:** Switched to a responsive 3-column layout for daily risk cards.
        * **⚖️ Legal Safety Net:** Added permanent, muted agricultural disclaimers to the sidebar.
        """)

    st.markdown("---")

    # 🤝 Section 2: Welcome & Our Philosophy (Describe, Don't Prescribe)
    col_welcome, col_philosoph = st.columns(2)
    
    with col_welcome:
        st.markdown("### 👋 Welcome to the Patch")
        st.write("""
        This platform is built for competitive giant pumpkin growers who want to replace guesswork with data. 
        Whether you are tracking daily over-the-top (OTT) growth, timing your pollination windows, or auditing 
        atmospheric stress, this suite of tools formats your metrics cleanly so you can make informed decisions 
        right from your phone.
        """)
        
    with col_philosoph:
        st.markdown("### ⚖️ Our Copilot Philosophy")
        st.info("""
        **We describe; we do not prescribe.** This app will never tell you what fertilizer to apply, how much water to dump, or when to spray. 
        Instead, we translate complex environmental variables into clean mathematical metrics. **You** are the grower, 
        and **you** make the final calls.
        """)

    st.markdown("---")

    # 💡 Section 3: Interactive Quick-Start Guide
    st.markdown("### 💡 Interactive Quick-Start Guide")
    
    guide_step = st.selectbox(
        "Select a tool to learn how to use it:",
        [
            "Select a tool...",
            "🎃 Weight Calculator (OTT)",
            "🌤️ Weather & Risk Dashboard",
            "📅 16-Day Weather Outlook",
            "🐝 Pollination Calculator",
            "🌱 Cell Division Optimizer"
        ]
    )
    
    if guide_step == "🎃 Weight Calculator (OTT)":
        st.write("""
        **What it does:** Estimates your pumpkin's weight using the standard Over-The-Top (OTT) formula.
        
        **How to use it:** 1. Grab a flexible tape measure.
        
        2. Measure *Side-to-Side* (ground to ground over the widest part), *End-to-End* (stem to blossom end), and *Circumference* (parallel to the ground at the widest midpoint).
        
        3. Input the numbers in inches to get your instant weight calculation in both pounds and kilograms.
        """)
    elif guide_step == "🌤️ Weather & Risk Dashboard":
        st.write("""
        **What it does:** Scores daily pumpkin growth potential and powdery mildew disease risks.
        
        **How to use it:** 1. Enter your 5-digit ZIP code in the sidebar.
        
        2. Enter your current Days After Pollination (DAP).
        
        3. Check the daily risk cards to see if overnight temps are dipping too low or if high humidity is creating a mildew risk.
        """)
    elif guide_step == "📅 16-Day Weather Outlook":
        st.write("""
        **What it does:** Provides a long-term look at wind trends, temperatures, and moisture.
        
        **How to use it:** 1. Enter your 5-digit ZIP code in the side bar.
        
        2. View the daily weather cards to see future weather conditions
        """)
    elif guide_step == "🐝 Pollination Calculator":
        st.write("""
        **What it does:** Evaluates your physical pollination technique and audits historical frost windows.
        
        **How to use it:** Input your pollination date, time, and flower protection steps. The app uses historical local frost records to evaluate your seasonal timing.
        
        **Note:** Pollination date must be either current day or within the next 7 days for the live atmospheric audit.
        
        **Note:** Only ZIP codes within the I-95 corridor work at this moment.
        """)
    elif guide_step == "🌱 Cell Division Optimizer":
        st.write("""
        **What it does:** Audits weather conditions during the crucial 10-day post-pollination cell division phase.
        
        **How to use it:** 1. Enter your 5-digit ZIP code.
        
        2. Enter the pollination date reference.
        
        3. Use the evaluation window slider to pick how many days you wish to view. Input your pollination date. If it falls within the active weather forecast, the app tracks daily high/low temperatures to pinpoint cellular stress windows.
        
        **Note:** Pollination date must fall within the evaluation window.
        """)
    else:
        st.write("👈 Select a tool from the dropdown above to read its manual!")

st.markdown("---")
st.caption(
    "**Notice:** Calculations, weather risk indicies, and growth timelines provided by this application "
    "are estimates based on environmental models and standard mathematical formulas. All patch management "
    "decisions, applications, and treatments are carried out entirely at the grower's own risk. This copilot "
    "is an informational tool, not an automated advisor. "
)

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
    st.write("Analyze growth environments and predict Powdery Mildew risks using live weather forecasting and geographic wind drift audits.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Dashboard Inputs")
    zip_code = st.sidebar.text_input("Enter 5-Digit ZIP Code:", value="11951").strip()
    dap_weather = st.sidebar.number_input("Current DAP:", min_value=0, value=30)
    fruit_set = st.sidebar.checkbox("Fruit is Set", value=True)

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

    def powdery_mildew_risk(day, multiplier, longitude):
        # 1. Base Score from microclimate factors
        base_score = (
            temp_score(day["mean_temp"]) +
            rh_score(day["avg_humidity"]) +
            cloud_score(day["avg_cloud_cover"]) +
            wind_score(day["max_wind"]) +
            dew_score(day["dewpoint"], day["mean_temp"]) -
            rain_penalty(day["rain_total"])
        )

        # 2. Long Island Geographical Wind Transmission Audit
        is_east_end = longitude > -72.7  # East of Riverhead / Shirley area
        wind_dir = day.get("avg_wind_direction", 270)
        
        is_west_wind = 200 <= wind_dir <= 310
        is_east_wind = 45 <= wind_dir <= 135

        wind_adjustment = 0
        wind_note = ""

        if is_east_end:
            if is_west_wind:
                wind_adjustment = 15
                wind_note = "💨 West Wind: Elevated spore drift risk from up-island patches."
            elif is_east_wind:
                wind_adjustment = -10
                wind_note = "🌊 East Wind: Marine air decreases incoming terrestrial spore load."
        else:
            if is_east_wind:
                wind_adjustment = 10
                wind_note = "💨 East Wind: Inland drift risks carrying spores westward."

        # Apply geographical adjustments
        base_score = max(0, min(base_score + wind_adjustment, 100))
        final_score = base_score * multiplier
        final_score = max(0, min(final_score, 100))

        if final_score < 25: category = "Low"
        elif final_score < 50: category = "Moderate"
        elif final_score < 75: category = "High"
        else: category = "Very High"
        
        return {
            "score": round(final_score, 1), 
            "category": category, 
            "wind_note": wind_note
        }

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

    @st.cache_data(ttl=3600)
    def get_forecast(lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat, "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,dewpoint_2m,precipitation_probability,precipitation,wind_speed_10m,cloud_cover,wind_direction_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,precipitation_sum",
            "temperature_unit": "fahrenheit", "wind_speed_unit": "mph", "precipitation_unit": "inch", "timezone": "auto", "forecast_days": 7
        }
        return requests.get(url, params=params, timeout=10).json()

    def summarize_hourly_by_day(hourly):
        grouped = defaultdict(lambda: {"humidity": [], "cloud_cover": [], "precip_prob": [], "temperature": [], "dewpoint": [], "wind_direction": []})
        for t, h, c, p, temp_f, dew_f, wind_d in zip(
            hourly["time"], hourly["relative_humidity_2m"], hourly["cloud_cover"], 
            hourly["precipitation_probability"], hourly["temperature_2m"], hourly["dewpoint_2m"], hourly["wind_direction_10m"]
        ):
            day = t.split("T")[0]
            grouped[day]["humidity"].append(h)
            grouped[day]["cloud_cover"].append(c)
            grouped[day]["precip_prob"].append(p)
            grouped[day]["temperature"].append(temp_f)
            grouped[day]["dewpoint"].append(dew_f)
            grouped[day]["wind_direction"].append(wind_d)
        
        summary = {}
        for day, values in grouped.items():
            summary[day] = {
                "avg_humidity": round(sum(values["humidity"]) / len(values["humidity"]), 1),
                "avg_cloud_cover": round(sum(values["cloud_cover"]) / len(values["cloud_cover"]), 1),
                "max_precip_prob": max(values["precip_prob"]),
                "mean_temp": round(sum(values["temperature"]) / len(values["temperature"]), 1),
                "dewpoint": round(sum(values["dewpoint"]) / len(values["dewpoint"]), 1),
                "avg_wind_direction": round(sum(values["wind_direction"]) / len(values["wind_direction"]), 1),
            }
        return summary

    if zip_code:
        location = geocode_zip(zip_code)
        if location:
            st.success(f"📍 Showing patch forecast for: **{location['name']}, {location['state']}**")
            raw_forecast = get_forecast(location["latitude"], location["longitude"])
            hourly_summary = summarize_hourly_by_day(raw_forecast["hourly"])
            daily = raw_forecast["daily"]
            multiplier = growth_stage_multiplier(dap_weather, fruit_set)

            st.write(f"**Growth Stage Multiplier Weight:** `{multiplier}`")
            st.markdown("---")

            for i in range(len(daily["time"])):
                day_string = daily["time"][i]
                extra = hourly_summary.get(day_string, {})
                day_data = {
                    "date": day_string, "high_temp": daily["temperature_2m_max"][i], "low_temp": daily["temperature_2m_min"][i],
                    "mean_temp": extra.get("mean_temp"), "rain_total": daily["precipitation_sum"][i], "rain_chance": daily["precipitation_probability_max"][i],
                    "max_wind": daily["wind_speed_10m_max"][i], "avg_humidity": extra.get("avg_humidity"), "avg_cloud_cover": extra.get("avg_cloud_cover"), "dewpoint": extra.get("dewpoint"),
                    "avg_wind_direction": extra.get("avg_wind_direction"),
                }
                dt = datetime.strptime(day_string, "%Y-%m-%d")
                readable_day = dt.strftime("%A, %b %d")
                growth_score, growth_label, growth_reasons = score_day(day_data)
                
                # Dynamic Spore risk calculation
                pm_result = powdery_mildew_risk(day_data, multiplier, location["longitude"])
                color_map = {"Low": "🟢 Low Risk", "Moderate": "🟡 Moderate Risk", "High": "🟠 High Risk", "Very High": "🔴 Very High Risk"}
                pm_badge = color_map.get(pm_result['category'], "💡 Unknown")

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
                        st.write(f"• Wind Direction: {int(day_data['avg_wind_direction'])}°")
                    with col_right:
                        st.markdown("**🔬 Disease Metrics**")
                        st.write(f"• Dew Point: {day_data['dewpoint']}°F")
                        st.write(f"• Cloud Cover: {day_data['avg_cloud_cover']}%")
                        st.write(f"• Mildew Index Score: `{pm_result['score']}/100`")
                    
                    # Display special downwind transmission alerts if applicable
                    if pm_result["wind_note"] or growth_reasons:
                        st.markdown("**⚠️ Notes for the Day:**")
                        if pm_result["wind_note"]:
                            st.info(pm_result["wind_note"])
                        for reason in growth_reasons: 
                            st.info(reason)
        else:
            st.error("Invalid ZIP code or location not found. Please verify input.")

        # ==============================================================================
        # 💨 WILDFIRE SMOKE & AIR QUALITY MONITOR
        # ==============================================================================
        st.markdown("### 💨 Live Smoke & Air Quality Monitor")
        
        aqi_data = get_air_quality_data(location["latitude"], location["longitude"])
        
        if aqi_data and "hourly" in aqi_data:
            hourly_aqi = aqi_data["hourly"]["us_aqi"]
            hourly_pm25 = aqi_data["hourly"]["pm2_5"]
            times = aqi_data["hourly"]["time"]
            
            # Find current hourly indices
            now_str = datetime.now().strftime("%Y-%m-%dT%H:00")
            # Fallback to index 0 if exact hour match fails
            current_idx = 0
            for idx, t in enumerate(times):
                if t.startswith(now_str):
                    current_idx = idx
                    break
                    
            current_aqi = hourly_aqi[current_idx]
            current_pm = hourly_pm25[current_idx]
            
            # Determine Hazard Class & Guidance
            if current_aqi <= 50:
                aqi_status = "🟢 Good Air Quality"
                guidance = "Excellent patch working conditions. Full solar potential."
                aqi_box = st.success
            elif current_aqi <= 100:
                aqi_status = "🟡 Moderate Haze"
                guidance = "Slight reduction in solar radiation potential. Normal patch care."
                aqi_box = st.info
            elif current_aqi <= 150:
                aqi_status = "🟠 Unhealthy for Sensitive Groups (Hazy)"
                guidance = "Visible smoke aloft likely. Keep strenuous patch work minimal if sensitive."
                aqi_box = st.warning
            else:
                aqi_status = "🔴 Unhealthy / Smoky Skies"
                guidance = "Heavy haze. Photosynthesis is restricted. Avoid working hard in the patch today."
                aqi_box = st.error

            # Layout metrics
            col_aqi1, col_aqi2 = st.columns([1, 2])
            with col_aqi1:
                st.metric(label="Current Air Quality (AQI)", value=f"{int(current_aqi)} US", delta=f"{current_pm:.1f} µg/m³ PM2.5", delta_color="inverse")
            with col_aqi2:
                aqi_box(f"**Status:** {aqi_status}  \n**Patch Impact Guidance:** {guidance}")
                
            # Quick look-ahead for the next 48 hours (Detect oncoming smoke spikes!)
            upcoming_48_aqi = hourly_aqi[current_idx:current_idx+48]
            max_future_aqi = max(upcoming_48_aqi) if upcoming_48_aqi else current_aqi
            
            if max_future_aqi > current_aqi and max_future_aqi > 100:
                st.warning(f"⚠️ **Heads Up:** Air quality is forecast to deteriorate over the next 48 hours, peaking near a smoky **{int(max_future_aqi)} AQI**. Prepare for hazy solar conditions.")
        else:
            st.info("ℹ️ Air Quality data is temporarily unavailable for this region.")

# ==============================================================================
# TOOL 3: 16-DAY WEATHER OUTLOOK
# ==============================================================================
elif page == "📅 16-Day Weather Outlook":
    st.title("📅 16-Day Extended Weather Outlook")
    st.write("Track extended atmospheric data and wind trends for long-term planning.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Extended Outlook Inputs")
    extended_zip = st.sidebar.text_input("Enter 5-Digit ZIP Code:", value="11951", key="ext_zip").strip()

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

    if extended_zip:
        location = geocode_zip(extended_zip) # Now it can successfully find it!
        if location:
            st.success(f"📍 Showing 16-Day Outlook for: **{location['name']}, {location['state']}**")
            forecast_data = get_extended_forecast(location["latitude"], location["longitude"])
            extended_summary = summarize_hourly_extended(forecast_data["hourly"])
            daily_data = forecast_data["daily"]

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

# ==============================================================================
# TOOL 4: POLLINATION CALCULATOR & WEATHER AUDITOR
# ==============================================================================
elif page == "🐝 Pollination Calculator":
    st.title("🐝 Pollination Success & Weather Auditor")
    st.write("Track flower protection methods, regional seasonal windows, and audit atmospheric data during pollination.")

    import math
    import csv

    # Sidebar parameters for pollination tool
    st.sidebar.markdown("---")
    st.sidebar.subheader("Pollination Inputs")
    poll_zip = st.sidebar.text_input("Enter 5-Digit ZIP Code:", value="11951", key="poll_zip").strip()

    # Core UI Layout Inputs
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        p_date = st.date_input("Pollination Date:", datetime.today().date())
        p_time = st.time_input("Estimated Pollination Time (Local):", datetime.now().time())
        male_count = st.number_input("Number of male flowers used:", min_value=1, max_value=20, value=3)
    with col_in2:
        flower_covered = st.checkbox("Female flower was covered/bagged before and after pollination?", value=True)
        hand_pollinated = st.checkbox("Was it hand pollinated?", value=True)

    pollination_info = {
        "date": p_date, "time": p_time, "male_flowers_used": male_count,
        "flower_covered_before_after": flower_covered, "hand_pollinated": hand_pollinated
    }

    # Data Calculation Logic
    LAT_STEP, LON_STEP = 0.5, 1.0
    def snap_down(val, step): return math.floor(val / step) * step

    @st.cache_data
    def load_frost_regions(filename="average_last_frost_grid_filled.csv"):
        regions = []
        try:
            with open(filename, newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    regions.append({
                        "region_name": row["region_name"].strip(),
                        "lat_min": float(row["lat_min"]), "lat_max": float(row["lat_max"]),
                        "lon_min": float(row["lon_min"]), "lon_max": float(row["lon_max"]),
                        "avg_last_frost": row["avg_last_frost"].strip()
                    })
            return regions
        except FileNotFoundError:
            return None

    def find_frost_region(lat, lon, region_list):
        for r in region_list:
            if r["lat_min"] <= lat < r["lat_max"] and r["lon_min"] <= lon < r["lon_max"]: return r
        return None

    def parse_frost_date(frost_str, year):
        # Clean up any accidental leading/trailing spaces or quotes
        frost_str = str(frost_str).strip().replace('"', '').replace("'", "")
        
        # List of candidate formats to try parsing
        # %m/%d for "4/23", %m-%d for "04-23", %b-%d for "Apr-23" or "23-Apr" etc.
        for fmt in ["%m/%d", "%m-%d", "%d-%b", "%b-%d", "%Y/%m/%d", "%m/%d/%Y", "%Y-%m-%d"]:
            try:
                # If the string already looks like a full date with a 4-digit year, parse it directly
                if len(frost_str) >= 8 and ("/" in frost_str or "-" in frost_str):
                    # Check if it has a 4-digit year in it anywhere
                    parts = frost_str.replace("-", "/").split("/")
                    if any(len(p) == 4 for p in parts):
                        if parts[0].isdigit() and len(parts[0]) == 4:
                            return datetime.strptime(frost_str, "%Y/%m/%d" if "/" in frost_str else "%Y-%m-%d").date()
                        else:
                            return datetime.strptime(frost_str, "%m/%d/%Y").date()

                # Otherwise, append the current pollination year to the MM/DD string
                # We normalize delimiters to '/' to make matching cleaner
                normalized_str = frost_str.replace("-", "/")
                normalized_fmt = fmt.replace("-", "/")
                
                # If the format doesn't have a year component, add it
                if "%Y" not in normalized_fmt:
                    return datetime.strptime(f"{year}/{normalized_str}", f"%Y/{normalized_fmt}").date()
                else:
                    return datetime.strptime(normalized_str, normalized_fmt).date()
            except ValueError:
                continue
                
        raise ValueError(f"Unsupported Frost Date Format: {frost_str}")

    def score_pollination_date(poll_date, f_date):
        days_after_frost = (poll_date - f_date).days
        if 45 <= days_after_frost <= 60: return 30, f"Ideal Timing ({days_after_frost} days after frost)"
        elif 40 <= days_after_frost < 45 or 61 <= days_after_frost <= 67: return 24, f"Good Timing ({days_after_frost} days after frost)"
        elif 35 <= days_after_frost < 40 or 68 <= days_after_frost <= 75: return 18, f"Acceptable Timing ({days_after_frost} days after frost)"
        elif 30 <= days_after_frost < 35 or 76 <= days_after_frost <= 85: return 10, f"Suboptimal Timing ({days_after_frost} days after frost)"
        return 4, f"Poor season timing ({days_after_frost} days after frost)"

    def score_pollination_time(p_t):
        tot_min = p_t.hour * 60 + p_t.minute
        if 5 * 60 <= tot_min <= 8 * 60: return 20, "Ideal Early Morning Window"
        elif 8 * 60 < tot_min <= 10 * 60: return 16, "Good Morning Window"
        elif 10 * 60 < tot_min <= 12 * 60: return 10, "Poor Midday Window"
        return 5, "Suboptimal Windows (High Heat/Pollen Degrade Risks)"

    def score_male_flower_count(m_c):
        if m_c >= 4: return 20, "Strong Genetic Load (>=4 Male Flowers)"
        elif m_c == 3: return 16, "Good Genetic Load (3 Male Flowers)"
        elif m_c == 2: return 12, "Moderate Genetic Load (2 Male Flowers)"
        return 8, "Minimum Genetic Load (1 Male Flower)"

    def score_hand_pollinated(h_p): return (15, "Hand Pollinated") if h_p else (5, "Natural/Insect Pollinated")
    def score_flower_covered(f_c): return (15, "Protected (Covered Before & After)") if f_c else (5, "Exposed to Competitors/Weather")

    def score_pollination_weather(temp_f, wind_mph, rain_chance, humidity):
        score, reasons = 100, []
        if temp_f >= 90: score -= 25; reasons.append("❌ Too Hot: Pollen tubes degrade over 90°F.")
        elif temp_f >= 75: score -= 10; reasons.append("⚠️ Warm: Higher sweat risk inside bags.")
        elif temp_f <= 55: score -= 25; reasons.append("❌ Too Cold: Bee activity stops, flower metabolism freezes.")
        elif temp_f <= 65: score -= 15; reasons.append("⚠️ Cool: Sluggish pollen growth development rates.")
        else: reasons.append("🟢 Ideal temperature window.")

        if wind_mph >= 20: score -= 20; reasons.append("❌ Severe Wind: High loss risk or physical blossom scarring.")
        elif wind_mph >= 11: score -= 10; reasons.append("⚠️ Breezy: Increases physical tearing risk to protective bagging structures.")
        else: reasons.append("🟢 Ideal gentle wind velocity.")

        if rain_chance >= 60: score -= 20; reasons.append("❌ Rain Warning: Moisture destroys pollen grains instantly on contact.")
        elif rain_chance >= 20: score -= 5; reasons.append("⚠️ Low Risk: Keep an eye on rain clouds.")
        else: reasons.append("🟢 Low precipitation risk.")

        if humidity >= 80 or humidity < 50: score -= 20; reasons.append("⚠️ Humidity Issue: Extreme values alter pollen consistency.")
        else: reasons.append("🟢 Good pollination humidity profiles.")
        return max(score, 0), reasons

    def get_closest_pollination_hour(hourly, poll_date, poll_time):
        target_dt = datetime.combine(poll_date, poll_time)
        forecast_times = [datetime.fromisoformat(t.replace('Z', '')) for t in hourly["time"]]
        if target_dt < min(forecast_times) or target_dt > max(forecast_times): return None
        best_index = min(range(len(forecast_times)), key=lambda i: abs((forecast_times[i] - target_dt).total_seconds()))
        return {
            "time": hourly["time"][best_index], "temperature_2m": hourly["temperature_2m"][best_index],
            "relative_humidity_2m": hourly["relative_humidity_2m"][best_index], "precipitation_probability": hourly["precipitation_probability"][best_index],
            "wind_speed_10m": hourly["wind_speed_10m"][best_index]
        }

    # Evaluation Execution Pipeline
    if poll_zip:
        location = geocode_zip(poll_zip)
        regions_list = load_frost_regions()
        
        if regions_list is None:
            st.error("⚠️ `average_last_frost_grid_filled.csv` file not found in your repository folder. Please upload it to GitHub.")
        elif location:
            match = find_frost_region(location["latitude"], location["longitude"], regions_list)
            
            if match:
                frost_date = parse_frost_date(match["avg_last_frost"], pollination_info["date"].year)
                
                # Execute Core Calculations
                d_score, d_reason = score_pollination_date(pollination_info["date"], frost_date)
                t_score, t_reason = score_pollination_time(pollination_info["time"])
                m_score, m_reason = score_male_flower_count(pollination_info["male_flowers_used"])
                h_score, h_reason = score_hand_pollinated(pollination_info["hand_pollinated"])
                c_score, c_reason = score_flower_covered(pollination_info["flower_covered_before_after"])
                
                total_procedural_score = d_score + t_score + m_score + h_score + c_score
                
                def get_pollination_label(s):
                    if s >= 95: return "🏆 Perfect!"
                    elif s >= 85: return "💎 Elite"
                    elif s >= 75: return "🥇 Strong"
                    elif s >= 60: return "🥈 Average"
                    elif s >= 40: return "🥉 Weak"
                    return "⚠️ Very Poor"

                st.markdown("---")
                st.subheader(f"📊 Procedural Execution Score: **{total_procedural_score}/100** ({get_pollination_label(total_procedural_score)})")
                
                # Render Breakdown metrics visually using metric cards
                col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
                col_m1.metric("Date Score", f"{d_score} pts", help=d_reason)
                col_m2.metric("Time Window", f"{t_score} pts", help=t_reason)
                col_m3.metric("Genetic Load", f"{m_score} pts", help=m_reason)
                col_m4.metric("Technique", f"{h_score} pts", help=h_reason)
                col_m5.metric("Protection", f"{c_score} pts", help=c_reason)

                # Execute Weather Auditor Section
                st.markdown("---")
                st.subheader("🌦️ Live Atmospheric Audit")
                
                url = "https://api.open-meteo.com/v1/forecast"
                params = {
                    "latitude": location["latitude"], "longitude": location["longitude"],
                    "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m",
                    "temperature_unit": "fahrenheit", "wind_speed_unit": "mph", "timezone": "auto", "forecast_days": 7
                }
                weather_res = requests.get(url, params=params, timeout=10).json()
                
                poll_hour = get_closest_pollination_hour(weather_res["hourly"], pollination_info["date"], pollination_info["time"])
                
                if poll_hour is None:
                    st.info("ℹ️ Weather Auditing can only be run for dates falling within the active 7-day forecast window.")
                else:
                    w_score, w_reasons = score_pollination_weather(
                        poll_hour["temperature_2m"], poll_hour["wind_speed_10m"],
                        poll_hour["precipitation_probability"], poll_hour["relative_humidity_2m"]
                    )
                    
                    col_w1, col_w2 = st.columns([1, 2])
                    with col_w1:
                        st.metric("Weather Match Score", f"{w_score}/100")
                        st.caption(f"Closest Forecast Slot: `{poll_hour['time'].split('T')[1]}`")
                    with col_w2:
                        st.write("**Patch Condition Audit Logs:**")
                        for reason in w_reasons:
                            st.write(f"- {reason}")
            else:
                st.warning("No historical frost zone matched your exact coordinates inside the database dataset.")
        else:
            st.error("Invalid ZIP profile entry configuration.")

# ==============================================================================
# TOOL 5: CELL DIVISION WINDOW OPTIMIZER
# ==============================================================================
elif page == "🌱 Cell Division Optimizer":
    st.title("🌱 Cell Division Window Optimizer")
    st.write("Monitor the critical 10-day post-pollination cellular growth phase to maximize ultimate weight potential.")

    # Sidebar layout for parameters
    st.sidebar.markdown("---")
    st.sidebar.subheader("Cell Division Inputs")
    cell_zip = st.sidebar.text_input("Enter 5-Digit ZIP Code:", value="11951", key="cell_zip").strip()
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        p_date_cell = st.date_input("Pollination Date Reference:", datetime.today().date(), key="cell_p_date")
    with col_c2:
        days_window = st.slider("Evaluation Window (Days):", min_value=5, max_value=14, value=10)

    # Core Calculation Helpers
    def score_cell_division_day(day_max, day_min, rain_total, avg_humidity=None):
        score, reasons = 100, []
        
        if day_max > 92: score -= 25; reasons.append("❌ Excessive Daytime Heat (Restricts division)")
        elif day_max > 86: score -= 10; reasons.append("⚠️ Warm Daytime Temperatures")
        elif day_max < 65: score -= 15; reasons.append("⚠️ Cool Daytime Temperatures (Slows metabolism)")
        else: reasons.append("🟢 Good Daytime Temperatures")

        if day_min < 48: score -= 25; reasons.append("❌ Cold Nighttime Lows (Stops plant growth)")
        elif day_min < 55: score -= 10; reasons.append("⚠️ Cool Nighttime Temperatures")
        elif day_min > 72: score -= 8; reasons.append("⚠️ Very Warm Nights (High respiration load)")
        else: reasons.append("🟢 Good Nighttime Temperatures")

        if rain_total >= 1.00: score -= 20; reasons.append("❌ Heavy Rainfall (Saturated patch risks)")
        elif rain_total >= 0.50: score -= 10; reasons.append("⚠️ Moderate Rainfall")
        else: reasons.append("🟢 Safe moisture levels")

        if avg_humidity is not None:
            if avg_humidity >= 90: score -= 10; reasons.append("⚠️ High Humidity (Disease risk)")
            elif avg_humidity < 40: score -= 5; reasons.append("⚠️ Low Humidity Stress")
            
        return max(score, 0), reasons

    # Shared weather summarizer
    def summarize_hourly_cell(hourly):
        grouped = defaultdict(lambda: {"humidity": []})
        for t, h in zip(hourly["time"], hourly["relative_humidity_2m"]):
            day = t.split("T")[0]
            grouped[day]["humidity"].append(h)
        return {day: {"avg_humidity": round(sum(v["humidity"]) / len(v["humidity"]), 1)} for day, v in grouped.items()}

    if cell_zip:
        location = geocode_zip(cell_zip)
        if location:
            # Fetch a 14-day window forecast so we have enough data buffer
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": location["latitude"], "longitude": location["longitude"],
                "hourly": "relative_humidity_2m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "temperature_unit": "fahrenheit", "precipitation_unit": "inch", "timezone": "auto", "forecast_days": 14
            }
            raw_res = requests.get(url, params=params, timeout=10).json()
            hourly_sum = summarize_hourly_cell(raw_res["hourly"])
            daily = raw_res["daily"]

            daily_results = []
            for day_str, tmax, tmin, rain in zip(daily["time"], daily["temperature_2m_max"], daily["temperature_2m_min"], daily["precipitation_sum"]):
                day_date = datetime.strptime(day_str, "%Y-%m-%d").date()
                days_from_poll = (day_date - p_date_cell).days

                if 1 <= days_from_poll <= days_window:
                    extra = hourly_sum.get(day_str, {})
                    h_avg = extra.get("avg_humidity")
                    score, reasons = score_cell_division_day(tmax, tmin, rain, avg_humidity=h_avg)
                    
                    daily_results.append({
                        "date": day_str, "days_from_pollination": days_from_poll,
                        "score": score, "max_temp": tmax, "min_temp": tmin,
                        "rain_total": rain, "avg_humidity": h_avg, "reasons": reasons
                    })

            if not daily_results:
                st.info("ℹ️ No forecast days line up with your selection. Make sure the Pollination Date matches the upcoming forecast window!")
            else:
                avg_window_score = round(sum(d["score"] for d in daily_results) / len(daily_results), 1)
                
                def get_cell_division_label(s):
                    if s >= 95: return "🏆 Perfect"
                    elif s >= 85: return "💎 Elite"
                    elif s >= 75: return "🥇 Strong"
                    elif s >= 60: return "🥈 Average"
                    return "⚠️ Suboptimal"

                st.markdown("---")
                st.subheader(f"📊 Overall Window Score: **{avg_window_score}/100** ({get_cell_division_label(avg_window_score)})")
                st.caption(f"Averages tracked over **{len(daily_results)} active growth days** inside the cell-splitting cycle.")

                # Render Interactive Daily Timeline
                st.write("**🗓️ Cellular Growth Timeline:**")
                for day in daily_results:
                    dt = datetime.strptime(day["date"], "%Y-%m-%d")
                    readable_date = dt.strftime("%A, %b %d")
                    
                    with st.expander(f"🌱 Day {day['days_from_pollination']} | {readable_date} | Day Score: **{day['score']}/100**"):
                        col_fa, col_fb = st.columns(2)
                        with col_fa:
                            st.write(f"• **High Temp:** {day['max_temp']}°F")
                            st.write(f"• **Low Temp:** {day['min_temp']}°F")
                            st.write(f"• **Total Rain:** {day['rain_total']} in")
                            if day['avg_humidity']: st.write(f"• **Avg Humidity:** {day['avg_humidity']}%")
                        with col_fb:
                            st.write("**Cell Division Stress Factors:**")
                            for r in day["reasons"]:
                                st.write(f"- {r}")
        else:
            st.error("Invalid ZIP code selection.")


# =================================================================
# TOOL: POWDERY MILDEW RISK CENTER
# =================================================================

elif page == "Powdery Mildew Risk Center":
    st.title("Powdery Mildew Risk Center")
    st.write("Track microclimatic humidity and weather conditions favoring fungal outbreaks.")

    st.sidebare.markdown("---")
    st.sidebar.subheader("Mildew Parameters")
    zip_code = st.sidebar.text_input("Enter 5-Digit ZIP Code:", value=" ", key="pm_zip").strip()
    dap_pm = st.sidebar.number_input("Current DAP:", min_value=0, value=" ", key="pm_dap")
    fruit_set = st.sidebare.checkbox("Fruit is Set", value=True, key="pm_fruit_set")

def temp_score(temp_f):
        if temp_f < 50: return 0
elif temp_f < 60: return 10
elif temp_f <  68: return 20
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

def growth_stage_multiplier(dap, fruit_set):
    if not fruit_set or dap < 20: return 0.65
elif dap < 35: return: 0.9
else: return 1.1

def calculate_pm_details(day, multiplier, longitude):
    base_score = (
        temp_score(day["mean_temp"]) +
        rh_score(day["avg_humidity"]) +
        cloud_score(day["avg_cloud_cover"]) +
        wind_score(day["max_wind"]) +
        dew_score(day["dewpoint"], day["mean_temp"]) -
        rain_penalty(day["rain_total"])
    )

is_east_end = longitude > 72.7
wind_dir = day.get("avg_wind_direction", 270)
is_west_wind = 200 <= wind_dir <= 310
is_east_wind = 45 <= wind_dir <= 135

wind_adjustment = 0
wind_note = ""

if is_east_end:
    if is_west_wind:
        wind_adjustment = 15
        wind_note = "Westerly Winds: Elevated spore drift from western patches possible."
    elif is_east_wind:
        wind_adjustment = -10
        wind_note = "Eastrly Winds: Clean marine air, reduction in spore risk possible."
    else: if is_east_wind:
        wind_adjustment = 10
        wind_note = "Easterly Wind: Spores migrating westward from agricultural hubs possible."
# 2 East winds??
# North or South winds?
if final_score < 25:
    category = "Low"
    status_desc = "Powdery Mildew pressure is minimal, but not zero. Conditions unfavorable for outbreak."
    action_guidance = "Normal scouting; regular preventative program is sufficient."
    box_style = st.success
elif final_score < 50:
    category = "Moderate"
    status_desc = "Midlew conditons rising slightly. Conditions neutral for outbreak."
    action_guidance = "Maintain protective coverage. Insprect shaded inner vine structures."
    box_style = st.info
elif final_score <  75:
    category = "High"
    status_desc = "Powdery Mildew pressure is high, favorable conditons for spore growth. Spores may germinate quickly."
    action_guidance = "High risk. Ensure fungicide coverage is active and clean."
    box_style = st.warning
else:
    category = "Very High"
    status_desc = "Powdery Mildew pressure is very high. Ideal conditions for spore germination and spore transfers between leaves and patches."
    action_guidance = "Check patch immediately for spots or signs of powdery mildew."
    box_style = st.error

return {
    "score": round(final_score, 1),
    "category": category,
    "desc": status_desc,
    "action": action_guidance,
    "wind_note": wind_note,
    "box_style": box_style
}

#fetch 7 days of forecast to fill 1 main box + 6 sidebar layout.
@st.cache_data(ttl=3600)
    def get_forecast_pm(lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat, "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,dewpoint_2m,precipitation_probability,precipitation,wind_speed_10m,cloud_cover,wind_direction_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,precipitation_sum",
            "temperature_unit": "fahrenheit", "wind_speed_unit": "mph", "precipitation_unit": "inch", "timezone": "auto", "forecast_days": 7
        }
        return requests.get(url, params=params, timeout=10).json()

    def summarize_hourly_pm(hourly):
        grouped = defaultdict(lambda: {"humidity": [], "cloud_cover": [], "precip_prob": [], "temperature": [], "dewpoint": [], "wind_direction": []})
        for t, h, c, p, temp_f, dew_f, wind_d in zip(
            hourly["time"], hourly["relative_humidity_2m"], hourly["cloud_cover"], 
            hourly["precipitation_probability"], hourly["temperature_2m"], hourly["dewpoint_2m"], hourly["wind_direction_10m"]
        ):
            day = t.split("T")[0]
            grouped[day]["humidity"].append(h)
            grouped[day]["cloud_cover"].append(c)
            grouped[day]["precip_prob"].append(p)
            grouped[day]["temperature"].append(temp_f)
            grouped[day]["dewpoint"].append(dew_f)
            grouped[day]["wind_direction"].append(wind_d)
        
        summary = {}
        for day, values in grouped.items():
            summary[day] = {
                "avg_humidity": round(sum(values["humidity"]) / len(values["humidity"]), 1),
                "avg_cloud_cover": round(sum(values["cloud_cover"]) / len(values["cloud_cover"]), 1),
                "max_precip_prob": max(values["precip_prob"]),
                "mean_temp": round(sum(values["temperature"]) / len(values["temperature"]), 1),
                "dewpoint": round(sum(values["dewpoint"]) / len(values["dewpoint"]), 1),
                "avg_wind_direction": round(sum(values["wind_direction"]) / len(values["wind_direction"]), 1),
            }
        return summary

    if zip_code:
        location = geocode_zip(zip_code)
        if location:
            raw_forecast = get_forecast_pm(location["latitude"], location["longitude"])
            hourly_summary = summarize_hourly_pm(raw_forecast["hourly"])
            daily = raw_forecast["daily"]
            multiplier = growth_stage_multiplier(dap_pm, fruit_set)

            # Process days
            processed_days = []
            for i in range(len(daily["time"])):
                day_string = daily["time"][i]
                extra = hourly_summary.get(day_string, {})
                day_data = {
                    "date": day_string, "high_temp": daily["temperature_2m_max"][i], "low_temp": daily["temperature_2m_min"][i],
                    "mean_temp": extra.get("mean_temp"), "rain_total": daily["precipitation_sum"][i], "rain_chance": daily["precipitation_probability_max"][i],
                    "max_wind": daily["wind_speed_10m_max"][i], "avg_humidity": extra.get("avg_humidity"), "avg_cloud_cover": extra.get("avg_cloud_cover"), "dewpoint": extra.get("dewpoint"),
                    "avg_wind_direction": extra.get("avg_wind_direction"),
                }
                pm_details = calculate_pm_details(day_data, multiplier, location["longitude"])
                processed_days.append((day_data, pm_details))

            # Split UI into a Main Left Box and 6 Right Sidebar blocks
            col_main, col_list = st.columns([3, 2])

            with col_main:
                # Get Day 0 (Today) for the big focus window
                today_data, today_pm = processed_days[0]
                dt = datetime.strptime(today_data["date"], "%Y-%m-%d")
                readable_date = dt.strftime("%A, %b %d")

                st.subheader(f"📅 Today's Risk Profile ({readable_date})")
                
                # Render the stylized status block
                today_pm["box_style"](
                    f"### **{today_pm['category']} Risk** — Index Score: `{today_pm['score']}/100`  \n"
                    f"**Guidance:** {today_pm['action']}"
                )

                # Summary metrics card list below
                st.markdown("#### 🔬 Atmospheric Disease Metrics")
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.metric(label="Average Humidity", value=f"{today_data['avg_humidity']}%")
                    st.metric(label="Mean Temperature", value=f"{today_data['mean_temp']}°F")
                    st.metric(label="Avg Wind Direction", value=f"{int(today_data['avg_wind_direction'])}°")
                with col_m2:
                    st.metric(label="Dew Point Spread", value=f"{today_data['dewpoint']}°F")
                    st.metric(label="Cloud Cover Coverage", value=f"{today_data['avg_cloud_cover']}%")
                    st.write(f"ℹ️ **Transmission Factor:** {today_pm['wind_note'] or 'No active wind adjustments.'}")

            with col_list:
                st.subheader("🔮 6-Day Outlook")
                # Loop through days 1 to 6
                for day_data, pm_details in processed_days[1:]:
                    dt_f = datetime.strptime(day_data["date"], "%Y-%m-%d")
                    day_lbl = dt_f.strftime("%a, %b %d")
                    
                    # Small, clean container cards for each upcoming day
                    with st.container(border=True):
                        st.markdown(f"**{day_lbl}**")
                        # Emphasize color inline
                        if pm_details["category"] == "Low":
                            lbl_color = "green"
                        elif pm_details["category"] == "Moderate":
                            lbl_color = "orange"
                        else:
                            lbl_color = "red"
                            
                        st.markdown(
                            f"Risk: :**{lbl_color}**[{pm_details['category']}] | Score: `{pm_details['score']}`"
                        )
                        st.caption(f"Temp: {day_data['mean_temp']}°F | Humid: {day_data['avg_humidity']}%")

        else:
            st.error("Invalid ZIP code selection.")

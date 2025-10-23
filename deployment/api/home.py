def home():
    import streamlit as st

    # ------------------------------
    # 1️⃣ Page Title & Introduction
    # ------------------------------
    #st.set_page_config(page_title="Patient Activity Tracking", layout="wide")
    #st.title("🩺 Patient Activity Tracking System")

    st.markdown("""
        Welcome to the **Flood Monitoring System**. 🌊
        This system uses **AI and computer vision** to monitor real-time flood conditions, such as water level detection, object tracking in the water, and early flood prediction.
        It is designed to assist emergency services and local authorities in tracking flood progression in real-time using **webcam feeds or camera URLs**.
        """)

    # ------------------------------
    # 2️⃣ Two Columns: Students + Image
    # ------------------------------
    col1, col2 = st.columns([1, 2])

    # Left Column → Student Names
    with col1:
        st.subheader("Team Members")
        students = ["GANASREE A (1AJ22CS049)", "Student 2", "Student 3"]
        for s in students:
            st.write(f"- {s}")

    # Right Column → Image/Logo
    with col2:
        st.subheader("Project Logo")
        st.image("floods/flood_10.jpg", use_container_width=True)  # replace with your image path

    st.markdown("""
---
## Real-World Context: Why AI Flood Monitoring Matters

### 1. The Challenge of Traditional Methods
Historically, flood monitoring relied on physical **river gauges** and manual reports, which are often slow, require maintenance, and can be inaccessible or destroyed during a flood. AI systems address this by offering **non-contact** measurement (via camera), providing **24/7 coverage**, and offering insights in remote or hard-to-reach areas.

### 2. Integration with IoT and Data Fusion
In practice, these AI systems are rarely standalone. They are highly effective when **fused with IoT data** from ground-based sensors.
* **Ultrasonic/Pressure Sensors:** Provide precise, numerical water level readings that supplement the visual data.
* **Rain Gauges and Weather APIs:** Feed essential rainfall and atmospheric pressure data directly into the Machine Learning prediction models to improve forecasting accuracy.

### 3. Applications Beyond Rivers
While river monitoring is common, AI systems are increasingly deployed in:
* **Urban Drainage Systems:** Monitoring water accumulation in storm drains and underpasses to prevent flash flooding on roads.
* **Roadway Safety:** Triggering alerts on **digital road signs** (e.g., "ROAD CLOSED DUE TO FLOODING") the moment a camera detects water over a critical threshold.
""")
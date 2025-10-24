import sys
import os

# Add project root (two levels up from main.py) to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)




import streamlit as st
import base64
from pathlib import Path


from deployment.api.home import home
from deployment.api.risk import risk
from src.models.prediction import pre1
from deployment.api.live import live_cam
from src.models.model import track

# --- Function to convert local file to base64 for embedding ---
def img_to_base64(img_path):
    """Converts local image to base64 string for embedding in HTML."""
    try:
        img_path_obj = Path(img_path)
        if not img_path_obj.exists():
            # Only print error if running locally and file isn't found
            # st.error(f"Error: Local image not found at '{img_path}'. Please check the file path.")
            return None

        with open(img_path, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read()).decode()
            return f"data:image/{img_path_obj.suffix.lstrip('.')};base64,{b64_string}"

    except Exception as e:
        # st.error(f"An error occurred during image conversion for {img_path}: {e}")
        return None

# !!! IMPORTANT: REPLACE THESE PATHS WITH YOUR ACTUAL LOCAL IMAGE PATHS !!!
# Ensure these files exist relative to where you run your Streamlit app.
#main="C:/Users/User/OneDrive/Documents/Flood_Monitor/floods"
LOCAL_IMAGE_PATHS = [
    
    "floods/flood_0.jpg",
    "floods/flood_1.jpg",
    "floods/flood_2.jpg",
    "floods/flood_3.jpg",
    "floods/flood_4.jpg",
    "floods/flood_5.jpg",
    "floods/flood_6.jpg",
    "floods/flood_7.jpg",
    "floods/flood_8.jpg",
    "floods/flood_9.jpg",
    "floods/flood_10.jpg",
    "floods/flood_11.jpg",
    "floods/flood_12jpg",
    "floods/flood_13.jpg",
    "floods/flood_14.jpg",
    "floods/flood_15.jpg",
    "floods/flood_16.jpg",
    "floods/flood_17.jpg",
    "floods/flood_18.jpg",
    "floods/flood_21.jpg",
    "floods/flood_22.jpg",
    "floods/flood_23.jpg",
    "floods/flood_24.jpg",
    "floods/flood_25.jpg"
]

# Process all local images into a list of Base64 URIs
b64_image_uris = [img_to_base64(p) for p in LOCAL_IMAGE_PATHS if img_to_base64(p)]


st.set_page_config(page_title="Patient Dashboard", layout="wide")

# Initialize state
if "subpage" not in st.session_state:
    st.session_state.subpage = "Home"

# --- CSS for bottom nav (Updated for functionality) ---
st.markdown(
    """
<style>
/* Remove Streamlit default padding for a cleaner look */
.block-container {
    padding-bottom: 80px !important; /* Extra space for the fixed navbar */
}
#MainMenu, footer {
    visibility: hidden;
}

/* --- STREAMLIT BUTTON OVERLAY FIX (CORE FIX) --- */
/* 1. Target the overall container for the columns (st.columns) */
.bottom-nav + div > div {
    display: flex;
    justify-content: space-around;
}

/* 2. Target the individual column container */
.bottom-nav + div > div > div {
    position: relative; /* Establish positioning context */
    min-width: 60px; 
    height: 72px; /* Set height to match the nav bar */
    display: flex; /* Helps center children */
    justify-content: center;
    align-items: center;
}

/* 3. Target the hidden Streamlit Button container (The Click Target) */
[data-testid^="stButton"] {
    position: absolute; /* Take it out of flow */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2; /* Place on top of the icon */
    opacity: 0.01; /* Virtually invisible, but still clickable */
    margin: 0 !important;
    padding: 0 !important;
}

/* 4. Target the actual button element to remove all style */
[data-testid^="stButton"] button {
    background: transparent !important;
    border: none !important;
    color: transparent !important;
    cursor: pointer;
    width: 100%;
    height: 100%;
}

/* 5. Target the custom HTML icon */
.nav-item-wrapper {
    position: absolute; /* Take it out of flow */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1; /* Place below the hidden button */
    pointer-events: none; /* CRITICAL: Allows click to pass through to the button */
    display: flex;
    justify-content: center;
    align-items: center;
}


/* --- CUSTOM CSS STYLING (YOUR ORIGINAL STYLES) --- */
.bottom-nav {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    height: 72px;
    background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(10,14,26,0.98));
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    box-shadow: 0 -6px 20px rgba(2,6,23,0.45);
}
.nav-inner {
    display: flex;
    justify-content: space-around;
    width: 100%;
    max-width: 1000px;
    position: relative;
}
.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #94a3b8;
    font-size: 12px;
    transition: all 0.25s ease;
}
.nav-item img {
    width: 25px;
    height: 25px;
    filter: invert(50%) sepia(10%) saturate(100%) hue-rotate(180deg); 
    transition: all 0.25s ease;
}

/* Hover effect: We apply the visual change when the underlying button is hovered */
[data-testid^="stButton"]:hover + .nav-item-wrapper .nav-item { 
    transform: translateY(-4px); 
    color: #e2eef1; 
}
[data-testid^="stButton"]:hover + .nav-item-wrapper .nav-item img {
      /* Green filter */
    filter: invert(58%) sepia(86%) saturate(274%) hue-rotate(110deg) brightness(95%) contrast(90%);
}

.nav-active {
    color: #00C896 !important;
    transform: translateY(-6px);
}
.nav-active img {
    filter: invert(58%) sepia(86%) saturate(274%) hue-rotate(110deg) brightness(95%) contrast(90%) !important;
}

/* --- CAROUSEL ANIMATION CSS for Home Page (Bi-Directional Flood Images) --- */

/* Container to hold the moving "tape" of images */
.flood-row-container {
    width: 100%;
    overflow: hidden; 
    margin: 30px 0;
    padding: 10px 0;
    border-radius: 12px;
    background: #0d121c; 
}

/* Base style for both tapes */
.flood-tape {
    display: flex;
    white-space: nowrap; 
    width: fit-content; 
    /* Set min-width to 200% to ensure enough content for the -50% loop */
    min-width: 200%; 
    margin-bottom: 20px; /* Space between the two moving tapes */
}

/* 1. RIGHT-TO-LEFT Animation Track */
.flood-tape-left {
    animation: moveTapeLeft 60s linear infinite;
}

/* 2. LEFT-TO-RIGHT Animation Track */
.flood-tape-right {
    animation: moveTapeRightFixed 60s linear infinite; 
}

/* Individual Flood Image Styling */
.flood-item {
    margin: 0 8px;
    height: 160px; 
    width: 280px; 
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.7);
    transition: transform 0.3s ease-in-out, border 0.3s;
    filter: brightness(0.8) grayscale(0.1); 
}

/* Pause animation and zoom/highlight on hover */
.flood-tape:hover, .flood-tape-left:hover, .flood-tape-right:hover {
    animation-play-state: paused;
}
.flood-item:hover {
    transform: scale(1.08) translateY(-5px); 
    border: 3px solid #00C896; 
    filter: brightness(1) grayscale(0); 
}

/* --- KEYFRAMES --- */

/* Animation 1: Right-to-Left (Moves negatively from 0 to -50%) */
@keyframes moveTapeLeft {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-50%); 
    }
}

/* Animation 2: Left-to-Right (Moves positively from -50% to 0) */
@keyframes moveTapeRightFixed {
    0% {
        /* Start at the negative offset (second copy is visible on the left) */
        transform: translateX(-50%); 
    }
    100% {
        /* Move back to the starting position (first copy aligns perfectly) */
        transform: translateX(0); 
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Nav items ---
nav_items = [
    ("Home", "https://img.icons8.com/ios-filled/24/00C896/home.png"),
    ("Early Prediction", "https://img.icons8.com/ios-filled/24/00C896/user-male-circle.png"), 
    ("Risk Graph", "https://img.icons8.com/ios-filled/24/00C896/bar-chart.png"),
    ("Add Camera URL", "https://img.icons8.com/ios-filled/24/00C896/camera.png"),
    ("Flood Monitor", "https://img.icons8.com/ios-filled/24/00C896/heart-monitor.png"), 
]

# --- Display nav bar ---
st.markdown('<div class="bottom-nav"><div class="nav-inner">', unsafe_allow_html=True)
st.markdown("</div></div>", unsafe_allow_html=True) # Close the inner and outer nav divs

cols = st.columns(len(nav_items))
for i, (label, icon) in enumerate(nav_items):
    active_class = "nav-active" if st.session_state.subpage == label else ""
    with cols[i]:
        # 1. THE HIDDEN STREAMLIT BUTTON (Must be created first)
        if st.button(
            "_", # Use an invisible character/text
            key=label, # Use the label as the key
        ):
            st.session_state.subpage = label

        # 2. THE VISIBLE CUSTOM ICON (Must be created second)
        st.markdown(
            f"""
            <div class="nav-item-wrapper">
                <div class="nav-item {active_class}">
                    <img src="{icon}" />
                    <div>{label.split()[0]}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- PAGE CONTENT (updates instantly) ---
st.markdown(f"<h3 style='text-align:center; margin-top:40px;'> {st.session_state.subpage}</h3>", unsafe_allow_html=True)

if st.session_state.subpage == "Home":
    #st.info("🏠 Welcome to the **Home Page** — **Real-time Flood Surveillance Dashboard**.")
    st.header("Flood Monitoring System")
    # ----------------------------------------------------
    # START: BI-DIRECTIONAL CAROUSEL WITH MULTIPLE LOCAL IMAGES
    # ----------------------------------------------------
    
    if b64_image_uris:
        # 1. Create the HTML string for one full set of images (using all different URIs)
        image_set_html = "".join([
            f'<img class="flood-item" src="{uri}" alt="Local Flood Feed {i+1}"/>'
            for i, uri in enumerate(b64_image_uris)
        ])
        
        # 2. Repeat the entire set twice for the seamless CSS loop
        tape_content = image_set_html * 1 
        
        # Use the same content for both tapes (left and right moving)
        st.markdown(f"""
        <div class="flood-row-container">
            <!-- Tape 1: Moves Right-to-Left -->
            <div class="flood-tape flood-tape-left">
                {tape_content}
            </div>
            <!-- Tape 2: Moves Left-to-Right -->
            <div class="flood-tape flood-tape-right">
                {tape_content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"""
        Cannot display image carousel. 
        Please ensure the local image paths defined in the **LOCAL_IMAGE_PATHS** list 
        at the top of the file are correct (e.g., '232.jpg' or 'images/flood.png') and the files exist.
        **Found 0 valid images.**
        """)

    # ----------------------------------------------------
    # END: BI-DIRECTIONAL CAROUSEL WITH MULTIPLE LOCAL IMAGES
    # ----------------------------------------------------

    home()

elif st.session_state.subpage == "Early Prediction":
    st.success("📈 View **early flood prediction models** and output here.")
    pre1()
elif st.session_state.subpage == "Risk Graph":
    st.warning("📊 **Risk Graph:** Visualize the current and forecasted risk levels.") 
    risk()
elif st.session_state.subpage == "Add Camera URL":
    #st.info("📷 Add and manage camera URLs.")
    #st.header("📷 Add Camera URL")
        import streamlit as st
        import requests
        import numpy as np
        import cv2
        import time

        st.title("📷 IP Camera Live Feed")

        # Input URL
        url_input = st.text_input("Enter Camera Stream URL (e.g., http://IP:8080)")
        camera_on = st.checkbox("Camera ON/OFF")

        # Placeholder
        FRAME_WINDOW = st.empty()

        if camera_on and url_input.strip() != "":
            url = url_input.strip()
            if not url.endswith("shot.jpg"):
                url = f"{url}/shot.jpg"

            # Poll camera continuously
            while camera_on:
                try:
                    img_resp = requests.get(url, timeout=5)
                    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                    frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
                    
                    if frame is not None:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        FRAME_WINDOW.image(frame)
                    else:
                        st.warning("Failed to capture frame")
                        
                    time.sleep(0.1)  # small delay for polling
                except Exception as e:
                    st.error(f"Error fetching frame: {e}")
                    break
        elif camera_on:
            st.warning("Please enter a valid URL!")





elif st.session_state.subpage == "Flood Monitor": 
    #st.info("❤️ Real-time **flood monitoring interface**.")
    track()

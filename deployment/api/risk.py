def risk():
    import streamlit as st
    import random
    from PIL import Image
    # NOTE: You MUST install the 'ultralytics' library for this code to work:
    # pip install ultralytics
    try:
        from ultralytics import YOLO
    except ImportError:
        st.error("The 'ultralytics' library is required for YOLO model integration.")
        st.error("Please install it using: pip install ultralytics")
        YOLO = None # Set to None if import fails

    #st.set_page_config(layout="centered", page_title="YOLO Percentage Display")

    st.title("YOLO Flood Risk Monitor")
    st.markdown("---")

    # ----------------------------------------------------
    # 1. MODEL LOADING (Cached for efficiency)
    # ----------------------------------------------------
    # IMPORTANT: Update 'seg.pt' if your model file is located elsewhere.
    MODEL_PATH = 'seg.pt' 
    TARGET_CLASS_NAME = 'flood' # Assuming your model detects a class named 'flood'

    @st.cache_resource
    def load_yolo_model():
        """Loads the YOLO model only once."""
        if YOLO is None:
            return None
        try:
            model = YOLO(MODEL_PATH)
            return model
        except Exception as e:
            st.error(f"Error loading YOLO model from '{MODEL_PATH}'. Ensure the file exists in the correct directory. Error: {e}")
            return None

    model = load_yolo_model()
    # ----------------------------------------------------


    # Initialize session state for the image and its associated score
    if 'uploaded_file_name' not in st.session_state:
        st.session_state.uploaded_file_name = None
    if 'flood_risk_score' not in st.session_state:
        st.session_state.flood_risk_score = None


    # --- File Uploader ---
    st.subheader("1. Upload Image for Analysis")
    uploaded_file = st.file_uploader(
        "Choose an image (JPEG, PNG) to run the flood detection model.", 
        type=["jpg", "jpeg", "png"]
    )

    # --- Button Logic ---
    #analyze_button = False
    if uploaded_file is not None:
        # If a file is uploaded, show the analysis button
        #analyze_button = st.button("Run Flood Analysis", type="primary")
        
        # If a new file is uploaded, we clear the old score to force a button click
        if st.session_state.uploaded_file_name != uploaded_file.name:
            st.session_state.flood_risk_score = None

    #analyze_button = st.button("Run Flood Analysis")

    # --- Main Logic: Triggered by Button ---
    if uploaded_file is not None:
        # Set the file name now that we are analyzing it
        st.session_state.uploaded_file_name = uploaded_file.name
        
        # ------------------------------------------------------------------
        # >>> MODEL INTEGRATION POINT <<<
        # ------------------------------------------------------------------
        if model:
            try:
                # 1. Read the uploaded file into a PIL Image object
                input_image = Image.open(uploaded_file)
                
                # 2. Run the prediction (inference)
                # Setting verbose=False suppresses console output from YOLO
                results = model.predict(input_image, verbose=False) 
                
                # 3. Extract the highest confidence score for any detected object
                new_score = 0.0
                if len(results) > 0 and results[0].boxes:
                    # Get the detection box with the highest confidence
                    best_box = results[0].boxes[results[0].boxes.conf.argmax()]
                    new_score = best_box.conf.item()
                    
                    # Optional: Check if the detected class is the TARGET_CLASS_NAME ('flood')
                    # class_id = best_box.cls.item()
                    # if model.names[class_id] != TARGET_CLASS_NAME:
                    #     new_score = 0.0 # Ignore if it's not the target class
                    
                st.session_state.flood_risk_score = new_score
                
            except Exception as e:
                st.error(f"Prediction failed. Error: {e}")
                st.session_state.flood_risk_score = 0.0 # Set to zero on failure
        
        else:
            # Fallback if model failed to load (keeping the random simulation logic here 
            # as a backup so the app doesn't crash)
            new_score = random.uniform(0.45, 0.95) 
            st.session_state.flood_risk_score = new_score
            st.warning("Using simulated score because the YOLO model failed to load.")

        st.toast(f"Analysis complete for {uploaded_file.name}!", icon="✅")


    # ------------------------------------------------------------------
    # --- Conditional Display of Results ---
    # ------------------------------------------------------------------

    if st.session_state.flood_risk_score is not None and uploaded_file is not None:
        # If a score exists for the current file, display the results
        flood_risk_score = st.session_state.flood_risk_score
        
        # --- Display Image and Prediction ---
        
        # 1. Display the uploaded image
        st.subheader("2. Image Preview")
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width="always")
        
        # 2. Process the Prediction Score
        # Ensure score is between 0 and 1 before converting
        flood_risk_score = max(0.0, min(1.0, flood_risk_score)) 
        percentage = int(flood_risk_score * 100) 

        # Determine the status based on the score
        if percentage >= 80:
            status_text = "Critical Flood Alert"
            color = "red"
        elif percentage >= 50:
            status_text = "High Risk Detected"
            color = "orange"
        else:
            status_text = "Low Risk / Clear"
            color = "green"

        st.subheader("3. Model Confidence Result")

        # Display the main metric (The exact percentage number)
        st.metric(
            label=status_text, 
            value=f"{percentage}%", 
            delta="YOLO Model Confidence Score",
            delta_color="off"
        )

        st.caption("Visual Confidence Bar")

        # Display the percentage bar (The Streamlit "Graph")
        st.progress(flood_risk_score)

        st.markdown(f"""
        <div style="margin-top: 10px; color: {color}; font-weight: bold;">
            Model Interpretation: {status_text}
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Display initial instructions
    # st.info("Upload an image file above and click 'Run Flood Analysis' to begin.")
        pass

    st.markdown("---")
    st.caption(f"Waiting for prediction from `{MODEL_PATH}`...")

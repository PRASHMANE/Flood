from src.models.alert import email
def track():
    import cv2
    from ultralytics import YOLO
    import streamlit as st
    import tempfile
    import os
    from deep_sort_realtime.deepsort_tracker import DeepSort
    import numpy as np

    # ------------------------------
    # Load Models
    # ------------------------------
    yolo_model = YOLO("seg.pt")  # YOLO flood detection model
    tracker = DeepSort(max_age=30)  # DeepSORT tracker
    tr=[]
    # ------------------------------
    # Streamlit UI
    # ------------------------------
    st.title("🌊 Flood Detection & Tracking System")
    uploaded_file = st.file_uploader("Upload video", type=["mp4", "avi"])
    use_webcam = st.checkbox("Use Webcam Instead")

    # ------------------------------
    # Helper Functions
    # ------------------------------
    def detect_and_track(frame):
        # YOLO detection
        results = yolo_model.predict(frame, save=False, conf=0.5)
        detections = []
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                cls = int(box.cls[0])
                label = r.names[cls]

                # Only track "floods"
                if label.lower() == "floods":
                    detections.append(([x1, y1, x2 - x1, y2 - y1], 0.99, label))

                    #email()
        
        # Update tracker
        tracks = tracker.update_tracks(detections, frame=frame)
        
        # Draw tracked boxes
        flood_detected = False
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            l, t, r, b = track.to_ltrb()
            cv2.rectangle(frame, (int(l), int(t)), (int(r), int(b)), (0, 255, 0), 3)
            cv2.putText(frame, f"ID {track_id}: Flood", (int(l), int(t)-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            flood_detected = True
            if track_id not in tr and flood_detected == True:
                tr.append(track_id)
                email()# ----------------------------------------------------------> sending the alert msg

        return frame, flood_detected

    def process_video(cap, frame_window):
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame, flood_detected = detect_and_track(frame)
            
            # Convert BGR → RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_window.image(frame_rgb)

        cap.release()
        cv2.destroyAllWindows()

    # ------------------------------
    # Main logic
    # ------------------------------
    if uploaded_file and use_webcam:
        if uploaded_file:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
            temp_file.close()

            cap = cv2.VideoCapture(temp_file_path)
            frame_window = st.image([])
            process_video(cap, frame_window)

            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        elif use_webcam:
            cap = cv2.VideoCapture(0)
            frame_window = st.image([])
            process_video(cap, frame_window)

    else:
        st.info("Please upload a video or enable webcam.")

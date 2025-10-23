import base64
from pathlib import Path
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
main="C:/Users/User/OneDrive/Documents/Flood_Monitor/floods"
LOCAL_IMAGE_PATHS = [
    
    f"{main}/flood_0.jpg",
    f"{main}/flood_1.jpg",
    f"{main}/flood_2.jpg",
    f"{main}/flood_3.jpg",
    f"{main}/flood_4.jpg",
   # "floods/flood_5.jpg",
   # "floods/flood_6.jpg",
   # "floods/flood_7.jpg",
   # "floods/flood_8.jpg",
    #"floods/flood_9.jpg",
    #"floods/flood_10.jpg",
    #"floods/flood_11.jpg",
    #"floods/flood_12jpg",
    #"floods/flood_13.jpg",
    #"floods/flood_14.jpg",
    #"floods/flood_15.jpg",
    #"floods/flood_16.jpg",
   # "floods/flood_17.jpg",
    #"floods/flood_18.jpg",
    ###"floods/flood_21.jpg",
   # "floods/flood_22.jpg",
    #"floods/flood_23.jpg",
   # "floods/flood_24.jpg",
    #"floods/flood_25.jpg"
]

# Process all local images into a list of Base64 URIs
#b64_image_uris = [img_to_base64(p) for p in LOCAL_IMAGE_PATHS if img_to_base64(p)]
path=f"{main}/flood_0.jpg"

res=img_to_base64(path)
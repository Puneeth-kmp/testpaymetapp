import streamlit as st
import os

def list_directory_contents(path):
    try:
        # Get the contents of the directory
        contents = os.listdir(path)
        return contents
    except FileNotFoundError:
        return ["The provided path does not exist."]
    except PermissionError:
        return ["You do not have permission to access this path."]
    except Exception as e:
        return [f"An error occurred: {e}"]

# Streamlit app interface
st.title("Windows Directory Contents Viewer")

# Input box for Windows path
path = st.text_input("Enter a Windows path:", "C:\\")

if path:
    st.subheader("Contents of the directory:")
    contents = list_directory_contents(path)
    
    # Display contents in a list format
    for item in contents:
        st.write(item)

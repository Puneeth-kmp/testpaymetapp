import streamlit as st
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

def normalize_windows_path(path_string: str) -> Path:
    """Normalize a Windows path string to a Path object"""
    # Replace potential forward slashes with backslashes
    normalized = path_string.replace('/', '\\')
    return Path(normalized)

def get_directory_contents(path: Path) -> list:
    """Get contents of a directory with proper error handling"""
    contents = []
    try:
        # Check if path exists and is a directory
        if not path.exists():
            st.error("❌ The specified path does not exist")
            return []
        if not path.is_dir():
            st.error("❌ The specified path is not a directory")
            return []
            
        # List directory contents
        for item in path.iterdir():
            try:
                stats = item.stat()
                contents.append({
                    "Name": item.name,
                    "Type": "📁 Directory" if item.is_dir() else "📄 File",
                    "Size": stats.st_size if item.is_file() else "N/A",
                    "Last Modified": datetime.fromtimestamp(stats.st_mtime)
                })
            except PermissionError:
                contents.append({
                    "Name": item.name,
                    "Type": "🚫 Access Denied",
                    "Size": "N/A",
                    "Last Modified": "N/A"
                })
                
        return contents
        
    except PermissionError:
        st.error("🚫 Permission denied. Please check your access rights.")
        return []
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        return []

def format_size(size):
    """Format file size to human-readable format"""
    if isinstance(size, (int, float)):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
    return size

# Streamlit UI
st.title("📂 Windows Directory Viewer")

# Input field with example
st.write("Paste your Windows folder path below:")
example_path = "Example: C:\\Users\\YourName\\Desktop\\YourFolder"
path_input = st.text_input("Directory Path:", placeholder=example_path)

if path_input:
    try:
        # Normalize and process the path
        path = normalize_windows_path(path_input)
        
        # Show the normalized path
        st.write("📁 Analyzing path:", str(path))
        
        # Get directory contents
        contents = get_directory_contents(path)
        
        if contents:
            # Convert to DataFrame
            df = pd.DataFrame(contents)
            
            # Format the size column
            if 'Size' in df.columns:
                df['Size'] = df['Size'].apply(format_size)
                
            # Show total items found
            st.write(f"Found {len(contents)} items in directory")
            
            # Display contents in a nice table
            st.dataframe(
                df,
                column_config={
                    "Name": st.column_config.TextColumn("Name", width="large"),
                    "Type": st.column_config.TextColumn("Type", width="medium"),
                    "Size": st.column_config.TextColumn("Size", width="medium"),
                    "Last Modified": st.column_config.DatetimeColumn("Last Modified", width="medium")
                }
            )
            
            # Add export option
            if st.button("Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"directory_contents_{path.name}.csv",
                    mime="text/csv"
                )
                
    except Exception as e:
        st.error(f"❌ Error processing path: {str(e)}")

# Help section
with st.expander("ℹ️ Help"):
    st.markdown("""
    ### How to use:
    1. Copy your Windows folder path
    2. Paste it in the input box above
    3. The contents will be displayed automatically
    
    ### Tips:
    - Make sure you have permission to access the folder
    - The path should be a valid Windows directory path
    - You can export the results to CSV using the export button
    """)

import streamlit as st
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
from tkinter import filedialog
import tkinter as tk
import platform

def select_folder():
    """Open folder selection dialog"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Set attributes for dialog to stay on top
    root.attributes('-topmost', True)
    
    # Open folder selection dialog
    folder_path = filedialog.askdirectory(
        title='Select Folder to View',
        parent=root
    )
    
    return folder_path if folder_path else None

def get_directory_contents(path: Path) -> list:
    """Get contents of a directory with proper error handling"""
    contents = []
    try:
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
st.title("📂 Local Directory Viewer")
st.write("This app will help you view contents of folders on your computer.")

# Add a button to trigger folder selection
if st.button("Browse Folders"):
    try:
        # Get selected folder path
        folder_path = select_folder()
        
        if folder_path:
            # Store the path in session state
            st.session_state['selected_path'] = folder_path
            st.experimental_rerun()
            
    except Exception as e:
        st.error(f"Error opening folder dialog: {str(e)}")
        st.info("If you're running this in a browser, make sure to allow pop-ups and file system access.")

# If path is in session state, show contents
if 'selected_path' in st.session_state:
    path = Path(st.session_state['selected_path'])
    st.write("📁 Selected folder:", str(path))
    
    # Get and display contents
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

# Important notes for users
st.info("""
### Important Notes:
1. This app needs permission to access your local files
2. When you click 'Browse Folders', a folder selection dialog will open
3. Select the folder you want to view
4. The app will only access folders you explicitly choose
""")

# Help section
with st.expander("ℹ️ Help & Troubleshooting"):
    st.markdown("""
    ### If the folder dialog doesn't appear:
    1. Make sure pop-ups are allowed in your browser
    2. Check if your browser allows file system access
    3. Try clicking the 'Browse Folders' button again
    
    ### Security Notes:
    - The app only accesses folders you explicitly select
    - No data is stored or transmitted to any external servers
    - You can see exactly which folder is being accessed above the file list
    
    ### Tips:
    - Use the export feature to save the directory listing as CSV
    - You can browse different folders by clicking 'Browse Folders' again
    """)

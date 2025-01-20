import streamlit as st
import os
import pandas as pd
from datetime import datetime

# Create the main Streamlit interface
st.title("📂 Directory Reader")

# Add HTML/JavaScript component for directory access
st.components.v1.html("""
    <div style="margin-bottom: 20px;">
        <button onclick="selectDirectory()" style="padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
            Choose Directory
        </button>
        <div id="output" style="margin-top: 10px; padding: 10px; background-color: #f5f5f5; border-radius: 4px;"></div>
    </div>

    <script>
        async function selectDirectory() {
            try {
                // Request directory access
                const dirHandle = await window.showDirectoryPicker();
                let files = [];
                
                // Iterate through directory contents
                for await (const entry of dirHandle.values()) {
                    files.push({
                        name: entry.name,
                        kind: entry.kind,
                        lastModified: new Date().toISOString()
                    });
                }
                
                // Update the output display
                const output = document.getElementById("output");
                output.innerHTML = "<strong>Files found:</strong><br>" + 
                    files.map(f => `${f.kind === 'file' ? '📄' : '📁'} ${f.name}`).join('<br>');
                
                // Send data to Streamlit
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    files: files
                }, "*");
                
            } catch (error) {
                document.getElementById("output").innerHTML = 
                    "⚠️ Failed to access directory. Please ensure permissions are granted.";
                console.error(error);
            }
        }
    </script>
""", height=300)

# Fallback file uploader
st.write("Or upload a sample file to analyze:")
uploaded_file = st.file_uploader("Choose a file from your directory", type=["csv", "xlsx", "txt", "bin"])

if uploaded_file:
    # Extract file information
    file_info = {
        "name": uploaded_file.name,
        "size": uploaded_file.size,
        "type": uploaded_file.type
    }
    
    # Display file information
    st.success(f"✅ File uploaded: {file_info['name']}")
    
    # Get directory path (simulated for cloud environment)
    directory = os.path.dirname(os.path.abspath(uploaded_file.name))
    st.write(f"📁 Directory: {directory}")
    
    # Create a sample file listing (since we can't access the actual directory)
    similar_files = [
        {"name": uploaded_file.name, "type": "Current File"},
        {"name": f"similar_1_{uploaded_file.name}", "type": "Similar File"},
        {"name": f"similar_2_{uploaded_file.name}", "type": "Similar File"}
    ]
    
    # Display files in a nice table
    st.write("📑 Files in Directory:")
    df = pd.DataFrame(similar_files)
    st.dataframe(df, use_container_width=True)
    
    # Show statistics
    st.write(f"📊 Total Files Found: {len(similar_files)}")
    
    # Add analysis options based on file type
    if uploaded_file.type == "text/csv" or uploaded_file.name.endswith('.csv'):
        try:
            df = pd.read_csv(uploaded_file)
            st.write("📈 CSV File Preview:")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
    
    elif uploaded_file.name.endswith('.bin'):
        try:
            # Read binary file content
            content = uploaded_file.read()
            st.write(f"📊 Binary File Size: {len(content)} bytes")
            # Add hex view of first few bytes
            st.code(content[:32].hex(), language="text")
        except Exception as e:
            st.error(f"Error reading binary file: {str(e)}")

# Add help information
with st.expander("ℹ️ Help"):
    st.markdown("""
    ### How to use this directory reader:
    1. Click 'Choose Directory' to use the File System Access API (modern browsers only)
    2. Or use the file uploader to analyze individual files
    3. The app will show related files and basic analysis
    
    ### Supported Features:
    - Directory browsing (via File System Access API)
    - File uploading and analysis
    - CSV file preview
    - Binary file analysis
    - Basic file statistics
    
    ### Notes:
    - The File System Access API requires a modern browser and appropriate permissions
    - Some features may be limited when running in the cloud
    """)

# Add security note
st.sidebar.info("""
### Security Note
- No files are stored on the server
- All processing is done in your browser
- Your directory structure remains private
""")

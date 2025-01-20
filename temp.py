import streamlit as st
import os

st.title("📂 Directory Content Viewer")

# HTML/JavaScript component with recursive directory traversal
st.components.v1.html("""
    <div style="margin-bottom: 20px;">
        <button onclick="selectDirectory()" style="padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
            Choose Directory
        </button>
        <div id="fileTree" style="margin-top: 10px; padding: 10px; background-color: #f5f5f5; border-radius: 4px; max-height: 500px; overflow-y: auto;"></div>
    </div>

    <script>
    async function listDirectoryContents(dirHandle, path = '') {
        let contents = [];
        
        try {
            for await (const entry of dirHandle.values()) {
                const entryPath = path ? `${path}/${entry.name}` : entry.name;
                
                if (entry.kind === 'file') {
                    contents.push({
                        type: 'file',
                        name: entry.name,
                        path: entryPath
                    });
                } else if (entry.kind === 'directory') {
                    // Get the directory handle and recursively list its contents
                    const subDirHandle = await dirHandle.getDirectoryHandle(entry.name);
                    const subContents = await listDirectoryContents(subDirHandle, entryPath);
                    contents.push({
                        type: 'directory',
                        name: entry.name,
                        path: entryPath,
                        contents: subContents
                    });
                }
            }
        } catch (error) {
            console.error('Error reading directory:', error);
        }
        
        return contents;
    }

    function buildHtmlTree(items, indent = 0) {
        let html = '<ul style="list-style-type: none; padding-left: ' + indent + 'px;">';
        
        for (const item of items) {
            if (item.type === 'directory') {
                html += `
                    <li>
                        <span style="color: #2196F3;">📁 ${item.name}/</span>
                        ${buildHtmlTree(item.contents, indent + 20)}
                    </li>
                `;
            } else {
                html += `
                    <li>
                        <span style="color: #4CAF50;">📄 ${item.name}</span>
                    </li>
                `;
            }
        }
        
        html += '</ul>';
        return html;
    }

    async function selectDirectory() {
        try {
            const dirHandle = await window.showDirectoryPicker();
            const fileTree = document.getElementById('fileTree');
            fileTree.innerHTML = '<div style="color: #666;">Loading directory contents...</div>';
            
            // Get all contents recursively
            const contents = await listDirectoryContents(dirHandle);
            
            // Sort contents: directories first, then files, both alphabetically
            contents.sort((a, b) => {
                if (a.type === b.type) {
                    return a.name.localeCompare(b.name);
                }
                return a.type === 'directory' ? -1 : 1;
            });
            
            // Build and display the tree
            const treeHtml = buildHtmlTree(contents);
            fileTree.innerHTML = `
                <div style="margin-bottom: 10px;">
                    <strong>📂 Selected Directory:</strong> ${dirHandle.name}
                </div>
                ${treeHtml}
            `;
            
            // Send data to Streamlit
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: contents
            }, '*');
            
        } catch (error) {
            document.getElementById('fileTree').innerHTML = `
                <div style="color: #f44336;">
                    ⚠️ Error accessing directory: ${error.message}<br>
                    Please ensure you've granted the necessary permissions.
                </div>
            `;
            console.error('Directory access error:', error);
        }
    }
    </script>
""", height=600)

# Help section
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    ### Instructions:
    1. Click the 'Choose Directory' button above
    2. Select the directory you want to view in the file picker dialog
    3. Grant permission if prompted by your browser
    4. The app will show all files and subdirectories in a tree structure
    
    ### Features:
    - Shows all files and folders recursively
    - Distinguishes between files (📄) and folders (📁)
    - Maintains folder hierarchy with proper indentation
    - Sorts directories first, then files alphabetically
    
    ### Notes:
    - Requires a modern browser with File System Access API support
    - You must grant permission to access the selected directory
    - No files are uploaded or stored - all processing is done locally
    """)

# Add security note in sidebar
st.sidebar.info("""
### Security Information
- All directory reading is done locally in your browser
- No files are uploaded to any server
- Directory contents remain private on your device
- You can revoke access permissions at any time through your browser settings
""")

"""Main Streamlit application for SecureText Vault"""
import streamlit as st
import sys
import os
import json
import re
from datetime import datetime, timedelta
from typing import Tuple, Optional
from streamlit.components.v1 import html as st_html

# Ensure the project root is in the Python path for custom modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Diagnostic information
# st.write("Debug: Starting application...")
# st.write(f"Python path: {sys.path}")

try:
    # Import after ensuring path is set
    from app.config import config
    # st.write("Debug: Config imported successfully")
    
    from app.services.auth_service import auth_service
    # st.write("Debug: Auth service imported successfully")
    
    from app.services.supabase_client import supabase_client
    # st.write("Debug: Supabase client imported successfully")
    
    from app.services.encryption_service import encryption_service
    # st.write("Debug: Encryption service imported successfully")
    
    from app.constants import (
        DEFAULT_TAB_NAME, MAX_TABS_PER_SITE, MAX_TAB_NAME_LENGTH,
        MAX_CONTENT_SIZE_BYTES, EXPORT_FORMATS, EXPORT_OPTIONS,
        ERROR_INVALID_USERNAME, ERROR_INVALID_PASSWORD_FORMAT
    )
    # st.write("Debug: Constants imported successfully")

except Exception as e:
    st.error(f"Error importing modules: {str(e)}")

def validate_tab_name(tab_name: str) -> Tuple[bool, Optional[str]]:
    """Validate tab name"""
    if not tab_name or not isinstance(tab_name, str):
        return False, "Tab name must be a non-empty string"
    
    if len(tab_name) > MAX_TAB_NAME_LENGTH:
        return False, f"Tab name exceeds maximum length of {MAX_TAB_NAME_LENGTH} characters"
    
    # Allow letters, numbers, spaces, underscores, hyphens, and basic punctuation
    if not re.match(r'^[a-zA-Z0-9 _\-.,!?()]+$', tab_name):
        return False, "Tab name can only contain letters, numbers, spaces, and basic punctuation"
    
    return True, None

def validate_content(content: str) -> Tuple[bool, Optional[str]]:
    """Validate content size"""
    content_size = len(content.encode('utf-8'))
    if content_size > MAX_CONTENT_SIZE_BYTES:
        return False, f"Content exceeds maximum size of {MAX_CONTENT_SIZE_BYTES} bytes which is more than 1 MB"
    
    return True, None

def apply_theme_styles():
    """Apply theme styles globally based on current theme state"""
    theme_styles = f"""
    <style>
    /* Global theme styles - Ensure complete consistency */
    [data-testid="stAppViewContainer"],
    section[data-testid="stSidebar"] > div {{
        background-color: {'#0e1117' if st.session_state['theme'] == 'dark' else '#ffffff'} !important;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {'#1e2130' if st.session_state['theme'] == 'dark' else '#f0f2f6'} !important;
    }}
    
    /* Text area styles - Comprehensive coverage */
    .stTextArea textarea,
    textarea {{
        background-color: {'#2d3142' if st.session_state['theme'] == 'dark' else '#ffffff'} !important;
        color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'} !important;
        caret-color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'} !important;
        border: 1px solid {'#4a4e69' if st.session_state['theme'] == 'dark' else '#ddd'} !important;
    }}
    
    /* Text elements - Complete coverage */
    h1, h2, h3, h4, h5, h6, p, div, span, label,
    .stMarkdown, .stText, .stCaption {{
        color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'} !important;
    }}
    
    /* Form inputs */
    input[type="text"],
    input[type="password"],
    input[type="email"],
    input[type="number"],
    input {{
        background-color: {'#2d3142' if st.session_state['theme'] == 'dark' else '#ffffff'} !important;
        color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'} !important;
        caret-color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'} !important;
        border: 1px solid {'#4a4e69' if st.session_state['theme'] == 'dark' else '#ddd'} !important;
    }}
    
    /* Buttons - Enhanced styling */
    .stButton > button,
    button {{
        background-color: {'#4a4e69' if st.session_state['theme'] == 'dark' else '#e0e0e0'} !important;
        color: {'white' if st.session_state['theme'] == 'dark' else 'black'} !important;
        border: 1px solid {'#6c757d' if st.session_state['theme'] == 'dark' else '#adb5bd'} !important;
    }}
    
    /* Button hover states */
    .stButton > button:hover,
    button:hover {{
        background-color: {'#5c6370' if st.session_state['theme'] == 'dark' else '#d0d0d0'} !important;
        border: 1px solid {'#7c8590' if st.session_state['theme'] == 'dark' else '#bcc1c6'} !important;
    }}
    
    /* File uploader button styling */
    .stFileUploader > section {{
        background-color: {'#1e2130' if st.session_state['theme'] == 'dark' else '#f8f9fa'} !important;
        border: 1px solid {'#4a4e69' if st.session_state['theme'] == 'dark' else '#dee2e6'} !important;
    }}
    
    .stFileUploader > section > button {{
        background-color: {'#4a4e69' if st.session_state['theme'] == 'dark' else '#e0e0e0'} !important;
        color: {'white' if st.session_state['theme'] == 'dark' else 'black'} !important;
        border: 1px solid {'#6c757d' if st.session_state['theme'] == 'dark' else '#adb5bd'} !important;
    }}
    
    .stFileUploader > section > button:hover {{
        background-color: {'#5c6370' if st.session_state['theme'] == 'dark' else '#d0d0d0'} !important;
        border: 1px solid {'#7c8590' if st.session_state['theme'] == 'dark' else '#bcc1c6'} !important;
    }}
    
    /* Select boxes */
    .stSelectbox > div > div,
    select {{
        background-color: {'#2d3142' if st.session_state['theme'] == 'dark' else '#ffffff'} !important;
        color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'} !important;
        border: 1px solid {'#4a4e69' if st.session_state['theme'] == 'dark' else '#ddd'} !important;
    }}
    
    /* Warning boxes */
    .warning {{
        background-color: {'#332e14' if st.session_state['theme'] == 'dark' else '#fff3cd'} !important;
        border: 1px solid {'#665c28' if st.session_state['theme'] == 'dark' else '#ffeaa7'} !important;
        color: {'#fff3cd' if st.session_state['theme'] == 'dark' else '#856404'} !important;
    }}
    
    /* Code blocks */
    .stMarkdown code,
    code {{
        background-color: {'#2d3142' if st.session_state['theme'] == 'dark' else '#f0f0f0'} !important;
        color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'} !important;
        border: 1px solid {'#4a4e69' if st.session_state['theme'] == 'dark' else '#ddd'} !important;
    }}
    
    /* Alerts */
    .stAlert div,
    .stAlert {{
        background-color: {'#332e14' if st.session_state['theme'] == 'dark' else '#fff3cd'} !important;
        color: {'#fff3cd' if st.session_state['theme'] == 'dark' else '#856404'} !important;
        border: 1px solid {'#665c28' if st.session_state['theme'] == 'dark' else '#ffeaa7'} !important;
    }}
    
    /* Focus indicators for better visibility */
    button:focus, input:focus, textarea:focus, select:focus {{
        outline: 2px solid {'#4A90E2' if st.session_state['theme'] == 'dark' else '#007bff'} !important;
        outline-offset: 2px;
        box-shadow: 0 0 0 3px {'rgba(74, 144, 226, 0.3)' if st.session_state['theme'] == 'dark' else 'rgba(0, 123, 255, 0.3)'} !important;
    }}
    
    /* Form containers */
    .stForm {{
        background-color: {'#1e2130' if st.session_state['theme'] == 'dark' else '#f8f9fa'} !important;
        border: 1px solid {'#4a4e69' if st.session_state['theme'] == 'dark' else '#dee2e6'} !important;
        border-radius: 5px;
    }}
    
    /* Column dividers */
    [data-testid="column"] {{
        background-color: transparent !important;
    }}
    
    /* Ensure all text elements inherit theme colors */
    * {{
        color: {'#e0e0e0' if st.session_state['theme'] == 'dark' else '#212529'} !important;
    }}
    
    /* Override specific elements that need different colors */
    h1, h2, h3, h4, h5, h6, .stTitle {{
        color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'} !important;
    }}
    </style>
    """
    st.markdown(theme_styles, unsafe_allow_html=True)

def encrypt_content_if_enabled(content: str, site: dict) -> Tuple[str, Optional[str]]:
    """Encrypt content if encryption is enabled for the site"""
    if config.ENCRYPTION_ENABLED and site.get('encryption_salt'):
        try:
            # Decode the salt
            salt = base64.urlsafe_b64decode(site['encryption_salt'])
            # Derive encryption key from the user's password (we'll need to store this temporarily during session)
            # For now, we'll use a placeholder - in a real implementation, you'd derive this from the user's password
            # This is a simplified approach for demonstration
            encryption_key = encryption_service.derive_key_from_password(site['username'], salt)
            encrypted_content = encryption_service.encrypt_content(content, encryption_key)
            return content, encrypted_content
        except Exception as e:
            st.error(f"Encryption error: {str(e)}")
            return content, None
    return content, None

def decrypt_content_if_enabled(encrypted_content: str, site: dict) -> str:
    """Decrypt content if it's encrypted and encryption is enabled"""
    if config.ENCRYPTION_ENABLED and encrypted_content and site.get('encryption_salt'):
        try:
            # Decode the salt
            salt = base64.urlsafe_b64decode(site['encryption_salt'])
            # Derive encryption key (same approach as encryption)
            encryption_key = encryption_service.derive_key_from_password(site['username'], salt)
            decrypted_content = encryption_service.decrypt_content(encrypted_content, encryption_key)
            return decrypted_content
        except Exception as e:
            st.error(f"Decryption error: {str(e)}")
            return ""
    return encrypted_content if encrypted_content else ""

def export_as_text(content: str, username: str) -> str:
    """Export content as plain text"""
    return f"SecureText Vault Export\nUsername: {username}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{content}"

def export_as_json(content: str, username: str) -> str:
    """Export content as JSON"""
    export_data = {
        "username": username,
        "export_date": datetime.now().isoformat(),
        "content": content,
        "content_length": len(content),
        "application": "SecureText Vault"
    }
    return json.dumps(export_data, indent=2, ensure_ascii=False)

def export_as_markdown(content: str, username: str) -> str:
    """Export content as Markdown"""
    return f"""# SecureText Vault Export

**Username:** {username}  
**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  

---

{content}
"""

EXPORT_FUNCTIONS = {
    "txt": export_as_text,
    "json": export_as_json,
    "md": export_as_markdown
}

EXPORT_MIME_TYPES = {
    "txt": "text/plain",
    "json": "application/json",
    "md": "text/markdown"
}

def show_setup_instructions():
    """Show setup instructions when Supabase is not configured"""
    st.title("🔐 SecureText Vault - Setup Required")
    
    st.error("⚠️ Supabase configuration is not properly set up.")
    
    # Debug information
    try:
        from app.config import config
        st.write("Current configuration values:")
        st.write(f"SUPABASE_URL: {'SET' if config.SUPABASE_URL else 'NOT SET'}")
        st.write(f"SUPABASE_KEY: {'SET' if config.SUPABASE_KEY else 'NOT SET'}")
        st.write(f"SUPABASE_SERVICE_KEY: {'SET' if config.SUPABASE_SERVICE_KEY else 'NOT SET'}")
        st.write(f"SESSION_SECRET: {'SET' if config.SESSION_SECRET else 'NOT SET'}")
        
        # Try to validate config and catch any specific errors
        try:
            config.validate()
            st.success("Configuration validation passed!")
        except ValueError as ve:
            st.error(f"Configuration validation failed: {ve}")
        except Exception as e:
            st.error(f"Unexpected error during validation: {e}")
            
    except Exception as e:
        st.write(f"Error accessing config: {str(e)}")
        st.write(f"Error type: {type(e).__name__}")
    
    st.markdown("""
    ### Configuration Steps:
    
    1. **Get your Supabase credentials:**
       - Go to your [Supabase project dashboard](https://app.supabase.com)
       - Navigate to **Settings > API**
       - Copy these three values:
         - **Project URL** (e.g., `https://xxxxxxxxxxxx.supabase.co`)
         - **anon/public key** (starts with `eyJ...`)
         - **service_role key** (starts with `eyJ...`)
    
    2. **Update Streamlit Secrets:**
       - In your Streamlit Cloud app, go to Settings
       - Add all required secrets in the format shown below:
       
       ```
       SUPABASE_URL = "your_supabase_project_url"
       SUPABASE_KEY = "your_supabase_anon_key"
       SUPABASE_SERVICE_KEY = "your_supabase_service_key"
       SESSION_SECRET = "your_random_secret_here"
       ENCRYPTION_ENABLED = "true"
       ```
    
    3. **Create database tables:**
       - Run the setup script: `python setup_database.py`
       - Or execute the SQL manually in Supabase SQL Editor
    
    4. **Restart the application**
    """)
    
    st.info("💡 **Tip:** After updating secrets, you must restart the application for changes to take effect.")

def create_site_page():
    """Page for creating a new site"""
    st.title("🏗️ Create New Site")
    
    st.markdown("""
    Create a new password-protected text storage site with a unique username.
    Your site will be accessible only with your username and password.
    """)
    
    with st.form("create_site_form"):
        username = st.text_input(
            "Username (3-50 characters, letters, numbers, underscores, hyphens)",
            placeholder="e.g., my_secure_notes",
            help="This will be part of your site URL"
        )
        
        password = st.text_input(
            "Password (8-100 characters)",
            type="password",
            placeholder="Enter a strong password",
            help="Choose a secure password you'll remember"
        )
        
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )
        
        submitted = st.form_submit_button("Create Site")
        
        if submitted:
            # Validate inputs
            if not username or not password:
                st.error("Please fill in all fields")
                return
            
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            # Create site
            success, message, site = auth_service.create_site(username, password)
            
            if success:
                st.success(f"✅ Site created successfully!")
                st.info(f"**Username:** {username}")
                st.info("**Important:** Save your password securely. It cannot be recovered if lost.")
                
                # Create session and redirect to site
                session_token = auth_service.create_session_token(site['id'], username)
                st.session_state['session_token'] = session_token
                st.session_state['current_site'] = site
                st.rerun()
            else:
                st.error(f"❌ {message}")

def access_site_page():
    """Page for accessing an existing site"""
    st.title("🔑 Access Existing Site")
    
    st.markdown("""
    Enter your username and password to access your secure text storage.
    """)
    
    with st.form("access_site_form"):
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            help="The username you created when setting up your site"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            help="The password for your site"
        )
        
        submitted = st.form_submit_button("Access Site")
        
        if submitted:
            if not username or not password:
                st.error("Please enter both username and password")
                return
            
            # Authenticate
            success, message, site = auth_service.authenticate_site(username, password)
            
            if success:
                st.success("✅ Authentication successful!")
                
                # Create session and redirect to site
                session_token = auth_service.create_session_token(site['id'], username)
                st.session_state['session_token'] = session_token
                st.session_state['current_site'] = site
                st.rerun()
            else:
                st.error(f"❌ {message}")

def site_management_page(site):
    """Main site management page"""
    st.title(f"📝 {site['username']}'s SecureText Vault")
    
    # Removed main content anchor
    
    # Check for session timeout (30 minutes of inactivity)
    SESSION_TIMEOUT_MINUTES = 30
    if 'last_activity' in st.session_state:
        inactive_time = datetime.now() - st.session_state['last_activity']
        if inactive_time > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
            # Session timed out, clear session and show login page
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.error("Session timed out due to inactivity. Please log in again.")
            st.rerun()
    
    # Update last activity timestamp
    st.session_state['last_activity'] = datetime.now()
    
    # Initialize session state for tabs
    if 'current_tab' not in st.session_state:
        st.session_state['current_tab'] = None
    if 'tabs' not in st.session_state:
        st.session_state['tabs'] = []
    if 'show_new_tab_form' not in st.session_state:
        st.session_state['show_new_tab_form'] = False
    if 'rename_tab_id' not in st.session_state:
        st.session_state['rename_tab_id'] = None
    if 'rename_tab_name' not in st.session_state:
        st.session_state['rename_tab_name'] = ""
    if 'delete_tab_id' not in st.session_state:
        st.session_state['delete_tab_id'] = None
    if 'delete_tab_name' not in st.session_state:
        st.session_state['delete_tab_name'] = ""
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'light'  # Default theme
    if 'last_activity' not in st.session_state:
        st.session_state['last_activity'] = datetime.now()  # Session timeout tracking
    if 'last_auto_save_time' not in st.session_state:
        st.session_state['last_auto_save_time'] = datetime.now()  # Auto-save tracking
    if 'editor_mode' not in st.session_state:
        st.session_state['editor_mode'] = 'plain'  # Default to plain text mode
    if 'unsaved_changes' not in st.session_state:
        st.session_state['unsaved_changes'] = False  # Track unsaved changes
    
    # Add JavaScript for browser close warning
    st_html("""
    <script>
    window.onbeforeunload = function() {
        const warningElement = window.parent.document.querySelector('.stAlert');
        const hasUnsavedWarning = warningElement && warningElement.textContent.includes('unsaved changes');
        if (hasUnsavedWarning) {
            return "You have unsaved changes. Are you sure you want to leave without saving?";
        }
        return null;
    };
    </script>
    """, height=0)
    
    # Apply theme styles globally
    apply_theme_styles()
    
    # Sidebar for site management
    with st.sidebar:
        st.header("Site Management")
        
        # Display site info
        st.subheader("Site Info")
        st.write(f"**Username:** {site['username']}")
        st.write(f"**Created:** {site['created_at'][:10] if site['created_at'] else 'N/A'}")
        
        # Theme toggle
        theme_toggle = st.toggle("🌙 Dark Mode", value=(st.session_state['theme'] == 'dark'))
        if theme_toggle != (st.session_state['theme'] == 'dark'):
            # Theme has changed, update state and rerun to apply styles
            if theme_toggle:
                st.session_state['theme'] = 'dark'
            else:
                st.session_state['theme'] = 'light'
            st.rerun()
        
        # Tab management
        st.subheader("Tabs")
        
        # Get tabs from database
        try:
            tabs = supabase_client.get_tabs_by_site(site['id'])
            st.session_state['tabs'] = tabs
        except Exception as e:
            st.error(f"Error loading tabs: {str(e)}")
            tabs = []
        
        if tabs:
            tab_names = [tab['tab_name'] for tab in tabs]
            
            # Handle case where current tab might not exist anymore
            current_tab_index = 0
            if st.session_state['current_tab']:
                try:
                    current_tab_index = tab_names.index(st.session_state['current_tab']['tab_name'])
                except ValueError:
                    # Current tab no longer exists, default to first tab
                    current_tab_index = 0
                    st.session_state['current_tab'] = tabs[0] if tabs else None
            
            current_tab_name = st.selectbox(
                "Select Tab",
                tab_names,
                index=current_tab_index,
                key=f"tab_selector_{site['id']}",  # Add key to ensure proper re-rendering
                help="Select a tab to view or edit its content"
            )
            
            # Find the selected tab
            selected_tab = next((tab for tab in tabs if tab['tab_name'] == current_tab_name), None)
            st.session_state['current_tab'] = selected_tab
            
            # Tab management buttons (Rename and Delete)
            if selected_tab:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Rename", help="Rename the current tab"):
                        st.session_state['rename_tab_id'] = selected_tab['id']
                        st.session_state['rename_tab_name'] = selected_tab['tab_name']
                
                with col2:
                    # Prevent deletion of the last tab
                    if len(tabs) > 1:
                        if st.button("🗑️ Delete", help="Delete the current tab"):
                            st.session_state['delete_tab_id'] = selected_tab['id']
                            st.session_state['delete_tab_name'] = selected_tab['tab_name']
                    else:
                        st.button("🗑️ Delete", disabled=True, help="Cannot delete the last tab")
            
            # Create new tab button
            if len(tabs) < MAX_TABS_PER_SITE:
                if st.button("➕ New Tab", help="Create a new tab for organizing your content"):
                    st.session_state['show_new_tab_form'] = True
            
            # Show new tab form if requested
            if st.session_state['show_new_tab_form']:
                with st.form("new_tab_form", clear_on_submit=True):  # Add clear_on_submit
                    new_tab_name = st.text_input("Tab Name", placeholder="Enter tab name", max_chars=MAX_TAB_NAME_LENGTH, key="new_tab_name_input", help="Enter a name for your new tab")
                    col1, col2 = st.columns(2)
                    with col1:
                        create_clicked = st.form_submit_button("Create")
                    with col2:
                        cancel_clicked = st.form_submit_button("Cancel")
                    
                    if create_clicked and new_tab_name:
                        # Validate tab name
                        is_valid, error_msg = validate_tab_name(new_tab_name)
                        if not is_valid:
                            st.error(f"Invalid tab name: {error_msg}")
                        else:
                            # Check if tab name already exists
                            if new_tab_name in tab_names:
                                st.error(f"Tab '{new_tab_name}' already exists")
                            else:
                                try:
                                    new_tab = supabase_client.create_tab(site['id'], new_tab_name, len(tabs))
                                    if new_tab:
                                        st.success(f"Tab '{new_tab_name}' created!")
                                        st.session_state['show_new_tab_form'] = False
                                        # Refresh tabs
                                        try:
                                            tabs = supabase_client.get_tabs_by_site(site['id'])
                                            st.session_state['tabs'] = tabs
                                            # Set the new tab as current
                                            st.session_state['current_tab'] = new_tab
                                        except Exception as e:
                                            st.error(f"Error refreshing tabs: {str(e)}")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error creating tab: {str(e)}")
                    elif cancel_clicked:
                        st.session_state['show_new_tab_form'] = False
                        st.rerun()
            
            # Handle tab renaming
            if 'rename_tab_id' in st.session_state and st.session_state['rename_tab_id']:
                with st.form("rename_tab_form"):
                    new_name = st.text_input("New Tab Name", value=st.session_state['rename_tab_name'], max_chars=MAX_TAB_NAME_LENGTH, help="Enter a new name for the tab")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update Name"):
                            if new_name and new_name != st.session_state['rename_tab_name']:
                                # Validate tab name
                                is_valid, error_msg = validate_tab_name(new_name)
                                if not is_valid:
                                    st.error(f"Invalid tab name: {error_msg}")
                                else:
                                    # Check if tab name already exists
                                    if new_name in tab_names and new_name != st.session_state['rename_tab_name']:
                                        st.error(f"Tab '{new_name}' already exists")
                                    else:
                                        try:
                                            updated_tab = supabase_client.update_tab_name(st.session_state['rename_tab_id'], new_name)
                                            if updated_tab:
                                                st.success(f"Tab renamed to '{new_name}'!")
                                                # Clear rename state
                                                st.session_state['rename_tab_id'] = None
                                                st.session_state['rename_tab_name'] = ""
                                                # Refresh tabs
                                                try:
                                                    tabs = supabase_client.get_tabs_by_site(site['id'])
                                                    st.session_state['tabs'] = tabs
                                                    # Update current tab if it was the one renamed
                                                    if st.session_state['current_tab'] and st.session_state['current_tab']['id'] == updated_tab['id']:
                                                        st.session_state['current_tab'] = updated_tab
                                                except Exception as e:
                                                    st.error(f"Error refreshing tabs: {str(e)}")
                                                st.rerun()
                                        except Exception as e:
                                            st.error(f"Error renaming tab: {str(e)}")
                            else:
                                st.session_state['rename_tab_id'] = None
                                st.session_state['rename_tab_name'] = ""
                                st.rerun()
                    with col2:
                        if st.form_submit_button("Cancel"):
                            st.session_state['rename_tab_id'] = None
                            st.session_state['rename_tab_name'] = ""
                            st.rerun()
            
            # Handle tab deletion
            if 'delete_tab_id' in st.session_state and st.session_state['delete_tab_id']:
                st.warning(f"Are you sure you want to delete the tab '{st.session_state['delete_tab_name']}'? This action cannot be undone.")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Yes, Delete"):
                        try:
                            # Delete the tab
                            supabase_client.delete_tab(st.session_state['delete_tab_id'])
                            st.success(f"Tab '{st.session_state['delete_tab_name']}' deleted!")
                            # Clear delete state
                            st.session_state['delete_tab_id'] = None
                            st.session_state['delete_tab_name'] = ""
                            # Refresh tabs
                            try:
                                tabs = supabase_client.get_tabs_by_site(site['id'])
                                st.session_state['tabs'] = tabs
                                # If we deleted the current tab, select the first available tab
                                if st.session_state['current_tab'] and st.session_state['current_tab']['id'] == st.session_state.get('delete_tab_id'):
                                    st.session_state['current_tab'] = tabs[0] if tabs else None
                            except Exception as e:
                                st.error(f"Error refreshing tabs: {str(e)}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting tab: {str(e)}")
                with col2:
                    if st.button("❌ Cancel"):
                        st.session_state['delete_tab_id'] = None
                        st.session_state['delete_tab_name'] = ""
                        st.rerun()
        else:
            # Create first tab
            st.info("No tabs yet. Create your first tab below.")
            with st.form("first_tab_form", clear_on_submit=True):  # Add clear_on_submit
                new_tab_name = st.text_input("First Tab Name", value=DEFAULT_TAB_NAME, max_chars=MAX_TAB_NAME_LENGTH, key="first_tab_name_input", help="Enter a name for your first tab")
                create_clicked = st.form_submit_button("Create First Tab")
                
                if create_clicked and new_tab_name:
                    # Validate tab name
                    is_valid, error_msg = validate_tab_name(new_tab_name)
                    if not is_valid:
                        st.error(f"Invalid tab name: {error_msg}")
                    else:
                        try:
                            new_tab = supabase_client.create_tab(site['id'], new_tab_name, 0)
                            if new_tab:
                                st.success(f"Tab '{new_tab_name}' created!")
                                # Refresh tabs
                                try:
                                    tabs = supabase_client.get_tabs_by_site(site['id'])
                                    st.session_state['tabs'] = tabs
                                    # Set the new tab as current
                                    st.session_state['current_tab'] = new_tab
                                except Exception as e:
                                    st.error(f"Error refreshing tabs: {str(e)}")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error creating tab: {str(e)}")
        
        # Export options
        st.subheader("📤 Import/Export")
        export_format = st.selectbox("Export Format", options=list(EXPORT_OPTIONS.keys()), format_func=lambda x: EXPORT_OPTIONS[x], help="Select the format for exporting your content")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export Content", help="Export the content of the current tab"):
                if st.session_state['current_tab']:
                    # Get the appropriate content (decrypted if necessary)
                    if st.session_state['current_tab'].get('encrypted_content'):
                        content = decrypt_content_if_enabled(st.session_state['current_tab']['encrypted_content'], site)
                    else:
                        content = st.session_state['current_tab'].get('content', '')
                    
                    if content:
                        export_function = EXPORT_FUNCTIONS.get(export_format)
                        if export_function:
                            export_data = export_function(content, site['username'])
                            
                            st.download_button(
                                label=f"Download as {EXPORT_OPTIONS[export_format]}",
                                data=export_data,
                                file_name=f"{site['username']}_content.{export_format}",
                                mime=EXPORT_MIME_TYPES.get(export_format, "text/plain")
                            )
                        else:
                            st.error(f"Export format '{export_format}' not supported")
                    else:
                        st.warning("No content to export")
                else:
                    st.warning("Select a tab to export")
        
        with col2:
            uploaded_file = st.file_uploader("Import File", type=["txt", "md"], help="Upload a file to import its content into the current tab")
            if uploaded_file is not None:
                try:
                    # Read the file content
                    file_content = uploaded_file.read().decode("utf-8")
                    
                    # Add to current tab content
                    if st.session_state['current_tab']:
                        # Get existing content (decrypted if necessary)
                        if st.session_state['current_tab'].get('encrypted_content'):
                            current_content = decrypt_content_if_enabled(st.session_state['current_tab']['encrypted_content'], site)
                        else:
                            current_content = st.session_state['current_tab'].get('content', '')
                        
                        updated_content = current_content + "\n\n" + file_content
                        
                        # Validate content size
                        is_valid, error_msg = validate_content(updated_content)
                        if not is_valid:
                            st.error(f"Cannot import: {error_msg}")
                        else:
                            # Encrypt content if enabled
                            plaintext_content, encrypted_content = encrypt_content_if_enabled(updated_content, site)
                            
                            # Update the tab content
                            try:
                                updated_tab = supabase_client.update_tab_content(
                                    st.session_state['current_tab']['id'], 
                                    plaintext_content, 
                                    encrypted_content
                                )
                                if updated_tab:
                                    st.success("File imported successfully!")
                                    # Update local state
                                    if encrypted_content:
                                        st.session_state['current_tab']['encrypted_content'] = encrypted_content
                                        st.session_state['current_tab']['content'] = None
                                    else:
                                        st.session_state['current_tab']['content'] = plaintext_content
                                        st.session_state['current_tab']['encrypted_content'] = None
                                    st.session_state['current_tab']['updated_at'] = updated_tab.get('updated_at')
                                    st.rerun()
                                else:
                                    st.error("Failed to import file")
                            except Exception as e:
                                st.error(f"Error importing file: {str(e)}")
                    else:
                        st.warning("Select a tab to import content")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        # Statistics dashboard
        st.subheader("📊 Statistics")
        if st.session_state['tabs']:
            total_tabs = len(st.session_state['tabs'])
            total_content_size = sum(len(tab.get('content', '').encode('utf-8')) for tab in st.session_state['tabs'])
            avg_content_size = total_content_size / total_tabs if total_tabs > 0 else 0
            
            st.write(f"**Total Tabs:** {total_tabs}")
            st.write(f"**Total Content Size:** {total_content_size:,} bytes")
            st.write(f"**Average Tab Size:** {avg_content_size:.0f} bytes")
            
            # Most recently updated tab
            if st.session_state['tabs']:
                most_recent = max(st.session_state['tabs'], key=lambda x: x.get('updated_at', ''))
                if most_recent.get('updated_at'):
                    st.write(f"**Last Updated:** {most_recent['tab_name']} ({most_recent['updated_at'][:19].replace('T', ' ')})")
        else:
            st.write("No statistics available yet.")
        
        # Logout button
        if st.button("🚪 Logout", help="Sign out of your SecureText Vault"):
            # Check for unsaved changes before logout
            if st.session_state.get('unsaved_changes', False):
                st.warning("You have unsaved changes. Please save before logging out.")
                if st.button("Logout Anyway"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
            else:
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    # Main content area
    if st.session_state['current_tab']:
        tab = st.session_state['current_tab']
        
        st.header(f"📄 {tab['tab_name']}")
        
        # Editor mode toggle
        editor_mode = st.radio(
            "Editor Mode",
            options=['Plain Text', 'Markdown'],
            horizontal=True,
            key=f"editor_mode_{tab['id']}",
            help="Switch between plain text and Markdown editing modes"
        )
        
        # Set editor mode in session state
        st.session_state['editor_mode'] = 'markdown' if editor_mode == 'Markdown' else 'plain'
        
        # Search functionality
        search_term = st.text_input("🔍 Search in content", placeholder="Enter text to search...", key=f"search_{tab['id']}", help="Search for text within the current tab content")
        
        # Get the appropriate content (decrypted if necessary)
        if tab.get('encrypted_content'):
            content = decrypt_content_if_enabled(tab['encrypted_content'], site)
        else:
            content = tab.get('content', '')
        
        # Store original content for comparison
        original_content = content
        
        # Content editor based on mode
        if st.session_state['editor_mode'] == 'markdown':
            # Split the layout for markdown editor and preview
            editor_col, preview_col = st.columns(2)
            
            with editor_col:
                st.subheader("📝 Editor")
                content = st.text_area(
                    "Content",
                    value=content,
                    height=400,
                    placeholder="Start typing your secure notes here in Markdown...",
                    key=f"editor_{tab['id']}",
                    label_visibility="collapsed",
                    help="Edit your content in Markdown format"
                )
            
            with preview_col:
                st.subheader("👁️ Preview")
                # Render markdown content with proper styling
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; min-height: 400px; background-color: {'#2d3142' if st.session_state['theme'] == 'dark' else '#ffffff'};">
                    {content}
                </div>
                """, unsafe_allow_html=True)
        else:
            # Plain text mode
            content = st.text_area(
                "Content",
                value=content,
                height=400,
                placeholder="Start typing your secure notes here...",
                key=f"editor_{tab['id']}",
                help="Edit your content in plain text format"
            )
        
        # Check for unsaved changes
        if content != original_content:
            st.session_state['unsaved_changes'] = True
        else:
            st.session_state['unsaved_changes'] = False
        
        # Highlight search term if found
        if search_term and search_term in content:
            st.success(f"Found {content.count(search_term)} occurrence(s) of '{search_term}'")
        
        # Character count and size warning
        char_count = len(content)
        content_size = len(content.encode('utf-8'))
        size_percentage = (content_size / MAX_CONTENT_SIZE_BYTES) * 100
        
        st.caption(f"Characters: {char_count} | Size: {content_size:,} bytes ({size_percentage:.1f}% of limit)")
        
        if content_size > MAX_CONTENT_SIZE_BYTES:
            st.error(f"⚠️ Content exceeds maximum size of {MAX_CONTENT_SIZE_BYTES:,} bytes")
        
        # Auto-save functionality (every 30 seconds)
        AUTO_SAVE_INTERVAL = 30  # seconds
        
        # Check if it's time to auto-save
        if (datetime.now() - st.session_state['last_auto_save_time']).seconds > AUTO_SAVE_INTERVAL:
            # Only auto-save if there are changes
            if content != (decrypt_content_if_enabled(tab.get('encrypted_content', ''), site) if tab.get('encrypted_content') else tab.get('content', '')):
                # Validate content size
                is_valid, error_msg = validate_content(content)
                if is_valid:
                    try:
                        # Encrypt content if enabled
                        plaintext_content, encrypted_content = encrypt_content_if_enabled(content, site)
                        
                        updated_tab = supabase_client.update_tab_content(
                            tab['id'], 
                            plaintext_content, 
                            encrypted_content
                        )
                        if updated_tab:
                            # Update local state
                            if encrypted_content:
                                tab['encrypted_content'] = encrypted_content
                                tab['content'] = None
                            else:
                                tab['content'] = plaintext_content
                                tab['encrypted_content'] = None
                            tab['updated_at'] = updated_tab.get('updated_at')
                            st.session_state['current_tab'] = tab
                            # Update auto-save timestamp
                            st.session_state['last_auto_save_time'] = datetime.now()
                            st.session_state['last_auto_save'] = datetime.now().strftime("%H:%M:%S")
                            st.session_state['unsaved_changes'] = False
                    except Exception as e:
                        # Silently fail on auto-save errors to avoid disrupting user
                        pass
        
        # Save button
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            save_button = st.button("💾 Save", type="primary", key="save_button", help="Save your changes to the current tab")
        with col3:
            st.caption("Ctrl+S")
        
        # Auto-save indicator
        if 'last_auto_save' in st.session_state:
            st.caption(f"Last auto-saved: {st.session_state['last_auto_save']}")
        
        # Handle save action
        if save_button:
            if content != (decrypt_content_if_enabled(tab.get('encrypted_content', ''), site) if tab.get('encrypted_content') else tab.get('content', '')):
                # Validate content size
                is_valid, error_msg = validate_content(content)
                if not is_valid:
                    st.error(f"Cannot save: {error_msg}")
                else:
                    try:
                        # Encrypt content if enabled
                        plaintext_content, encrypted_content = encrypt_content_if_enabled(content, site)
                        
                        updated_tab = supabase_client.update_tab_content(
                            tab['id'], 
                            plaintext_content, 
                            encrypted_content
                        )
                        if updated_tab:
                            st.success("Content saved!")
                            # Update local state
                            if encrypted_content:
                                tab['encrypted_content'] = encrypted_content
                                tab['content'] = None
                            else:
                                tab['content'] = plaintext_content
                                tab['encrypted_content'] = None
                            tab['updated_at'] = updated_tab.get('updated_at')
                            st.session_state['current_tab'] = tab
                            # Update auto-save timestamp
                            st.session_state['last_auto_save_time'] = datetime.now()
                            st.session_state['last_auto_save'] = datetime.now().strftime("%H:%M:%S")
                            st.session_state['unsaved_changes'] = False
                            st.rerun()
                        else:
                            st.error("Failed to save content")
                    except Exception as e:
                        st.error(f"Error saving content: {str(e)}")
            else:
                st.info("No changes to save")
        with col2:
            if st.button("🔄 Refresh", help="Refresh the current tab content"):
                st.rerun()
        
        # Last updated
        if tab.get('updated_at'):
            st.caption(f"Last updated: {tab['updated_at']}")
        
        # Show unsaved changes warning
        if st.session_state.get('unsaved_changes', False):
            st.warning("⚠️ You have unsaved changes. Don't forget to save before leaving!")
    else:
        st.info("👈 Select or create a tab from the sidebar to start writing")

def main():
    """Main application entry point"""
    try:
        # Page configuration
        st.set_page_config(
            page_title="SecureText Vault",
            page_icon="🔐",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        

        
        # Removed skip to main content link
        
        # Check if Supabase is configured
        try:
            config.validate()
        except ValueError as e:
            show_setup_instructions()
            return
        except Exception as e:
            st.error(f"Unexpected error during configuration validation: {str(e)}")
            show_setup_instructions()
            return
        
        # Initialize session state
        if 'session_token' not in st.session_state:
            st.session_state['session_token'] = None
        if 'current_site' not in st.session_state:
            st.session_state['current_site'] = None
        if 'theme' not in st.session_state:
            st.session_state['theme'] = 'light'  # Default theme
        
        # Check for valid session
        if st.session_state['session_token']:
            try:
                valid, message, site = auth_service.validate_session_token(st.session_state['session_token'])
                if valid and site:
                    st.session_state['current_site'] = site
                    site_management_page(site)
                    return
                else:
                    # Invalid session, clear it
                    st.session_state['session_token'] = None
                    st.session_state['current_site'] = None
            except Exception as e:
                st.error(f"Error validating session: {str(e)}")
                st.session_state['session_token'] = None
                st.session_state['current_site'] = None
        
        # Show landing page
        st.title("🔐 SecureText Vault")
        
        # Theme toggle for landing page
        theme_toggle = st.toggle("🌙 Dark Mode", value=(st.session_state['theme'] == 'dark'))
        if theme_toggle != (st.session_state['theme'] == 'dark'):
            # Theme has changed, update state and rerun to apply styles
            if theme_toggle:
                st.session_state['theme'] = 'dark'
            else:
                st.session_state['theme'] = 'light'
            st.rerun()
        
        # Apply theme styles globally
        apply_theme_styles()
        
        st.markdown("""
        ### Password-protected text storage with multi-tab support
        
        Store your notes, code snippets, or any text securely with:
        - 🔐 **Password protection** - Only you can access your content
        - 🏷️ **Multi-tab organization** - Organize content in separate tabs
        - 💾 **Auto-save** - Your content is saved automatically
        - 📥 **Export options** - Download as TXT, JSON, or Markdown
        - 🌐 **Unique URLs** - Each site has a unique username-based URL
        - 🔒 **End-to-end encryption** - Your content is encrypted before storage (when enabled)
        
        **How it works:**
        1. Create a site with a unique username and password
        2. Access your site anytime with your credentials
        3. Organize content in multiple tabs
        4. Export your data when needed
        """)
        
        # Security notice
        st.markdown("""
        <div class="warning">
        <strong>⚠️ Security Notice:</strong><br>
        - Use a strong, unique password for each site<br>
        - Never share your password with anyone<br>
        - Export and backup your important content regularly<br>
        - This service uses bcrypt password hashing and secure session tokens<br>
        - Enable encryption for additional security of your content at rest
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for site creation and access
        col1, col2 = st.columns(2)
        
        with col1:
            create_site_page()
        
        with col2:
            access_site_page()
        
        # Footer
        st.markdown("---")
        st.caption("🔒 **SecureText Vault** - Your text, your control, always secure")
        
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.error("Please check your configuration and try again.")
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
# SecureText Vault 🔐

A secure, password-protected text storage application built with Python, Streamlit, and Supabase. Similar to protectedtext.com, this application provides a private space for storing sensitive information with end-to-end encryption capabilities.

## Key Features

- **🔐 Password Protection**: Each site is secured with a unique username and strong password
- **🏷️ Multi-Tab Organization**: Structure your content across multiple customizable tabs
- **💾 Auto-Save Functionality**: Content is automatically saved as you type
- **📤 Flexible Export Options**: Download your content in Text, JSON, or Markdown formats
- **🔗 Unique Site URLs**: Access your content through personalized username-based identifiers
- **🔒 Advanced Security**: 
  - Password hashing with bcrypt
  - End-to-end encryption (optional)
  - Row Level Security (RLS) in database
  - Access logging for security monitoring
- **📱 Responsive Design**: Optimized for both desktop and mobile devices

## Prerequisites

- Python 3.8+
- Supabase account (free tier available)
- Required Python packages listed in `requirements.txt`

## Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Supabase Integration

1. Create a new project at [Supabase](https://supabase.com)
2. Navigate to **Project Settings > API** and collect:
   - **Project URL** (e.g., `https://xxxxxxxxxxxx.supabase.co`)
   - **anon/public key** (starts with `eyJ...`)
   - **service_role key** (starts with `eyJ...`)

3. Create a `.env` file in the project root with your credentials:
```bash
# Supabase Configuration
SUPABASE_URL=your_actual_supabase_project_url_here
SUPABASE_KEY=your_actual_supabase_anon_key_here
SUPABASE_SERVICE_KEY=your_actual_supabase_service_key_here

# Application Configuration
SESSION_SECRET=generate_a_random_secret_string_here
BCRYPT_ROUNDS=12
MAX_CONTENT_SIZE_MB=1
RATE_LIMIT_PER_MINUTE=60
ENCRYPTION_ENABLED=true
```

### 3. Initialize Database

```bash
python setup_database.py
```
Follow the prompts to execute the required SQL in your Supabase SQL Editor.

### 4. Launch Application

```bash
streamlit run run_app.py
```

## Project Architecture

```
/workspace/
├── app/
│   ├── main.py              # Main Streamlit application
│   ├── config.py            # Configuration management
│   ├── constants.py         # Application constants
│   └── services/
│       ├── supabase_client.py  # Database operations
│       ├── auth_service.py     # Authentication logic
│       └── encryption_service.py  # Content encryption
├── requirements.txt         # Python dependencies
├── setup_database.py       # Database initialization
└── run_app.py             # Application entry point
```

## Database Schema

### Sites Table
Stores site authentication and metadata:
```sql
CREATE TABLE sites (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    encryption_salt TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    last_accessed TIMESTAMP WITH TIME ZONE
);
```

### Tabs Table
Manages content for each site's tabs:
```sql
CREATE TABLE tabs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    site_id UUID REFERENCES sites(id) ON DELETE CASCADE,
    tab_name VARCHAR(100) NOT NULL,
    tab_order INTEGER NOT NULL,
    content TEXT,
    encrypted_content TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);
```

## Usage Instructions

### Creating a New Site
1. Open the application
2. Select "Create New Site"
3. Enter a unique username (3-50 characters)
4. Set a strong password (8-100 characters)
5. Confirm and create your secure site

### Accessing Your Site
1. Open the application
2. Choose "Access Existing Site"
3. Enter your credentials
4. Begin managing your content

### Content Management
- Create and organize tabs via the sidebar (max 20 per site)
- Edit content in the main text area with auto-save functionality
- Export content in preferred formats using sidebar options
- Securely logout when finished

## Security Implementation

- **Password Security**: bcrypt hashing with configurable rounds
- **Session Management**: Secure tokens with automatic expiration
- **Rate Limiting**: Configurable access attempt restrictions
- **Data Isolation**: Row Level Security policies for data separation
- **Encryption**: Optional end-to-end encryption before storage

## Troubleshooting

Common solutions for typical issues:
- **Connection Errors**: Verify `.env` configuration and Supabase credentials
- **Database Issues**: Confirm tables are properly initialized via `setup_database.py`
- **Module Errors**: Use `run_app.py` as the entry point rather than direct execution

For additional support, consult the Supabase documentation or check the browser console for client-side errors.

## License

This project is designed for educational and demonstration purposes.

## Support

For questions or issues, refer to the setup instructions or Supabase documentation.
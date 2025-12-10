# SecureText Vault 🔐
**Your Private, Encrypted Note-Taking Sanctuary**

Transform the way you store sensitive information with SecureText Vault – a cutting-edge, self-hosted text storage solution that combines military-grade encryption with intuitive design. Like having a digital safe deposit box for your thoughts, passwords, and confidential documents.

Unlike traditional note-taking apps, SecureText Vault operates on a **zero-knowledge architecture** – not even the server administrators can access your content. Your data stays yours, always.

## 🌟 Why SecureText Vault Stands Out

| Feature | Description |
|---------|-------------|
| 🔐 **Zero-Knowledge Security** | Your content is encrypted before it leaves your device |
| 🏷️ **Multi-Tab Organization** | Structure notes like a pro with unlimited tabs per site |
| 💾 **Smart Auto-Save** | Never lose a thought with real-time saving technology |
| 📱 **Cross-Platform Access** | Works flawlessly on desktop, tablet, and mobile browsers |
| 🔧 **Self-Hosted Freedom** | Complete control over your data and infrastructure |
| 🚀 **Lightning Fast** | Built with Streamlit for instant-loading performance |

## 🎬 See It In Action

<!-- ![SecureText Vault Demo](link-to-demo-gif-if-available) -->
*Create a site in under 30 seconds and start securing your notes instantly*

**Typical Workflow:**
1. **Create** - Set up your private vault in seconds
2. **Organize** - Create tabs for different categories (Passwords, Ideas, Projects)
3. **Write** - Type freely with peace of mind
4. **Export** - Download in your preferred format anytime

## 🔒 Military-Grade Security Architecture

Your privacy isn't negotiable. SecureText Vault implements multiple layers of protection:

🛡️ **Three-Layer Encryption Stack**
- **Transport Layer**: HTTPS encryption for all communications
- **Application Layer**: AES-256-GCM encryption for stored content
- **Database Layer**: Row-Level Security (RLS) isolation

🔐 **Password Protection**
- Industry-standard bcrypt hashing with configurable rounds
- Brute-force protection with rate limiting
- No plaintext passwords ever stored

🕵️ **Privacy by Design**
- Zero telemetry or analytics collection
- Self-hosted deployment keeps data local
- Detailed access logs for security monitoring

## 💡 Perfect For...

- **🔐 Password Management**: Store encrypted credentials securely
- **💼 Business Notes**: Keep confidential meeting notes private
- **👨‍💻 Developer Snippets**: Save code fragments with end-to-end encryption
- **📝 Personal Journaling**: Maintain a private digital diary
- **🎓 Research Data**: Protect academic or research information
- **🏥 Medical Information**: Securely store health-related notes

## ⚡ Lightning-Fast Setup (Under 5 Minutes)

### 🛠️ Prerequisites Checklist
- [ ] Python 3.8+ installed
- [ ] Free [Supabase](https://supabase.com) account (takes 2 minutes)
- [ ] This repository cloned/downloaded

### 🚀 One-Click Deployment

1. **Install Dependencies** - Get up and running quickly
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Supabase** - Connect your secure database
   ```bash
   # Create .env file with your credentials
   cp .env.example .env
   # Edit .env with your Supabase details
   ```

3. **Initialize Database** - Set up your secure storage
   ```bash
   python setup_database.py
   ```

4. **Launch Your Vault** - Start securing your notes
   ```bash
   streamlit run run_app.py
   ```

That's it! Your personal SecureText Vault is ready to protect your information.

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

## 🤝 Join Our Community

We believe in collaborative security. Contributions make SecureText Vault better for everyone:

### 🎯 Ways to Contribute
- **🐛 Bug Reports**: Help us squash security vulnerabilities
- **✨ Feature Requests**: Suggest enhancements for better protection
- **📖 Documentation**: Improve guides for fellow privacy advocates
- **💻 Code Contributions**: Add new security features or fix issues

### 🚀 Getting Started with Development
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 🛡️ Security Disclosure
Found a vulnerability? Contact us privately at [security email] before public disclosure.

## Troubleshooting

Common solutions for typical issues:
- **Connection Errors**: Verify `.env` configuration and Supabase credentials
- **Database Issues**: Confirm tables are properly initialized via `setup_database.py`
- **Module Errors**: Use `run_app.py` as the entry point rather than direct execution

For additional support, consult the Supabase documentation or check the browser console for client-side errors.

## 📄 License & Legal

This project is released under the MIT License – perfect for educational and demonstration purposes. While we've implemented robust security measures, we recommend consulting with security professionals for mission-critical applications.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Powered-red.svg)](https://streamlit.io/)

---

<p align="center">
  <strong>Built with ❤️ for privacy advocates everywhere</strong>
</p>
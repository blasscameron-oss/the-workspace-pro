# Wrangler CLI Installation & Deployment Guide

## 📋 Prerequisites

### **1. Check Required Software**
Open **terminal** (macOS/Linux) or **Command Prompt/PowerShell** (Windows) and run:

```bash
# Check Node.js version (needs v16.13.0+)
node --version

# Check npm version
npm --version
```

**Expected output:** Version numbers (not errors).

**If missing Node.js/npm:**
- **macOS:** `brew install node`
- **Ubuntu/Debian:** `sudo apt install nodejs npm`
- **Windows:** Download from [nodejs.org](https://nodejs.org/)
- **Verify:** Restart terminal and check versions again

---

## 🚀 **Step 1: Install Wrangler CLI**

### **Option A: Install via npm (Recommended)**
```bash
# Install globally (requires sudo on Linux/macOS)
npm install -g wrangler

# OR install locally in project (no sudo needed)
npm install wrangler --save-dev
```

### **Option B: macOS with Homebrew**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Wrangler
brew install cloudflare/wrangler/wrangler
```

### **Option C: Windows with Chocolatey**
```bash
# Install Chocolatey if not installed
# Follow: https://chocolatey.org/install

# Install Wrangler
choco install wrangler
```

### **Option D: Install Script (Linux/macOS)**
```bash
# Download and run install script
curl -s https://install.wrangler.dev | bash
```

### **Verify Installation**
```bash
# Check Wrangler version
wrangler --version

# Expected output: "wrangler x.x.x" or similar
# If "command not found": restart terminal or add to PATH
```

---

## 🔐 **Step 2: Login to Cloudflare**

```bash
# Authenticate with Cloudflare
wrangler login

# This will:
# 1. Open your default browser
# 2. Go to Cloudflare login page
# 3. Ask you to authorize Wrangler
# 4. Return to terminal when complete
```

**Troubleshooting:**
- **Browser doesn't open:** Copy the URL shown and paste into browser
- **Login fails:** Ensure you're logged into correct Cloudflare account
- **Permissions error:** Make sure account has "Pages" access

---

## 📦 **Step 3: Prepare Your Site Files**

### **Download the Deployment Package**
```bash
# Create a new directory for the project
mkdir the-workspace-pro
cd the-workspace-pro

# Download the optimized site (choose one):
# Option 1: Using curl
curl -O http://72.198.87.116:9000/workspace-pro-root.zip

# Option 2: Using wget
wget http://72.198.87.116:9000/workspace-pro-root.zip

# Extract the files
unzip workspace-pro-root.zip

# Verify files are extracted
ls -la
```

**Expected files:**
- `index.html` (homepage)
- `content/` directory (17 guide pages)
- `static/` directory (CSS, JS, images)
- `_headers`, `_redirects`, `robots.txt`, `sitemap.xml`

---

## 🚀 **Step 4: Deploy with Wrangler**

### **Option A: Deploy to Cloudflare Pages (Recommended)**
```bash
# From your project directory (where index.html is)
wrangler pages deploy . --project-name=the-workspace-pro
```

**This will:**
1. Upload all files to Cloudflare
2. Create a new Pages project called "the-workspace-pro"
3. Return a URL like: `https://the-workspace-pro.pages.dev`

### **Option B: Create wrangler.toml Configuration**
```bash
# Create configuration file
cat > wrangler.toml << 'EOF'
name = "the-workspace-pro"
compatibility_date = "2026-04-19"

[site]
bucket = "."
entry-point = "workers-site"
EOF

# Then deploy
wrangler publish
```

### **Option C: One-Command Deployment**
```bash
# Download and deploy in one command (advanced)
curl -s http://72.198.87.116:9000/workspace-pro-root.zip | \
  funzip | \
  wrangler pages deploy --project-name=the-workspace-pro -
```

---

## 🔧 **Step 5: Verify Deployment**

### **Check Deployment Status**
```bash
# List your Pages projects
wrangler pages project list

# View deployment details
wrangler pages deployment list --project-name=the-workspace-pro
```

### **Test Your Site**
1. **Open browser** to the URL provided after deployment
2. **Check homepage**: `https://the-workspace-pro.pages.dev`
3. **Test navigation**: Click through to guide pages
4. **Verify search**: Ctrl+K or click search icon
5. **Check mobile**: Resize browser or use phone

---

## ⚙️ **Step 6: Configure Custom Domain**

### **In Cloudflare Dashboard:**
1. **Go to**: [Cloudflare Dashboard](https://dash.cloudflare.com)
2. **Select**: Pages → `the-workspace-pro` project
3. **Click**: "Custom domains"
4. **Add domain**: `theworkspacepro.com`
5. **Follow DNS setup instructions**

### **Or via Wrangler CLI:**
```bash
# Add custom domain
wrangler pages domain add theworkspacepro.com --project-name=the-workspace-pro
```

---

## 🚨 **Troubleshooting Common Issues**

### **1. "wrangler: command not found"**
```bash
# Fix PATH on macOS/Linux
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or reinstall with different method
npm uninstall -g wrangler
npm install -g wrangler@latest
```

### **2. "Authentication failed"**
```bash
# Clear authentication cache
wrangler logout
wrangler login
```

### **3. "Project already exists"**
```bash
# Use different project name
wrangler pages deploy . --project-name=the-workspace-pro-2

# Or delete existing project (in dashboard)
```

### **4. "File too large" or upload hangs**
```bash
# Deploy in chunks (if many files)
tar -czf site.tar.gz .
wrangler pages deploy site.tar.gz --project-name=the-workspace-pro
```

### **5. "No such file or directory"**
```bash
# Ensure you're in correct directory
pwd  # Should show files like index.html
ls -la  # Should list site files
```

---

## 📚 **Additional Resources**

### **Wrangler Documentation**
- [Official Docs](https://developers.cloudflare.com/workers/wrangler/)
- [Pages CLI Reference](https://developers.cloudflare.com/pages/platform/cli/)

### **Cloudflare Pages Guide**
- [Getting Started](https://developers.cloudflare.com/pages/get-started/)
- [Custom Domains](https://developers.cloudflare.com/pages/platform/custom-domains/)

### **Support**
- [Cloudflare Community](https://community.cloudflare.com/)
- [Discord](https://discord.cloudflare.com/)

---

## ✅ **Quick Reference Card**

```bash
# 1. Install
npm install -g wrangler

# 2. Login
wrangler login

# 3. Download site
curl -O http://72.198.87.116:9000/workspace-pro-root.zip
unzip workspace-pro-root.zip

# 4. Deploy
wrangler pages deploy . --project-name=the-workspace-pro

# 5. Add domain (optional)
wrangler pages domain add theworkspacepro.com --project-name=the-workspace-pro
```

---

## 🆘 **Need Help?**

**Common questions answered:**

**Q: Do I need a Cloudflare account?**
A: Yes, free account at [cloudflare.com](https://www.cloudflare.com/)

**Q: Is there a cost?**
A: Cloudflare Pages is free for up to 500 builds/month

**Q: Can I update the site later?**
A: Yes, run `wrangler pages deploy` again with updated files

**Q: What if deployment fails?**
A: Check error message, ensure all prerequisites are met

**Still stuck?** Share the exact error message for specific help.
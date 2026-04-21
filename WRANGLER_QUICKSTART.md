# Wrangler Quick Start - 5 Steps to Deploy

## ⚡ **Ultra-Simple Instructions**

### **STEP 1: Install Node.js (if needed)**
```bash
# Check if installed:
node --version

# If not installed:
# - macOS: brew install node
# - Windows: Download from nodejs.org
# - Linux: sudo apt install nodejs npm
```

### **STEP 2: Install Wrangler**
```bash
# One command:
npm install -g wrangler

# Verify:
wrangler --version
# Should show "wrangler x.x.x"
```

### **STEP 3: Login to Cloudflare**
```bash
wrangler login
```
- **Browser opens** → Log in to Cloudflare
- **Click "Authorize"** → Return to terminal
- **Should see**: "Successfully logged in"

### **STEP 4: Download & Extract Site**
```bash
# Create folder and download
mkdir workspace-pro && cd workspace-pro
curl -O http://72.198.87.116:9000/workspace-pro-root.zip
unzip workspace-pro-root.zip

# Verify files
ls -la
# Should see: index.html, content/, static/, etc.
```

### **STEP 5: Deploy!**
```bash
# One command deployment:
wrangler pages deploy . --project-name=the-workspace-pro
```

**Done!** You'll get a URL like: `https://the-workspace-pro.pages.dev`

---

## 🚨 **If You Get Stuck**

### **Common Errors & Fixes:**

**1. "npm: command not found"**
```bash
# Install Node.js first:
# macOS: brew install node
# Windows: Download from nodejs.org
# Ubuntu: sudo apt install nodejs npm
```

**2. "Permission denied" (npm install)**
```bash
# Try without -g (local install):
npm install wrangler

# Or use sudo (macOS/Linux):
sudo npm install -g wrangler
```

**3. Browser doesn't open for login**
- **Copy the URL** shown in terminal
- **Paste into browser** manually
- **Login** and authorize

**4. "Project already exists"**
```bash
# Use different name:
wrangler pages deploy . --project-name=workspace-pro-$(date +%s)
```

**5. Upload hangs/stuck**
```bash
# Try smaller package:
curl -O http://72.198.87.116:9000/workspace-pro-lite.zip
unzip workspace-pro-lite.zip
wrangler pages deploy . --project-name=the-workspace-pro
```

---

## ✅ **Verification Checklist**

- [ ] `node --version` shows version (v16+)
- [ ] `npm --version` shows version
- [ ] `wrangler --version` shows version
- [ ] `wrangler login` successful
- [ ] Downloaded ZIP file (~1.4 MB)
- [ ] Extracted files (index.html exists)
- [ ] `wrangler pages deploy` completed
- [ ] Received deployment URL
- [ ] Site loads in browser

---

## 📞 **Need Immediate Help?**

**Share the exact error message** and which step you're on.

**Example:**
```
Step: 2 (npm install)
Error: "npm: command not found"
```

**Or:**
```
Step: 5 (deploy)
Error: "Authentication failed"
```

**I can provide specific fixes for your exact error!**
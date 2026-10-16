# GitHub Setup Guide

This guide will help you push your FraudGuard AI project to GitHub.

---

## 📋 Prerequisites

1. **Git installed** on your computer
   - Download from: https://git-scm.com/downloads
   - Install with default settings

2. **GitHub account**
   - Sign up at: https://github.com/signup
   - Free account is sufficient

---

## 🚀 Step-by-Step Instructions

### Step 1: Initialize Git Repository

Open a terminal/command prompt in your project folder:

```bash
cd C:\Users\LENOVO\Desktop\fraud-detection-project
git init
```

### Step 2: Add All Files

```bash
git add .
```

### Step 3: Create First Commit

```bash
git commit -m "Initial commit: FraudGuard AI - Real-time fraud detection system"
```

### Step 4: Create GitHub Repository

1. Go to https://github.com
2. Click the **+** icon (top right)
3. Select **New repository**
4. Fill in:
   - **Repository name**: `fraud-detection-project` (or your preferred name)
   - **Description**: `Real-time financial fraud detection system with ML`
   - **Public/Private**: Choose based on your preference
   - **⚠️ IMPORTANT**: UNCHECK "Initialize this repository with a README"
5. Click **Create repository**

### Step 5: Link Local Repository to GitHub

Copy the repository URL from GitHub (choose HTTPS or SSH):

**HTTPS (easier for beginners):**
```bash
git remote add origin https://github.com/YOUR_USERNAME/fraud-detection-project.git
```

**SSH (requires SSH key setup):**
```bash
git remote add origin git@github.com:YOUR_USERNAME/fraud-detection-project.git
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

### Step 6: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

### Step 7: Authenticate (if using HTTPS)

When prompted, enter:
- **Username**: Your GitHub username
- **Password**: Your GitHub Personal Access Token (NOT your account password)

**To create a Personal Access Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Fraud Detection Project")
4. Select scopes: check `repo` (full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when pushing

---

## ✅ Verification

After pushing, go to your GitHub repository page. You should see:
- All your project files
- README.md displayed
- Commit history

---

## 🔄 How to Update GitHub Later

After making changes to your project:

```bash
# Check status
git status

# Add changed files
git add .

# Commit changes
git commit -m "Your commit message here"

# Push to GitHub
git push
```

---

## 📁 What Will Be Uploaded

The `.gitignore` file will exclude:
- Virtual environment (`.venv/`)
- Python cache files (`__pycache__/`)
- Jupyter notebook checkpoints
- Large data files
- Environment variables (`.env`)
- IDE settings

**Included:**
- All source code
- Documentation (README, PROJECT_REPORT)
- Frontend files (HTML, CSS, JS, images)
- Trained models (production models only)
- Startup scripts
- Test files

---

## 🎯 Quick Commands Reference

```bash
# Initialize repository
git init

# Add files
git add .
git add filename.txt

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push
git push -u origin main

# Check status
git status

# View changes
git diff

# View commit history
git log

# Create branch
git branch feature-name
git checkout feature-name

# Merge branch
git checkout main
git merge feature-name
```

---

## 🐛 Troubleshooting

### Error: "fatal: not a git repository"
**Solution:** Run `git init` in your project folder

### Error: "remote origin already exists"
**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/fraud-detection-project.git
```

### Error: "Authentication failed"
**Solution:** Use a Personal Access Token instead of your password

### Error: "refusing to merge unrelated histories"
**Solution:**
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

### Large files won't upload
**Solution:** Large files (>100MB) need Git LFS (Large File Storage)
- Install Git LFS: https://git-lfs.github.com/
- Run: `git lfs install`
- Track large files: `git lfs track "*.pkl"`

---

## 📝 Best Practices

1. **Write clear commit messages**
   - ✅ "Add visualization section to frontend"
   - ❌ "update files"

2. **Commit frequently**
   - Small, focused commits
   - Easier to track changes

3. **Use branches for features**
   - `git checkout -b feature/new-feature`
   - Merge back to main when done

4. **Keep README updated**
   - Update with new features
   - Keep installation instructions current

---

## 🎉 After Successful Upload

Your project is now on GitHub! You can:

- Share the repository URL with others
- Show it in your portfolio
- Enable GitHub Pages for hosting
- Add collaborators for team projects
- Use GitHub Issues for bug tracking

---

## 📚 Additional Resources

- [GitHub Documentation](https://docs.github.com/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub Learning Lab](https://lab.github.com/)

---

**Good luck! Your fraud detection project will be on GitHub in no time! 🚀**

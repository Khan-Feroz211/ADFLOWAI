#!/bin/bash

# ADFLOWAI - GitHub Push Script
# Pushes all files to your GitHub repository

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         ADFLOWAI - GitHub Repository Setup              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if git is configured
if ! git config user.name > /dev/null 2>&1; then
    echo "Please configure git first:"
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    print_status "Git configured"
fi

# Get GitHub repository URL
REPO_URL="https://github.com/Khan-Feroz211/ADFLOWAI.git"
print_status "Repository: $REPO_URL"

# Check if already initialized
if [ -d .git ]; then
    print_status "Git repository already initialized"
else
    git init
    print_status "Git repository initialized"
fi

# Add remote if not exists
if ! git remote get-url origin > /dev/null 2>&1; then
    git remote add origin $REPO_URL
    print_status "Remote origin added"
else
    print_status "Remote origin already exists"
fi

# Create main branch
git branch -M main

# Add all files
echo ""
print_status "Adding all files to git..."
git add .

# Show what will be committed
echo ""
echo "Files to be committed:"
git status --short | head -20
echo ""

# Commit
read -p "Enter commit message (default: 'Initial commit - Production-ready ADFLOWAI'): " commit_msg
commit_msg=${commit_msg:-"Initial commit - Production-ready ADFLOWAI platform"}

git commit -m "$commit_msg"
print_status "Changes committed"

# Push to GitHub
echo ""
print_warning "Ready to push to GitHub"
echo "Repository: $REPO_URL"
echo ""
read -p "Push to GitHub now? (y/n): " confirm

if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    echo ""
    print_status "Pushing to GitHub..."
    
    # Try to push
    if git push -u origin main; then
        print_status "Successfully pushed to GitHub!"
        echo ""
        echo "╔═══════════════════════════════════════════════════════════╗"
        echo "║              PUSHED TO GITHUB SUCCESSFULLY!              ║"
        echo "╚═══════════════════════════════════════════════════════════╝"
        echo ""
        echo "View your repository at:"
        echo "👉 https://github.com/Khan-Feroz211/ADFLOWAI"
        echo ""
    else
        print_error "Failed to push to GitHub"
        echo ""
        echo "This might be because:"
        echo "  1. You need to authenticate with GitHub"
        echo "  2. The repository doesn't exist yet"
        echo "  3. You don't have write access"
        echo ""
        echo "Solutions:"
        echo "  1. Create repository at: https://github.com/new"
        echo "  2. Or use: gh auth login (GitHub CLI)"
        echo "  3. Or set up SSH key"
        echo ""
        echo "Manual push command:"
        echo "  git push -u origin main"
    fi
else
    print_warning "Push cancelled"
    echo ""
    echo "To push later, run:"
    echo "  git push -u origin main"
fi

echo ""
print_status "Setup complete!"

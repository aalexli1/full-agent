# macOS Development Setup for Full Agent

## Essential Foundation (Install First)

```bash
# 1. Xcode Command Line Tools (required for everything)
xcode-select --install

# 2. Homebrew (package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Core Development Tools

```bash
# Node.js & Package Managers
brew install node          # Includes npm
brew install yarn          # Alternative to npm
brew install pnpm          # Faster alternative
brew install bun           # All-in-one JavaScript runtime

# Python
brew install python@3.12   # Latest stable Python
brew install pipx          # Install Python apps in isolated environments
pipx install poetry        # Modern Python dependency management

# Docker
brew install --cask docker

# Database Systems
brew install postgresql@16
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
echo 'export LDFLAGS="-L/opt/homebrew/opt/postgresql@16/lib"' >> ~/.zshrc
echo 'export CPPFLAGS="-I/opt/homebrew/opt/postgresql@16/include"' >> ~/.zshrc

# To start:
brew services start postgresql@16

brew install mysql

# To start:
brew services start mysql

# To run:
mysql -u root

brew install redis
brew services start redis

# MongoDB (requires tap first)
brew tap mongodb/brew
brew install mongodb-community
brew install sqlite

# Start database services
brew services start postgresql@16
brew services start redis
brew services start mongodb/brew/mongodb-community
```

## Mobile Development

```bash
# iOS Development
brew install cocoapods
brew install watchman      # File watcher for React Native
brew install ios-deploy    # Install and debug iOS apps from command line

# Android Development  
brew install --cask android-studio
brew install --cask android-commandlinetools
brew install gradle

# React Native specific
brew install flipper       # Debugging platform

# After Android Studio install, add to ~/.zshrc:
echo 'export ANDROID_HOME=$HOME/Library/Android/sdk' >> ~/.zshrc
echo 'export PATH=$PATH:$ANDROID_HOME/emulator' >> ~/.zshrc
echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools' >> ~/.zshrc
echo 'export PATH=$PATH:$ANDROID_HOME/tools' >> ~/.zshrc
echo 'export PATH=$PATH:$ANDROID_HOME/tools/bin' >> ~/.zshrc
```

## Additional Languages & Runtimes

```bash
# Java
brew install --cask temurin  # OpenJDK (required for Android)

# Go
brew install go

# Rust
brew install rust

# Ruby (macOS has it, but better to have updated version)
brew install rbenv ruby-build
rbenv install 3.3.0
rbenv global 3.3.0

# .NET
brew install --cask dotnet-sdk

# PHP
brew install php
brew install composer
```

## Security & Certificates

```bash
# Local HTTPS certificates
brew install mkcert
brew install nss  # For Firefox support
mkcert -install   # Sets up local CA

# SSL/TLS tools
brew install openssl
brew install certbot  # Let's Encrypt certificates

# Security scanning
brew install gnupg    # GPG encryption
```

## Cloud & Deployment Tools

```bash
# Cloud CLIs
brew install awscli
brew install azure-cli
brew install --cask google-cloud-sdk
brew install doctl       # DigitalOcean
brew install vercel-cli  # Vercel deployment
brew install netlify-cli # Netlify deployment
brew install heroku/brew/heroku

# Container tools
brew install kubectl
brew install helm
brew install minikube
brew install podman      # Docker alternative

# Infrastructure as Code
brew install terraform
brew install ansible
```

## Development Utilities

```bash
# API Testing
brew install curl
brew install wget
brew install httpie      # User-friendly HTTP client
brew install insomnia     # API client with GUI
brew install --cask postman

# Text Processing
brew install jq          # JSON processor
brew install yq          # YAML processor
brew install ripgrep     # Fast text search
brew install bat         # Better cat
brew install fzf         # Fuzzy finder

# Development Tools
brew install gh          # GitHub CLI
brew install git-lfs     # Git Large File Storage
brew install tmux        # Terminal multiplexer
brew install neovim      # Text editor
brew install tree        # Directory visualization

# Network Tools
brew install ngrok       # Expose local servers
brew install mitmproxy   # HTTP/HTTPS proxy
brew install nmap        # Network scanner

# Media Processing
brew install ffmpeg      # Video/audio processing
brew install imagemagick # Image processing
brew install graphviz    # Graph visualization

# Compression
brew install p7zip
brew install unrar
```

## Code Quality & Testing

```bash
# Linters & Formatters
brew install prettier
brew install eslint
brew install black       # Python formatter
brew install ruff        # Fast Python linter
brew install shellcheck  # Shell script linter

# Testing Tools
brew install selenium-server
brew install --cask chromedriver
brew install geckodriver  # Firefox driver

brew services start selenium-server

# Code Analysis
brew install sonarqube
brew install cloc        # Count lines of code
```

## Browsers for Testing

```bash
brew install --cask google-chrome
brew install --cask firefox
brew install --cask microsoft-edge
brew install --cask brave-browser
brew install --cask arc
```

## Set up common global npm packages

```bash
# Essential global npm tools
npm install -g typescript
npm install -g ts-node
npm install -g nodemon
npm install -g pm2          # Process manager
npm install -g serve        # Static file server
npm install -g json-server  # Quick REST API
npm install -g create-react-app
npm install -g create-next-app
npm install -g @angular/cli
npm install -g @vue/cli
npm install -g expo-cli     # React Native
npm install -g react-native-cli
npm install -g nest-cli     # NestJS
npm install -g nx          # Monorepo tools
npm install -g lerna
npm install -g turbo
```

## Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
```

## Optional but Useful

```bash
# Documentation
brew install --cask dash         # API documentation browser
brew install --cask obsidian     # Note taking

# Database GUIs
brew install --cask dbeaver-community
brew install --cask tableplus
brew install --cask pgadmin4

# Development IDEs (if agent needs to open projects)
brew install --cask visual-studio-code
brew install --cask jetbrains-toolbox
brew install --cask sublime-text

# Virtualization
brew install --cask virtualbox
brew install vagrant

# System Monitoring
brew install htop
brew install btop
brew install ncdu         # Disk usage analyzer
```

## Environment Setup

Add to `~/.zshrc`:

```bash
# Homebrew
export PATH="/opt/homebrew/bin:$PATH"

# Node Version Manager (if using nvm instead of brew node)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Python
export PATH="$HOME/.local/bin:$PATH"

# Go
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# Rust
source "$HOME/.cargo/env"

# Ruby
eval "$(rbenv init - zsh)"

# Java
export JAVA_HOME=$(/usr/libexec/java_home)

# Android (after Android Studio install)
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin

# pnpm
export PNPM_HOME="$HOME/Library/pnpm"
export PATH="$PNPM_HOME:$PATH"
```

## Quick Install Script

Save this as `setup.sh` and run with `bash setup.sh`:

```bash
#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up macOS for Full Agent development..."

# Check for Xcode CLI tools
if ! xcode-select -p &> /dev/null; then
    echo "📦 Installing Xcode Command Line Tools..."
    xcode-select --install
    echo "Please complete the Xcode CLI tools installation, then run this script again."
    exit 1
fi

# Install Homebrew
if ! command -v brew &> /dev/null; then
    echo "🍺 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo "📦 Installing essential tools..."
brew install git node yarn postgresql@16 redis docker mkcert

echo "🔧 Starting services..."
brew services start postgresql@16
brew services start redis

echo "🔒 Setting up local HTTPS..."
mkcert -install

echo "✅ Basic setup complete!"
echo "Run 'brew bundle' with a Brewfile for complete installation"
```

## Notes

1. **Xcode**: For iOS development, you'll also need the full Xcode from the App Store (not just CLI tools)
2. **Android Studio**: Requires manual setup after installation to download SDKs
3. **Docker Desktop**: May require license for commercial use
4. **Services**: Use `brew services list` to see what's running
5. **Updates**: Keep everything updated with `brew update && brew upgrade`

This setup enables the agent to:
- Build web apps (React, Vue, Angular, Next.js, etc.)
- Build mobile apps (React Native, Flutter, native iOS/Android)
- Work with any database (PostgreSQL, MySQL, MongoDB, Redis)
- Deploy to any cloud provider
- Generate SSL certificates
- Run Docker containers
- Create and manage Git repositories
- Test with real browsers
- Process media files
- And much more...

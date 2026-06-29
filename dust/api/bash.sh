#!/usr/bin/env bash
# setup_env.sh - Cross-Runtime Provisioning and Dependency Alignment Script

set -eo pipefail

echo "=== [1/4] Validating Core System Engines ==="
# Verify necessary interpreters are present on the local system
command -v ruby >/dev/null 2>&1 || { echo "❌ Error: Ruby is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Error: Python3 is required but not installed."; exit 1; }

echo "=== [2/4] Setting Up Ruby Dependencies ==="
# Initialize and sync the Ruby dependency architecture
if [ -f "Gemfile" ]; then
    bundle config set --local path 'vendor/bundle'
    bundle install
else
    echo "⚠️ Gemfile not detected. Installing base system gems manually..."
    gem install bundler --no-document
    gem install eth rspec standard --no-document
fi

echo "=== [3/4] Structuring Virtual Python Inference Box ==="
# Protect host systems by creating an isolated virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pipeline package managers
pip install --upgrade pip setuptools wheel

# Install required mathematical modules and compiler dependencies 
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not detected. Compiling default binary dependencies..."
    pip install numpy pandas cython fastapi uvicorn
fi

echo "=== [4/4] Syncing System Path Environment Envelopes ==="
# Explicitly anchor cross-runtime references inside a local workspace profile
cat << 'EOF' > .env
# Q-lang System Path Bindings
export PYTHONPATH="${PYTHONPATH}:${PWD}:${PWD}/Learning_loop"
export RUBYLIB="${RUBYLIB}:${PWD}:${PWD}/Core:${PWD}/Engine"
export Q_ENV="development"
export CONFIG_PATH="./etc/system.conf"
EOF

echo "✅ Environment configured successfully!"
echo "👉 Run: 'source .env && source .venv/bin/activate' to enter your shell space."

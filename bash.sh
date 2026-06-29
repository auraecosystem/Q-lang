git clone https://github.com/Homebrew/homebrew-brew-vulns
cd homebrew-brew-vulns
bin/setup
rake test
#!/usr/bin/env bash
# bash.sh - Q-lang Automated Core Verification CI Script

set -eo pipefail

echo "=== [1/3] Loading Aura Ecosystem Configuration ==="
export Q_ENV="test"
export CONFIG_PATH="./etc/system.conf"

echo "=== [2/3] Executing Parser & AST Integrity Tests ==="
# Calls the Ruby engine core to parse example .q scripts
ruby ./Core/test_parser.rb ./example/Program.pq

echo "=== [3/3] Testing Unknown Object Lifecycle & Loop ==="
# Feeds a dummy raw prototype through the Python learning inference loops
python3 ./Learning_loop/test_learning.py ./prototype/.anancondq

echo ">>> All Semantic Integrity Tests Passed Successfully <<<"

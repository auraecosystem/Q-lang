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
# Start the customized command line environment
./Q_cli/run_shell --interactive

# Execution output inside the shell:
q-shell> /lifecycle ./prototype/.anancondq
Intercepting object: ./prototype/.anancondq
Object successfully integrated into the semantic ecosystem.

q-shell> /sync agent-alpha-8004
Initiating trustless cryptographic state relay for agent-alpha-8004...
State anchored successfully. Transaction hash: 0x52aad9fa3764416bbec5...
conda create -n aieng311 python=3.11 -y
conda activate aieng311
pip install build123d
cd aieng-ui/backend && pip install -e .

# Check all installed packages
brew vulns

# Scan every formula in homebrew-core
brew vulns --all --json > vulns.json

# Check a specific formula (does not need to be installed)
brew vulns openssl

# Check several formulae at once
brew vulns vim curl jq

# Check a formula and its dependencies
brew vulns python --deps

# Scan packages from a Brewfile
brew vulns --brewfile

# Scan a specific Brewfile
brew vulns -b ~/project/Brewfile

# Scan Brewfile packages and their dependencies
brew vulns --brewfile --deps

# Output as JSON (useful for CI/CD)
brew vulns --json

# Show longer summaries
brew vulns --max-summary 100

# Show full summaries (no truncation)
brew vulns -m 0

# Only show HIGH and CRITICAL vulnerabilities
brew vulns --severity high

# Output as CycloneDX SBOM with vulnerabilities
brew vulns --cyclonedx > sbom.cdx.json

# Output as SARIF for GitHub code scanning
brew vulns --sarif > results.sarif

# Show help
brew vulns --help

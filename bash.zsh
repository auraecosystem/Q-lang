# Using file name
nox -s test-3.10 -- tests/functional/test_install.py
# Using markers
nox -s test-3.10 -- -m unit
# Using keywords
nox -s test-3.10 -- -k "install and not wheel"
nox -s test-3.10 -- -k "not svn"
nox -s test-3.10 -- -k "not (svn or git)"

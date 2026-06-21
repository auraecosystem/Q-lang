scripts:{x*x}
language:{x*x}
analyze:{x*x}

detect "*.py"
analyze "./project"
run "./main.py"

files:{
    "*.name":{x*x}
}

detect:{
    "*.py" => python
    "*.rs" => rust
    "*" => unknown
}

# DNSPECT

**Professional DNS Lookup CLI Tool using Python, Typer & Rich.**

---

## Features

- Lookup A, MX, NS, TXT, CNAME, SOA records  
- Reverse DNS lookup (IP → hostname)  
- Trace DNS resolution path from root to authoritative servers  
- Shows response time for each query  
- Beautiful terminal output with Rich tables and colors  

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yumna-ux/Dnspect.git
cd Dnspect

# Create a virtual environment and activate it
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Lookup DNS records

```bash
python -m dnspect.cli lookup google.com --all
python -m dnspect.cli lookup google.com --record A,MX
```

### Reverse DNS lookup

```bash
python -m dnspect.cli reverse 8.8.8.8
```

### Trace DNS resolution

```bash
python -m dnspect.cli trace google.com
```

---

## Author

Yumna Mohammed  
Cybersecurity & Technology Enthusiast

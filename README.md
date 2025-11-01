# StatForge

StatForge is a modular Python analytics engine for college football metrics. 
It integrates the [CollegeFootballData API](https://collegefootballdata.com) 
to calculate and adjust team performance indicators such as **Simple Rating 
System (SRS)**, **Predicted Points Added (PPA)**, and **Havoc Rate**.

It combines these into a single **adjusted SRS line** for each matchup.

---

## Features

- **SRS** — Computes baseline team strength and raw matchup odds.  
- **PPA** — Measures offensive and defensive play efficiency.  
- **Havoc** — Evaluates how disruptive a defense is based on negative plays.  
- **Adjusted Model** — Merges SRS, PPA, and Havoc for a more complete team comparison.  
- **Modular Design** — Each metric runs independently, connected through `main.py`.  

StatForge performs best during the **mid-to-late regular season**, when enough game data has accumulated to stabilize team efficiency metrics.

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/tdeluca06/statforge.git
cd statforge
```

### 2. Install dependencies
``` bash
pip install -r requirements.txt
```

### 3. Configure your API key
Statforge expects a .env file in the **root** of the project.

```ini
API_KEY=your_api_key_here
```

### 4. Configure season year
The season year is set in config.py, not in the environment variable.

## Usage

Run the entrypoint and provide the week:
```bash
python main.py
```

Example:
```yaml
Enter the week you need data for:
  7
Adjusted SRS Odds:
Texas vs Oklahoma: 5.73
Georgia vs Tennessee: 8.44
```
# neuromag_triggers

🧠 A lightweight Python module to extract **digital triggers** from **Neuromag analog STI lines** (STI001–STI006), accounting for jitter and hardware timing constraints.

---

## 🚀 What it does

- Converts 6 analog STI channels into **digital binary codes**
- Detects only the **rising edges**
- Applies a **refractory period** (e.g. 50 ms) to avoid repeated triggers
- Returns a `pandas.DataFrame` with **sample indices and trigger values**

Ideal for Neuromag 122 MEG systems using hardware-based binary-coded triggers.

---

## 📦 Installation

Clone the repository and install it in **editable mode** (modern `src/` layout):

```bash
git clone https://github.com/YOUR_USERNAME/neuromag_triggers.git
cd neuromag_triggers
uv pip install -e .
```

> If you don't have `uv`, you can still use regular pip:
> ```bash
> pip install -e .
> ```

---

## 🧩 Usage

```python
from neuromag_triggers import get_triggers_from_raw
import mne

# Load your raw file
raw = mne.io.read_raw_fif("your_data.fif", preload=True)

# Extract triggers from STI001–STI006
trigger_df = get_triggers_from_raw(raw, threshold=0.5, refractory_ms=50)

print(trigger_df.head())
```

---

## 📘 Output

The function returns a `pandas.DataFrame` like this:

| sample_index | trigger_value |
|:------------:|:-------------:|
| 12345        | 5             |
| 18765        | 7             |
| ...          | ...           |

Each value represents the **binary combination** detected from rising edges:
- STI001 → bit 0 → value `1`
- STI002 → bit 1 → value `2`
- STI003 → bit 2 → value `4`
- … up to STI006 → value `32`

---

## 🛠 Parameters

| Argument         | Type          | Default | Description |
|------------------|---------------|---------|-------------|
| `raw`            | `mne.io.Raw`   | —       | Raw MEG data object with STI channels |
| `threshold`      | `float`        | `0.5`   | Threshold to binarize analog voltages |
| `refractory_ms`  | `int`          | `50`    | Time (in ms) to suppress triggers after each event |

---

## 📁 Folder Structure

```text
neuromag_triggers/
├── LICENSE
├── README.md
├── pyproject.toml
├── src/
│   └── neuromag_triggers/
│       ├── __init__.py
│       └── core.py          # Main trigger extraction logic
└── tests/                   # (optional) unit tests
```

---

## 📄 License

MIT License — feel free to use, modify, and share.

---

## ✨ Acknowledgments

Created by [André Rupp](https://github.com/YOUR_USERNAME) to support robust MEG experiments using Neuromag systems.

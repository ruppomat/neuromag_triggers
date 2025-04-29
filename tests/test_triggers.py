import numpy as np
import mne
import pytest
from neuromag_triggers import get_triggers_from_raw

def test_get_triggers_from_raw_basic():
    """Test trigger extraction from simple simulated Raw data (numpy array version)."""

    # Create 2 seconds of fake data at 1000 Hz
    sfreq = 1000  # Sampling frequency
    n_times = sfreq * 2
    times = np.arange(n_times) / sfreq

    # Create 6 channels for STI001–STI006, all zeros
    sti_data = np.zeros((6, n_times))

    # Simulate rising edges
    sti_data[0, 500] = 1.0  # STI001
    sti_data[1, 500] = 1.0  # STI002
    sti_data[2, 1500] = 1.0 # STI003

    # Create Raw object
    info = mne.create_info(
        ch_names=["STI 001", "STI 002", "STI 003", "STI 004", "STI 005", "STI 006"],
        sfreq=sfreq,
        ch_types=["misc"] * 6
    )
    raw = mne.io.RawArray(sti_data, info)

    # Call your function
    trigger_array, _ = get_triggers_from_raw(raw, threshold=0.5, refractory_ms=50)

    # Check that array is not empty
    assert trigger_array.size > 0, "No triggers found!"

    # Check trigger value at sample 500
    trigger_500 = trigger_array[500]
    assert trigger_500 == 3, f"Expected trigger 3 at sample 500, got {trigger_500}"

    # Check trigger value at sample 1500
    trigger_1500 = trigger_array[1500]
    assert trigger_1500 == 4, f"Expected trigger 4 at sample 1500, got {trigger_1500}"

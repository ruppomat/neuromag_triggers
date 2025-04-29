import numpy as np
import pandas as pd
import mne


def get_triggers_from_raw(raw, threshold=0.5, refractory_ms=50):
    """
    Detect rising digital triggers from 6 STI channels in a Neuromag system.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw MEG recording.
    threshold : float, optional
        Threshold to binarize analog STI lines, by default 0.5
    refractory_ms : int, optional
        Refractory period in ms to suppress multiple detections, by default 50

    Returns
    -------
    digital_trigger : np.ndarray
        1D array of trigger codes at each sample (0 where no trigger)
    trigger_events_df : pd.DataFrame
        DataFrame with 'sample_index' and 'trigger_value' columns
    """

    def _detect_triggers(sti_binary, sfreq):
        rising_edges = np.diff(sti_binary, axis=0, prepend=0) == 1
        bit_weights = np.array([1, 2, 4, 8, 16, 32])
        digital_trigger = np.zeros(sti_binary.shape[0], dtype=int)

        refractory_samples = int((refractory_ms / 1000) * sfreq)
        last_trigger_idx = -refractory_samples - 1

        for i in range(sti_binary.shape[0]):
            if i - last_trigger_idx < refractory_samples:
                continue
            code = np.dot(rising_edges[i], bit_weights)
            if code > 0:
                digital_trigger[i] = code
                last_trigger_idx = i

        return digital_trigger

    # Get 6 STI channels
    sti_picks = mne.pick_channels(
        raw.info["ch_names"], include=[f"STI 00{i}" for i in range(1, 7)]
    )
    sti_data = raw.get_data(picks=sti_picks).T  # shape: (n_samples, 6)
    sti_binary = (sti_data > threshold).astype(int)

    sfreq = raw.info["sfreq"]
    digital_trigger = _detect_triggers(sti_binary, sfreq)

    trigger_events_df = pd.DataFrame(
        {
            "sample_index": np.nonzero(digital_trigger)[0],
            "trigger_value": digital_trigger[digital_trigger > 0],
        }
    )

    return digital_trigger, trigger_events_df

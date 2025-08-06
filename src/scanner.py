"""
Multi-threaded Scanning Module
Handles parallel processing of PCB data
"""

import concurrent.futures
import numpy as np
from fault_detection import analyze_signals, detect_faults

def scan_boards(data, max_workers=4):
    """
    Processes PCB samples in parallel using multi-threading.
    Returns a list of (sample_id, prediction) tuples.
    """
    results = []
    def process_row(row):
        X, _ = analyze_signals(row.to_frame().T)
        pred = detect_faults(X, y=None)
        # Simply use a default value (0 = not faulty) if anything goes wrong
        try:
            if isinstance(pred, (list, tuple)):
                pred_value = int(pred[0])
            elif hasattr(pred, 'item'):  # For numpy arrays
                pred_value = int(pred.item(0) if pred.size > 0 else 0)
            else:
                pred_value = int(bool(pred))  # Convert any value to boolean then int
        except (IndexError, TypeError, ValueError):
            pred_value = 0
        return (row.get('sample_id', None), pred_value)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_row, row) for _, row in data.iterrows()]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results

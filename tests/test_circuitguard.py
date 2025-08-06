# CircuitGuard Test Suite
# Add unit and integration tests for each module here

def test_import_data():
    from src.data_acquisition import import_data
    import os
    sample_file = os.path.join(os.path.dirname(__file__), '../data/sample_pcb_data.csv')
    df = import_data(sample_file)
    assert not df.empty, "DataFrame should not be empty"
    assert 'voltage' in df.columns, "Missing expected column 'voltage'"
    assert 'faulty' in df.columns, "Missing expected column 'faulty'"
    print("test_import_data passed.")

def test_signal_analysis_and_fault_detection():
    from src.data_acquisition import import_data
    from src.fault_detection import analyze_signals, detect_faults
    import os
    sample_file = os.path.join(os.path.dirname(__file__), '../data/sample_pcb_data.csv')
    df = import_data(sample_file)
    X, y = analyze_signals(df)
    preds, accuracy = detect_faults(X, y)
    assert accuracy > 0.5, f"Accuracy too low: {accuracy}"
    print(f"test_signal_analysis_and_fault_detection passed. Accuracy: {accuracy:.2f}")

def test_detect_faults():
    # TODO: Implement test for fault detection
    pass

def test_multi_threaded_scanning():
    from src.data_acquisition import import_data
    from src.scanner import scan_boards
    import os
    sample_file = os.path.join(os.path.dirname(__file__), '../data/sample_pcb_data.csv')
    df = import_data(sample_file)
    results = scan_boards(df, max_workers=2)
    assert len(results) == len(df), "Not all samples processed"
    print(f"test_multi_threaded_scanning passed. Results: {results}")

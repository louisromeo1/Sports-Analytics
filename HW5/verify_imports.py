try:
    import nfl_data_py as nfl
    print("nfl_data_py imported successfully.")
except ImportError as e:
    print(f"Failed to import nfl_data_py: {e}")

try:
    import pandas as pd
    print("pandas imported successfully.")
except ImportError as e:
    print(f"Failed to import pandas: {e}")

try:
    import matplotlib.pyplot as plt
    print("matplotlib imported successfully.")
except ImportError as e:
    print(f"Failed to import matplotlib: {e}")

import sys
import numpy as np
import pandas as pd

try:
	# Python 3.8+ has importlib.metadata
	from importlib.metadata import version, PackageNotFoundError
except Exception:
    version = None
    PackageNotFoundError = Exception

print("=== Python 環境動作確認 ===")
print(f"Python version: {sys.version.split()[0]}")
print(f"numpy version: {np.__version__}")
print(f"pandas version: {pd.__version__}")

pyinstaller_version = "unknown"
if version:
	try:
		pyinstaller_version = version("pyinstaller")
	except PackageNotFoundError:
		pyinstaller_version = "not installed"

print(f"pyinstaller version: {pyinstaller_version}")

import os
import sys

# Add parent directory to path so relative imports work if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import main application runner
from app import *

if __name__ == "__main__":
    pass

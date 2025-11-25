#!/usr/bin/env python
"""
Setup script to train ML models
Run this once after deployment to generate the .pkl model files
"""

import os
import sys
from train_model import train_all_models

def main():
    print("🚀 Starting ML model training...")
    print("This may take a few minutes on first deployment...")
    
    try:
        # Train all models
        train_all_models()
        print("\n✅ Models trained successfully!")
        print("Your app is now ready to use.")
        return 0
    except Exception as e:
        print(f"\n❌ Error training models: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

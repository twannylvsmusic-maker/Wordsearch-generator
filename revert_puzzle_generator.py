#!/usr/bin/env python3
"""
Revert script for puzzle generator enhancements.
This script restores the original word placement algorithm.
"""

import shutil
import os

def revert_puzzle_generator():
    """Revert puzzle_generator.py to original algorithm."""
    
    # Check if enhanced version exists
    if not os.path.exists('utils/puzzle_generator_enhanced.py'):
        print("❌ Enhanced version not found. Nothing to revert.")
        return False
    
    # Check if original backup exists
    if not os.path.exists('utils/puzzle_generator_original.py'):
        print("⚠️  Original backup not found. Cannot revert safely.")
        print("   The enhanced version will be kept as-is.")
        return False
    
    try:
        # Restore original version
        shutil.copy('utils/puzzle_generator_original.py', 'utils/puzzle_generator.py')
        print("✅ Successfully reverted to original puzzle generator algorithm.")
        print("   Square shapes and non-square shapes now use the same algorithm.")
        return True
        
    except Exception as e:
        print(f"❌ Error reverting: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Reverting puzzle generator to original algorithm...")
    revert_puzzle_generator()



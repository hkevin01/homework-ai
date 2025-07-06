#!/usr/bin/env python3
"""
Quick test to verify PyInstaller can build our GUI
Creates a minimal test executable
"""

import os
import subprocess
import sys


def test_build():
    """Test PyInstaller setup with a minimal script."""
    print("🧪 Testing PyInstaller setup...")
    
    # Create a minimal test script
    test_script = """
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Test Build")
    label = QLabel("Build test successful!")
    window.resize(300, 100)
    print("✅ Test executable created successfully!")
    # Don't actually show the GUI in test
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
    
    with open('test_build.py', 'w') as f:
        f.write(test_script)
    
    try:
        # Test PyInstaller with minimal script
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--name', 'test-build',
            '--distpath', 'test_dist',
            'test_build.py'
        ]
        
        print("🔨 Running test build...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            if os.path.exists('test_dist/test-build'):
                print("✅ PyInstaller test successful!")
                print("✅ Build system is ready to use")
                return True
            else:
                print("⚠️  Build completed but executable not found")
                return False
        else:
            print("❌ PyInstaller test failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Build test timed out")
        return False
    except Exception as e:
        print(f"❌ Build test error: {e}")
        return False
    finally:
        # Cleanup
        for cleanup_item in ['test_build.py', 'test-build.spec', 'build', 'test_dist']:
            if os.path.exists(cleanup_item):
                if os.path.isdir(cleanup_item):
                    import shutil
                    shutil.rmtree(cleanup_item)
                else:
                    os.remove(cleanup_item)

if __name__ == "__main__":
    if test_build():
        print("\n🎉 Build system is ready!")
        print("💡 You can now run: ./run.sh build")
    else:
        print("\n❌ Build system needs troubleshooting")
        sys.exit(1)

import subprocess
import sys

python_exe = sys.executable
subprocess.run([python_exe, "flatten.py"])
subprocess.run([python_exe, "aggregate.py"])
subprocess.run([python_exe, "filter.py"])
subprocess.run([python_exe, "count.py"])
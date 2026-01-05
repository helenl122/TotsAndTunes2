import subprocess
import sys

python_exe = sys.executable
subprocess.run([python_exe, "comparison_analysis/pivot_and_sample.py"])
subprocess.run([python_exe, "comparison_analysis/plot_distribution.py"])
subprocess.run([python_exe, "coder_analysis/yes_reasons.py"])
subprocess.run([python_exe, "plot_counts.py"])
subprocess.run([python_exe, "plot_diffs.py"])

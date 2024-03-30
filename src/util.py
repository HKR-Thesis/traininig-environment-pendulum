import subprocess
import threading
import platform

benchmark_scripts = {
    'embedded': 'src/benchmarking/jetson_metrics.py',
    'server': 'src/benchmarking/server_metrics.py'
}

def print_pipe(stream, prefix=""):
    """
    Prints the lines from the given stream with an optional prefix.

    Args:
        stream (file-like object): The stream to read lines from.
        prefix (str, optional): The prefix to add to each line. Defaults to "".
    """
    while True:
        line = stream.readline()
        if not line:
            break
        print(f"{prefix}: {line.strip()}")

def monitor_subprocess(proc, benchmark_proc=None):
    """
    Monitors the given subprocess and terminates the benchmark process if it is still running.

    Args:
        proc (subprocess.Popen): The subprocess to monitor.
        benchmark_proc (subprocess.Popen, optional): The benchmark process to terminate if `proc` is finished.

    Returns:
        None
    """
    proc.wait()
    if proc.poll() is not None and benchmark_proc is not None:
        if benchmark_proc.poll() is None:
            benchmark_proc.terminate()

def get_metrics_path():
    """
    Returns the path to the metrics based on the current system.

    Returns:
        str: The path to the metrics.
    """
    uname = platform.uname()
    if uname.system == 'Linux' and 'tegra' in uname.release:
        return benchmark_scripts['embedded']
    elif uname.system == 'Linux' and 'tegra' not in uname.release:
        return benchmark_scripts['server']
    return None

def run_process(command, output_prefix):
    """
    Run a given command as a subprocess and print its output and error streams in separate threads.
    
    Args:
    - command: List of command line arguments to be executed.
    - output_prefix: Prefix string to be added to the output for identification.
    
    Returns:
    - process: The subprocess.Popen object for further manipulation or inspection.
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    output_thread = threading.Thread(target=print_pipe, args=(process.stdout, f"{output_prefix} Output"))
    error_thread = threading.Thread(target=print_pipe, args=(process.stderr, f"{output_prefix} Error"))
    output_thread.start()
    error_thread.start()
    
    return process
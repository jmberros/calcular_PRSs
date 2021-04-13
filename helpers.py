import subprocess
import time
from contextlib import contextmanager
from os.path import isfile, getsize, dirname
import stat
import os

import requests
from termcolor import cprint, colored
from humanfriendly import format_timespan

def check_output_exists(fp):
    if isfile(fp) or isfile(fp + ".gz"):
        print(f"Output exists:", colored(f"{fp}[.gz]", "green"))
        return True
    else:
        print(f"Output absent:", colored(f"{fp}[.gz]", "red"))
        return False

def gzip(fp):
    run_shell_command(f"gzip -vf {fp}")

def gunzip(fp):
    run_shell_command(f"gunzip -vf {fp}")

def make_executable(fp):
    # Taken from: https://stackoverflow.com/a/12792002/1664522
    st = os.stat(fp)
    os.chmod(fp, st.st_mode | stat.S_IEXEC)

def file_is_present(fp):
    if isfile(fp) and getsize(fp):
        print("File present:", colored(fp, "green"))
        return True
    else:
        print("File absent:", colored(fp, "red"))
        return False

def raise_if_missing(fp):
    if not file_is_present(fp):
        cprint(f"Missing required input: {fp}", "red")
        exit()

def download_url_to(url, fp):
    if file_is_present(fp):
        return

    print(f"Downloading: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Status {response.status_code} :(")
        return

    print(f"Write to: {fp}")
    os.makedirs(dirname(fp), exist_ok=True)
    with open(fp, "wb") as out_file:
        out_file.write(response.content)

    print("---")

def run_shell_command(command, verbose=True):
    """Run a *command* (string) in the shell. Return the output."""
    colored_command = colored(command, 'magenta')

    if verbose:
        print(f'Running:\n\n  {colored_command} \n')

    timer = Timer()
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    )

    output_lines = []

    if verbose:
        print(f'Output:\n')

    while True:
        output = process.stdout.readline()
        output = output.decode('utf-8')
        command_finished = (output == '' and process.poll() is not None)
        if command_finished:
            break
        if verbose:
            cprint('  ' + output.rstrip("\n"), 'blue')
        output_lines.append(output)

    if verbose:
        timer.stop()
        print(f"\nTook {timer.elapsed_time_formatted}\n")

    return output_lines

class Timer:
    """
    Usage:
    >>> timer = Timer()
    >>> timer.start()
    >>> do_some_computation()
    >>> timer.stop_and_log()
    # Done! Took: 10 seconds
    >>> with timer_running():
    >>>     do_some_computation()
    # Done! Took: 9 seconds
    """

    def __init__(self):
        self.start()

    def start(self, task_name=None):
        self.reset()
        self.start_time = time.time()
        self.task_name = task_name

    def reset(self):
        self.stop_time = None
        self.elapsed_time = None
        self.elapsed_time_formatted = None

    def stop(self):
        self.stop_time = time.time()
        self.elapsed_time = self.stop_time - self.start_time
        self.elapsed_time_formatted = format_timespan(self.elapsed_time)

    def log(self, message):
        txt = f"{message} {self.elapsed_time_formatted}"
        if self.task_name:
            txt = f"[{self.task_name}] {txt}"
        print(txt)

    def stop_and_log(self, message='Done! Took:'):
        self.stop()
        self.log(message)

    def stop_log_and_restart(self, message='Done! Took:', task_name=None):
        self.stop_and_log(message)
        self.start(task_name=task_name)

@contextmanager
def timer_running(task_name=None, log=True):
    timer = Timer()
    timer.start(task_name=task_name)

    yield

    if log:
        timer.stop_and_log()
    else:
        timer.stop()

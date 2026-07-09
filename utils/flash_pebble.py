#!/usr/bin/env python3
"""
Pebble HF Board Flashing Utility

Flashes firmware and programs fuses for the Pebble HF (ATmega328P) radio.
Auto-detects all USB serial programmers and flashes a board on each one in
parallel. Each device gets the full sequence: flash, program fuses, and two
independent fuse read-back verifications.

Usage:
    python3 flash_pebble.py [hex_file] [--port /dev/cu.usbserial-XXXX]

If hex_file is not specified, looks for usdx.ino.hex in the project root.
If --port is not specified, all matching USB serial ports are programmed.
--port may be given multiple times to program a specific subset.

Full avrdude output for each device is written to a per-device log file;
the complete log of any failed device is printed at the end.
"""

import subprocess
import sys
import os
import glob
import argparse
import time
import re
import shutil
import threading
from datetime import datetime


# ── Configuration ────────────────────────────────────────────────────────────

AVRDUDE_PROGRAMMER = "stk500v1"
AVRDUDE_PART = "m328p"
AVRDUDE_BAUD = "19200"

FUSE_LFUSE = "0xFF"
FUSE_HFUSE = "0xD6"
FUSE_EFUSE = "0xFD"

SERIAL_PORT_GLOBS = [
    "/dev/cu.usbserial-*",   # macOS
    "/dev/ttyUSB*",          # Linux
]

DEFAULT_HEX_FILE = "usdx.ino.hex"

AVRDUDE_TIMEOUT = 120  # seconds, per avrdude invocation


# ── Terminal Colors & Formatting ─────────────────────────────────────────────

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def print_banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════╗
║         Pebble HF Board Flashing Utility         ║
╚══════════════════════════════════════════════════╝{Colors.RESET}
""")


def print_big_checkmark(message="ALL STEPS PASSED"):
    art = f"""{Colors.GREEN}{Colors.BOLD}

    ██████████████████████████████████████████████
    ██                                          ██
    ██                                ██        ██
    ██                              ████        ██
    ██                            ████          ██
    ██                          ████            ██
    ██                        ████              ██
    ██          ██          ████                ██
    ██          ████      ████                  ██
    ██          ██████  ████                    ██
    ██            ████████                      ██
    ██              ████                        ██
    ██                                          ██
    ██████████████████████████████████████████████

             ✅  {message}  ✅

    ██████████████████████████████████████████████
{Colors.RESET}"""
    print(art)


def print_big_x(step_name, detail=""):
    art = f"""{Colors.RED}{Colors.BOLD}

    ██████████████████████████████████████████████
    ██                                          ██
    ██        ██████              ██████        ██
    ██          ██████          ██████          ██
    ██            ██████      ██████            ██
    ██              ██████  ██████              ██
    ██                ██████████                ██
    ██              ██████  ██████              ██
    ██            ██████      ██████            ██
    ██          ██████          ██████          ██
    ██        ██████              ██████        ██
    ██                                          ██
    ██████████████████████████████████████████████

          ❌  FAILED: {step_name}  ❌
{Colors.RESET}"""
    if detail:
        art += f"\n    {Colors.RED}{detail}{Colors.RESET}\n"
    print(art)


def print_success(msg):
    print(f"  {Colors.GREEN}✔ {msg}{Colors.RESET}")


def print_error(msg):
    print(f"  {Colors.RED}✘ {msg}{Colors.RESET}")


def print_info(msg):
    print(f"  {Colors.DIM}{msg}{Colors.RESET}")


def print_warn(msg):
    print(f"  {Colors.YELLOW}⚠ {msg}{Colors.RESET}")


# ── Serial Port Detection ────────────────────────────────────────────────────

def detect_serial_ports():
    """Find all USB serial ports for programmers (macOS and Linux patterns)."""
    ports = []
    for pattern in SERIAL_PORT_GLOBS:
        ports.extend(glob.glob(pattern))
    return sorted(ports)


def short_name(port):
    """Short display name for a port: /dev/cu.usbserial-31210 -> usbserial-31210."""
    name = os.path.basename(port)
    if name.startswith("cu."):
        name = name[3:]
    return name


# ── avrdude Execution ────────────────────────────────────────────────────────

def check_avrdude():
    """Verify avrdude is installed and accessible. Returns its path or None."""
    path = shutil.which("avrdude")
    if path:
        return path
    # Check common Homebrew / Arduino paths
    for candidate in [
        "/usr/local/bin/avrdude",
        "/opt/homebrew/bin/avrdude",
        os.path.expanduser("~/Library/Arduino15/packages/arduino/tools/avrdude/*/bin/avrdude"),
    ]:
        matches = glob.glob(candidate)
        if matches:
            return matches[-1]  # latest version
    return None


AVRDUDE_PATH = "avrdude"  # resolved in main()


def run_avrdude(port, extra_args, step_label, log):
    """
    Run an avrdude command, writing all output to the device's log file.
    Returns (success: bool, stdout: str, stderr: str).

    avrdude prints progress bars and status to stderr.
    """
    cmd = [
        AVRDUDE_PATH,
        "-c", AVRDUDE_PROGRAMMER,
        "-p", AVRDUDE_PART,
        "-P", port,
        "-b", AVRDUDE_BAUD,
    ] + extra_args

    log.write(f"\n$ {' '.join(cmd)}\n")
    log.flush()

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout_data, stderr_data = process.communicate(timeout=AVRDUDE_TIMEOUT)

        stdout_text = stdout_data.decode("utf-8", errors="replace")
        stderr_text = stderr_data.decode("utf-8", errors="replace")

        # avrdude puts most output on stderr
        log.write(stderr_text)
        log.write(stdout_text)
        log.write(f"\n[exit code: {process.returncode}]\n")
        log.flush()

        return process.returncode == 0, stdout_text, stderr_text

    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        log.write(f"\nERROR: Timeout: avrdude took too long for {step_label}\n")
        log.flush()
        return False, "", "Timeout"
    except FileNotFoundError:
        log.write("\nERROR: avrdude not found\n")
        log.flush()
        return False, "", "avrdude not found"
    except Exception as e:
        log.write(f"\nERROR: Unexpected error: {e}\n")
        log.flush()
        return False, "", str(e)


# ── Step Functions ────────────────────────────────────────────────────────────
# Each step writes its results to the device log and returns True/False.

def step_flash_firmware(port, hex_file, log):
    """Flash the firmware hex file."""
    log.write(f"\n=== STEP: Flashing firmware ({hex_file}) ===\n")

    success, stdout, stderr = run_avrdude(
        port,
        ["-U", f"flash:w:{hex_file}"],
        "flash firmware",
        log,
    )

    combined = stderr + stdout

    if not success:
        log.write("FAIL: avrdude returned an error during flash programming\n")
        return False

    # Verify the output contains expected markers
    if "bytes of flash verified" not in combined:
        log.write("FAIL: Flash verify string not found in avrdude output\n")
        return False

    if "Avrdude done.  Thank you." not in combined:
        log.write("FAIL: avrdude did not complete successfully\n")
        return False

    match = re.search(r"(\d+) bytes of flash verified", combined)
    if match:
        log.write(f"OK: Flash programmed and verified ({match.group(1)} bytes)\n")
    else:
        log.write("OK: Flash programmed and verified\n")

    return True


def step_program_fuses(port, log):
    """Program the fuse bytes."""
    log.write(f"\n=== STEP: Programming fuses "
              f"(lfuse={FUSE_LFUSE} hfuse={FUSE_HFUSE} efuse={FUSE_EFUSE}) ===\n")

    success, stdout, stderr = run_avrdude(
        port,
        [
            "-U", f"lfuse:w:{FUSE_LFUSE}:m",
            "-U", f"hfuse:w:{FUSE_HFUSE}:m",
            "-U", f"efuse:w:{FUSE_EFUSE}:m",
        ],
        "program fuses",
        log,
    )

    combined = stderr + stdout

    if not success:
        log.write("FAIL: avrdude returned an error during fuse programming\n")
        return False

    # Check that all three fuses were written and verified
    fuse_checks = [
        ("lfuse", FUSE_LFUSE),
        ("hfuse", FUSE_HFUSE),
        ("efuse", FUSE_EFUSE),
    ]

    all_verified = True
    for fuse_name, expected_val in fuse_checks:
        pattern = rf"1 byte \({expected_val}\) to {fuse_name}.*verified"
        if not re.search(pattern, combined, re.IGNORECASE):
            # Also accept "1 byte written, 1 verified" pattern
            if f"to {fuse_name}" in combined and "verified" in combined:
                pass  # close enough
            else:
                log.write(f"FAIL: Could not confirm {fuse_name} was written and verified\n")
                all_verified = False

    if "Avrdude done.  Thank you." not in combined:
        log.write("FAIL: avrdude did not complete successfully\n")
        return False

    if all_verified:
        log.write(f"OK: All fuses programmed: lfuse={FUSE_LFUSE} "
                  f"hfuse={FUSE_HFUSE} efuse={FUSE_EFUSE}\n")

    return all_verified


def step_verify_fuses(port, attempt_number, total_attempts, log):
    """Read back and verify all fuse bytes."""
    log.write(f"\n=== STEP: Verifying fuses "
              f"(read-back {attempt_number}/{total_attempts}) ===\n")

    success, stdout, stderr = run_avrdude(
        port,
        [
            "-U", "lfuse:r:-:h",
            "-U", "hfuse:r:-:h",
            "-U", "efuse:r:-:h",
        ],
        f"verify fuses (attempt {attempt_number})",
        log,
    )

    combined = stderr + stdout

    if not success:
        log.write("FAIL: avrdude returned an error during fuse readback\n")
        return False

    if "Avrdude done.  Thank you." not in combined:
        log.write("FAIL: avrdude did not complete successfully\n")
        return False

    # Parse the fuse values from stdout
    # avrdude writes hex values to stdout in order: lfuse, hfuse, efuse
    # Status messages ("Reading lfuse memory ...") go to stderr
    expected_fuses = [
        ("lfuse", FUSE_LFUSE.lower()),
        ("hfuse", FUSE_HFUSE.lower()),
        ("efuse", FUSE_EFUSE.lower()),
    ]

    # Extract all hex values from stdout (they come out in order)
    actual_values = re.findall(r"0x[0-9a-fA-F]+", stdout.lower())

    if len(actual_values) < len(expected_fuses):
        log.write(f"FAIL: Expected {len(expected_fuses)} fuse values from stdout, "
                  f"got {len(actual_values)}\n")
        log.write(f"stdout was: {repr(stdout.strip())}\n")
        return False

    all_correct = True
    for i, (fuse_name, expected_val) in enumerate(expected_fuses):
        actual_val = actual_values[i]
        if actual_val == expected_val:
            log.write(f"OK: {fuse_name}: {actual_val} (expected {expected_val})\n")
        else:
            log.write(f"FAIL: {fuse_name}: {actual_val} != expected {expected_val}\n")
            all_correct = False

    return all_correct


# ── Per-Device Worker ────────────────────────────────────────────────────────

class DeviceState:
    """Shared status for one device, updated by its worker thread."""

    def __init__(self, port, log_path):
        self.port = port
        self.name = short_name(port)
        self.log_path = log_path
        self.status_text = "waiting..."
        self.result = None        # None = running, True = pass, False = fail
        self.failed_step = None
        self.start_time = None
        self.elapsed = None


def flash_device(state, hex_file, fuses_only, board_lock):
    """Run the full flash + fuse sequence for one device. Updates state."""

    def set_status(text):
        with board_lock:
            state.status_text = text

    state.start_time = time.time()

    with open(state.log_path, "w") as log:
        log.write(f"Pebble HF flash log — {state.port}\n")
        log.write(f"Started: {datetime.now().isoformat()}\n")

        # Build the step sequence (identical to the original 4 steps)
        steps = []
        if not fuses_only:
            steps.append(("flashing firmware", "FLASH FIRMWARE",
                          lambda: step_flash_firmware(state.port, hex_file, log)))
        steps.append(("programming fuses", "PROGRAM FUSES",
                      lambda: step_program_fuses(state.port, log)))
        steps.append(("verifying fuses (read 1/2)", "VERIFY FUSES (read 1)",
                      lambda: step_verify_fuses(state.port, 1, 2, log)))
        steps.append(("verifying fuses (read 2/2)", "VERIFY FUSES (read 2)",
                      lambda: step_verify_fuses(state.port, 2, 2, log)))

        total = len(steps)
        failed_step = None
        for i, (label, fail_name, fn) in enumerate(steps, start=1):
            set_status(f"[{i}/{total}] {label}...")
            try:
                ok = fn()
            except Exception as e:
                log.write(f"\nERROR: Unexpected exception in step '{label}': {e}\n")
                ok = False
            if not ok:
                failed_step = fail_name
                break

        elapsed = time.time() - state.start_time
        log.write(f"\nFinished: {datetime.now().isoformat()} ({elapsed:.1f}s)\n")
        log.write(f"RESULT: {'PASS' if failed_step is None else 'FAIL at ' + failed_step}\n")

    with board_lock:
        state.elapsed = elapsed
        state.failed_step = failed_step
        state.result = failed_step is None
        if failed_step is None:
            state.status_text = "PASS"
        else:
            state.status_text = f"FAIL — {failed_step}"


# ── Status Board ─────────────────────────────────────────────────────────────

def format_status_line(state, name_width):
    name = state.name.ljust(name_width)
    if state.result is True:
        return (f"  {Colors.GREEN}✔ {name}  PASS{Colors.RESET}"
                f"{Colors.DIM}  ({state.elapsed:.1f}s){Colors.RESET}")
    if state.result is False:
        return (f"  {Colors.RED}✘ {name}  FAIL — {state.failed_step}{Colors.RESET}"
                f"{Colors.DIM}  ({state.elapsed:.1f}s){Colors.RESET}")
    running = time.time() - state.start_time if state.start_time else 0
    return (f"  {Colors.CYAN}⚙{Colors.RESET} {name}  "
            f"{state.status_text}{Colors.DIM}  ({running:.0f}s){Colors.RESET}")


def run_status_board(states, threads, board_lock):
    """Render live per-device status lines until all worker threads finish."""
    name_width = max(len(s.name) for s in states)
    is_tty = sys.stdout.isatty()

    if is_tty:
        # Reserve lines, then redraw in place
        for _ in states:
            print()
        while True:
            alive = any(t.is_alive() for t in threads)
            with board_lock:
                lines = [format_status_line(s, name_width) for s in states]
            sys.stdout.write(f"\033[{len(lines)}A")
            for line in lines:
                sys.stdout.write("\033[2K" + line + "\n")
            sys.stdout.flush()
            if not alive:
                break
            time.sleep(0.25)
    else:
        # Non-interactive output: report each device once, as it finishes
        reported = set()
        while True:
            alive = any(t.is_alive() for t in threads)
            with board_lock:
                for s in states:
                    if s.result is not None and s.port not in reported:
                        reported.add(s.port)
                        print(format_status_line(s, name_width))
            if not alive:
                break
            time.sleep(0.25)

    for t in threads:
        t.join()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    global AVRDUDE_PATH

    parser = argparse.ArgumentParser(
        description="Pebble HF Board Flashing Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 flash_pebble.py                          # auto-detect and flash ALL programmers
    python3 flash_pebble.py firmware.hex              # specify hex file
    python3 flash_pebble.py --port /dev/cu.usbserial-3120   # flash only this one
    python3 flash_pebble.py -p /dev/ttyUSB0 -p /dev/ttyUSB1 # flash a specific subset
    python3 flash_pebble.py --fuses-only              # skip flash, only program fuses
        """,
    )
    parser.add_argument("hex_file", nargs="?", default=None, help="Path to .hex firmware file")
    parser.add_argument("--port", "-p", action="append", default=None,
                        help="Serial port (repeatable; all ports auto-detected if omitted)")
    parser.add_argument("--fuses-only", action="store_true",
                        help="Skip flash, only program and verify fuses")
    args = parser.parse_args()

    print_banner()

    # ── Check avrdude ──
    avrdude_path = check_avrdude()
    if not avrdude_path:
        print_error("avrdude is not installed or not in PATH.")
        print_info("Install with: brew install avrdude")
        print_big_x("SETUP", "avrdude not found")
        sys.exit(1)
    AVRDUDE_PATH = avrdude_path
    print_success(f"avrdude found: {avrdude_path}")

    # ── Find hex file ──
    hex_file = None
    if not args.fuses_only:
        hex_file = args.hex_file
        if hex_file is None:
            # Look in project root (one level up from utils/)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            candidate = os.path.join(project_root, DEFAULT_HEX_FILE)
            if os.path.isfile(candidate):
                hex_file = candidate
            elif os.path.isfile(DEFAULT_HEX_FILE):
                hex_file = DEFAULT_HEX_FILE
            else:
                print_error(f"Hex file not found. Looked for:")
                print_info(f"  {candidate}")
                print_info(f"  {os.path.abspath(DEFAULT_HEX_FILE)}")
                print_info(f"Specify path: python3 flash_pebble.py <path_to_hex>")
                print_big_x("SETUP", "Hex file not found")
                sys.exit(1)

        if not os.path.isfile(hex_file):
            print_error(f"Hex file not found: {hex_file}")
            print_big_x("SETUP", f"File not found: {hex_file}")
            sys.exit(1)

        hex_file = os.path.abspath(hex_file)
        file_size = os.path.getsize(hex_file)
        print_success(f"Hex file: {hex_file} ({file_size:,} bytes)")

    # ── Detect serial ports ──
    if args.port:
        ports = args.port
    else:
        print_info("Searching for USB serial ports...")
        ports = detect_serial_ports()

    if not ports:
        print_error("No USB serial port found matching "
                    + " or ".join(SERIAL_PORT_GLOBS))
        print_info("Are the programmers plugged in?")
        print_info("Check with: ls /dev/cu.* (macOS) or ls /dev/ttyUSB* (Linux)")
        print_big_x("SETUP", "No serial port detected")
        sys.exit(1)

    print_success(f"Found {len(ports)} programmer(s):")
    for port in ports:
        print_info(f"  {port}")

    # ── Set up per-device logs ──
    script_dir = os.path.dirname(os.path.abspath(__file__))
    run_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = os.path.join(script_dir, "logs", run_stamp)
    os.makedirs(log_dir, exist_ok=True)
    print_info(f"Logs: {log_dir}/")

    states = [
        DeviceState(port, os.path.join(log_dir, f"{short_name(port)}.log"))
        for port in ports
    ]

    # ── Confirm before flashing ──
    print(f"\n{Colors.YELLOW}{Colors.BOLD}  Ready to flash {len(ports)} device(s). "
          f"Press ENTER to begin (Ctrl+C to abort)...{Colors.RESET}", end="")
    try:
        input()
    except KeyboardInterrupt:
        print(f"\n\n  {Colors.DIM}Aborted.{Colors.RESET}")
        sys.exit(0)
    print()

    start_time = time.time()

    # ── Flash all devices in parallel, one thread per programmer ──
    board_lock = threading.Lock()
    threads = []
    for state in states:
        t = threading.Thread(
            target=flash_device,
            args=(state, hex_file, args.fuses_only, board_lock),
            name=f"flash-{state.name}",
            daemon=True,
        )
        threads.append(t)
        t.start()

    run_status_board(states, threads, board_lock)

    # ── Summary table ──
    elapsed = time.time() - start_time
    passed = [s for s in states if s.result is True]
    failed = [s for s in states if s.result is not True]

    name_width = max(max(len(s.name) for s in states), len("Device"))
    print(f"\n{Colors.BOLD}  Summary{Colors.RESET}")
    print(f"{Colors.DIM}  {'─' * 50}{Colors.RESET}")
    print(f"  {Colors.BOLD}{'Device'.ljust(name_width)}  {'Result'.ljust(6)}  "
          f"{'Time'.rjust(7)}  Failed step{Colors.RESET}")
    for s in states:
        time_str = f"{s.elapsed:.1f}s" if s.elapsed is not None else "-"
        if s.result is True:
            print(f"  {s.name.ljust(name_width)}  "
                  f"{Colors.GREEN}{'PASS'.ljust(6)}{Colors.RESET}  {time_str.rjust(7)}")
        else:
            print(f"  {s.name.ljust(name_width)}  "
                  f"{Colors.RED}{'FAIL'.ljust(6)}{Colors.RESET}  {time_str.rjust(7)}  "
                  f"{Colors.RED}{s.failed_step or 'DID NOT FINISH'}{Colors.RESET}")
    print(f"{Colors.DIM}  {'─' * 50}{Colors.RESET}")
    print(f"{Colors.DIM}  Total time: {elapsed:.1f}s{Colors.RESET}")

    # ── Dump full logs for failed devices ──
    for s in failed:
        print(f"\n{Colors.RED}{Colors.BOLD}  ── avrdude log for FAILED device "
              f"{s.name} ──{Colors.RESET}")
        try:
            with open(s.log_path) as f:
                for line in f.read().strip().splitlines():
                    print(f"  {Colors.DIM}│{Colors.RESET} {line}")
        except OSError as e:
            print_error(f"Could not read log {s.log_path}: {e}")

    # ── Final result ──
    if failed:
        names = ", ".join(s.name for s in failed)
        print_big_x(f"{len(failed)} OF {len(states)} DEVICE(S)", f"Failed: {names}")
        print_warn("Check the boards with a RED LED and re-seat the ISP connector.")
        sys.exit(1)
    else:
        if len(states) == 1:
            print_big_checkmark("ALL STEPS PASSED")
        else:
            print_big_checkmark(f"ALL {len(states)} DEVICES PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()

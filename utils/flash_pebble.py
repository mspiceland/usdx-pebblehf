#!/usr/bin/env python3
"""
Pebble HF Board Flashing Utility

Flashes firmware and programs fuses for the Pebble HF (ATmega328P) radio.
Auto-detects USB serial programmer, flashes hex file, programs and verifies fuses.

Usage:
    python3 flash_pebble.py [hex_file] [--port /dev/cu.usbserial-XXXX]

If hex_file is not specified, looks for usdx.ino.hex in the project root.
If --port is not specified, auto-detects the USB serial port.
"""

import subprocess
import sys
import os
import glob
import argparse
import time
import re
import shutil


# ── Configuration ────────────────────────────────────────────────────────────

AVRDUDE_PROGRAMMER = "stk500v1"
AVRDUDE_PART = "m328p"
AVRDUDE_BAUD = "19200"

FUSE_LFUSE = "0xFF"
FUSE_HFUSE = "0xD6"
FUSE_EFUSE = "0xFD"

SERIAL_PORT_GLOB = "/dev/cu.usbserial-*"

DEFAULT_HEX_FILE = "usdx.ino.hex"


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


def print_big_checkmark():
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

             ✅  ALL STEPS PASSED  ✅

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


def print_step(number, total, description):
    print(f"\n{Colors.CYAN}{Colors.BOLD}[{number}/{total}]{Colors.RESET} {Colors.BOLD}{description}{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 50}{Colors.RESET}")


def print_success(msg):
    print(f"  {Colors.GREEN}✔ {msg}{Colors.RESET}")


def print_error(msg):
    print(f"  {Colors.RED}✘ {msg}{Colors.RESET}")


def print_info(msg):
    print(f"  {Colors.DIM}{msg}{Colors.RESET}")


def print_warn(msg):
    print(f"  {Colors.YELLOW}⚠ {msg}{Colors.RESET}")


# ── Serial Port Detection ────────────────────────────────────────────────────

def detect_serial_port():
    """Auto-detect USB serial port for the programmer."""
    ports = sorted(glob.glob(SERIAL_PORT_GLOB))

    if not ports:
        return None

    if len(ports) == 1:
        return ports[0]

    # Multiple ports found — ask the user
    print(f"  {Colors.YELLOW}Multiple USB serial ports detected:{Colors.RESET}")
    for i, port in enumerate(ports):
        print(f"    {Colors.BOLD}{i + 1}.{Colors.RESET} {port}")
    print()

    while True:
        try:
            choice = input(f"  Select port [1-{len(ports)}]: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(ports):
                return ports[idx]
        except (ValueError, KeyboardInterrupt):
            pass
        print(f"  {Colors.RED}Invalid choice. Try again.{Colors.RESET}")


# ── avrdude Execution ────────────────────────────────────────────────────────

def check_avrdude():
    """Verify avrdude is installed and accessible."""
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


def run_avrdude(port, extra_args, step_label, show_output=True):
    """
    Run an avrdude command and capture output.
    Returns (success: bool, stdout: str, stderr: str).

    avrdude prints progress bars and status to stderr.
    """
    cmd = [
        "avrdude",
        "-c", AVRDUDE_PROGRAMMER,
        "-p", AVRDUDE_PART,
        "-P", port,
        "-b", AVRDUDE_BAUD,
    ] + extra_args

    print_info(f"Running: {' '.join(cmd)}")
    print()

    try:
        # Run the process, streaming stderr in real-time (where avrdude outputs progress)
        # stdout is captured for fuse readback values
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Read output in real-time while process runs
        # avrdude writes progress to stderr; we'll collect both
        stdout_data, stderr_data = process.communicate(timeout=120)

        stdout_text = stdout_data.decode("utf-8", errors="replace")
        stderr_text = stderr_data.decode("utf-8", errors="replace")

        # avrdude puts most output on stderr
        combined = stderr_text + stdout_text

        if show_output:
            # Print the avrdude output indented
            for line in combined.strip().splitlines():
                print(f"  {Colors.DIM}│{Colors.RESET} {line}")
            print()

        return process.returncode == 0, stdout_text, stderr_text

    except subprocess.TimeoutExpired:
        process.kill()
        print_error(f"Timeout: avrdude took too long for {step_label}")
        return False, "", "Timeout"
    except FileNotFoundError:
        print_error("avrdude not found. Please install it (brew install avrdude)")
        return False, "", "avrdude not found"
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False, "", str(e)


# ── Step Functions ────────────────────────────────────────────────────────────

def step_flash_firmware(port, hex_file):
    """Flash the firmware hex file."""
    print_step(1, 4, "Flashing firmware")
    print_info(f"Hex file: {hex_file}")

    success, stdout, stderr = run_avrdude(
        port,
        ["-U", f"flash:w:{hex_file}"],
        "flash firmware",
    )

    combined = stderr + stdout

    if not success:
        print_error("avrdude returned an error during flash programming")
        return False

    # Verify the output contains expected markers
    if "bytes of flash verified" not in combined:
        print_error("Flash verify string not found in avrdude output")
        return False

    if "Avrdude done.  Thank you." not in combined:
        print_error("avrdude did not complete successfully")
        return False

    # Extract byte counts for display
    match = re.search(r"(\d+) bytes of flash verified", combined)
    if match:
        print_success(f"Flash programmed and verified ({match.group(1)} bytes)")
    else:
        print_success("Flash programmed and verified")

    return True


def step_program_fuses(port):
    """Program the fuse bytes."""
    print_step(2, 4, "Programming fuses")
    print_info(f"lfuse={FUSE_LFUSE}  hfuse={FUSE_HFUSE}  efuse={FUSE_EFUSE}")

    success, stdout, stderr = run_avrdude(
        port,
        [
            "-U", f"lfuse:w:{FUSE_LFUSE}:m",
            "-U", f"hfuse:w:{FUSE_HFUSE}:m",
            "-U", f"efuse:w:{FUSE_EFUSE}:m",
        ],
        "program fuses",
    )

    combined = stderr + stdout

    if not success:
        print_error("avrdude returned an error during fuse programming")
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
                print_error(f"Could not confirm {fuse_name} was written and verified")
                all_verified = False

    if "Avrdude done.  Thank you." not in combined:
        print_error("avrdude did not complete successfully")
        return False

    if all_verified:
        print_success(f"All fuses programmed: lfuse={FUSE_LFUSE} hfuse={FUSE_HFUSE} efuse={FUSE_EFUSE}")

    return all_verified


def step_verify_fuses(port, attempt_number, total_attempts):
    """Read back and verify all fuse bytes."""
    step_num = 2 + attempt_number  # steps 3 and 4
    print_step(step_num, 4, f"Verifying fuses (read-back {attempt_number}/{total_attempts})")

    success, stdout, stderr = run_avrdude(
        port,
        [
            "-U", "lfuse:r:-:h",
            "-U", "hfuse:r:-:h",
            "-U", "efuse:r:-:h",
        ],
        f"verify fuses (attempt {attempt_number})",
    )

    combined = stderr + stdout

    if not success:
        print_error("avrdude returned an error during fuse readback")
        return False

    if "Avrdude done.  Thank you." not in combined:
        print_error("avrdude did not complete successfully")
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

    all_correct = True
    if len(actual_values) < len(expected_fuses):
        print_error(f"Expected {len(expected_fuses)} fuse values from stdout, got {len(actual_values)}")
        print_info(f"stdout was: {repr(stdout.strip())}")
        return False

    for i, (fuse_name, expected_val) in enumerate(expected_fuses):
        actual_val = actual_values[i]
        if actual_val == expected_val:
            print_success(f"{fuse_name}: {actual_val} (expected {expected_val})")
        else:
            print_error(f"{fuse_name}: {actual_val} != expected {expected_val}")
            all_correct = False

    return all_correct


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Pebble HF Board Flashing Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 flash_pebble.py                          # auto-detect everything
    python3 flash_pebble.py firmware.hex              # specify hex file
    python3 flash_pebble.py --port /dev/cu.usbserial-3120
    python3 flash_pebble.py --fuses-only              # skip flash, only program fuses
        """,
    )
    parser.add_argument("hex_file", nargs="?", default=None, help="Path to .hex firmware file")
    parser.add_argument("--port", "-p", default=None, help="Serial port (auto-detected if omitted)")
    parser.add_argument("--fuses-only", action="store_true", help="Skip flash, only program and verify fuses")
    args = parser.parse_args()

    print_banner()

    # ── Check avrdude ──
    avrdude_path = check_avrdude()
    if not avrdude_path:
        print_error("avrdude is not installed or not in PATH.")
        print_info("Install with: brew install avrdude")
        print_big_x("SETUP", "avrdude not found")
        sys.exit(1)
    print_success(f"avrdude found: {avrdude_path}")

    # ── Find hex file ──
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

    # ── Detect serial port ──
    port = args.port
    if port is None:
        print_info("Searching for USB serial port...")
        port = detect_serial_port()

    if port is None:
        print_error("No USB serial port found matching /dev/cu.usbserial-*")
        print_info("Is the programmer plugged in?")
        print_info("Check with: ls /dev/cu.*")
        print_big_x("SETUP", "No serial port detected")
        sys.exit(1)

    print_success(f"Serial port: {port}")

    # ── Confirm before flashing ──
    print(f"\n{Colors.YELLOW}{Colors.BOLD}  Ready to flash. Press ENTER to begin (Ctrl+C to abort)...{Colors.RESET}", end="")
    try:
        input()
    except KeyboardInterrupt:
        print(f"\n\n  {Colors.DIM}Aborted.{Colors.RESET}")
        sys.exit(0)

    start_time = time.time()
    failed_step = None

    # ── Step 1: Flash firmware ──
    if not args.fuses_only:
        if not step_flash_firmware(port, hex_file):
            failed_step = "FLASH FIRMWARE"
    else:
        print(f"\n  {Colors.DIM}Skipping flash (--fuses-only){Colors.RESET}")

    # ── Step 2: Program fuses ──
    if not failed_step:
        if not step_program_fuses(port):
            failed_step = "PROGRAM FUSES"

    # ── Steps 3-4: Verify fuses (twice) ──
    if not failed_step:
        if not step_verify_fuses(port, 1, 2):
            failed_step = "VERIFY FUSES (read 1)"

    if not failed_step:
        if not step_verify_fuses(port, 2, 2):
            failed_step = "VERIFY FUSES (read 2)"

    # ── Final result ──
    elapsed = time.time() - start_time
    print(f"\n{Colors.DIM}  Total time: {elapsed:.1f}s{Colors.RESET}")

    if failed_step:
        print_big_x(failed_step)
        sys.exit(1)
    else:
        print_big_checkmark()
        sys.exit(0)


if __name__ == "__main__":
    main()

# Compiling into a Native Binary

Compiling the CLI into a native binary is the best way to distribute the CLI.
This approach ensures the end user do not need to install Python to use the CLI.
This guide explains how to compile the CLI using [PyInstaller](https://pyinstaller.org/en/stable/).

!!! info "OS Support"
    PyInstaller binaries are platform-specific. Compile your binary on the target OS (e.g., Linux, macOS, or Windows).

## Prerequisites

Ensure the following are installed on your system:

1. Python 3.9 or later
2. PyInstaller

Install PyInstaller using pip:

```bash
pip install pyinstaller
```

## Setup Guide

### 1. Test Your CLI

Before compiling, test the CLI to ensure it works correctly. For example:

```bash
python s3-cli.py --help
```

Verify the output displays the help message and that all commands work as expected.

### 2. Compile the CLI

Run the following command to compile `s3-cli.py` into a standalone binary:

```bash
pyinstaller --onefile s3-cli.py
```

This will create a `dist` folder containing the binary file named `s3-cli`.

!!! tip
    To reduce the binary size, you can exclude unused modules:
      ```bash
      pyinstaller --onefile --exclude-module tkinter s3-cli.py
      ```

### 3. Execute the Compiled Binary

Navigate to the `dist` folder and run the binary:

```bash
cd dist
./s3-cli --help
```

You should see the help message and be able to execute all commands like before.

!!! note "Distribution"
    You can distribute the binary in the `dist` folder to users.
    It is a standalone executable, so users do not need Python installed to run it. 🚀

### Troubleshooting

- **Dependency Issues**:
  If the binary fails to run, ensure all required dependencies are installed and correctly imported in your script.

- **Platform-Specific Binaries**:
  PyInstaller binaries are platform-specific. Compile your binary on the target OS (e.g., Linux, macOS, or Windows).

- **Debugging Errors**:
  Use the `--debug` flag with PyInstaller to diagnose issues during compilation:
  ```bash
  pyinstaller --onefile --debug=all s3-cli.py
  ```
# LUCIFER
LUCIFER is an esolang based on the 7 deadly sins as well as Dante's Inferno.

## Command palette
- `GREED(X, Y)`
    Set the value of X to Y.
- `PRIDE(X)`
    Print X
- `WRATH()`
    End the program
- `GLUTTONY(X, Y)`
    X mod Y
- `LUST(X, Y)`
    Pick a number from X to Y inclusive.
- `ENVY(X)`
    Get user input
- `SLOTH(X)`
    Wait X seconds
- `REPENT(ID)`
    Jump to the gate of ID.
- `GATE: ID`
    Make a gate with ID
- `TREACH { ... }`
    Loop code inside forever
- `LIMBO`
    Break outside a loop.
- `JUDGE EXPRESSION { ... }`
    If condition (uses Python's expression syntax)

LUCIFER has 2 variables, SIN and ZEN.

# Installation

## Prerequisites

- **Python 3.6** or higher (required)
- **Recommended:** Python 3.10+ for better performance and security
- Python must be accessible via the `python` command

## Quick Install (Windows)

1. Download `LUCIFER.py` and `luci.bat`
2. Put them in a folder (e.g., `C:\Lucifer`)
3. Add that folder to your User PATH
4. Open a new terminal and run:

   luci

## Windows

1. **Download and Setup**
   - Download `LUCIFER.py` and `luci.bat`
   - Create a folder in `C:` (name it LUCIFER)
   - Place both files in this folder

2. **Add to System PATH**
   - Press <kbd>Win</kbd> + <kbd>S</kbd> to open Search
   - Search for "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "User variables," select `Path` and click "Edit"
   - Click "New" and paste the path "C:\LUCIFER"
   - Click "OK" to save changes

3. **Verify Installation**
   - Open a new terminal and type `luci`
   - You should see this welcome screen:

```
      \
   _,--=-,_
  /       =\
 :LUCIFER-##;
 ;  7DS -=##;
  \_  -==##/
    '==##

--- LUCIFER REPL (Type RUN to execute, END to exit) ---
LUCIFER>
```

## Mac/Linux

1. **Download and Setup**
   - Download `LUCIFER.py` and `luci`
   - Open your terminal and navigate to the directory

2. **Make Script Executable**
   ```bash
   chmod +x luci
   ```

3. **Install to PATH**
   ```bash
   sudo mkdir -p /usr/local/bin/LUCIFER/
   sudo mv luci /usr/local/bin/LUCIFER/
   sudo mv LUCIFER.py /usr/local/bin/LUCIFER/
   ```

4. **Verify Installation**
   - Open a new terminal and type `luci`
   - You should see this welcome screen:

```
      \
   _,--=-,_
  /       =\
 :LUCIFER-##;
 ;  7DS -=##;
  \_  -==##/
    '==##

--- LUCIFER REPL (Type RUN to execute, END to exit) ---
LUCIFER>
```

## Running a File

To execute a `.luci` file:

luci myprogram.luci

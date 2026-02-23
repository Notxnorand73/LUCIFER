import time
import random
import re
import sys
import os
import requests
import json
version = "ALPHA 1.2"
def check_and_update(flag=False):
    """Check for updates and update LUCIFER.py if a newer version is available."""
    try:
        # Fetch version info from data.json
        data_url = "https://raw.githubusercontent.com/Notxnorand73/LUCIFER/main/data.json"
        data_response = requests.get(data_url, timeout=5)
        data_response.raise_for_status()
        data = json.loads(data_response.text)
        remote_version = data.get("version", "")
        print("LOCAL VERSION:", version.upper())
        print("REMOTE VERSION:", remote_version.upper())
        if remote_version and remote_version.lower() != version.lower():
            print(f"\nNEW VERSION AVAILABLE: {remote_version}")
            if input("UPDATE (y/n):").lower() == "y":
                # Fetch the latest LUCIFER.py
                py_url = "https://raw.githubusercontent.com/Notxnorand73/LUCIFER/main/LUCIFER.py"
                py_response = requests.get(py_url, timeout=5)
                py_response.raise_for_status()
                # Write to current file
                script_path = os.path.abspath(sys.argv[0])
                with open(script_path, 'w') as f:
                    f.write(py_response.text)
                with open(script_path, "r") as f:
                    lines = f.readlines()
                lines = [line for line in lines if line.strip()]
                with open(script_path, "w") as f:
                    f.writelines(lines)
                print(f"UPDATED TO {remote_version}!")
        elif flag:
            # Fetch the latest LUCIFER.py
            py_url = "https://raw.githubusercontent.com/Notxnorand73/LUCIFER/main/LUCIFER.py"
            py_response = requests.get(py_url, timeout=5)
            py_response.raise_for_status()
            # Write to current file
            script_path = os.path.abspath(sys.argv[0])
            with open(script_path, 'w') as f:
                f.write(py_response.text)
            with open(script_path, "r") as f:
                lines = f.readlines()
            lines = [line for line in lines if line.strip()]
            with open(script_path, "w") as f:
                f.writelines(lines)
            print(f"UPDATED TO {remote_version}!")
        else:
            print(f"YOU HAVE THE LATEST VERSION: {version}")
    except Exception as e:
        print(f"FAILED: {e}")
class LuciferInterpreter:
    def __init__(self, code):
        self.code = code
        # Filter out empty lines and comments
        self.lines = [line.strip() for line in code.split('\n') if line.strip()]
        self.vars = {"SIN": 0, "ZEN": 0}
        self.gates = {}
        self.pc = 0 
        self.loop_stack = []
        self._find_gates()
    def _find_gates(self):
        for i, line in enumerate(self.lines):
            if line.startswith("GATE:"):
                # Captures ID after "GATE:"
                gate_id = line.split(":", 1)[1].strip()
                self.gates[gate_id] = i
    def _get_val(self, expr):
        """Evaluates an expression or returns a literal."""
        expr = str(expr).strip()
        # Replace variable names with their current values
        temp_expr = expr.replace("SIN", str(self.vars["SIN"])).replace("ZEN", str(self.vars["ZEN"]))
        try:
            # Safely evaluate simple math (+ - * / %)
            return int(eval(temp_expr, {"__builtins__": None}, {}))
        except:
            # If it's not math, return as string (for PRIDE)
            return expr
    def run(self):
        self.pc = 0
        while self.pc < len(self.lines):
            line = self.lines[self.pc]
            jumped = False
            # If we hit a closing brace, just move on (unless it's a TREACH loop)
            if line == "}":
                if self.loop_stack:
                    self.pc = self.loop_stack[-1]
                    jumped = True
                else:
                    self.pc += 1
                continue
            match = re.match(r"(\w+)\((.*)\)", line)
            if match:
                cmd = match.group(1).upper()
                args = [a.strip() for a in match.group(2).split(',')]
                if cmd == "REPENT":
                    gate_id = args[0]
                    if gate_id in self.gates:
                        self.pc = self.gates[gate_id]
                        # We don't clear loop_stack here so TREACH still works,
                        # but we effectively 'teleport' the PC.
                        jumped = True
                if cmd == "GREED":
                    self.vars[args[0]] = self._get_val(args[1])
                elif cmd == "PRIDE":
                    print(self._get_val(args[0]))
                elif cmd == "GLUTTONY":
                    self.vars[args[0]] %= self._get_val(args[1])
                elif cmd == "LUST":
                    low = self._get_val(args[1])
                    high = self._get_val(args[2])
                    self.vars[args[0]] = random.randint(low, high)
                elif cmd == "ENVY":
                    try:
                        self.vars[args[0]] = int(input(">> "))
                    except ValueError:
                        print("INVALID OFFERING (Input must be an integer)")
                elif cmd == "SLOTH":
                    time.sleep(self._get_val(args[0]))
            elif line.startswith("JUDGE"):
                # Clean the expression of the command and the brace
                expr_str = line.replace("JUDGE", "").replace("{", "").strip()
                if not self._get_val(expr_str):
                    # IF FALSE: Find the matching '}' and jump PAST it
                    depth = 1
                    while depth > 0 and self.pc < len(self.lines) - 1:
                        self.pc += 1
                        if "{" in self.lines[self.pc]: depth += 1
                        if "}" in self.lines[self.pc]: depth -= 1
                    jumped = True # Landed on '}', next cycle will move past it
                # IF TRUE: Just move to the next line (the first line inside the { )
            elif line.startswith("TREACH"):
                self.loop_stack.append(self.pc)
            elif line.startswith("LIMBO"):
                if self.loop_stack: self.loop_stack.pop()
                while "}" not in self.lines[self.pc]:
                    self.pc += 1
            elif line.startswith("WRATH"):
                return
            # Only move forward if we didn't just jump to a GATE
            if not jumped:
                self.pc += 1
    def repl(self):
        print("\n".join(logo))
        print("\n--- LUCIFER REPL (Type RUN to execute, END to exit) ---")
        while True:
            program_lines = []
            while True:
                user = input("LUCIFER> ")
                if user.upper() == "END": return
                if user.upper() == "RUN": break
                program_lines.append(user)
            self.lines = [l.strip() for l in program_lines if l.strip()]
            self._find_gates()
            try:
                self.run()
            except Exception as e:
                print(f"DIABOLICAL ERROR: {e}")
logo = [
    "      \\",
    "   _,--=-,_",
    "  /       =\\ ",
    " :LUCIFER-##;",
    " ;  7DS -=##;",
    "  \\_  -==##/",
    "    '==##"
]
if __name__ == "__main__":
    luci = LuciferInterpreter("")
    if len(sys.argv) > 1:
        # Load from file
        if sys.argv[1] == "--version":
            print(version)
        elif sys.argv[1] == "--update":
            check_and_update()
        elif sys.argv[1] == "--forceupdate":
            check_and_update(flag=True)   
        else:
            try:
                with open(sys.argv[1], 'r') as f:
                    luci.lines = [l.strip() for l in f.readlines() if l.strip()]
                    luci._find_gates()
                    luci.run()
            except Exception as e:
                print(e)
    else:
        luci.repl()

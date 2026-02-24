import time
import random
import re
import sys
import os
import shutil
import requests
import json
version = "ALPHA 1.1"
config_file = "LUCIFER.txt"
if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        f.write('SHACKLED')
        shackled = True
else:
    with open(config_file, 'r') as f:
        if f.read() == "UNSHACKLED":
            shackled = False
        else:
            shackled = True
def check_and_update(flag=False):
    try:
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
                py_url = "https://raw.githubusercontent.com/Notxnorand73/LUCIFER/main/LUCIFER.py"
                py_response = requests.get(py_url, timeout=5)
                py_response.raise_for_status()
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
            py_url = "https://raw.githubusercontent.com/Notxnorand73/LUCIFER/main/LUCIFER.py"
            py_response = requests.get(py_url, timeout=5)
            py_response.raise_for_status()
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
def download_circle_versions():
    try:
        tree_url = "https://api.github.com/repos/Notxnorand73/LUCIFER/git/trees/main?recursive=1"
        response = requests.get(tree_url, timeout=15)
        response.raise_for_status()
        tree = response.json().get("tree", [])
        allowed_prefixes = ("ALPHA", "BETA", "RELEASE", "PRERELEASE")
        version_files = []
        for item in tree:
            if item.get("type") != "blob":
                continue
            path = str(item.get("path", "")).strip()
            if not path.lower().endswith(".py"):
                continue
            filename = os.path.basename(path).upper()
            if filename.startswith(allowed_prefixes):
                version_files.append(path)
        version_files = sorted(set(version_files), key=lambda x: x.upper())
        if not version_files:
            print("NO MATCHING VERSION FILES FOUND.")
            return
        download_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        downloaded = 0
        attempted = 0
        for path in version_files:
            attempted += 1
            try:
                file_url = f"https://raw.githubusercontent.com/Notxnorand73/LUCIFER/main/{path}"
                py_response = requests.get(file_url, timeout=10)
                py_response.raise_for_status()
                output_path = os.path.join(download_dir, os.path.basename(path))
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(py_response.text)
                downloaded += 1
                print(f"DOWNLOADED: {path} -> {output_path}")
            except Exception as e:
                print(f"SKIPPED {path}: {e}")
        print(f"CIRCLE COMPLETE. DOWNLOADED {downloaded}/{attempted} VERSION FILES.")
    except Exception as e:
        print(f"CIRCLE FAILED: {e}")
class LuciferInterpreter:
    def __init__(self, code, lucifer=False):
        self.code = code
        self.lines = [line.strip() for line in code.split('\n') if line.strip()]
        self.vars = {"SIN": 0, "ZEN": 0}
        if lucifer:
            self.vars = {"SIN": 0, "ZEN": 0, "REPRIVE": 0, "LITANY": 0, "SUFFER": 0, "DAMN": 0, "PIT": 0}
        self.gates = {}
        self.pc = 0 
        self.loop_stack = []
        self._find_gates()
    def _find_gates(self):
        for i, line in enumerate(self.lines):
            if line.startswith("GATE:"):
                gate_id = line.split(":", 1)[1].strip()
                self.gates[gate_id] = i
    def _get_val(self, expr):
        expr = str(expr).strip()
        temp_expr = expr
        for var_name, var_value in self.vars.items():
            temp_expr = temp_expr.replace(var_name, str(var_value))
        try:
            return int(eval(temp_expr, {"__builtins__": None}, {}))
        except:
            return expr
    def run(self):
        self.pc = 0
        while self.pc < len(self.lines):
            line = self.lines[self.pc]
            jumped = False
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
                expr_str = line.replace("JUDGE", "").replace("{", "").strip()
                if not self._get_val(expr_str):
                    depth = 1
                    while depth > 0 and self.pc < len(self.lines) - 1:
                        self.pc += 1
                        if "{" in self.lines[self.pc]: depth += 1
                        if "}" in self.lines[self.pc]: depth -= 1
                    jumped = True
            elif line.startswith("TREACH"):
                self.loop_stack.append(self.pc)
            elif line.startswith("LIMBO"):
                if self.loop_stack: self.loop_stack.pop()
                while "}" not in self.lines[self.pc]:
                    self.pc += 1
            elif line.startswith("WRATH"):
                return
            if not jumped:
                self.pc += 1
    def repl(self):
        print("\n".join(logo))
        if shackled:
            print("\n--- LUCIFER REPL (Type RUN to execute, END to exit) ---")
        else:
            print("\n--- ####### #### ##### ### ## ######## ### ## ##### ---")
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
horns = [
    " /                \\",
    "/|                |\\",
    "|\\                /|",
    "| \\              / |",
    "\\  '\\_        _/'  /",
    " \\    '\\    /'    /",
    "  '\   |    |   /'",
    "    '-=/    \\=-'",
    "",
    "      .      .",
    "      '      '"
]
if __name__ == "__main__":
    luci = LuciferInterpreter("", lucifer=shackled)
    if len(sys.argv) > 1:
        # Load from file
        if sys.argv[1] == "--version":
            print(version)
        elif sys.argv[1] == "--update":
            check_and_update()
        elif sys.argv[1] == "--forceupdate":
            check_and_update(flag=True)   
        elif sys.argv[1] == "--circle":
            download_circle_versions()
        elif sys.argv[1] == "--zen":
            script_path = os.path.abspath(sys.argv[0])
            with open(script_path, 'w') as f:
                f.write('print("--( ZEN )--")')
        elif sys.argv[1] == "--sin":
            script_path = os.path.abspath(sys.argv[0])
            code = '''image = """      \\\\
    ,--=-,_
   ==\\\\    =\\\\
  ====   -##;
 ;==/  -=##;
  \\\\_  -==##/
    '==##"""
print(image)'''
            with open(script_path, 'w') as f:
                f.write(code)
        elif sys.argv[1] == "--grace":
            if shackled:
                target = r"C:\Lucifer" if os.name == "nt" else "/usr/local/bin/LUCIFER/"
                try:
                    if os.path.exists(target):
                        if os.path.isdir(target):
                            shutil.rmtree(target)
                        else:
                            os.remove(target)
                        print(f"REMOVED: {target}")
                    else:
                        print(f"NOT FOUND: {target}")
                except Exception as e:
                    print(f"FAILED TO GRACE {target}: {e}")
            else:
                shackled = True
                print("RESHACKLED")
                with open(config_file, 'w') as f:
                    f.write('SHACKLED')
        elif sys.argv[1] == "--lucifer":
            with open(config_file, 'w') as f:
                f.write('UNSHACKLED')
        elif sys.argv[1] == "--shackle":
            print(shackled)
        elif sys.argv[1] == "--purgatory":
            will_timeout = random.choice([True, False])
            timeout = 0
            for i in range(600):
                os.system("cls" if os.name == "nt" else "clear")
                if i > 300 and will_timeout:
                    timeout = random.randint(1, 50)
                    if timeout == 25:
                        raise TimeoutError("...")
                time_left = 600-i
                if time_left == 426:
                    print("~ 666 ~")
                else:
                    print(f"{(time_left//60):02}:{(time_left%60):02}")
                time.sleep(1)
        elif sys.argv[1] == "--free":
            while True:
                try:
                    os.system("cls" if os.name == "nt" else "clear")
                    for i in horns:
                        print(i)
                except BaseException:
                    pass
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

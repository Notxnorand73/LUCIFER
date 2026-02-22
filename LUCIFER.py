import time
import random
import re
import sys
import os

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
    "  /       =\ ",
    " :LUCIFER-##;",
    " ;  7DS -=##;",
    "  \_  -==##/",
    "    '==##"
]

if __name__ == "__main__":
    luci = LuciferInterpreter("")
    if len(sys.argv) > 1:
        # Load from file
        if sys.argv[1] == "--version":
            print("ALPHA 1.1")
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

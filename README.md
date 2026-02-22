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

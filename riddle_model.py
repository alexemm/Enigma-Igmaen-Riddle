from gurobipy import quicksum, Model, GRB


def solve():
    model = Model("Enigma Riddle")
    letters = {"E", "N", "I", "G", "M", "A"}
    digits = range(1, 10)
    x = model.addVars(letters, digits, vtype=GRB.BINARY)
    y = model.addVars(letters, vtype=GRB.INTEGER)
    # Stay in digit range
    for i in letters:
        model.addRange(y[i], 1, 9, f"digitRange{i}")
    # Final value for first word
    b = model.addVar(vtype=GRB.INTEGER)
    first_word = "ENIGMA"
    second_word = "IGMAEN"

    # Constraint for the enigma-igmaen numbers
    model.addConstr(quicksum(10 ** (len(first_word) - 1 - i) * y[first_word[i]] for i in range(len(first_word))) == b)
    model.addConstr(
        quicksum(10 ** (len(second_word) - 1 - i) * y[second_word[i]] for i in range(len(second_word))) == b * 1.2)

    # Conflict constraint
    model.addConstrs(x[i_1, j] + x[i_2, j] <= 1 for i_1 in letters for i_2 in letters for j in digits if i_1 != i_2)

    # Linking constraint
    model.addConstrs(j * x[i, j] <= y[i] for i in letters for j in digits)

    # Exactly one digit has to be packed
    model.addConstrs(quicksum(x[i, j] for j in digits) == 1 for i in letters)

    model.optimize()
    return model

from gurobipy import quicksum, Model, GRB


def solve():
    model = Model("Enigma Riddle Binary Program")
    letters = {"E", "N", "I", "G", "M", "A"}
    digits = range(1, 10)
    # x[i, j] == 1 => Letter i uses digit j
    x = model.addVars(letters, digits, vtype=GRB.BINARY)
    # Final value for first word
    b = model.addVar(vtype=GRB.INTEGER)
    first_word = "ENIGMA"
    second_word = "IGMAEN"

    # Constraints for the enigma-igmaen numbers
    model.addConstr(
        quicksum(quicksum(10 ** (len(first_word) - 1 - i) * j * x[first_word[i], j] for j in digits) for i in
                 range(len(first_word))) == b)
    model.addConstr(
        quicksum(quicksum(10 ** (len(second_word) - 1 - i) * j * x[second_word[i], j] for j in digits) for i in
                 range(len(second_word))) == b * 1.2)

    # Conflict constraint, different letters have different digits
    model.addConstrs(x[i_1, j] + x[i_2, j] <= 1 for i_1 in letters for i_2 in letters for j in digits if i_1 != i_2)

    # Exactly one digit has to be used per letter
    model.addConstrs(quicksum(x[i, j] for j in digits) == 1 for i in letters)

    model.optimize()
    return model

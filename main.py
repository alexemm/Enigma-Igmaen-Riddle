
from riddle_binary_model import solve


if __name__ == "__main__":
    m = solve()
    for v in m.getVars():
        if v.x == 1:
            print('%s %g' % (v.varName, v.x))

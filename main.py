
from riddle_model import solve


if __name__ == "__main__":
    m = solve()
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))
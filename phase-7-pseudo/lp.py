from functools import reduce
from pulp      import LpInteger, LpMinimize, LpProblem, LpStatus, LpVariable


# 2020年10月25日 京都 10R 三連単のオッズ
data = [73.7, 78.4, 91.4, 94.8, 96.0, 100.1, 101.4, 104.0, 106.4, 120.4, 129.7, 130.6, 136.1, 140.0, 145.9, 146.1, 146.8, 148.4, 151.8, 153.0, 156.0, 161.4, 164.6, 167.0, 168.1, 169.4, 170.3, 171.2, 180.2, 191.8, 193.2, 193.6, 198.1, 198.2, 198.3, 201.3, 205.7, 206.2, 207.8, 209.7, 210.6, 212.2, 214.9, 216.0, 224.0, 228.7, 231.5, 235.2, 238.9, 240.4, 241.7, 243.9, 251.5, 251.8, 252.5, 253.0, 255.4, 255.9, 260.8, 261.1, 261.9, 262.0, 271.2, 273.6, 277.1, 277.3, 278.4, 282.5, 282.7, 284.9, 285.6, 288.5, 289.7, 289.7, 291.1, 295.3, 303.5, 309.6, 310.4, 311.7, 312.0, 312.2, 312.9, 313.8, 318.1, 319.3, 320.6, 325.1, 326.1, 327.5, 329.3, 331.4, 331.7, 341.2, 341.8, 342.3, 343.5, 344.3, 346.9, 347.1]

xs = LpVariable.dicts('x', range(len(data)), 1, 1000, LpInteger)

problem = LpProblem('upro', LpMinimize)
problem += reduce(lambda acc, i: acc + xs[i], range(len(data)), 0)

for i in range(len(data)):
    problem += (xs[i] * data[i] >= reduce(lambda acc, i: acc + xs[i], range(len(data)), 0) * 2.0)

status = problem.solve()

print(LpStatus[status])

for i in range(len(data)):
    print(f'{int(xs[i].value() * 100):,d}\t{data[i]:.1f}\t{int(xs[i].value() * 100 * data[i]):,d}')

print(f'{reduce(lambda acc, i: acc + int(xs[i].value() * 100), range(len(data)), 0):,d}')

from functools import reduce
from funcy     import filter, partial, map
from itertools import permutations
from operator  import add
from pulp      import LpInteger, LpMinimize, LpProblem, LpVariable, PULP_CBC_CMD


# 2013年9月20日 名古屋 1R
#          単勝    馬単
data = [[  14.7,  347.2,   37.4,   54.0,  662.7,  169.6,  607.5],
        [  72.6,  455.6,  177.8,  197.1, 1457.9,  331.4, 2429.8],
        [   1.4,   23.0,   86.8,    5.4,   50.7,   13.0,  177.8],
        [   2.3,   10.3,   49.3,    1.9,   90.0,    5.9,  123.6],
        [ 151.8, 1214.9, 1457.9,   74.4,  455.6,  560.8, 3644.7],
        [  18.0,  119.5,  347.2,   27.6,   43.2,  486.0,  455.6],
        [  66.8, 1041.4, 2429.8, 1214.9,  911.2, 3644.7,  911.2]]

labels = tuple(map(lambda i: (f'{i}',) + tuple(map(lambda j: f'{i}-{j}',
                                                   filter(lambda j: i != j,
                                                          map(partial(add, 1),
                                                              range(7))))),
                   map(partial(add, 1),
                       range(7))))

for exacta_count in range(1, 4):
    for exacta in map(set, permutations(range(7), exacta_count)):
        xs = LpVariable.dicts('x', (range(7), range(7)), 0, 1000, LpInteger)

        expense = reduce(lambda acc, i: acc + reduce(lambda acc, j: acc + xs[i][j],
                                                     range(7), 0),
                         range(7), 0)

        problem = LpProblem('umameshi.com', LpMinimize)
        problem += expense
        problem += expense >= 1

        for i in range(7):
            if i in exacta:
                for j in range(1, 7):
                    problem += xs[i][j] * data[i][j] >= expense
            else:
                problem += xs[i][0] * data[i][0] >= expense

        status = problem.solve(PULP_CBC_CMD(msg=0))

        if status > 0:
            for i in range(7):
                for j in range(7):
                    print(f'{labels[i][j]}\t{int(xs[i][j].value() * 100):,d}\t{data[i][j]:.1f}\t{int(xs[i][j].value() * 100 * data[i][j]):,d}')

            print(f'{reduce(lambda acc, i: acc + reduce(lambda acc, j: acc + int(xs[i][j].value() * 100), range(7), 0), range(7), 0):,d}')
            print()

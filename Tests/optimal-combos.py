from TypeData.charthelper import *

allCombos = ChartHelper.getAllTypeCombos()
points: dict[TypeCombo, int] = dict()
for combo1 in allCombos:
    points[combo1] = 0
    for combo2 in allCombos:
        points[combo1] += combo1.matchup(combo2)
    print(f"{str(combo1)}: {points[combo1]}")
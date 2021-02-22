import random

a0 = 2
a1 = 3
a2 = 8
a3 = 5
X1 = [random.randrange(1, 21, 1) for i in range(8)]
X2 = [random.randrange(1, 21, 1) for i in range(8)]
X3 = [random.randrange(1, 21, 1) for i in range(8)]
Y = [a0 + a1 * X1[i] + a2 * X2[i] + a3 * X3[i] for i in range(8)]
X01 = (max(X1) + min(X1)) / 2
X02 = (max(X2) + min(X2)) / 2
X03 = (max(X3) + min(X3)) / 2
dX1 = X01 - min(X1)
dX2 = X02 - min(X2)
dX3 = X03 - min(X3)
Xn1 = [(X1[i] - X01) / dX1 for i in range(8)]
Xn2 = [(X2[i] - X02) / dX2 for i in range(8)]
Xn3 = [(X3[i] - X03) / dX3 for i in range(8)]
Yet = a0 + a1 * X01 + a2 * X02 + a3 * X03

index = Y.index(min(Y))
minimal = [X1[index], X2[index], X3[index]]

print("N   X1   X2   X3     Y3       XH1    XH2    XH3")
for i in range(8):
    print(f"{i + 1:^1} |{X1[i]:^4} {X2[i]:^4} {X3[i]:^4} |"
          f" {Y[i]:^5} || {'%.2f' % Xn1[i]:^5}  {'%.2f' % Xn2[i]:^5}  {'%.2f' % Xn3[i]:^5} |")

print(f"\nX0| {X01:^4} {X02:^4} {X03:^4}|")
print(f"dx| {dX1:^4} {dX2:^4} {dX3:^4}|")
print("Function: y=", a0, "+", a1, "*X1", "+", a2, "*X2", "+", a3, "*X3")
print("Yет =", Yet)
print("min(Y):  Y({0}, {1}, {2}) = {3}".format(*minimal, "%.1f" % min(Y)))

from sympy import *

bz,p1,p2,p3,p4,px,t = symbols("bz p1 p2 p3 p4 px t")

bz = (1-t)**3*p1 + 3*(1-t)**2*t*p2 + 3*(1-t)*t**2*p3 +t**3*p4
j = (px - bz) ** 2
jp2 = simplify(diff(j,p2)/2)
jp3 = simplify(diff(j,p3)/2)

points = [(0,0),(0.2,65),(0.7,45),(1.0,100)]

const = ((p1, points[0][0]),(p4,points[-1][1]))
tp2 = sum([jp2.subs(const + ((t,x[0]),(px, x[1]))) for x in points[1:-1]])
tp3 = sum([jp3.subs(const + ((t,x[0]),(px, x[1]))) for x in points[1:-1]])

print('tp2:',tp2);
print('tp3:',tp3)

r = solve([tp2, tp3], [p2,p3])
print(r)

def emi_calculator(principal, years):
    p = principal
    t = years    
    r = 10 # rate
    r = r/(12*100)
    t = t*12
    emi = (p * r * ((1+r)**t)) / (((1+r)**t)-1)
    return round(emi)

#e = emi_calculator(principal=5000000, years = 5)

def principal_nth_month(emi, years, n):
    N = years * 12
    rate = 10 # rate
    pn = ((1/(1+(rate/1200)))**(N-n+1))*emi
    return round(pn)


#p2 = principal_nth_month(emi = e, years=5, n=46)
    
def summarize(principal, years, mode):
    e = emi_calculator(principal, years)
    #print("EMI",e)
    total_emi_paid = 0
    total_interest_paid = 0
    total_principal_paid = 0
    total_tax_saved = 0
    total_wastage = 0
    for i in range(years):
        yearly_emi_out = 0
        yearly_interest_out = 0
        yearly_principal_out = 0        
        for j in range(12):
            n = (i*12)+(j+1)
            ptn = principal_nth_month(e, years, n)
            itn = e - ptn
            yearly_emi_out += e
            yearly_interest_out += itn
            yearly_principal_out += ptn            
                
        total_emi_paid += yearly_emi_out
        total_interest_paid += yearly_interest_out
        total_principal_paid += yearly_principal_out
        
        owners = 2
        eff_yearly_interest = yearly_interest_out/owners
        eff_yearly_principal = yearly_principal_out/owners
        # Interest Rebated
        rebate_limit = 200000
        # Could come into effect in future to boost real estate
        #if mode == 3 :            
            #rebate_limit += 150000
            
        rebate = min(rebate_limit, eff_yearly_interest)
        wastage = max(rebate_limit, eff_yearly_interest) - rebate_limit
        p80c = min(150000, eff_yearly_principal)          
        # Wastage
        # interest_wastage = max(eff_yearly_interest-200000,0)
        # principal_wastage = max(eff_yearly_principal-150000,0)
        
        # Equity investments can be made against 80c, Not necessarily Home Loan Principal
        p80c = 0        
        
        # Tax Saved on rebate
        yearly_tax_saved = round(( rebate + p80c ) * 0.3) * owners     
        yearly_wastage = wastage * owners
        total_tax_saved += yearly_tax_saved
        total_wastage += yearly_wastage

    #print("Emi Paid",total_emi_paid)                
    #print("Interest Paid",total_interest_paid)
    #print("Principal Paid",total_principal_paid)    
    #print("Total Tax Saved",total_tax_saved)
    total_delta_loss = total_interest_paid-total_tax_saved    
    
    # Mode 3 : Inflation 
    # Mode 4 : Grandness 
    # (Bigger House can lead to paying out more property tax every year ?)
    # (Bigger House better than 2 Small Houses, as Resale of smaller houser attracts tax)
    # Appreciate the Tenure (adjust against inflation)
    
    
    total_loss_pct = (total_delta_loss/principal)*100
    total_wastage_pct = (total_wastage/principal)*100
    #print("Total Delta Loss",total_delta_loss)
    salary = (15*(10**5))/12
    total_emi_pct = (e/salary)*100        
    if mode == 1 :
        return total_loss_pct    
    elif mode == 3 :
        return total_wastage_pct
    elif mode == 2 :
        return total_emi_pct
    else :
        return 0
    
Lakhs = 100000    

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
ax = plt.axes(projection='3d')

def f(x, y, m):
    a_x = []
    for _x in x :
        a_y = [] 
        for _y in y :
            _z = summarize(principal = _x*Lakhs, years = _y, mode = m)
            a_y.append(_z)
        a_x.append(a_y)
    return a_x

def zero(x, y):
    a_x = []
    for _x in x :
        a_y = [] 
        for _y in y :
            _z = 0
            a_y.append(_z)
        a_x.append(a_y)
    return a_x

# Max Eligibility for Gross 1.5 Lakhs ( Joint Owners ) HDFC
Eligibility = []
Eligibility.append([5,38*Lakhs])
Eligibility.append([6,44*Lakhs])
Eligibility.append([7,49*Lakhs])
Eligibility.append([8,54*Lakhs])
Eligibility.append([9,58*Lakhs])
Eligibility.append([10,62*Lakhs])
Eligibility.append([11,65*Lakhs])
Eligibility.append([12,69*Lakhs])
Eligibility.append([13,71*Lakhs])
Eligibility.append([14,74*Lakhs])
Eligibility.append([15,76*Lakhs])
Eligibility.append([16,78*Lakhs])
Eligibility.append([17,80*Lakhs])
Eligibility.append([18,82*Lakhs])
Eligibility.append([19,84*Lakhs])
Eligibility.append([20,85*Lakhs])
Eligibility.append([21,86*Lakhs])
Eligibility.append([22,87*Lakhs])
Eligibility.append([23,88*Lakhs])
Eligibility.append([24,89*Lakhs])
Eligibility.append([25,90*Lakhs])
Eligibility = np.array(Eligibility)

Line = []
for xi in range(5,26):
    Line.append([xi,((2.5*xi) + 27.5)*Lakhs])
Line = np.array(Line)

GP = np.transpose( [Line[:,1],Eligibility[:,1]] ) 

# Mesh Grid 
x = np.array(range(10, 91,10))
y = np.array(range(5, 26,1))
X, Y = np.meshgrid(x, y)

Z = np.transpose(np.array(f(x, y, 1)))
C = np.transpose(np.array(f(x, y, 2)))
E = np.transpose(np.array(f(x, y, 3)))

tt = C > 65 # Percentage of EMI Cannot be greater than 65% as per SBI
#tt = Z > C 
C[tt] = np.NaN
#Z[tt] = np.NaN

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow', edgecolor='none')

ax.plot_surface(X, Y, C, rstride=1, cstride=1, cmap='rainbow', edgecolor='none')

#ax.plot_surface(X, Y, E, rstride=1, cstride=1, cmap='hot', edgecolor='none')

#G = np.transpose(np.array(zero(x, y)))
#ax.plot_surface(X, Y, G, rstride=1, cstride=1, cmap='hot', edgecolor='none')


#hot
#viridis
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_zlim(-50, 200)

'''
xdata = np.linspace(0, 15, 100)
ydata = np.linspace(0, 15, 100)
zdata = xdata + ydata
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');

# Data for a three-dimensional line
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')


# Data for three-dimensional scattered points
zdata = 15 * np.random.random(100)
xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');


def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z, 50, cmap='binary')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z');
ax.view_init(60, 35)


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_wireframe(X, Y, Z, color='black')
ax.set_title('wireframe');


ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
ax.set_title('surface');
'''



































    

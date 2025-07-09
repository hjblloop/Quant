import scipy.integrate as integrate
result, error = integrate.quad(lambda x: x**2, 0, 2)
print("integral: ", result)
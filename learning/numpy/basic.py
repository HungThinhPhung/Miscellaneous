import numpy as np

# Create array
x = np.array([[1,2],[3,4]], dtype=np.float64)
y = np.array([[5,6],[7,8]], dtype=np.float64)

# Calculate
# print(x + y)
# print(np.add(x, y))
# print(x - y)
# print(np.subtract(x, y))
# print(x * y)
# print(np.multiply(x, y))
# print(x / y)
# print(np.divide(x, y))
# print(np.sqrt(x))

# Elementwise calculate
print(x.dot(y))
print(np.dot(x, y))
print(sum(x))
print(np.sum(x))
print(np.sum(x, axis=0))
print(np.sum(x, axis=1))
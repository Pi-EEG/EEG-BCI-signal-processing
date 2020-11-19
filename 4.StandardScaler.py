from sklearn.preprocessing import StandardScaler
import numpy as np

data = np.array([[10, 5], [40, 10], [341, 3], [7, 22]])
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

print(data)
print(scaled_data)

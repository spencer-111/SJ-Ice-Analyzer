import numpy as np
import xgboost as xgb
import xarray as xr
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

ds = xr.open_dataset("ice_20190111-20190131.nc")
temp = ds["temp"]
ice = xr.where(temp < 0, -temp, np.nan)

ice_np = ice.values


lag = 3  # number of days used as an input

time, ny, nx = ice_np.shape # Defines the dimensions

# x_list will contain the features and y_list will contain the targets
X_list = []
y_list = []

for t in range(lag, time):
    # Flattens past lag days of ice into features
    ice_lagged = ice_np[t - lag:t].reshape(lag, ny * nx)  # shape: (lag, num_pixels)
    X_t = ice_lagged.T  # shape: (num_pixels, lag)

    # Target: ice concentration on day t
    y_t = ice_np[t].reshape(ny * nx)  # shape: (num_pixels,)

    X_list.append(X_t)
    y_list.append(y_t)

# Combines all time steps
X = np.vstack(X_list)  # shape: (num_pixels*(time-lag), lag)
y = np.hstack(y_list)  # shape: (num_pixels*(time-lag),)

# Sets all NaNs values to 0.0
X = np.nan_to_num(X, 0.0)
y = np.nan_to_num(y, 0.0)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train XGBoost regressor
model = xgb.XGBRegressor(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    objective='reg:squarederror'
)

# This is where the model learns from the training data
model.fit(X_train, y_train)

# The model makes predictions
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))


# Saves the model to a json file
model.save_model("ice_model.json")

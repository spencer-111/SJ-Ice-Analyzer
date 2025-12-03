import xarray as xr
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt

# Get ice concentration from nc file
ds = xr.open_dataset("glsea_ice_test_initial_condition.nc", decode_times=False)
sst = ds["sst"]
# turn negative decimals to positive and discard water temp values
ice = xr.where(sst < 0, -sst, np.nan)
ice_np = ice.values

# Create a "time" dimension for the model
n_time = 3
ice_np_3d = np.broadcast_to(ice_np, (n_time, *ice_np.shape)).copy()

time, ny, nx = ice_np_3d.shape
lag = 3

# Build X_Test
ice_lagged = ice_np_3d[:lag].reshape(lag, ny * nx)
X_test = ice_lagged.T  # shape: (num_pixels, lag)

# Replace NaN with zeros
X_test = np.nan_to_num(X_test, 0.0)

# load model
model = xgb.XGBRegressor()
model.load_model("ice_model.json")

y_pred_flat = model.predict(X_test)
y_pred = y_pred_flat.reshape(ny, nx)

# Replace zeros with NaN
y_pred[y_pred == 0] = np.nan

n_extra_days = 3
predictions = [ice_np]

ice_np_3d_extended = ice_np_3d.copy()

for day in range(n_extra_days):
    # Prepare lagged features from last 'lag' days
    ice_lagged = ice_np_3d_extended[-lag:].reshape(lag, ny * nx)
    X_test = ice_lagged.T
    X_test = np.nan_to_num(X_test, 0.0)

    # Predict next day
    y_pred_flat = model.predict(X_test)
    y_pred_next = y_pred_flat.reshape(ny, nx)

    # Replace zeros with NaN
    y_pred_next[y_pred_next == 0] = np.nan

    # Append prediction to 3D array for next iteration
    ice_np_3d_extended = np.concatenate(
        [ice_np_3d_extended, y_pred_next[np.newaxis, :, :]], axis=0
    )

    predictions.append(y_pred_next)

for i in range(len(predictions)):
    predictions[i][predictions[i] < 0.01] = np.nan


# Define zoomed-in regions as slices (y_min:y_max, x_min:x_max)
zoom_regions = {
    "Straits of Mackinaw": (slice(400, 700), slice(300, 700)),
    "St. Clair & Detroit River": (slice(200, 450), slice(500, 800))
}

for data in predictions:
    # Full map
    plt.figure(figsize=(8, 6))
    im = plt.imshow(data, origin="lower", cmap="plasma")
    plt.axis('off')
    cbar = plt.colorbar(im, orientation="horizontal", fraction=0.046, pad=0.08)
    cbar.set_label("% Ice Concentration")
    plt.show()

    # Zoomed-in regions
    for region_name, (yslice, xslice) in zoom_regions.items():
        plt.figure(figsize=(6, 5))
        im_zoom = plt.imshow(data[yslice, xslice], origin="lower", cmap="plasma")
        plt.axis('off')
        plt.show()

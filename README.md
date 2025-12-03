# SJ Ice Analyzer
Visit the [live project](https://spencer-111.github.io/SJ-Ice-Analyzer/website) to see the finished project.  
Click on the arrows to change which day the prediction is for.

## Project Structure
- **`website/`** – Contains the code for the GitHub Pages site.  
- **`ice_20190111-20190131.nc`** – Data used to train the model.  
- **`glsea_ice_test_initial_condition.nc`** – Data used by the model to make predictions.  
- **`ice_model.json`** – The model created from running `ml.py`.  
- **`ml.py`** – Creates the model `ice_model.json` using `ice_20190111-20190131.nc`.  
- **`plot.py`**
  - Uses `glsea_ice_test_initial_condition.nc` and the `ice_model.json` model to predict the next three days of ice coverage.  
  - Generates plots for each day and the initial day.  
  - Creates zoomed-in plots around northern Michigan and the Detroit–Canada area for all four days.

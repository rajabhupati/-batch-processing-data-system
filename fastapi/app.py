from fastapi import FastAPI, HTTPException
import pandas as pd
import os
import glob

app = FastAPI()

# Check if the CSV directory or file exists
if os.path.exists("/data/output/processed_trips.csv"):
    print("Directory found for processed trips!")
else:
    print("Directory not found for processed trips!")

@app.get("/trip_data/")
async def read_trip_data():
    folder_path = "/data/output/processed_trips.csv/"
    csv_file_pattern = os.path.join(folder_path, "*.csv")  # Search for any CSV files in the folder
    csv_files = glob.glob(csv_file_pattern)

    if csv_files:
        df = pd.read_csv(csv_files[0])  # Read the first CSV file found
        return df.to_dict(orient="records")
    else:
        raise HTTPException(status_code=404, detail="Processed trips data not found")

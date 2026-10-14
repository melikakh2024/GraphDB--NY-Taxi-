import pandas
import requests
from pathlib import Path


url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet"
file=Path()
if not file.is_file():
        response=requests.get(url)
        response.raise_for_status()

        with open(file/"taxi.parquet","wb") as f:
                f.write(response.content)
                print(f"file downloaded")
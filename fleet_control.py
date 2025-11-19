
import json
import os
from typing import Any, List, Dict, Union

from app import VEHICLE_DATA_PATH


def retrieve_vehicle_list(source: Union[str, None] = None) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
	"""
	Retrieve a list (or dict) of vehicles.

	Behavior:
	- If `source` is provided and points to a file, read JSON from it.
	- Otherwise attempts to read `fleet.json` located next to this module.
	- If no file exists, returns a small sample list so the API route can return useful data.
	"""
	file_path = None
	print(f"retrieve_vehicle_list called with source: {source}")
	
	if source:
		file_path = source
		print(f"Using provided source: {file_path}")
	else:
		# Prefer the network-mounted vehicle list if available
		z_path = rf"{VEHICLE_DATA_PATH}vehicles.json"
		print(f"Checking Z: path: {z_path}")

		# choose the first existing path
		for p in (z_path,):
			print(f"Checking path: {p}")
			if os.path.exists(p):
				file_path = p
				print(f"Found existing file: {file_path}")
				break
		
		if not file_path:
			print(f"No file found at {z_path}")

	try:
		if file_path and os.path.exists(file_path):
			print(f"Opening file: {file_path}")
			with open(file_path, "r", encoding="utf-8") as fh:
				data = json.load(fh)
				print(f"Successfully loaded JSON data: {len(data)} items")
				return data

		# default sample data when no file is available
		print("No file path or file doesn't exist, returning default sample data")
		return [
			{"id": "veh1", "name": "Delivery Van 1", "status": "active"},
			{"id": "veh2", "name": "Service Truck A", "status": "maintenance"},
		]
	except Exception as e:
		# Let caller handle exceptions; re-raise for the Flask route to catch and return 500
		print(f"ERROR: {type(e).__name__}: {e}")
		raise


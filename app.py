from cgitb import text
from flask import Flask
from flask import request
from flask import Response
from datetime import datetime
import json
import os
import subprocess
from subprocess import check_output
from subprocess import CalledProcessError
from syncer import Syncer
from syncer import generate_ftp_instructions
from syncer import handle_ftp_instructions
from fleet_control import retrieve_vehicle_list

app = Flask(__name__)


def generate_response(status, text):
    res = Response(response=json.dumps(text), status=status)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res


@app.route("/")
def connect():
    return "DashFox Backend API is ONLINE"


# ================
# Plutonium Routes
# ================


@app.route("/plutonium/status", endpoint="plutonium_status", methods=["GET"])
def plutonium_status():
    try:
        output = str(
            check_output(
                "Z:\Private\conecommons\scripts\plutonium\status.bat", shell=True
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/plutonium/gungame", endpoint="plutonium_gungame", methods=["GET"])
def plutonium_gungame():
    try:
        output = str(
            check_output(
                "Z:\Private\conecommons\scripts\plutonium\select_gungame.bat",
                shell=True,
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/plutonium/domination", endpoint="plutonium_domination", methods=["GET"])
def plutonium_domination():
    try:
        output = str(
            check_output(
                "Z:\Private\conecommons\scripts\plutonium\select_domination.bat",
                shell=True,
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


# ==========
# Git Routes
# ==========


@app.route(
    "/git/deploy/theconeportal", endpoint="git_deploy_theconeportal", methods=["GET"]
)
def git_deploy_theconeportal():
    try:
        output = str(
            check_output(
                "Z:\Private\conecommons\scripts\\theconeportal\\update.bat", shell=True
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route(
    "/git/deploy/conecommons", endpoint="git_deploy_conecommons", methods=["GET"]
)
def git_deploy_conecommons():
    try:
        output = str(
            check_output(
                "Z:\Private\conecommons\scripts\conecommons\\update.bat", shell=True
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/git/deploy/dashfox", endpoint="git_deploy_dashfox", methods=["GET"])
def git_deploy_dashfox():
    try:
        command = "Z:\Private\conecommons\scripts\dashfox\\update.bat"
        subprocess.Popen(
            ["cmd", "/c", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return generate_response(200, "RESTARTING API - BLA")
    except CalledProcessError:
        return generate_response(200, "ERROR")


# ================
# Minecraft Routes
# ================


@app.route("/minecraft/status", endpoint="minecraft_status", methods=["GET"])
def minecraft_status():
    try:
        output = str(
            check_output(
                "powershell Z:\Private\conecommons\scripts\minecraft\get_running_servers.ps1",
                shell=True,
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/minecraft/start_ftb", endpoint="minecraft_start_ftb", methods=["GET"])
def minecraft_start_ftb():
    try:
        output = str(
            check_output(
                "Z:\Private\conecommons\scripts\minecraft\start_minecraft_ftb_server.bat",
                shell=True,
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/minecraft/stop_ftb", endpoint="minecraft_stop_ftb", methods=["GET"])
def minecraft_stop_ftb():
    try:
        output = str(
            check_output(
                "powershell Z:\Private\conecommons\scripts\minecraft\stop_minecraft_ftb_server.ps1",
                shell=True,
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route(
    "/minecraft/start_latest", endpoint="minecraft_start_latest", methods=["GET"]
)
def minecraft_start_latest():
    try:
        output = str(
            check_output(
                "Z:\Private\conecommons\scripts\minecraft\start_minecraft_latest_server.bat",
                shell=True,
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/minecraft/stop_latest", endpoint="minecraft_stop_latest", methods=["GET"])
def minecraft_stop_latest():
    try:
        output = str(
            check_output(
                "powershell Z:\Private\conecommons\scripts\minecraft\stop_minecraft_latest_server.ps1",
                shell=True,
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/minecraft/start_beta", endpoint="minecraft_start_beta", methods=["GET"])
def minecraft_start_beta():
    try:
        output = str(
            check_output(
                "Z:\Private\conecommons\scripts\minecraft\start_minecraft_beta_server.bat",
                shell=True,
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/minecraft/stop_beta", endpoint="minecraft_stop_beta", methods=["GET"])
def minecraft_stop_beta():
    try:
        output = str(
            check_output(
                "powershell Z:\Private\conecommons\scripts\minecraft\stop_minecraft_beta_server.ps1",
                shell=True,
            )
        )
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


# ================
#  Routes
# ================


@app.route("/syncer/rgh/sync_saves", endpoint="syncer_rgh_sync_saves", methods=["GET"])
def sync_xbox_360_saves():
    try:
        syncer = Syncer()
        print("Querying all Xboxs")
        ftp_dump = syncer.query_all()
        print("FTP Dump")
        print(ftp_dump)
        ftp_instructions = generate_ftp_instructions(ftp_dump)
        print("FTP Instructions")
        print(ftp_instructions)
        syncer.purge_old_saves()
        syncer.create_directories_on_nas()
        handle_ftp_instructions(syncer, ftp_instructions)
        return generate_response(200, ftp_instructions)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/fleet_control/vehicle_list", endpoint="fleet_vehicle_list", methods=["GET"])
def fleet_vehicle_list():
    try:
        vehicles = retrieve_vehicle_list()
        return generate_response(200, vehicles)
    except Exception as e:
        return generate_response(500, {"error": str(e)})


@app.route("/fleet_control/vehicle_add", endpoint="fleet_vehicle_add", methods=["POST"])
def fleet_vehicle_add():
    try:
        payload = request.get_json()
        if not payload:
            return generate_response(400, {"error": "Missing JSON body"})

        name = payload.get("name")
        description = payload.get("description")

        if not name or not isinstance(name, str):
            return generate_response(400, {"error": "Invalid or missing 'name'"})
        if not description or not isinstance(description, str):
            return generate_response(400, {"error": "Invalid or missing 'description'"})

        # Use fixed Z: path for vehicles.json
        z_path = r"Z:\Private\fleet_control\vehicle_data\vehicles.json"
        vehicles_path = z_path
        vehicles = []
        if os.path.exists(vehicles_path):
            try:
                with open(vehicles_path, "r", encoding="utf-8") as fh:
                    vehicles = json.load(fh)
                    if not isinstance(vehicles, list):
                        vehicles = []
            except Exception:
                # If file exists but is invalid, overwrite with a fresh list
                vehicles = []

        new_item = {"name": name, "description": description}
        vehicles.append(new_item)

        # Persist updated list (flush and fsync to ensure write-through)
        with open(vehicles_path, "w", encoding="utf-8") as fh:
            json.dump(vehicles, fh, indent=4)
            fh.flush()
            try:
                os.fsync(fh.fileno())
            except Exception:
                # os.fsync may not be available on all platforms/open modes; ignore if it fails
                pass

        # Verify the file was written and read it back
        file_exists = os.path.exists(vehicles_path)
        file_count = None
        try:
            if file_exists:
                with open(vehicles_path, "r", encoding="utf-8") as fh:
                    loaded = json.load(fh)
                    if isinstance(loaded, list):
                        file_count = len(loaded)
        except Exception:
            file_exists = False
            file_count = None

        resp = {"vehicle": new_item, "vehicles_path": vehicles_path, "file_exists": file_exists, "total": file_count}
        return generate_response(200, resp)
    except Exception as e:
        return generate_response(500, {"error": str(e)})


@app.route("/fleet_control/vehicle_maintenance", endpoint="fleet_vehicle_maintenance", methods=["GET", "POST", "PUT", "DELETE"])
def fleet_vehicle_maintenance():
    try:
        if request.method == "GET":
            # Return all maintenance records or filter by vehicle_name if provided
            vehicle_name = request.args.get("vehicle_name")
            maintenance_path = rf"Z:\Private\fleet_control\vehicle_data\{vehicle_name.replace(' ', '_').replace('.', '_')}_maintenance.json"

            maintenance_records = []
            if os.path.exists(maintenance_path):
                try:
                    with open(maintenance_path, "r", encoding="utf-8") as fh:
                        maintenance_records = json.load(fh)
                        if not isinstance(maintenance_records, list):
                            maintenance_records = []
                        
                        # Ensure all records have IDs (for backward compatibility)
                        updated = False
                        for record in maintenance_records:
                            if "id" not in record:
                                record["id"] = str(uuid.uuid4())
                                updated = True
                        
                        # Save back if we added IDs
                        if updated:
                            with open(maintenance_path, "w", encoding="utf-8") as write_fh:
                                json.dump(maintenance_records, write_fh, indent=4)
                                write_fh.flush()
                                try:
                                    os.fsync(write_fh.fileno())
                                except Exception:
                                    pass
                                    
                except Exception:
                    maintenance_records = []
                        
            return generate_response(200, maintenance_records)
        
        elif request.method == "POST":
            # Add new maintenance record
            payload = request.get_json()
            if not payload:
                return generate_response(400, {"error": "Missing JSON body"})
            
            vehicle_name = request.args.get("vehicle_name")
            if not vehicle_name:
                return generate_response(400, {"error": "Missing 'vehicle_name' parameter"})
                
            maintenance_path = rf"Z:\Private\fleet_control\vehicle_data\{vehicle_name.replace(' ', '_').replace('.', '_')}_maintenance.json"

            job = payload.get("job")
            date_started = payload.get("date_started")
            date_completed = payload.get("date_completed")
            mileage = payload.get("mileage")
            hours = payload.get("hours")
            notes = payload.get("notes")
            cost = payload.get("cost")
                        
            # Load existing maintenance records
            maintenance_records = []
            if os.path.exists(maintenance_path):
                try:
                    with open(maintenance_path, "r", encoding="utf-8") as fh:
                        maintenance_records = json.load(fh)
                        if not isinstance(maintenance_records, list):
                            maintenance_records = []
                except Exception:
                    maintenance_records = []
            
            # Create new maintenance record with unique ID
            new_record = {
                "id": len(maintenance_records) + 1,
                "job": job,
                "date_started": date_started,
                "date_completed": date_completed,
                "notes": notes,
                "cost": cost
            }
            if mileage:
                new_record["milage"] = mileage
            elif hours:
                new_record["hours"] = hours
            maintenance_records.append(new_record)
            
            # Save to file
            with open(maintenance_path, "w", encoding="utf-8") as fh:
                json.dump(maintenance_records, fh, indent=4)
                fh.flush()
                try:
                    os.fsync(fh.fileno())
                except Exception:
                    pass
            
            return generate_response(200, new_record)
        
        elif request.method == "PUT":
            # Update existing maintenance record by ID
            record_id = request.args.get("id")
            payload = request.get_json()
            vehicle_name = request.args.get("vehicle_name")
            
            if not payload:
                return generate_response(400, {"error": "Missing JSON body"})
            if not record_id:
                return generate_response(400, {"error": "Missing 'id' parameter"})
            if not vehicle_name:
                return generate_response(400, {"error": "Missing 'vehicle_name' parameter"})
            
            maintenance_path = rf"Z:\Private\fleet_control\vehicle_data\{vehicle_name.replace(' ', '_').replace('.', '_')}_maintenance.json"
            
            # Load existing maintenance records
            maintenance_records = []
            if os.path.exists(maintenance_path):
                try:
                    with open(maintenance_path, "r", encoding="utf-8") as fh:
                        maintenance_records = json.load(fh)
                        if not isinstance(maintenance_records, list):
                            maintenance_records = []
                except Exception:
                    maintenance_records = []
            
            # Find and update the record
            record_found = False
            for i, record in enumerate(maintenance_records):
                if record.get("id") == record_id:
                    # Update the record with new data, preserving the ID
                    updated_record = {
                        "id": record_id,
                        "job": payload.get("job", record.get("job")),
                        "date_started": payload.get("date_started", record.get("date_started")),
                        "date_completed": payload.get("date_completed", record.get("date_completed")),
                        "notes": payload.get("notes", record.get("notes")),
                        "cost": payload.get("cost", record.get("cost"))
                    }
                    
                    # Handle optional fields
                    if "mileage" in payload:
                        updated_record["milage"] = payload["mileage"]
                    elif "milage" in record:
                        updated_record["milage"] = record["milage"]
                    
                    if "hours" in payload:
                        updated_record["hours"] = payload["hours"]
                    elif "hours" in record:
                        updated_record["hours"] = record["hours"]
                    
                    maintenance_records[i] = updated_record
                    record_found = True
                    break
            
            if not record_found:
                return generate_response(404, {"error": "Record not found"})
            
            # Save updated records
            with open(maintenance_path, "w", encoding="utf-8") as fh:
                json.dump(maintenance_records, fh, indent=4)
                fh.flush()
                try:
                    os.fsync(fh.fileno())
                except Exception:
                    pass
            
            return generate_response(200, updated_record)
        
        elif request.method == "DELETE":
            # Delete maintenance record by ID
            record_id = request.args.get("id")
            vehicle_name = request.args.get("vehicle_name")
            
            if not record_id:
                return generate_response(400, {"error": "Missing 'id' parameter"})
            if not vehicle_name:
                return generate_response(400, {"error": "Missing 'vehicle_name' parameter"})

            maintenance_path = rf"Z:\Private\fleet_control\vehicle_data\{vehicle_name.replace(' ', '_').replace('.', '_')}_maintenance.json"
            
            # Load existing maintenance records
            maintenance_records = []
            if os.path.exists(maintenance_path):
                try:
                    with open(maintenance_path, "r", encoding="utf-8") as fh:
                        maintenance_records = json.load(fh)
                        if not isinstance(maintenance_records, list):
                            maintenance_records = []
                except Exception:
                    maintenance_records = []
            
            # Find and remove the record by ID
            original_count = len(maintenance_records)
            deleted_record = None
            maintenance_records = [
                record for record in maintenance_records 
                if record.get("id") != record_id or (deleted_record := record, False)[1]
            ]
            
            if len(maintenance_records) == original_count:
                return generate_response(404, {"error": "Record not found"})
            
            # Save updated records
            with open(maintenance_path, "w", encoding="utf-8") as fh:
                json.dump(maintenance_records, fh, indent=4)
                fh.flush()
                try:
                    os.fsync(fh.fileno())
                except Exception:
                    pass
            
            return generate_response(200, {"message": "Record deleted successfully", "deleted_id": record_id})
            
    except Exception as e:
        return generate_response(500, {"error": str(e)})


@app.route("/fleet_control/vehicle_purchases", endpoint="fleet_vehicle_purchases", methods=["GET", "POST", "PUT", "DELETE"])
def fleet_vehicle_purchases():
    try:
        if request.method == "GET":
            # Return all purchase records or filter by vehicle_name if provided
            vehicle_name = request.args.get("vehicle_name")
            if not vehicle_name:
                return generate_response(400, {"error": "Missing 'vehicle_name' parameter"})
                
            purchases_path = rf"Z:\Private\fleet_control\vehicle_data\{vehicle_name.replace(' ', '_').replace('.', '_')}_purchases.json"

            purchase_records = []
            if os.path.exists(purchases_path):
                try:
                    with open(purchases_path, "r", encoding="utf-8") as fh:
                        purchase_records = json.load(fh)
                        if not isinstance(purchase_records, list):
                            purchase_records = []
                        
                        # Ensure all records have IDs (for backward compatibility)
                        updated = False
                        for record in purchase_records:
                            if "id" not in record:
                                record["id"] = str(uuid.uuid4())
                                updated = True
                        
                        # Save back if we added IDs
                        if updated:
                            with open(purchases_path, "w", encoding="utf-8") as write_fh:
                                json.dump(purchase_records, write_fh, indent=4)
                                write_fh.flush()
                                try:
                                    os.fsync(write_fh.fileno())
                                except Exception:
                                    pass
                                    
                except Exception:
                    purchase_records = []
                        
            return generate_response(200, purchase_records)
        
        elif request.method == "POST":
            # Add new purchase record
            vehicle_name = request.args.get("vehicle_name")
            payload = request.get_json()
            if not payload:
                return generate_response(400, {"error": "Missing JSON body"})
            if not vehicle_name:
                return generate_response(400, {"error": "Missing 'vehicle_name' parameter"})
            
            item = payload.get("item")
            date_purchased = payload.get("date_purchased")
            installed = payload.get("installed")
            cost = payload.get("cost")
            store = payload.get("store")
                        
            purchases_path = rf"Z:\Private\fleet_control\vehicle_data\{vehicle_name.replace(' ', '_').replace('.', '_')}_purchases.json"
            
            # Load existing purchase records
            purchase_records = []
            if os.path.exists(purchases_path):
                try:
                    with open(purchases_path, "r", encoding="utf-8") as fh:
                        purchase_records = json.load(fh)
                        if not isinstance(purchase_records, list):
                            purchase_records = []
                except Exception:
                    purchase_records = []
            
            # Create new purchase record with unique ID
            new_record = {
                "id": len(purchase_records) + 1,
                "item": item,
                "date_purchased": date_purchased,
                "installed": installed,
                "cost": cost,
                "store": store
            }
            purchase_records.append(new_record)
            
            # Save to file
            with open(purchases_path, "w", encoding="utf-8") as fh:
                json.dump(purchase_records, fh, indent=4)
                fh.flush()
                try:
                    os.fsync(fh.fileno())
                except Exception:
                    pass
            
            return generate_response(200, new_record)
        
        elif request.method == "PUT":
            # Update existing purchase record
            record_id = request.args.get("id")
            vehicle_name = request.args.get("vehicle_name")
            payload = request.get_json()
            
            if not payload:
                return generate_response(400, {"error": "Missing JSON body"})
            if not record_id:
                return generate_response(400, {"error": "Missing 'id' parameter"})
            if not vehicle_name:
                return generate_response(400, {"error": "Missing 'vehicle_name' parameter"})
            
            purchases_path = rf"Z:\Private\fleet_control\vehicle_data\{vehicle_name.replace(' ', '_').replace('.', '_')}_purchases.json"
            
            # Load existing purchase records
            purchase_records = []
            if os.path.exists(purchases_path):
                try:
                    with open(purchases_path, "r", encoding="utf-8") as fh:
                        purchase_records = json.load(fh)
                        if not isinstance(purchase_records, list):
                            purchase_records = []
                except Exception:
                    purchase_records = []
            
            # Find and update the record
            record_found = False
            for i, record in enumerate(purchase_records):
                if record.get("id") == record_id:
                    # Update the record with new data, preserving the ID and existing values if not provided
                    updated_record = {
                        "id": record_id,
                        "item": payload.get("item", record.get("item")),
                        "date_purchased": payload.get("date_purchased", record.get("date_purchased")),
                        "installed": payload.get("installed", record.get("installed")),
                        "cost": payload.get("cost", record.get("cost")),
                        "store": payload.get("store", record.get("store")),
                    }
                    purchase_records[i] = updated_record
                    record_found = True
                    break
            
            if not record_found:
                return generate_response(404, {"error": "Record not found"})
            
            # Save updated records
            with open(purchases_path, "w", encoding="utf-8") as fh:
                json.dump(purchase_records, fh, indent=4)
                fh.flush()
                try:
                    os.fsync(fh.fileno())
                except Exception:
                    pass
            
            return generate_response(200, updated_record)
        
        elif request.method == "DELETE":
            # Delete purchase record by ID
            record_id = request.args.get("id")
            vehicle_name = request.args.get("vehicle_name")
            
            if not record_id:
                return generate_response(400, {"error": "Missing 'id' parameter"})
            if not vehicle_name:
                return generate_response(400, {"error": "Missing 'vehicle_name' parameter"})
            
            purchases_path = rf"Z:\Private\fleet_control\vehicle_data\{vehicle_name.replace(' ', '_').replace('.', '_')}_purchases.json"
            
            # Load existing purchase records
            purchase_records = []
            if os.path.exists(purchases_path):
                try:
                    with open(purchases_path, "r", encoding="utf-8") as fh:
                        purchase_records = json.load(fh)
                        if not isinstance(purchase_records, list):
                            purchase_records = []
                except Exception:
                    purchase_records = []
            
            # Find and remove the record by ID
            original_count = len(purchase_records)
            purchase_records = [record for record in purchase_records if record.get("id") != record_id]
            
            if len(purchase_records) == original_count:
                return generate_response(404, {"error": "Record not found"})
            
            # Save updated records
            with open(purchases_path, "w", encoding="utf-8") as fh:
                json.dump(purchase_records, fh, indent=4)
                fh.flush()
                try:
                    os.fsync(fh.fileno())
                except Exception:
                    pass
            
            return generate_response(200, {"message": "Record deleted successfully", "deleted_id": record_id})
            
    except Exception as e:
        return generate_response(500, {"error": str(e)})


if __name__ == "__main__":
    app.run(host="192.168.0.219", port=5000, debug=True)

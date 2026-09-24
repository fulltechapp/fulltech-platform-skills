import sys
import json
import asyncio

async def get_lockdown():
    from pymobiledevice3.lockdown import create_using_usbmux
    return await create_using_usbmux()

async def action_info():
    try:
        lockdown = await get_lockdown()
        vals = lockdown.all_values
        return {
            "status": "success",
            "data": {
                "DeviceName": vals.get("DeviceName"),
                "ProductType": vals.get("ProductType"),
                "ProductVersion": vals.get("ProductVersion"),
                "BuildVersion": vals.get("BuildVersion"),
                "SerialNumber": vals.get("SerialNumber"),
                "UniqueDeviceID": vals.get("UniqueDeviceID"),
                "ModelNumber": vals.get("ModelNumber"),
                "WiFiAddress": vals.get("WiFiAddress"),
                "PasswordProtected": vals.get("PasswordProtected"),
                "PhoneNumber": vals.get("PhoneNumber"),
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def action_battery():
    try:
        lockdown = await get_lockdown()
        from pymobiledevice3.services.diagnostics import DiagnosticsService
        async with DiagnosticsService(lockdown) as diag:
            bat = await diag.get_battery()
            
            cycle_count = bat.get("CycleCount")
            design_cap = bat.get("DesignCapacity")
            nominal_cap = bat.get("NominalChargeCapacity")
            current_cap = bat.get("CurrentCapacity")
            temp = bat.get("Temperature")
            is_charging = bat.get("IsCharging")
            
            health_pct = None
            if design_cap and nominal_cap:
                health_pct = round((nominal_cap / design_cap) * 100.0, 1)
                
            temp_c = None
            if temp is not None:
                temp_c = round(temp / 100.0, 1)

            return {
                "status": "success",
                "data": {
                    "CycleCount": cycle_count,
                    "DesignCapacity": design_cap,
                    "NominalChargeCapacity": nominal_cap,
                    "CurrentCapacity": current_cap,
                    "HealthPercentage": health_pct,
                    "TemperatureC": temp_c,
                    "IsCharging": is_charging
                }
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def action_apps():
    try:
        lockdown = await get_lockdown()
        from pymobiledevice3.services.installation_proxy import InstallationProxyService
        async with InstallationProxyService(lockdown) as proxy:
            apps = await proxy.get_apps(application_type="User")
            summary = []
            for k, v in apps.items():
                summary.append({
                    "bundle_id": k,
                    "name": v.get("CFBundleDisplayName") or v.get("CFBundleName") or k,
                    "version": v.get("CFBundleShortVersionString")
                })
            return {
                "status": "success",
                "data": summary
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def action_crashes():
    try:
        lockdown = await get_lockdown()
        from pymobiledevice3.services.crash_reports import CrashReportsManager
        async with CrashReportsManager(lockdown) as cm:
            files = await cm.ls('/')
            suspicious = [f for f in files if any(k in f.lower() for k in ['panic', 'jetsam', 'watchdog', 'stackshot'])]
            panics = []
            try:
                panics = await cm.ls('/Panics')
            except Exception:
                pass
            return {
                "status": "success",
                "data": {
                    "total_reports": len(files),
                    "suspicious_reports": suspicious,
                    "panics_count": len(panics)
                }
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "info"
    if action == "info":
        res = await action_info()
    elif action == "battery":
        res = await action_battery()
    elif action == "apps":
        res = await action_apps()
    elif action == "crashes":
        res = await action_crashes()
    elif action == "all":
        res = {
            "info": await action_info(),
            "battery": await action_battery(),
            "apps": await action_apps(),
            "crashes": await action_crashes()
        }
    else:
        res = {"status": "error", "message": f"Unknown action: {action}"}
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

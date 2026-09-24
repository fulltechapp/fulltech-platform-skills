import sys
import json
import asyncio

async def get_lockdown():
    from pymobiledevice3.lockdown import create_using_usbmux
    return await create_using_usbmux()

async def action_uninstall(bundle_id):
    try:
        lockdown = await get_lockdown()
        from pymobiledevice3.services.installation_proxy import InstallationProxyService
        async with InstallationProxyService(lockdown) as proxy:
            await proxy.uninstall(bundle_id)
            return {
                "status": "success",
                "bundle_id": bundle_id,
                "message": f"Aplicativo '{bundle_id}' desinstalado com sucesso via Lockdown."
            }
    except Exception as e:
        return {"status": "error", "bundle_id": bundle_id, "message": str(e)}

async def action_clear_crashes():
    try:
        lockdown = await get_lockdown()
        from pymobiledevice3.services.crash_reports import CrashReportsManager
        async with CrashReportsManager(lockdown) as cm:
            files = await cm.ls('/')
            cleared = 0
            for f in files:
                try:
                    await cm.remove(f)
                    cleared += 1
                except Exception:
                    pass
            return {
                "status": "success",
                "cleared_count": cleared,
                "message": f"{cleared} arquivos de diagnósticos e relatórios de crash limpos com sucesso."
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def action_remove_profile(profile_id):
    try:
        lockdown = await get_lockdown()
        from pymobiledevice3.services.mobileconfig import MobileConfigService
        async with MobileConfigService(lockdown) as mcs:
            await mcs.remove_profile(profile_id)
            return {
                "status": "success",
                "profile_id": profile_id,
                "message": f"Perfil '{profile_id}' removido com sucesso."
            }
    except Exception as e:
        return {"status": "error", "profile_id": profile_id, "message": str(e)}

async def action_check_app(bundle_id):
    try:
        lockdown = await get_lockdown()
        from pymobiledevice3.services.installation_proxy import InstallationProxyService
        async with InstallationProxyService(lockdown) as proxy:
            apps = await proxy.get_apps(application_type="User")
            is_installed = bundle_id in apps
            name = None
            version = None
            if is_installed:
                app_info = apps[bundle_id]
                name = app_info.get("CFBundleDisplayName") or app_info.get("CFBundleName") or bundle_id
                version = app_info.get("CFBundleShortVersionString")
            return {
                "status": "success",
                "bundle_id": bundle_id,
                "installed": is_installed,
                "name": name,
                "version": version
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def action_install_profile(profile_path):
    try:
        lockdown = await get_lockdown()
        from pymobiledevice3.services.mobileconfig import MobileConfigService
        async with MobileConfigService(lockdown) as mcs:
            with open(profile_path, 'rb') as f:
                content = f.read()
            await mcs.install_profile(content)
            return {
                "status": "success",
                "message": "Perfil enviado com sucesso via cabo USB! O alerta de instalacao foi aberto diretamente na tela do iPhone."
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Nenhuma acao especificada"}))
        return

    action = sys.argv[1].lower()
    
    if action == "uninstall":
        bundle_id = sys.argv[2] if len(sys.argv) > 2 else "com.mediamushroom.copymydata2"
        res = await action_uninstall(bundle_id)
    elif action == "clear_crashes":
        res = await action_clear_crashes()
    elif action == "remove_profile":
        if len(sys.argv) < 3:
            res = {"status": "error", "message": "ID do perfil obrigatorio"}
        else:
            res = await action_remove_profile(sys.argv[2])
    elif action == "install_profile":
        if len(sys.argv) < 3:
            res = {"status": "error", "message": "Caminho do arquivo .mobileconfig obrigatorio"}
        else:
            res = await action_install_profile(sys.argv[2])
    elif action == "check_app":
        bundle_id = sys.argv[2] if len(sys.argv) > 2 else "com.mediamushroom.copymydata2"
        res = await action_check_app(bundle_id)
    else:
        res = {"status": "error", "message": f"Acao desconhecida: {action}"}

    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

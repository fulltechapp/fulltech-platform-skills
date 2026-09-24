"""Render linux_triage.json into a standalone HTML report (fulltech.app design system)."""
import datetime
import html
import json
import sys

CSS = """
:root {
    --bg: #090A0F; --card: #11131A; --border: #1E2230; --text: #F8FAFC; --text-muted: #94A3B8;
    --accent: #10B981; --cyan: #38BDF8; --rose: #F43F5E; --amber: #F59E0B;
    --font-sans: 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: var(--font-sans); font-size: 15px;
       line-height: 1.6; -webkit-font-smoothing: antialiased; padding: 40px 16px; }
.container { max-width: 960px; margin: 0 auto; }
header { padding-bottom: 24px; border-bottom: 1px solid var(--border); margin-bottom: 32px; }
h1 { font-size: 24px; font-weight: 700; letter-spacing: -0.5px; }
h2 { font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted); margin: 32px 0 12px; }
.meta { color: var(--text-muted); font-family: var(--font-mono); font-size: 12px; margin-top: 6px; }
.verdict { background: var(--card); border: 1px solid var(--border); border-left: 4px solid var(--accent);
           border-radius: 12px; padding: 20px 24px; font-size: 17px; font-weight: 500; }
.verdict.warn { border-left-color: var(--amber); } .verdict.crit { border-left-color: var(--rose); }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
.metric { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }
.metric .label { color: var(--text-muted); font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
.metric .value { font-family: var(--font-mono); font-size: 20px; font-weight: 600; margin-top: 4px; overflow-wrap: anywhere; }
.finding { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; margin-bottom: 10px; }
.finding .title { font-weight: 600; }
.finding .detail { color: var(--text-muted); font-size: 14px; margin-top: 4px; }
.tag { font-family: var(--font-mono); font-size: 11px; padding: 2px 8px; border-radius: 6px; margin-right: 8px; }
.tag.crit { background: rgba(244,63,94,.15); color: var(--rose); }
.tag.warn { background: rgba(245,158,11,.15); color: var(--amber); }
.tag.info { background: rgba(56,189,248,.15); color: var(--cyan); }
footer { color: var(--text-muted); font-size: 12px; margin-top: 40px; text-align: center; }
"""

SEVERITY_ORDER = {"crit": 0, "warn": 1, "info": 2}


def mb(value):
    if value is None:
        return "n/d"
    return f"{value / 1024:.1f} GB" if value >= 1024 else f"{value} MB"


def findings(d):
    out = []
    add = lambda sev, title, detail: out.append((sev, title, detail))
    sysinfo, disk, pkgs, sec = d["System"], d["Disk"], d["Packages"], d["Security"]

    used = disk["RootUsedPercent"]
    if used >= 90:
        add("crit", f"Disco raiz {used}% cheio", "Risco de falha em atualizacoes e servicos. Liberar espaco agora.")
    elif used >= 80:
        add("warn", f"Disco raiz {used}% cheio", "Ainda funcional, mas perto do limite.")

    if sysinfo["SwapTotalMB"] and sysinfo["SwapFreeMB"] < sysinfo["SwapTotalMB"] * 0.5:
        add("warn", "Swap mais da metade em uso",
            f"RAM disponivel: {mb(sysinfo['RamAvailableMB'])} de {mb(sysinfo['RamTotalMB'])}. Sinal de pressao de memoria.")
    if sysinfo.get("MaxThermalC") and sysinfo["MaxThermalC"] >= 85:
        add("crit", f"Temperatura {sysinfo['MaxThermalC']} C", "Verificar ventilacao e pasta termica.")

    if pkgs.get("SecurityUpgradable"):
        add("crit", f"{pkgs['SecurityUpgradable']} atualizacoes de seguranca pendentes", "Aplicar com apt upgrade.")
    if pkgs.get("Upgradable"):
        add("info", f"{pkgs['Upgradable']} pacotes atualizaveis", "Inclui as atualizacoes de seguranca acima, se houver.")
    if pkgs.get("Autoremovable"):
        add("info", f"{pkgs['Autoremovable']} pacotes orfaos", "Removiveis com remediate.sh --clean-packages.")

    for key, limit, label, action in [
        ("AptCacheMB", 500, "Cache do apt", "--clean-packages"),
        ("JournalMB", 1024, "Journal do systemd", "--vacuum-journal"),
    ]:
        if (disk.get(key) or 0) >= limit:
            add("warn", f"{label}: {mb(disk[key])}", f"Recuperavel com remediate.sh {action}.")
    if (disk.get("UserCacheMB") or 0) >= 2048:
        add("info", f"~/.cache: {mb(disk['UserCacheMB'])}", "Revisar manualmente; contem caches de apps do usuario.")
    if disk["DisabledSnapRevisions"]:
        add("warn", f"{len(disk['DisabledSnapRevisions'])} revisoes antigas de snaps", "Recuperavel com remediate.sh --prune-snaps.")
    if disk["DockerPresent"] and disk["DockerReclaimable"][:1] and disk["DockerReclaimable"][0].startswith("indisponivel"):
        add("info", "Docker: espaco nao medido", "docker system df excedeu 30s ou sem permissao. Rodar manualmente.")
    elif disk["DockerPresent"] and disk["DockerReclaimable"]:
        add("info", "Docker: espaco recuperavel", "; ".join(disk["DockerReclaimable"]) + ". Avaliar docker system prune manualmente.")

    if d["Services"]["Failed"]:
        add("warn", f"{len(d['Services']['Failed'])} servicos com falha", ", ".join(d["Services"]["Failed"]))
    if sec["TelemetryPackages"] or sec["MotdNewsEnabled"]:
        items = sec["TelemetryPackages"] + (["motd-news"] if sec["MotdNewsEnabled"] else [])
        add("info", "Telemetria ativa", ", ".join(items) + ". Desativavel com remediate.sh --disable-telemetry.")

    wsl = d.get("WSL")
    if wsl:
        if wsl["AppendWindowsPath"].lower() != "false" and wsl["WindowsPathEntries"]:
            add("warn", f"{wsl['WindowsPathEntries']} pastas do Windows no PATH",
                "Deixa o shell lento. Corrigir com remediate.sh --wsl-windows-path.")
        if wsl["GenerateHosts"].lower() != "false":
            add("info", "/etc/hosts gerado pelo Windows", "Sinkhole deve ser aplicado no Windows (windows-sanitizer).")
        if not wsl["WslConfigFiles"]:
            add("info", "Sem .wslconfig", "WSL2 pode usar ate 50% da RAM do Windows. Considerar limitar memory= no .wslconfig.")

    return sorted(out, key=lambda f: SEVERITY_ORDER[f[0]])


def render(d):
    e = html.escape
    items = findings(d)
    worst = items[0][0] if items else "info"
    verdict = {
        "crit": "Requer acao: ha problemas criticos abaixo.",
        "warn": "Saudavel com ressalvas: ha espaco a recuperar ou ajustes recomendados.",
        "info": "Sistema saudavel. Nenhum problema relevante encontrado.",
    }[worst]
    env, sysinfo, disk = d["Environment"], d["System"], d["Disk"]
    metrics = [
        ("Ambiente", env["Type"]), ("Sistema", sysinfo["OS"]), ("Kernel", sysinfo["Kernel"]),
        ("CPU", f"{sysinfo['CPU']} ({sysinfo['Cores']} cores)"),
        ("RAM disponivel", f"{mb(sysinfo['RamAvailableMB'])} / {mb(sysinfo['RamTotalMB'])}"),
        ("Disco livre", f"{mb(disk['RootFreeMB'])} / {mb(disk['RootTotalMB'])}"),
    ]
    metric_html = "".join(
        f'<div class="metric"><div class="label">{e(k)}</div><div class="value">{e(str(v))}</div></div>' for k, v in metrics)
    finding_html = "".join(
        f'<div class="finding"><div class="title"><span class="tag {s}">{s.upper()}</span>{e(t)}</div>'
        f'<div class="detail">{e(det)}</div></div>' for s, t, det in items) or '<div class="finding">Nada a reportar.</div>'
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Laudo Linux | Fulltech</title>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body><div class="container">
<header><h1>Laudo de Saude do Linux</h1><div class="meta">{e(sysinfo['OS'])} · {e(env['Type'])} · {now}</div></header>
<div class="verdict {worst}">{e(verdict)}</div>
<h2>Sistema</h2><div class="grid">{metric_html}</div>
<h2>Achados ({len(items)})</h2>{finding_html}
<footer>Gerado por linux-sanitizer · fulltech.app</footer>
</div></body></html>
"""


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "linux_triage.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "linux_report.html"
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(data))
    print(f"[+] Relatorio gerado em {out}")


if __name__ == "__main__":
    main()

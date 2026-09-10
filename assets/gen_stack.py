#!/usr/bin/env python3
"""Gera o card de stack do README a partir dos SVGs do simple-icons."""
import re, pathlib

D = pathlib.Path(__file__).parent / "ico"
OUT = pathlib.Path(__file__).parent / "stack.html"

# (slug, rótulo). slug None = sem logo, vira chip só de texto.
COLS = [
    [
        ("Infraestrutura", [
            ("linux", "Linux"), ("debian", "Debian"), ("docker", "Docker"),
            ("kubernetes", "Kubernetes"), ("rancher", "Rancher"), ("ansible", "Ansible"),
            ("proxmox", "Proxmox"), ("vmware", "VMware"), ("nginx", "Nginx"),
            ("traefikproxy", "Traefik"), ("cloudflare", "Cloudflare"), ("apachetomcat", "Tomcat"),
        ]),
        ("Redes, segurança e observabilidade", [
            ("asterisk", "Asterisk"), ("pfsense", "pfSense"), ("mikrotik", "Mikrotik"),
            ("wireguard", "WireGuard"), ("openvpn", "OpenVPN"), ("grafana", "Grafana"),
            ("prometheus", "Prometheus"), ("sentry", "Sentry"),
        ]),
        ("Bancos de dados", [
            ("postgresql", "PostgreSQL"), ("mysql", "MySQL"), ("mongodb", "MongoDB"),
            ("redis", "Redis"), ("clickhouse", "ClickHouse"), ("sqlite", "SQLite"),
        ]),
        ("Ferramentas", [
            ("git", "Git"), ("githubactions", "Actions"), ("precommit", "pre-commit"),
            ("pytest", "pytest"), ("vitest", "Vitest"), ("postman", "Postman"),
        ]),
    ],
    [
        ("Linguagens", [
            ("python", "Python"), ("typescript", "TypeScript"), ("javascript", "JavaScript"),
            ("csharp", "C#"), ("php", "PHP"), ("gnubash", "Bash"),
            ("openjdk", "Java"), ("swift", "Swift"),
        ]),
        ("Backend", [
            ("fastapi", "FastAPI"), ("flask", "Flask"), ("dotnet", "ASP.NET"),
            ("laravel", "Laravel"), ("springboot", "Spring"), ("nodedotjs", "Node.js"),
            ("fastify", "Fastify"), ("sqlalchemy", "SQLAlchemy"), ("celery", "Celery"),
            ("rabbitmq", "RabbitMQ"), ("socketdotio", "Socket.IO"),
        ]),
        ("Frontend", [
            ("react", "React"), ("nextdotjs", "Next.js"), ("vite", "Vite"), ("bun", "Bun"),
            ("tailwindcss", "Tailwind"), ("shadcnui", "shadcn/ui"), ("mui", "MUI"),
            ("reactquery", "TanStack"), ("reacthookform", "Hook Form"), ("zod", "Zod"),
            ("streamlit", "Streamlit"),
        ]),
    ],
]

RODAPE = ("SQL / PL-pgSQL · Entity Framework Core · Alembic · Pydantic · APScheduler · Recharts · "
          "RKE2 · MetalLB · Sealed Secrets · Coolify · Windows Server (IIS, Apache, Samba, "
          "Active Directory) · TR-069 / GenieACS · SNMP · DNS (Bind) · nftables · Fail2Ban · "
          "CrowdSec · gitleaks · Loki · Promtail · GlitchTip · Zabbix · MCP · Jasper Reports · "
          "QuestPDF · WeasyPrint")


def svg(slug):
    """Devolve o SVG do simple-icons pronto pra herdar cor do CSS."""
    raw = (D / f"{slug}.svg").read_text()
    raw = re.sub(r"<title>.*?</title>", "", raw)
    return raw.replace("<svg ", '<svg class="ic" ', 1)


def bloco(titulo, itens):
    celulas = "".join(
        f'<div class="it">{svg(s)}<span>{lbl}</span></div>' for s, lbl in itens
    )
    return f'<div class="grp"><div class="lbl">{titulo}</div><div class="row">{celulas}</div></div>'


colunas = "".join(
    f'<div class="col">{"".join(bloco(t, i) for t, i in col)}</div>' for col in COLS
)

OUT.write_text(f"""<!doctype html>
<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html,body {{ width:1200px; overflow:hidden; background:#0a0c10; }}
  .card {{
    position:relative; width:1200px; padding:40px 46px 30px; background:#0a0c10;
    background-image: radial-gradient(circle at 1px 1px, rgba(148,163,184,.15) 1px, transparent 0);
    background-size:22px 22px;
    font-family:"SF Pro Display","SF Pro Text",-apple-system,"Helvetica Neue",sans-serif;
  }}
  .glow {{ position:absolute; left:-180px; bottom:-260px; width:700px; height:700px; border-radius:50%;
           background:radial-gradient(circle, rgba(45,212,191,.10), transparent 62%); }}
  .cols {{ position:relative; display:flex; gap:54px; z-index:2; }}
  .col {{ flex:1; min-width:0; }}
  .grp {{ margin-bottom:26px; }}
  .grp:last-child {{ margin-bottom:0; }}
  .lbl {{ font-size:10.5px; letter-spacing:2.6px; text-transform:uppercase; color:#2dd4bf;
          font-weight:600; margin-bottom:14px; }}
  .row {{ display:flex; flex-wrap:wrap; gap:17px 8px; }}
  .it {{ width:56px; display:flex; flex-direction:column; align-items:center; gap:7px; }}
  .ic {{ width:26px; height:26px; fill:#cbd5e1; opacity:.92; }}
  .it span {{ font-size:8.8px; color:#7c8ea6; text-align:center; line-height:1.15;
              letter-spacing:.1px; white-space:nowrap; }}
  .rodape {{ position:relative; z-index:2; margin-top:32px; padding-top:18px;
             border-top:1px solid #1a2230; font-size:10.5px; line-height:1.85; color:#5b6b81; }}
</style>
<div class="card">
  <div class="glow"></div>
  <div class="cols">{colunas}</div>
  <div class="rodape">{RODAPE}</div>
</div>
""")
print("ok ->", OUT)

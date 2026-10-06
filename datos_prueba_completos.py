"""
datos_prueba_completos.py
Datos de prueba realistas para verificar que TODO funciona:
- 5 usuarios con distintas situaciones
- 6 tomas (uno con 2 tomas)
- Pagos de enero, febrero y marzo con todos los tipos
- Gastos reales de enero, febrero y marzo
- Ingresos extra
"""

import sqlite3

DB_PATH = "agua_potable.db"
OK    = "\033[92m✓\033[0m"
INFO  = "\033[94m→\033[0m"
TITLE = "\033[1m\033[96m"
RESET = "\033[0m"
SEP   = "─" * 60

def t(txt): print(f"\n{TITLE}{SEP}{RESET}\n{TITLE}  {txt}{RESET}\n{TITLE}{SEP}{RESET}")
def ok(txt): print(f"  {OK}  {txt}")
def info(txt): print(f"  {INFO}  {txt}")

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

# ─────────────────────────────────────────────────────────────
t("1. USUARIOS (5 personas reales del comité)")
# ─────────────────────────────────────────────────────────────
# Situaciones distintas:
# 1. Paga puntual mes a mes
# 2. Pagó el año completo en enero (oferta)
# 3. Tiene adeudo (no ha pagado enero ni febrero)
# 4. Paga adelantado
# 5. Tiene 2 tomas (casa y negocio)

usuarios = [
    ("Martínez Soria Rosa Elena",    "MORELOS"),
    ("Chávez Ruiz Joaquín",          "INDEPENDENCIA"),
    ("Bautista Manzo Francisco",     "JUAREZ"),
    ("Prado Canela Carlos",          "ALLENDE"),
    ("Manzo Pardo Salvador",         "MADERO"),
]
ids_u = []
for u in usuarios:
    c.execute("INSERT INTO usuarios (nombre, calle) VALUES (?,?)", u)
    ids_u.append(c.lastrowid)
    ok(f"Usuario {c.lastrowid}: {u[0]} — {u[1]}")
conn.commit()
u1,u2,u3,u4,u5 = ids_u
conn.commit()

# ─────────────────────────────────────────────────────────────
t("2. TOMAS (6 tomas — Manzo Pardo tiene 2)")
# ─────────────────────────────────────────────────────────────
# id_toma, id_usuario, calle, numero, tarifa, activa, fecha, notas
tomas = [
    (u1, "MORELOS",       "MR-01", 100.0, 1, "2025-01-10", None),
    (u2, "INDEPENDENCIA", "IN-07", 100.0, 1, "2025-03-15", None),
    (u3, "JUAREZ",        "JZ-03", 100.0, 1, "2024-06-01", None),
    (u4, "ALLENDE",       "AL-12", 100.0, 1, "2025-08-20", None),
    (u5, "MADERO",        "MD-05", 100.0, 1, "2023-02-10", "Casa"),
    (u5, "MADERO",        "MD-06", 100.0, 1, "2024-11-01", "Negocio (taller)"),
]
ids_t = []
for tm in tomas:
    c.execute("INSERT INTO tomas (id_usuario,calle,numero_toma,tarifa_mensual,activa,fecha_contrato,notas) VALUES (?,?,?,?,?,?,?)", tm)
    ids_t.append(c.lastrowid)
    ok(f"Toma {tm[2]} — Usuario {tm[0]} — ${tm[3]:.0f}/mes" + (f" — {tm[6]}" if tm[6] else ""))
conn.commit()
t1,t2,t3,t4,t5,t6 = ids_t
conn.commit()

# ─────────────────────────────────────────────────────────────
t("3. PAGOS DE ENERO")
# ─────────────────────────────────────────────────────────────
# Toma 1 (Rosa): paga enero normal $100
# Toma 2 (Chávez): paga AÑO COMPLETO en enero con oferta (paga 11 x $100 = $1100, lleva 12)
# Toma 3 (Bautista): NO paga (queda con adeudo)
# Toma 4 (Prado): paga enero normal $100
# Toma 5 (Manzo casa): paga enero normal $100
# Toma 6 (Manzo negocio): paga enero normal $100

info("Toma 1 — Rosa paga enero $100")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t1,'2026-01-08',100,'MENSUAL',2026,'Enero'))
p1 = c.lastrowid
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,1,2026,100,0)", (p1,))
ok(f"Pago #{p1} — Toma {t1} — Enero — $100")

info("Toma 2 — Chávez paga AÑO COMPLETO en enero (oferta: 1 mes gratis, paga 11)")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t2,'2026-01-10',1100,'ANUAL',2026,'Año completo — oferta enero: 1 mes gratis'))
p2 = c.lastrowid
for mes in range(1, 12):
    c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,?,2026,100,0)", (p2, mes))
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,12,2026,0,1)", (p2,))
ok(f"Pago #{p2} — Toma {t2} — Año completo $1100 — Dic bonificado")

info("Toma 3 — Bautista NO paga enero (quedará como adeudo)")
ok("Sin pago registrado — adeudo acumulándose")

info("Toma 4 — Prado paga enero $100")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t4,'2026-01-15',100,'MENSUAL',2026,'Enero'))
p4 = c.lastrowid
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,1,2026,100,0)", (p4,))
ok(f"Pago #{p4} — Toma {t4} — Enero — $100")

info("Toma 5 — Manzo casa paga enero $100")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t5,'2026-01-20',100,'MENSUAL',2026,'Enero'))
p5 = c.lastrowid
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,1,2026,100,0)", (p5,))
ok(f"Pago #{p5} — Toma {t5} — Enero — $100")

info("Toma 6 — Manzo negocio paga enero $100")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t6,'2026-01-20',100,'MENSUAL',2026,'Enero'))
p6 = c.lastrowid
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,1,2026,100,0)", (p6,))
ok(f"Pago #{p6} — Toma {t6} — Enero — $100")
conn.commit()

# ─────────────────────────────────────────────────────────────
t("4. PAGOS DE FEBRERO")
# ─────────────────────────────────────────────────────────────
# Toma 1 (Rosa): paga febrero $100
# Toma 2 (Chávez): ya pagó el año, no hace nada
# Toma 3 (Bautista): sigue sin pagar (adeudo enero+febrero)
# Toma 4 (Prado): paga febrero Y ADELANTA marzo, abril ($300)
# Toma 5 (Manzo casa): paga febrero $100
# Toma 6 (Manzo negocio): paga febrero $100

info("Toma 1 — Rosa paga febrero $100")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t1,'2026-02-06',100,'MENSUAL',2026,'Febrero'))
p = c.lastrowid
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,2,2026,100,0)", (p,))
ok(f"Pago #{p} — Toma {t1} — Febrero — $100")

info("Toma 2 — Chávez ya pagó el año, no paga")
ok("Sin movimiento — ya tiene todo el año cubierto")

info("Toma 3 — Bautista sigue sin pagar")
ok("Sin pago — adeudo acumulado: enero + febrero")

info("Toma 4 — Prado paga $300 (feb + adelanta mar y abr)")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t4,'2026-02-10',300,'ADELANTO',2026,'Febrero + adelanta marzo y abril'))
p = c.lastrowid
for mes in [2, 3, 4]:
    c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,?,2026,100,0)", (p, mes))
ok(f"Pago #{p} — Toma {t4} — $300 cubre feb, mar, abr")

info("Toma 5 — Manzo casa paga febrero $100")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t5,'2026-02-14',100,'MENSUAL',2026,'Febrero'))
p = c.lastrowid
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,2,2026,100,0)", (p,))
ok(f"Pago #{p} — Toma {t5} — Febrero — $100")

info("Toma 6 — Manzo negocio paga febrero $100")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t6,'2026-02-14',100,'MENSUAL',2026,'Febrero'))
p = c.lastrowid
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,2,2026,100,0)", (p,))
ok(f"Pago #{p} — Toma {t6} — Febrero — $100")
conn.commit()

# ─────────────────────────────────────────────────────────────
t("5. PAGOS DE MARZO")
# ─────────────────────────────────────────────────────────────
# Toma 1 (Rosa): paga marzo $100
# Toma 2 (Chávez): ya pagó el año
# Toma 3 (Bautista): LIQUIDA adeudo — paga enero+feb+mar = $300
# Toma 4 (Prado): ya tiene marzo pagado (adelantó en febrero)
# Toma 5 (Manzo casa): paga marzo $100
# Toma 6 (Manzo negocio): paga marzo $100

info("Toma 1 — Rosa paga marzo $100")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t1,'2026-03-07',100,'MENSUAL',2026,'Marzo'))
p = c.lastrowid
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,3,2026,100,0)", (p,))
ok(f"Pago #{p} — Toma {t1} — Marzo — $100")

info("Toma 3 — Bautista LIQUIDA adeudo enero+feb+mar = $300")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t3,'2026-03-07',300,'ADEUDO',2026,'Liquida adeudo: enero, febrero y marzo'))
p = c.lastrowid
for mes in [1, 2, 3]:
    c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,?,2026,100,0)", (p, mes))
ok(f"Pago #{p} — Toma {t3} — $300 liquida ene+feb+mar (adeudo saldado)")

info("Toma 5 — Manzo casa paga marzo $100")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t5,'2026-03-07',100,'MENSUAL',2026,'Marzo'))
p = c.lastrowid
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,3,2026,100,0)", (p,))
ok(f"Pago #{p} — Toma {t5} — Marzo — $100")

info("Toma 6 — Manzo negocio paga marzo $100")
c.execute("INSERT INTO pagos (id_toma,fecha_pago,monto_pagado,tipo_pago,anio,notas) VALUES (?,?,?,?,?,?)",(t6,'2026-03-07',100,'MENSUAL',2026,'Marzo'))
p = c.lastrowid
c.execute("INSERT INTO detalle_pagos_meses (id_pago,mes,anio,monto_mes,es_bonificado) VALUES (?,3,2026,100,0)", (p,))
ok(f"Pago #{p} — Toma {t6} — Marzo — $100")
conn.commit()

# ─────────────────────────────────────────────────────────────
t("6. GASTOS DE ENERO, FEBRERO Y MARZO")
# ─────────────────────────────────────────────────────────────
# id_categoria: 1=SUELDOS 2=LUZ 3=ARREGLOS_OFICINA 4=ARREGLOS_CALLE 5=CONTRATOS 6=OTROS
gastos = [
    (1, "2026-01-31", "Sueldo cobrador enero",             5000, 1),
    (1, "2026-01-31", "Sueldo fontanero enero",            4500, 1),
    (2, "2026-01-20", "Luz pozos enero",                   3200, 1),
    (4, "2026-01-12", "Reparación fuga calle Morelos",     1500, 1),
    (3, "2026-01-05", "Papelería oficina enero",            350, 1),
    (1, "2026-02-28", "Sueldo cobrador febrero",           5000, 2),
    (1, "2026-02-28", "Sueldo fontanero febrero",          4500, 2),
    (2, "2026-02-18", "Luz pozos febrero",                 3400, 2),
    (4, "2026-02-10", "Cambio tubería calle Independencia",2200, 2),
    (6, "2026-02-25", "Compra herramientas",                650, 2),
    (1, "2026-03-31", "Sueldo cobrador marzo",             5000, 3),
    (1, "2026-03-31", "Sueldo fontanero marzo",            4500, 3),
    (2, "2026-03-20", "Luz pozos marzo",                   3100, 3),
    (5, "2026-03-15", "Materiales nueva toma calle Juárez", 900, 3),
    (4, "2026-03-08", "Arreglo fuga calle Allende",         800, 3),
]
cats = {1:"SUELDOS",2:"LUZ",3:"ARREGLOS_OFICINA",4:"ARREGLOS_CALLE",5:"CONTRATOS",6:"OTROS"}
meses = {1:"Enero",2:"Febrero",3:"Marzo"}
for g in gastos:
    c.execute("INSERT INTO gastos (id_categoria,fecha,concepto,monto,mes,anio) VALUES (?,?,?,?,?,2026)", g)
    ok(f"{meses[g[4]]} — {cats[g[0]]:20s} — ${g[3]:,} — {g[2]}")
conn.commit()

# ─────────────────────────────────────────────────────────────
t("7. INGRESOS EXTRA (contratos nuevos)")
# ─────────────────────────────────────────────────────────────
extras = [
    ("2026-01-15", "Contrato nueva toma — Pérez Ceja Manuel",   500, 1),
    ("2026-02-20", "Contrato nueva toma — León Estrada Arturo", 500, 2),
    ("2026-03-05", "Contrato nueva toma — Soria Pérez Salvador",500, 3),
]
for e in extras:
    c.execute("INSERT INTO ingresos_extra (fecha,concepto,monto,mes,anio) VALUES (?,?,?,?,2026)", e)
    ok(f"{meses[e[3]]} — Contrato nuevo — $500 — {e[1]}")
conn.commit()


# ═════════════════════════════════════════════════════════════
# VERIFICACIÓN DE REPORTES
# ═════════════════════════════════════════════════════════════

t("✅ REPORTE 1 — PADRÓN DE TOMAS ACTIVAS")
c.execute("SELECT id_toma, nombre_usuario, calle_toma, numero_toma, tarifa_mensual FROM vista_padron")
for r in c.fetchall():
    ok(f"Toma {r[3]:6s} — {r[1]:30s} — {r[2]:15s} — ${r[4]:.0f}/mes")

t("✅ REPORTE 2 — INGRESOS POR COBRO DE TOMAS (por mes)")
mnom = ["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
c.execute("SELECT anio,mes,tomas_que_pagaron,total_cobrado FROM vista_ingresos_mensuales ORDER BY mes")
for r in c.fetchall():
    ok(f"{mnom[r[1]]} {r[0]} — {r[2]} tomas pagaron — Total cobrado: ${r[3]:,.0f}")

t("✅ REPORTE 3 — GASTOS POR MES Y CATEGORÍA")
c.execute("SELECT anio,mes,categoria,total_gastado FROM vista_gastos_mensuales ORDER BY mes,categoria")
mes_actual = 0
for r in c.fetchall():
    if r[1] != mes_actual:
        mes_actual = r[1]
        print(f"\n  📅 {mnom[r[1]]} {r[0]}:")
    ok(f"  {r[2]:25s} — ${r[3]:,.0f}")

t("✅ REPORTE 4 — BALANCE MENSUAL (lo más importante)")
print(f"\n  {'Mes':<10} {'Entró de tomas':>16} {'Ingresos extra':>15} {'Total entró':>13} {'Total gastó':>13} {'SOBRANTE':>12}")
print(f"  {'─'*10} {'─'*16} {'─'*15} {'─'*13} {'─'*13} {'─'*12}")
c.execute("SELECT anio,mes,total_ingresos,total_gastos,sobrante FROM vista_balance_mensual ORDER BY mes")
for r in c.fetchall():
    # ingresos de tomas
    c2 = conn.cursor()
    c2.execute("SELECT COALESCE(SUM(monto_mes),0) FROM detalle_pagos_meses WHERE anio=? AND mes=? AND es_bonificado=0", (r[0],r[1]))
    ing_tomas = c2.fetchone()[0]
    c2.execute("SELECT COALESCE(SUM(monto),0) FROM ingresos_extra WHERE anio=? AND mes=?", (r[0],r[1]))
    ing_extra = c2.fetchone()[0]
    signo = "+" if r[4] >= 0 else ""
    ok(f"{mnom[r[1]]} {r[0]}   ${ing_tomas:>12,.0f}   ${ing_extra:>11,.0f}   ${r[2]:>9,.0f}   ${r[3]:>9,.0f}   {signo}${r[4]:,.0f}")

t("RESUMEN FINAL")
for tabla, label in [("usuarios","Usuarios"),("tomas","Tomas"),("pagos","Pagos registrados"),
                      ("detalle_pagos_meses","Meses cubiertos"),("gastos","Gastos"),("ingresos_extra","Ingresos extra")]:
    c.execute(f"SELECT COUNT(*) FROM {tabla}")
    ok(f"{label:25s}: {c.fetchone()[0]}")

print(f"\n  {'─'*55}")
print(f"  Base de datos lista. Abre DB Browser y verifica")
print(f"  cada tabla y cada vista para ver todo reflejado.")
print(f"  {'─'*55}\n")

conn.close()

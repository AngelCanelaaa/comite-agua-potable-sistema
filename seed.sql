-- ============================================================
-- DATOS INICIALES (SEED)
-- Ejecutar después de schema.sql
-- ============================================================


-- Categorías de gasto
INSERT INTO categorias_gasto (nombre, descripcion) VALUES
    ('SUELDOS',          'Pago al personal del comité (cobrador, fontanero, etc.)'),
    ('LUZ',              'Electricidad de pozos, bombas y oficina'),
    ('ARREGLOS_OFICINA', 'Reparaciones y mantenimiento dentro de la oficina'),
    ('ARREGLOS_CALLE',   'Reparaciones en tuberías, fugas y red de distribución en calle'),
    ('CONTRATOS',        'Materiales e instalación de nuevas tomas de agua'),
    ('OTROS',            'Gastos eventuales no clasificados en otras categorías');


-- Ofertas anuales 2026
INSERT INTO ofertas_anuales (anio, mes_limite, meses_bonificados, descripcion) VALUES
    (2026, 1, 2, 'Paga en enero el año completo: 2 meses gratis (pagas 10, llevas 12)'),
    (2026, 2, 1, 'Paga en febrero el año completo: 1 mes gratis (pagas 11, llevas 12)'),
    (2026, 3, 1, 'Paga en marzo el año completo: 1 mes gratis (pagas 11, llevas 12)');

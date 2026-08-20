INSERT INTO grids (zone_name, location, max_capacity) VALUES
    ('North Zone',        'Durgapur Industrial Park',        500.00),
    ('South Zone',        'Durgapur Residential Sector 4',    350.00),
    ('East Zone',         'Durgapur Commercial Belt',         420.00),
    ('West Zone',         'Durgapur Rural Outskirts',         200.00),
    ('Central Zone',      'Durgapur City Center',             600.00);


INSERT INTO users (username, email, password_hash, role) VALUES
    ('admin', 'admin@greengrid.local', 'placeholder_hash_replace_me', 'admin');
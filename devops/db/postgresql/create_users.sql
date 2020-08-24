SELECT 'CREATE USER stationsuser WITH PASSWORD ''stationsuser'''
WHERE NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'stationsuser')\gexec

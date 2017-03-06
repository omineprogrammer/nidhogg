SELECT * FROM client;

INSERT INTO client(code, name) VALUES('FSKRN9', 'KRAKEN 2');

DELETE FROM info WHERE client_id = 35;
DELETE FROM qinfo WHERE client_id = 35;
DELETE FROM client WHERE id = 35;
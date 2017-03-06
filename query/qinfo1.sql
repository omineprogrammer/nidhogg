SELECT * FROM qinfo;

INSERT INTO qinfo(Client_id, date, cpu, ram, hdd) VALUES(
	(SELECT id FROM client WHERE code = 'FSKRN9'),
    '2017-01-30 14:30:21',
    10, 20, 30);

SELECT * FROM qinfo
INNER JOIN client ON Client_id = client.id
WHERE code = 'FSKRN9';
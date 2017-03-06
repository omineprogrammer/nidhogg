SELECT * FROM nicconfig
INNER JOIN client ON Client_id = client.id;

DELETE FROM nicconfig WHERE id > 0;

INSERT INTO NICCONFIG(Client_id, mac, ip, subnet, gateway, dns, name) VALUES
(35, '0A:00:27:00:00:0F', '192.168.56.1', '255.255.255.0', 'NULL', 'NULL', 'VirtualBox Host-Only Ethernet Adapter')
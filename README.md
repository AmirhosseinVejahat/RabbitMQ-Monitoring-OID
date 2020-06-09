# RabbitMQ-Monitoring-OID

This is a script that collect essential data of rabbitmq server

copy rabbit.py script to rabbitmq server and install requirement packages (requirements.txt) 

make it executable and run it.


oids list [SNMP V2]: 


1.3.6.1.4.1.8072.1234.1234.1.0 check aliveness
1.3.6.1.4.1.8072.1234.1234.2.0 check queue exists
1.3.6.1.4.1.8072.1234.1234.3.0 total consumed message
1.3.6.1.4.1.8072.1234.1234.4.0 total published message
1.3.6.1.4.1.8072.1234.1234.5.0 rate of published messages
1.3.6.1.4.1.8072.1234.1234.6.0 rate of consumed messages
1.3.6.1.4.1.8072.1234.1234.7.0 total connections
1.3.6.1.4.1.8072.1234.1234.8.0 queue size


sample queue :  [uequeue]

ALTER TABLE "group" DISABLE TRIGGER ALL;
DELETE FROM "group";
INSERT INTO "group" ("id", "name", "subject_id")
VALUES
	(1,'GG1',1),
	(2,'GG2',1),
	(3,'GG1',2),
	(4,'GG1',3),
	(5,'GG1',4),
	(6,'GG1',5),
	(7,'GG1',6),
	(8,'GG2',6);
ALTER TABLE "group" ENABLE TRIGGER ALL;

ALTER TABLE "message" DISABLE TRIGGER ALL;
DELETE FROM "message";
ALTER TABLE "message" ENABLE TRIGGER ALL;

ALTER TABLE "message_body" DISABLE TRIGGER ALL;
DELETE FROM "message_body";
ALTER TABLE "message_body" ENABLE TRIGGER ALL;

ALTER TABLE "message_type" DISABLE TRIGGER ALL;
DELETE FROM "message_type";
INSERT INTO "message_type" ("id", "name")
VALUES
	(1,'DIRECT_MESSAGE'),
	(2,'GROUP_MESSAGE'),
	(3,'SUBJECT_MESSAGE');
ALTER TABLE "message_type" ENABLE TRIGGER ALL;


ALTER TABLE "student_group" DISABLE TRIGGER ALL;
DELETE FROM "student_group";
INSERT INTO "student_group" ("student_id", "group_id")
VALUES
	(1,1),
	(1,3),
	(1,4),
	(1,5),
	(1,6),
	(1,7),
	(2,1),
	(2,3),
	(2,4),
	(2,5),
	(2,6),
	(2,7),
	(3,2),
	(3,3),
	(3,5),
	(3,6),
	(3,7),
	(4,1);
ALTER TABLE "student_group" ENABLE TRIGGER ALL;

ALTER TABLE "subject" DISABLE TRIGGER ALL;
DELETE FROM "subject";
INSERT INTO "subject" ("id", "code", "name")
VALUES
	(1,21710,'Estructures de Dades'),
	(2,21711,'Programació Concurrent'),
	(3,21712,'Xarxes Avançades'),
	(4,21713,'Compiladors I'),
	(5,21714,'Gestió de Projectes'),
	(6,21715,'Sistemes Operatius II'),
	(7,21716,'Simulació');
ALTER TABLE "subject" ENABLE TRIGGER ALL;

ALTER TABLE "teacher_subject" DISABLE TRIGGER ALL;
DELETE FROM "teacher_subject";
INSERT INTO "teacher_subject" ("teacher_id", "subject_id")
VALUES
	(5,2),
	(5,6),
	(6,3),
	(7,1),
	(7,4),
	(8,5),
	(8,6),
	(9,1),
	(10,5);
ALTER TABLE "teacher_subject" DISABLE TRIGGER ALL;

ALTER TABLE "user" DISABLE TRIGGER ALL;
DELETE FROM "user";
INSERT INTO "user" ("id", "first_name", "last_name", "user", "password", "auth_token", "type_id")
VALUES
	(1,'Joan','Font','JFR164','0349d31dd658c45d37c213ca603af9ce','OLlmxXLkS2vdi1zEWy44W1vFj02gCFbv76JSI3Q6cS8=',2),
	(2,'Francesc','Sastre','FSC573','5764768f42aac6e99bf8059f2dea2dec','cP2AlEWpd9PjcsOf7qKm1/AB6CPf0dD0LI5GK3DZ1c8=',2),
	(3,'Marc','Perelló','MPF705','cebf514e7fbe8eb85c11c13ecdb1a595','OFPgVBtGYPOzvOCO/Mb2STEBCx2cJXbmgsLFwdGaXX8=',2),
	(4,'Llorenç','Segui','LSC025','27b7d88cf7581a70563e87e5d52583ae','q9kDKmzj4uafmP5a/Qs5tQe/fmAO26iLPBOAtjhMd2Y=',2),
	(5,'Ricardo','Galli','RGG111','c60c8c4234054c940fc6ba8b7855aa90','KchqozGR6JsZkB0VO1tojMAWMhIsQcDr3/TVwl/vLO4=',1),
	(6,'Bartolomé','Serra','BSC222','d93ca0bd14971fbe579ab39a35f16939','2vOzdUX3htQBC7rWWcUlF1LmOkeIsuRByn/FN5e1tGs=',1),
	(7,'Albert','Llemosí','ALC333','3d8e450dbad1a08694958766693abd69','vxgwqCDzvQNutHYqtuz0FzGwKheXfq9MV26RJCfKZQE=',1),
	(8,'Adelaida','Delgado','ADD444','a5160eda6ee87f1440292fc2bdb255cd','M2CnyVzP3YnWyYp1i7T/JJ5c73g8afS8pOfZjBj6wR0=',1),
	(9,'Gabriel','Moya','GMA555','846c6956bda0ee852aac2aca632f1cd9','3i5G38HP2gwkQ2KzeoHXQc6pg7Adcx+0ZKAt7yzCVR0=',1),
	(10,'Antonia','Mas','AMP666','5c88099e58331c70dd5bb36683ce7e6b','ulWUB1ffhrJktJi396hh3y8RAHEf2um/AOXP9+irOXo=',1);
ALTER TABLE "user" ENABLE TRIGGER ALL;


ALTER TABLE "user_type" DISABLE TRIGGER ALL;
DELETE FROM "user_type";
INSERT INTO "user_type" ("id", "name")
VALUES
	(1,'TEACHER'),
	(2,'STUDENT');
ALTER TABLE "user_type" ENABLE TRIGGER ALL;

ALTER TABLE "media_type" DISABLE TRIGGER ALL;
DELETE FROM "media_type";
INSERT INTO "media_type" ("id", "name")
VALUES
	(1,'AVATAR'),
	(2,'MESSAGE_FILE');
ALTER TABLE "media_type" ENABLE TRIGGER ALL;

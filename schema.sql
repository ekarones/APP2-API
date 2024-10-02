DROP TABLE IF EXISTS "diseases";
DROP TABLE IF EXISTS "advices";

CREATE TABLE "diseases" (
	"id"    INTEGER NOT NULL,
	"name"  TEXT NOT NULL,
	"description"   TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "advices" (
	"id"	INTEGER NOT NULL,
	"id_disease"	INTEGER NOT NULL,
	"content"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
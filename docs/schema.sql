CREATE TABLE "contatos" (
  "id" integer PRIMARY KEY,
  "nome" varchar,
  "telefone" varchar
);

CREATE TABLE "recursos" (
  "id" integer PRIMARY KEY,
  "nome" varchar,
  "intervalo_medio_dias" integer,
  "data_ultima_compra" date,
  "id_contato" integer
);

ALTER TABLE "recursos" ADD FOREIGN KEY ("id_contato") REFERENCES "contatos" ("id") DEFERRABLE INITIALLY IMMEDIATE;

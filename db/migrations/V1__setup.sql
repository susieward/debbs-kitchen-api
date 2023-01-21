
CREATE TABLE if not exists recipes (
	id uuid NOT null primary key,
	name varchar not null,
	tags jsonb,
	photo varchar
);

CREATE TABLE if not exists instructions (
	id uuid NOT null primary key,
	recipe_id uuid not null references recipes(id),
	step_text varchar NOT NULL,
	step_number int4 not null,
	created_on timestamptz not null default current_timestamp,
	updated_on timestamptz not null default current_timestamp,
	unique(recipe_id, step_number)
);

CREATE TABLE if not exists ingredients (
	id uuid NOT NULL primary key,
	recipe_id uuid NOT NULL references recipes(id),
	ingr_text varchar NOT NULL,
	ingr_order int4 NOT NULL,
	created_on timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_on timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
	UNIQUE (recipe_id, ingr_text)
);

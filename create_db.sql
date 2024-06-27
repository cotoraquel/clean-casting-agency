-- create_db.sql

-- Drop the database if it exists
-- DROP DATABASE IF EXISTS casting_agency_redux;

-- -- Create the database
-- CREATE DATABASE casting_agency_redux;

-- -- Connect to the new database
-- \c casting_agency_redux

-- Drop existing tables in the public schema if they exist
DROP TABLE IF EXISTS public.movies CASCADE;
DROP TABLE IF EXISTS public.actors CASCADE;

-- Create the movies table in the public schema
CREATE TABLE public.movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL
);

-- Create the actors table in the public schema
CREATE TABLE public.actors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(50) NOT NULL
);

-- Example data insertion (optional)
INSERT INTO public.movies (title, release_date) VALUES ('Inception', '2010-07-16');
INSERT INTO public.actors (name, age, gender) VALUES ('Leonardo DiCaprio', 46, 'Male');

-- Additional movies
INSERT INTO public.movies (title, release_date) VALUES ('The Matrix', '1999-03-31');
INSERT INTO public.movies (title, release_date) VALUES ('Titanic', '1997-12-19');
INSERT INTO public.movies (title, release_date) VALUES ('The Dark Knight', '2008-07-18');
INSERT INTO public.movies (title, release_date) VALUES ('Fight Club', '1999-10-15');
INSERT INTO public.movies (title, release_date) VALUES ('Pulp Fiction', '1994-10-14');
INSERT INTO public.movies (title, release_date) VALUES ('The Shawshank Redemption', '1994-09-23');
INSERT INTO public.movies (title, release_date) VALUES ('The Godfather', '1972-03-24');
INSERT INTO public.movies (title, release_date) VALUES ('Forrest Gump', '1994-07-06');
INSERT INTO public.movies (title, release_date) VALUES ('The Lord of the Rings: The Fellowship of the Ring', '2001-12-19');
INSERT INTO public.movies (title, release_date) VALUES ('Gladiator', '2000-05-05');

-- Additional actors
INSERT INTO public.actors (name, age, gender) VALUES ('Keanu Reeves', 56, 'Male');
INSERT INTO public.actors (name, age, gender) VALUES ('Kate Winslet', 45, 'Female');
INSERT INTO public.actors (name, age, gender) VALUES ('Christian Bale', 47, 'Male');
INSERT INTO public.actors (name, age, gender) VALUES ('Brad Pitt', 57, 'Male');
INSERT INTO public.actors (name, age, gender) VALUES ('John Travolta', 67, 'Male');
INSERT INTO public.actors (name, age, gender) VALUES ('Morgan Freeman', 83, 'Male');
INSERT INTO public.actors (name, age, gender) VALUES ('Al Pacino', 80, 'Male');
INSERT INTO public.actors (name, age, gender) VALUES ('Tom Hanks', 64, 'Male');
INSERT INTO public.actors (name, age, gender) VALUES ('Elijah Wood', 40, 'Male');
INSERT INTO public.actors (name, age, gender) VALUES ('Russell Crowe', 56, 'Male');

-- Relationships
-- (Here we assume there is a relationship table linking actors to movies. Let's create this table and populate it)
DROP TABLE IF EXISTS public.movie_actors CASCADE;

CREATE TABLE public.movie_actors (
    movie_id INT REFERENCES public.movies(id),
    actor_id INT REFERENCES public.actors(id),
    PRIMARY KEY (movie_id, actor_id)
);

-- Insert relationships
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='Inception'), (SELECT id FROM public.actors WHERE name='Leonardo DiCaprio'));
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='The Matrix'), (SELECT id FROM public.actors WHERE name='Keanu Reeves'));
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='Titanic'), (SELECT id FROM public.actors WHERE name='Kate Winslet'));
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='The Dark Knight'), (SELECT id FROM public.actors WHERE name='Christian Bale'));
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='Fight Club'), (SELECT id FROM public.actors WHERE name='Brad Pitt'));
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='Pulp Fiction'), (SELECT id FROM public.actors WHERE name='John Travolta'));
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='The Shawshank Redemption'), (SELECT id FROM public.actors WHERE name='Morgan Freeman'));
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='The Godfather'), (SELECT id FROM public.actors WHERE name='Al Pacino'));
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='Forrest Gump'), (SELECT id FROM public.actors WHERE name='Tom Hanks'));
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='The Lord of the Rings: The Fellowship of the Ring'), (SELECT id FROM public.actors WHERE name='Elijah Wood'));
INSERT INTO public.movie_actors (movie_id, actor_id) VALUES ((SELECT id FROM public.movies WHERE title='Gladiator'), (SELECT id FROM public.actors WHERE name='Russell Crowe'));

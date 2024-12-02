--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: restaurant_db; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE restaurant_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE restaurant_db OWNER TO postgres;

\connect restaurant_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: item_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.item_type AS ENUM (
    'pizza',
    'beverage'
);


ALTER TYPE public.item_type OWNER TO postgres;

--
-- Name: order_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.order_type AS ENUM (
    'on-site',
    'pick-up',
    'delivery'
);


ALTER TYPE public.order_type OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ingredient; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingredient (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(120)
);


ALTER TABLE public.ingredient OWNER TO postgres;

--
-- Name: ingredient_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ingredient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ingredient_id_seq OWNER TO postgres;

--
-- Name: ingredient_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingredient_id_seq OWNED BY public.ingredient.id;


--
-- Name: item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    type public.item_type NOT NULL,
    price numeric(5,2) NOT NULL,
    description character varying(250)
);


ALTER TABLE public.item OWNER TO postgres;

--
-- Name: item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_id_seq OWNER TO postgres;

--
-- Name: item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_id_seq OWNED BY public.item.id;


--
-- Name: order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."order" (
    id integer NOT NULL,
    order_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    order_type public.order_type NOT NULL,
    total_price numeric(8,2) NOT NULL,
    order_note text,
    customer_name character varying(250),
    customer_phone character varying(15),
    address character varying(250),
    pickup_time timestamp without time zone,
    delivery_time timestamp without time zone
);


ALTER TABLE public."order" OWNER TO postgres;

--
-- Name: order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_id_seq OWNER TO postgres;

--
-- Name: order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_id_seq OWNED BY public."order".id;


--
-- Name: order_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_item (
    id integer NOT NULL,
    order_id integer NOT NULL,
    item_id integer NOT NULL,
    quantity smallint DEFAULT 1 NOT NULL,
    price numeric(5,2) NOT NULL,
    detail_note text
);


ALTER TABLE public.order_item OWNER TO postgres;

--
-- Name: order_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_item_id_seq OWNER TO postgres;

--
-- Name: order_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_item_id_seq OWNED BY public.order_item.id;


--
-- Name: recipe; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recipe (
    item_id integer NOT NULL,
    ingredient_id integer NOT NULL,
    quantity smallint NOT NULL,
    unit character varying(50) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.recipe OWNER TO postgres;

--
-- Name: recipe_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.recipe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recipe_id_seq OWNER TO postgres;

--
-- Name: recipe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.recipe_id_seq OWNED BY public.recipe.id;


--
-- Name: ingredient id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredient ALTER COLUMN id SET DEFAULT nextval('public.ingredient_id_seq'::regclass);


--
-- Name: item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item ALTER COLUMN id SET DEFAULT nextval('public.item_id_seq'::regclass);


--
-- Name: order id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order" ALTER COLUMN id SET DEFAULT nextval('public.order_id_seq'::regclass);


--
-- Name: order_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_item ALTER COLUMN id SET DEFAULT nextval('public.order_item_id_seq'::regclass);


--
-- Name: recipe id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipe ALTER COLUMN id SET DEFAULT nextval('public.recipe_id_seq'::regclass);


--
-- Data for Name: ingredient; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ingredient (id, name, description) FROM stdin;
1	Tomato Sauce	A rich sauce made from tomatoes, used as a base for many pizzas.
2	Mozzarella Cheese	A soft, white cheese used commonly on pizzas, known for its melting properties.
3	Basil	An aromatic herb with a sweet, peppery flavor, often used fresh.
4	Pepperoni	A spicy, cured sausage made from pork and beef, sliced thinly for pizza toppings.
5	Ham	Cured pork, often sliced thinly, used in Hawaiian and other pizza varieties.
6	Pineapple	Sweet tropical fruit, used as a topping especially in Hawaiian pizzas.
7	Anchovies	Small, salt-cured fish filets, giving a strong umami flavor on pizzas.
8	Olives	Fruit of the olive tree, often used in slices on pizzas for a tangy taste.
9	Artichokes	A thistle plant vegetal, used as a pizza topping for its tender texture.
10	Mushrooms	Fungi with a meaty texture and earthy flavor, commonly used on vegetarian and other pizzas.
11	Bell Peppers	Sweet peppers in various colors, used for their crunch and color on pizzas.
12	Onions	Bulb vegetables used for their pungency and sweetness when cooked.
13	Parmesan Cheese	A hard, aged cheese with a nutty flavor used to top pizzas.
14	Gorgonzola	A veined Italian blue cheese, known for its strong and bold flavor.
15	Provolone	An Italian cheese with a mild flavor, used in Four Cheese pizzas.
16	Ricotta	A creamy, mild cheese used in combination with other cheeses on pizzas.
17	Cherry Tomatoes	Small, sweet tomatoes, often halved and used fresh on Caprese pizzas.
18	Olive Oil	A flavorful oil pressed from olives, used to enhance the flavor of pizzas.
19	Garlic	A pungent bulb used to add depth of flavor to pizzas and sauces.
20	Oregano	A herb with a slightly bitter taste, often used dried for seasoning pizzas.
\.


--
-- Data for Name: item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item (id, name, type, price, description) FROM stdin;
1	Margherita	pizza	12.99	Classic Italian pizza topped with fresh tomatoes, mozzarella cheese, fresh basil, and a drizzle of olive oil.
2	Pepperoni	pizza	14.99	A popular choice featuring a tomato sauce base, mozzarella cheese, and lots of spicy pepperoni slices.
3	Hawaiian	pizza	13.99	Topped with tomato sauce, mozzarella, ham, and sweet pineapple chunks for a tropical twist.
4	Neapoletana	pizza	15.99	Traditional Neapolitan pizza made with San Marzano tomatoes, mozzarella di bufala, fresh basil, salt, and extra-virgin olive oil.
5	Capricciosa	pizza	16.99	A delightful combination of tomato sauce, mozzarella, artichokes, mushrooms, ham, and olives.
6	Romana	pizza	14.49	Features tomato sauce, mozzarella, anchovies, capers, and oregano, offering a distinct and savory taste.
7	Carbonara	pizza	15.49	A creative take on carbonara pasta with a sauce of cream, eggs, Parmesan, and pancetta atop a pizza crust.
8	Vegetariana	pizza	13.49	Loaded with fresh vegetables including bell peppers, onions, mushrooms, and olives, on a tomato sauce base with mozzarella.
9	Four Cheese	pizza	14.99	A cheese lover’s delight combining mozzarella, Parmesan, gorgonzola, and fontina cheese on a tomato base.
10	Caprese	pizza	15.49	Inspired by the Caprese salad, this pizza is topped with cherry tomatoes, mozzarella di bufala, fresh basil, and a balsamic glaze.
11	Coca-Cola	beverage	2.99	The classic and refreshing cola beverage that pairs well with any meal.
12	Lemonade	beverage	3.49	A chilled glass of fresh lemonade, perfect for a tangy and sweet refreshment.
13	Iced Tea	beverage	3.49	Freshly brewed iced tea, available sweetened or unsweetened, served with a slice of lemon.
14	Sparkling Water	beverage	2.49	A refreshing and bubbly alternative to still water, perfect for cleansing the palate.
15	Craft Beer	beverage	5.99	A selection of local craft beers to complement your pizza choice, with varying styles and flavors.
\.


--
-- Data for Name: order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."order" (id, order_time, order_type, total_price, order_note, customer_name, customer_phone, address, pickup_time, delivery_time) FROM stdin;
\.


--
-- Data for Name: order_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_item (id, order_id, item_id, quantity, price, detail_note) FROM stdin;
\.


--
-- Data for Name: recipe; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.recipe (item_id, ingredient_id, quantity, unit, id) FROM stdin;
1	1	100	grams	1
1	2	150	grams	2
1	3	10	leaves	3
1	18	5	ml	4
2	1	100	grams	5
2	2	150	grams	6
2	4	100	grams	7
3	1	100	grams	8
3	2	150	grams	9
3	5	75	grams	10
3	6	75	grams	11
4	1	100	grams	12
4	2	150	grams	13
4	3	10	leaves	14
4	18	5	ml	15
5	1	100	grams	16
5	2	150	grams	17
5	9	50	grams	18
5	10	50	grams	19
5	5	50	grams	20
5	8	30	grams	21
6	1	100	grams	22
6	2	150	grams	23
6	7	30	grams	24
6	8	30	grams	25
6	20	5	grams	26
7	2	150	grams	27
7	19	5	grams	28
7	13	30	grams	29
7	5	75	grams	30
8	1	100	grams	31
8	2	150	grams	32
8	11	50	grams	33
8	12	50	grams	34
8	10	50	grams	35
8	8	30	grams	36
9	1	100	grams	37
9	2	50	grams	38
9	13	50	grams	39
9	14	50	grams	40
9	15	50	grams	41
10	17	100	grams	42
10	2	100	grams	43
10	3	10	leaves	44
10	18	5	ml	45
\.


--
-- Name: ingredient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingredient_id_seq', 20, true);


--
-- Name: item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_id_seq', 15, true);


--
-- Name: order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_id_seq', 1, false);


--
-- Name: order_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_item_id_seq', 1, false);


--
-- Name: recipe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.recipe_id_seq', 45, true);


--
-- Name: ingredient ingredient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredient
    ADD CONSTRAINT ingredient_pkey PRIMARY KEY (id);


--
-- Name: item item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_pkey PRIMARY KEY (id);


--
-- Name: order_item order_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT order_item_pkey PRIMARY KEY (id);


--
-- Name: order order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (id);


--
-- Name: recipe recipe_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT recipe_pkey PRIMARY KEY (id);


--
-- Name: unique_item_ingredient; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX unique_item_ingredient ON public.recipe USING btree (item_id, ingredient_id);


--
-- Name: order_item order_item_item_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT "order_item_item_FK" FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- Name: order_item order_item_order_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT "order_item_order_FK" FOREIGN KEY (order_id) REFERENCES public."order"(id) ON DELETE CASCADE;


--
-- Name: recipe recipe_ingredient_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT "recipe_ingredient_FK" FOREIGN KEY (ingredient_id) REFERENCES public.ingredient(id) ON DELETE CASCADE;


--
-- Name: recipe recipe_item_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT "recipe_item_FK" FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--

\restrict FEbR7DscCb8oOaJlbxvVvUJO1ryAqrrr10lMwFFxUBcFFhClfR2Q37hETzukRil

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    cat_id integer NOT NULL,
    cat_name text NOT NULL,
    cat_overcat integer
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    cust_id integer NOT NULL,
    cust_name text NOT NULL,
    cust_address text NOT NULL,
    cust_discount integer NOT NULL
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    emp_id integer NOT NULL,
    emp_name text NOT NULL,
    emp_position text NOT NULL
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Name: items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.items (
    item_id integer NOT NULL,
    item_ord_id integer NOT NULL,
    item_prod_id integer NOT NULL,
    item_prod_count integer NOT NULL
);


ALTER TABLE public.items OWNER TO postgres;

--
-- Name: manufacturers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.manufacturers (
    man_id integer NOT NULL,
    man_name text NOT NULL,
    man_address text NOT NULL
);


ALTER TABLE public.manufacturers OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    ord_id integer NOT NULL,
    ord_cust_id integer NOT NULL,
    ord_emp_id integer NOT NULL,
    ord_date date NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    prod_id integer NOT NULL,
    prod_name text NOT NULL,
    prod_price numeric(8,2) NOT NULL,
    prod_rest integer NOT NULL,
    prod_cat_id integer NOT NULL,
    prod_man_id integer NOT NULL
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (cat_id, cat_name, cat_overcat) FROM stdin;
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customers (cust_id, cust_name, cust_address, cust_discount) FROM stdin;
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (emp_id, emp_name, emp_position) FROM stdin;
\.


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.items (item_id, item_ord_id, item_prod_id, item_prod_count) FROM stdin;
\.


--
-- Data for Name: manufacturers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.manufacturers (man_id, man_name, man_address) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (ord_id, ord_cust_id, ord_emp_id, ord_date) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (prod_id, prod_name, prod_price, prod_rest, prod_cat_id, prod_man_id) FROM stdin;
\.


--
-- Name: categories categories_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pk PRIMARY KEY (cat_id);


--
-- Name: customers customers_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pk PRIMARY KEY (cust_id);


--
-- Name: employees employees_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pk PRIMARY KEY (emp_id);


--
-- Name: items items_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pk PRIMARY KEY (item_id);


--
-- Name: manufacturers manufacturers_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.manufacturers
    ADD CONSTRAINT manufacturers_pk PRIMARY KEY (man_id);


--
-- Name: orders orders_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pk PRIMARY KEY (ord_id);


--
-- Name: products products_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pk PRIMARY KEY (prod_id);


--
-- Name: categories categories_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_fk FOREIGN KEY (cat_overcat) REFERENCES public.categories(cat_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: items items_fk1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_fk1 FOREIGN KEY (item_ord_id) REFERENCES public.orders(ord_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: items items_fk2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_fk2 FOREIGN KEY (item_prod_id) REFERENCES public.products(prod_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: orders orders_fk1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_fk1 FOREIGN KEY (ord_cust_id) REFERENCES public.customers(cust_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: orders orders_fk2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_fk2 FOREIGN KEY (ord_emp_id) REFERENCES public.employees(emp_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: products products_fk1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_fk1 FOREIGN KEY (prod_cat_id) REFERENCES public.categories(cat_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: products products_fk2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_fk2 FOREIGN KEY (prod_man_id) REFERENCES public.manufacturers(man_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict FEbR7DscCb8oOaJlbxvVvUJO1ryAqrrr10lMwFFxUBcFFhClfR2Q37hETzukRil


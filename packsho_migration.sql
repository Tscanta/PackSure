--
-- PostgreSQL database dump
--

\restrict 03SvrYJdlNbcPOEHibV6IAcOJYVycnpuzFe7kBAqQwKz3aXShOsnTpxvfy1f8fB

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

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
-- Name: inspections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inspections (
    id integer NOT NULL,
    product_id integer NOT NULL,
    inspection_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    overall_status character varying(30),
    confidence numeric(5,2),
    CONSTRAINT check_confidence CHECK (((confidence >= (0)::numeric) AND (confidence <= (100)::numeric))),
    CONSTRAINT check_inspection_status CHECK (((overall_status)::text = ANY ((ARRAY['COMPLIANT'::character varying, 'NON_COMPLIANT'::character varying, 'REVIEW_REQUIRED'::character varying])::text[])))
);


--
-- Name: inspections_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inspections_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inspections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inspections_id_seq OWNED BY public.inspections.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.products (
    id integer NOT NULL,
    product_name character varying(255) NOT NULL,
    category character varying(100),
    brand character varying(100),
    manufacturer character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: rules; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rules (
    id integer NOT NULL,
    rule_id character varying(50) NOT NULL,
    category character varying(100) NOT NULL,
    requirement text NOT NULL,
    description text,
    mandatory boolean NOT NULL,
    validation_type character varying(50),
    severity character varying(20),
    source text,
    effective_date date,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_rule_severity CHECK (((severity)::text = ANY ((ARRAY['LOW'::character varying, 'MEDIUM'::character varying, 'HIGH'::character varying, 'CRITICAL'::character varying])::text[]))),
    CONSTRAINT check_validation_type CHECK (((validation_type)::text = ANY ((ARRAY['TEXT_EXISTS'::character varying, 'QUANTITY'::character varying, 'CURRENCY'::character varying, 'DATE'::character varying, 'ADDRESS'::character varying, 'PHONE'::character varying, 'EMAIL'::character varying])::text[])))
);


--
-- Name: rules_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rules_id_seq OWNED BY public.rules.id;


--
-- Name: violations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.violations (
    id integer NOT NULL,
    inspection_id integer NOT NULL,
    rule_id integer NOT NULL,
    status character varying(20) NOT NULL,
    detected_value text,
    expected_value text,
    message text,
    CONSTRAINT check_violation_status CHECK (((status)::text = ANY ((ARRAY['PASS'::character varying, 'FAIL'::character varying])::text[])))
);


--
-- Name: violations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.violations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: violations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.violations_id_seq OWNED BY public.violations.id;


--
-- Name: inspections id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inspections ALTER COLUMN id SET DEFAULT nextval('public.inspections_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: rules id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rules ALTER COLUMN id SET DEFAULT nextval('public.rules_id_seq'::regclass);


--
-- Name: violations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.violations ALTER COLUMN id SET DEFAULT nextval('public.violations_id_seq'::regclass);


--
-- Data for Name: inspections; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.inspections (id, product_id, inspection_date, overall_status, confidence) FROM stdin;
1	1	2026-09-04 13:18:39.810616	NON_COMPLIANT	95.50
4	7	2026-09-04 20:24:38.875659	REVIEW_REQUIRED	1.00
5	8	2026-09-04 20:33:51.851235	NON_COMPLIANT	0.78
6	10	2026-09-04 21:12:54.452911	REVIEW_REQUIRED	1.00
7	11	2026-09-04 21:21:04.396075	REVIEW_REQUIRED	1.00
8	12	2026-09-04 21:46:22.384232	REVIEW_REQUIRED	1.00
9	13	2026-09-04 21:46:22.573874	NON_COMPLIANT	0.78
10	14	2026-09-04 21:46:22.859698	NON_COMPLIANT	0.78
11	15	2026-09-04 21:46:23.275351	NON_COMPLIANT	0.78
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.products (id, product_name, category, brand, manufacturer, created_at) FROM stdin;
1	ABC Biscuits	Food	ABC	ABC Foods Pvt Ltd	2026-09-04 13:17:48.695131
2	XYZ Shampoo	Personal Care	XYZ	XYZ Consumer Products Pvt Ltd	2026-09-04 14:09:15.707561
3	Parle-G Biscuits	Food	Parle	Parle Products Pvt Ltd	2026-09-04 15:04:02.218697
4	Parle-G Biscuits	Food	Parle	Parle Products Pvt Ltd	2026-09-04 15:04:04.846732
5	Parle-G Biscuits	Food	Parle	Parle Products Pvt Ltd	2026-09-04 15:04:19.926715
6	Test Coca Cola	PACKAGED_COMMODITY	Coca Cola	Test Manufacturer	2026-09-04 20:18:39.219281
7	Test Coca Cola	PACKAGED_COMMODITY	Coca Cola	Test Manufacturer	2026-09-04 20:24:38.752912
8	Test Coca Cola	PACKAGED_COMMODITY	Coca Cola	Test Manufacturer	2026-09-04 20:33:51.771926
9	Test Coca Cola	PACKAGED_COMMODITY	Coca Cola	Test Manufacturer	2026-09-04 21:06:59.721584
10	Test Coca Cola	PACKAGED_COMMODITY	Coca Cola	Test Manufacturer	2026-09-04 21:12:54.100552
11	Test Product	PACKAGED_COMMODITY	Test Brand	Test Manufacturer	2026-09-04 21:21:04.269839
12	Test Product	PACKAGED_COMMODITY	Test Brand	Test Manufacturer	2026-09-04 21:46:22.274098
13	Test Product	PACKAGED_COMMODITY	Test Brand	Test Manufacturer	2026-09-04 21:46:22.430626
14	Test Product	PACKAGED_COMMODITY	Test Brand	Test Manufacturer	2026-09-04 21:46:22.76061
15	Test Product	PACKAGED_COMMODITY	Test Brand	Test Manufacturer	2026-09-04 21:46:23.073247
\.


--
-- Data for Name: rules; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.rules (id, rule_id, category, requirement, description, mandatory, validation_type, severity, source, effective_date, created_at) FROM stdin;
1	TEST001	Product	Product name must be present	The package must contain the product name.	t	TEXT_EXISTS	HIGH	TEST DATA	\N	2026-09-04 13:18:26.957352
3	LMPC-001	PACKAGED_COMMODITY	Manufacturer address	Package must display the name and address of the manufacturer/packer/importer as applicable.	t	ADDRESS	HIGH	Legal Metrology	2026-01-01	2026-09-04 15:55:26.622821
4	LMPC-002	PACKAGED_COMMODITY	Net quantity	Package must display the net quantity of the commodity.	t	QUANTITY	CRITICAL	Legal Metrology	2026-01-01	2026-09-04 15:55:26.622821
5	LMPC-003	PACKAGED_COMMODITY	Maximum retail price	Package must display the applicable maximum retail price.	t	CURRENCY	CRITICAL	Legal Metrology	2026-01-01	2026-09-04 15:55:26.622821
6	LMPC-004	PACKAGED_COMMODITY	Consumer care details	Package must provide the required consumer contact information.	t	PHONE	MEDIUM	Legal Metrology	2026-01-01	2026-09-04 15:55:26.622821
7	LMPC-005	PACKAGED_COMMODITY	Date declaration	Package must display the applicable date declaration where required.	t	DATE	MEDIUM	Legal Metrology	2026-01-01	2026-09-04 15:55:26.622821
\.


--
-- Data for Name: violations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.violations (id, inspection_id, rule_id, status, detected_value, expected_value, message) FROM stdin;
1	1	1	FAIL	\N	Product name	Product name is missing
2	5	5	FAIL	\N	\N	Maximum Retail Price declaration is missing
3	9	5	FAIL	\N	\N	Maximum Retail Price declaration is missing
4	10	4	FAIL	\N	\N	Net quantity declaration is missing
5	11	5	FAIL	\N	\N	MRP format is invalid
\.


--
-- Name: inspections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.inspections_id_seq', 11, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.products_id_seq', 15, true);


--
-- Name: rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rules_id_seq', 7, true);


--
-- Name: violations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.violations_id_seq', 5, true);


--
-- Name: inspections inspections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inspections
    ADD CONSTRAINT inspections_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: rules rules_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rules
    ADD CONSTRAINT rules_pkey PRIMARY KEY (id);


--
-- Name: rules rules_rule_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rules
    ADD CONSTRAINT rules_rule_id_key UNIQUE (rule_id);


--
-- Name: violations violations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.violations
    ADD CONSTRAINT violations_pkey PRIMARY KEY (id);


--
-- Name: idx_inspections_product_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_inspections_product_id ON public.inspections USING btree (product_id);


--
-- Name: idx_products_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_products_category ON public.products USING btree (category);


--
-- Name: idx_rules_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rules_category ON public.rules USING btree (category);


--
-- Name: idx_rules_validation_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_rules_validation_type ON public.rules USING btree (validation_type);


--
-- Name: idx_violations_inspection_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_violations_inspection_id ON public.violations USING btree (inspection_id);


--
-- Name: idx_violations_rule_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_violations_rule_id ON public.violations USING btree (rule_id);


--
-- Name: violations fk_inspection; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.violations
    ADD CONSTRAINT fk_inspection FOREIGN KEY (inspection_id) REFERENCES public.inspections(id);


--
-- Name: inspections fk_product; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inspections
    ADD CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: violations fk_rule; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.violations
    ADD CONSTRAINT fk_rule FOREIGN KEY (rule_id) REFERENCES public.rules(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 03SvrYJdlNbcPOEHibV6IAcOJYVycnpuzFe7kBAqQwKz3aXShOsnTpxvfy1f8fB


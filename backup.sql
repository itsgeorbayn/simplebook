--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

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
-- Name: admin_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin_permissions (
    id integer NOT NULL,
    list_posts boolean,
    edit_posts boolean,
    edit_comments boolean,
    remove_posts boolean,
    remove_comments boolean,
    list_messages boolean,
    edit_messages boolean,
    remove_messages boolean,
    ban_users boolean,
    created_at timestamp without time zone NOT NULL,
    last_edited timestamp without time zone,
    list_users boolean,
    edit_users boolean,
    list_comments boolean,
    list_admins boolean,
    edit_admins boolean,
    list_reports boolean,
    close_reports boolean
);


ALTER TABLE public.admin_permissions OWNER TO postgres;

--
-- Name: admin_permissions_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admin_permissions_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admin_permissions_user_id_seq OWNER TO postgres;

--
-- Name: admin_permissions_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admin_permissions_user_id_seq OWNED BY public.admin_permissions.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comments (
    id integer NOT NULL,
    author_id integer,
    post_id integer,
    content character varying(4096) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_deleted boolean,
    deleted_at timestamp without time zone,
    is_edited boolean,
    edited_at timestamp without time zone,
    is_migrated boolean
);


ALTER TABLE public.comments OWNER TO postgres;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comments_id_seq OWNER TO postgres;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- Name: friendships; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.friendships (
    id integer NOT NULL,
    user1_id integer NOT NULL,
    user2_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_accepted boolean NOT NULL
);


ALTER TABLE public.friendships OWNER TO postgres;

--
-- Name: friendships_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.friendships_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.friendships_id_seq OWNER TO postgres;

--
-- Name: friendships_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.friendships_id_seq OWNED BY public.friendships.id;


--
-- Name: likes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.likes (
    id integer NOT NULL,
    user_id integer,
    post_id integer,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.likes OWNER TO postgres;

--
-- Name: likes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.likes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.likes_id_seq OWNER TO postgres;

--
-- Name: likes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.likes_id_seq OWNED BY public.likes.id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    id integer NOT NULL,
    sender integer,
    receiver integer,
    sended_at timestamp without time zone NOT NULL,
    content character varying NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp without time zone,
    is_forwarded boolean,
    forwarded_at timestamp without time zone,
    is_edited boolean,
    edited_at timestamp without time zone,
    reference integer
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.messages_id_seq OWNER TO postgres;

--
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;


--
-- Name: news; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news (
    id integer NOT NULL,
    title character varying NOT NULL,
    content character varying NOT NULL,
    last_update timestamp without time zone,
    is_deleted boolean NOT NULL,
    deleted_at timestamp without time zone,
    recipient_id integer,
    reference_table character varying,
    reference_id integer
);


ALTER TABLE public.news OWNER TO postgres;

--
-- Name: news_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.news_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.news_id_seq OWNER TO postgres;

--
-- Name: news_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.news_id_seq OWNED BY public.news.id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    content character varying(4096) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    author_id integer,
    title character varying(64) NOT NULL,
    is_deleted boolean NOT NULL,
    slug character varying NOT NULL,
    deleted_at timestamp without time zone,
    is_edited boolean,
    edited_at timestamp without time zone,
    reference integer,
    is_reposted boolean,
    reposted_at timestamp without time zone
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posts_id_seq OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reports (
    id integer NOT NULL,
    author_id integer,
    reference_table character varying,
    reference_id integer,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.reports OWNER TO postgres;

--
-- Name: reports_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reports_id_seq OWNER TO postgres;

--
-- Name: reports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reports_id_seq OWNED BY public.reports.id;


--
-- Name: user_verifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_verifications (
    user_id integer NOT NULL,
    verification_code character varying(6) NOT NULL,
    code_expiration timestamp without time zone NOT NULL
);


ALTER TABLE public.user_verifications OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    password_hash character varying(255) NOT NULL,
    email character varying(30) NOT NULL,
    is_verified boolean NOT NULL,
    picture character varying,
    is_banned boolean,
    banned_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: admin_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_permissions ALTER COLUMN id SET DEFAULT nextval('public.admin_permissions_user_id_seq'::regclass);


--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- Name: friendships id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friendships ALTER COLUMN id SET DEFAULT nextval('public.friendships_id_seq'::regclass);


--
-- Name: likes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.likes ALTER COLUMN id SET DEFAULT nextval('public.likes_id_seq'::regclass);


--
-- Name: messages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);


--
-- Name: news id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news ALTER COLUMN id SET DEFAULT nextval('public.news_id_seq'::regclass);


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: reports id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports ALTER COLUMN id SET DEFAULT nextval('public.reports_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: admin_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin_permissions (id, list_posts, edit_posts, edit_comments, remove_posts, remove_comments, list_messages, edit_messages, remove_messages, ban_users, created_at, last_edited, list_users, edit_users, list_comments, list_admins, edit_admins, list_reports, close_reports) FROM stdin;
6	t	t	f	t	t	t	t	t	t	2025-06-29 22:02:15.577362	2025-06-29 22:02:15.577362	t	t	t	t	t	t	f
7	t	f	f	f	f	t	f	f	f	2025-07-22 14:20:40.82861	2025-07-22 14:20:40.82861	t	f	t	t	f	t	f
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
1b7c768ae30c
\.


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comments (id, author_id, post_id, content, created_at, is_deleted, deleted_at, is_edited, edited_at, is_migrated) FROM stdin;
29	6	11	<p>meow</p>	2025-07-02 22:57:08.891322	f	\N	t	2025-07-03 14:54:17.476869	f
12	19	37	<p>хм)</p>	2025-06-26 15:26:39.189374	f	\N	f	\N	t
13	19	37	<p>мяу</p>	2025-06-26 15:36:53.044869	f	\N	f	\N	t
14	19	37	<p>ggg</p>	2025-06-26 15:41:03.224165	f	\N	f	\N	f
2	19	9	<p>ааа)sss</p>	2025-06-23 15:05:41.42579	f	\N	t	2025-07-03 14:57:56.682399	f
3	19	10	<p>ssss!!</p>	2025-06-23 15:07:14.730622	f	\N	f	\N	f
4	19	10	<p>sss</p>	2025-06-23 18:14:50.555649	f	\N	f	\N	f
5	19	10	<p>aaa!)</p>	2025-06-23 18:15:51.557383	f	\N	f	\N	f
8	19	13	<p>сильный пост, <strong>братец!</strong></p>	2025-06-24 19:45:29.338407	f	\N	f	\N	f
9	19	13	<p>тоже умеем писать</p>	2025-06-25 00:20:50.516328	f	\N	f	\N	f
10	19	13	<p>а)</p>	2025-06-26 14:08:56.180828	f	\N	f	\N	f
11	19	13	<p>ого)</p>	2025-06-26 14:10:14.475932	f	\N	f	\N	f
30	28	43	<p>мяу</p>	2025-07-13 17:29:57.067544	f	\N	f	\N	t
20	19	8	<p>11</p>	2025-06-26 23:16:08.455079	t	2025-06-27 00:11:46.168593	f	\N	f
7	19	8	<p>дада согл сигма)<br><br></p>\r\n<p>&nbsp;</p>\r\n<p>&nbsp;</p>	2025-06-23 23:16:22.816607	t	2025-06-27 00:11:48.579818	f	\N	f
23	19	8	<p>айай</p>	2025-06-27 00:16:20.384731	t	2025-06-27 00:24:12.33066	f	\N	f
15	19	14	<p>приветули!</p>	2025-06-26 22:55:50.954527	t	2025-06-27 00:24:16.256274	f	\N	f
16	9	14	<p>даров братец !</p>	2025-06-26 22:56:35.31793	t	2025-06-27 00:30:59.938495	f	\N	f
17	9	14	<p>1)!</p>	2025-06-26 23:14:58.642625	t	2025-06-27 00:31:00.613486	f	\N	f
18	9	14	<p>мяу</p>	2025-06-26 23:15:34.955161	t	2025-06-27 00:31:31.66688	f	\N	f
21	9	14	<p>11</p>	2025-06-26 23:16:12.910675	t	2025-06-27 00:31:35.296543	f	\N	f
22	9	14	<p>111</p>	2025-06-26 23:16:25.705133	t	2025-06-27 00:31:35.919511	f	\N	f
24	19	14	<p>у</p>	2025-06-27 00:31:09.186356	t	2025-06-27 00:31:37.770764	f	\N	f
25	19	16	<p>вмваммав</p>	2025-06-27 00:31:42.204249	t	2025-06-27 00:33:20.35078	f	\N	f
26	19	16	<p>dfvdfvvdf</p>	2025-06-27 00:33:26.717902	f	\N	f	\N	f
19	9	8	<p>да</p>	2025-06-26 23:15:44.256254	t	2025-07-01 14:01:25.338575	f	\N	f
27	6	8	<p>o)</p>	2025-07-01 15:52:00.940621	t	2025-07-01 16:57:00.211359	f	\N	f
31	28	9	<p>прикольный постик</p>	2025-07-13 17:30:26.714312	f	\N	f	\N	f
32	6	17	<p><br><br>о<br><br><br></p>	2025-07-21 18:35:58.729523	f	\N	f	\N	f
28	6	8	<p>аа!x</p>	2025-07-01 17:52:51.949118	f	\N	t	2025-07-23 13:13:49.3431	f
1	6	8	<p>м)</p>	2025-06-20 19:38:00.871782	t	2025-07-28 20:53:14.307452	f	\N	f
6	19	8	<p>1</p>	2025-06-23 18:48:44.630562	t	2025-07-28 20:53:14.78658	f	\N	f
\.


--
-- Data for Name: friendships; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.friendships (id, user1_id, user2_id, created_at, is_accepted) FROM stdin;
17	9	6	2025-06-16 03:37:36.727296	t
19	19	20	2025-06-16 17:55:30.384052	t
20	6	19	2025-06-16 17:56:28.459904	t
21	9	19	2025-06-29 01:52:09.037561	t
24	9	24	2025-06-29 17:49:13.753011	t
23	24	6	2025-06-29 17:49:00.915628	t
25	28	6	2025-07-13 17:29:08.841985	t
26	28	8	2025-07-13 18:09:56.906508	t
27	6	20	2025-07-16 18:23:43.344495	t
29	6	27	2025-07-17 13:22:07.366755	f
28	6	8	2025-07-17 13:18:39.792517	t
30	29	6	2025-07-24 16:11:52.30676	t
\.


--
-- Data for Name: likes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.likes (id, user_id, post_id, created_at) FROM stdin;
20	19	14	2025-06-25 00:18:55.793681
22	19	13	2025-06-25 00:21:02.89178
23	19	26	2025-06-26 13:33:53.782134
24	19	37	2025-06-27 23:55:08.817289
25	9	14	2025-06-27 23:56:18.650677
27	6	13	2025-07-10 19:56:26.231518
31	6	38	2025-07-11 13:54:22.522626
33	28	9	2025-07-13 17:30:15.540626
35	29	11	2025-07-24 16:12:41.32164
36	29	12	2025-07-24 16:12:42.799839
37	29	85	2025-07-24 16:12:50.021061
38	29	86	2025-07-24 16:12:52.050729
40	6	17	2025-07-24 16:13:07.184478
41	29	9	2025-07-24 16:24:41.335552
44	6	87	2025-07-24 16:25:07.689759
45	6	86	2025-07-24 16:25:09.613258
46	6	85	2025-07-24 16:25:12.072936
47	6	12	2025-07-24 16:25:14.942781
48	6	11	2025-07-24 16:25:18.819691
50	6	9	2025-07-24 16:25:26.436948
51	6	8	2025-07-24 16:25:36.208741
52	29	8	2025-07-24 16:25:49.104753
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.messages (id, sender, receiver, sended_at, content, is_deleted, deleted_at, is_forwarded, forwarded_at, is_edited, edited_at, reference) FROM stdin;
99	19	20	2025-06-16 20:05:58.765239	ваиварирва	f	\N	t	2025-06-16 20:05:58.765239	f	\N	95
110	19	20	2025-06-21 20:58:23.857599	мм	f	\N	f	\N	f	\N	\N
125	9	19	2025-06-21 22:49:57.253976	g	f	\N	t	2025-06-21 22:49:00	f	\N	122
132	28	6	2025-07-13 17:29:31.220665	hello!	f	\N	f	\N	f	\N	\N
133	19	20	2025-07-14 17:12:13.497623	12345	f	\N	f	\N	t	2025-07-14 17:30:00	\N
135	19	20	2025-07-14 18:49:27.341885	1	f	\N	f	\N	f	\N	\N
136	19	20	2025-07-14 18:49:35.058035	2	f	\N	f	\N	f	\N	\N
137	19	20	2025-07-16 18:12:32.938354	3	f	\N	f	\N	f	\N	\N
138	19	20	2025-07-16 18:12:36.703529	4	f	\N	f	\N	f	\N	\N
140	19	20	2025-07-16 18:18:29.457493	6	f	\N	f	\N	f	\N	\N
146	6	20	2025-07-16 20:30:24.12377	123	f	\N	f	\N	f	\N	\N
147	6	19	2025-07-17 16:40:21.353836	123	f	\N	f	\N	f	\N	\N
148	6	29	2025-07-24 16:40:41.520312	123	f	\N	f	\N	f	\N	\N
150	6	29	2025-07-24 16:40:50.593679	как дела у тебя?	f	\N	f	\N	f	\N	\N
98	19	20	2025-06-16 20:05:49.744084	ваиварирва	f	\N	t	2025-06-16 20:05:49.744084	f	\N	95
101	19	6	2025-06-17 12:57:44.896577	)	f	\N	f	\N	f	\N	\N
102	6	19	2025-06-21 20:22:32.827919	о)	f	\N	f	\N	f	\N	\N
103	6	19	2025-06-21 20:22:34.370171	ку	f	\N	f	\N	f	\N	\N
104	6	19	2025-06-21 20:28:08.508815	vdfvfvfvf	f	\N	t	2025-06-21 20:28:00	t	2025-06-21 20:47:00	100
105	6	9	2025-06-21 20:48:07.523257	sadsdd	f	\N	f	\N	f	\N	\N
109	19	20	2025-06-21 20:58:03.895376	мм	f	\N	f	\N	f	\N	\N
108	6	9	2025-06-21 20:49:48.361134	bszfdsf bbdf	f	\N	f	\N	f	\N	\N
111	19	9	2025-06-21 22:19:07.237059	bszfdsf bbdf	f	\N	t	2025-06-21 22:19:00	f	\N	108
112	19	20	2025-06-21 22:19:09.378439	bszfdsf bbdf	f	\N	t	2025-06-21 22:19:00	f	\N	108
113	19	9	2025-06-21 22:19:14.072504	bszfdsf bbdf	f	\N	t	2025-06-21 22:19:00	f	\N	108
114	19	20	2025-06-21 22:19:16.01123	bszfdsf bbdf	f	\N	t	2025-06-21 22:19:00	f	\N	108
115	19	9	2025-06-21 22:19:20.209288	bszfdsf bbdf	f	\N	t	2025-06-21 22:19:00	f	\N	108
116	19	9	2025-06-21 22:20:59.705557	bszfdsf bbdf	f	\N	t	2025-06-21 22:20:00	f	\N	108
117	19	20	2025-06-21 22:21:22.324122	bszfdsf bbdf	f	\N	t	2025-06-21 22:21:00	f	\N	108
118	19	9	2025-06-21 22:21:36.244884	bszfdsf bbdf	f	\N	t	2025-06-21 22:21:00	f	\N	108
119	19	9	2025-06-21 22:23:41.249204	bszfdsf bbdf	f	\N	t	2025-06-21 22:23:00	f	\N	108
120	19	9	2025-06-21 22:23:50.162457	bszfdsf bbdf	f	\N	t	2025-06-21 22:23:00	f	\N	108
121	19	9	2025-06-21 22:24:25.698737	bszfdsf bbdf	f	\N	t	2025-06-21 22:24:00	f	\N	108
127	19	20	2025-06-21 23:05:21.406477	d	f	\N	t	2025-06-21 23:05:00	f	\N	123
128	19	6	2025-06-21 23:05:24.90485	d	f	\N	t	2025-06-21 23:05:00	f	\N	123
100	19	6	2025-06-16 20:06:30.242253	ваиваива	f	\N	f	\N	t	2025-06-17 12:59:00	\N
122	19	9	2025-06-21 22:30:51.983859	иваиваивавиа	f	\N	f	\N	t	2025-06-21 23:04:00	\N
126	19	9	2025-06-21 23:05:06.951807	d	f	\N	t	2025-06-21 23:05:00	f	\N	123
124	19	9	2025-06-21 22:49:50.689962	g	f	\N	t	2025-06-21 22:49:00	f	\N	122
97	19	9	2025-06-16 20:05:31.596473	12м2уцму	f	\N	f	\N	f	\N	\N
131	6	19	2025-07-11 13:53:26.260346	bsfbdfdbf	f	\N	f	\N	f	\N	\N
123	9	19	2025-06-21 22:31:56.913914	d	f	\N	f	\N	f	\N	\N
107	6	19	2025-06-21 20:49:25.432574	sadsdd	f	\N	t	2025-06-21 20:49:00	f	\N	105
129	19	20	2025-06-21 23:12:13.494234	g	f	\N	t	2025-06-21 23:12:00	f	\N	122
106	6	19	2025-06-21 20:48:44.932123	sadsdd	f	\N	t	2025-06-21 20:48:00	f	\N	105
130	6	19	2025-07-11 13:26:52.958943	sup, just wanna try how this work. wanna see those cuty kittens? idc, just watch them ^^ sup, just wanna try how this work. wanna see those cuty kittens? idc, just watch them ^^	f	\N	f	\N	f	\N	\N
96	19	9	2025-06-16 20:05:30.497509	123123іі	f	\N	f	\N	t	2025-07-14 17:11:00	\N
95	19	9	2025-06-16 20:05:29.325716	ваиварирваssf	f	\N	f	\N	t	2025-07-14 17:31:00	\N
134	19	20	2025-07-14 18:47:31.544398	1	f	\N	f	\N	f	\N	\N
139	19	20	2025-07-16 18:17:25.881381	5	f	\N	f	\N	f	\N	\N
141	19	20	2025-07-16 18:22:29.105486	7	f	\N	f	\N	f	\N	\N
142	19	20	2025-07-16 18:22:31.928303	8	f	\N	f	\N	f	\N	\N
143	6	20	2025-07-16 18:24:58.501235	1	f	\N	f	\N	f	\N	\N
144	6	20	2025-07-16 18:25:02.594324	4	f	\N	f	\N	f	\N	\N
145	20	6	2025-07-16 18:25:17.530712	1	f	\N	f	\N	f	\N	\N
149	6	29	2025-07-24 16:40:47.415637	привет	f	\N	f	\N	f	\N	\N
151	29	6	2025-07-24 16:41:07.401486	да нормик, а ты вообще как?	f	\N	f	\N	f	\N	\N
152	29	6	2025-07-24 16:47:01.289861	мяу	f	\N	f	\N	f	\N	\N
\.


--
-- Data for Name: news; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.news (id, title, content, last_update, is_deleted, deleted_at, recipient_id, reference_table, reference_id) FROM stdin;
14	New post by penis	Your friend has recently posted new post! Come on and check it!	2025-07-13 19:06:10.237032	t	2025-07-14 16:43:23.038339	9	posts	14
47	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	66
49	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	67
29	New post by penis	Your friend has recently posted new post! Come on and check it!	2025-07-16 20:30:23.464695	f	\N	9	posts	58
32	New post by penis	Your friend has recently posted new post! Come on and check it!	2025-07-16 21:15:43.691864	f	\N	9	posts	59
51	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	68
17	New post by penis	Your friend has recently posted new post! Come on and check it!	2025-07-13 19:11:12.52182	t	2025-07-14 16:42:39.61572	9	posts	56
53	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	69
8	New post by penis	Your friend has recently posted new post! Come on and check it!	2025-07-13 18:46:23.22701	t	2025-07-14 16:42:41.845604	9	posts	55
55	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	70
11	New post by penis	Your friend has recently posted new post! Come on and check it!	2025-07-13 19:05:31.473706	t	2025-07-14 16:42:44.645493	9	posts	54
57	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	71
35	New post by penis	Your friend has recently posted new post! Come on and check it!	2025-07-16 21:15:43.691864	f	\N	9	posts	60
37	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	61
39	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	62
41	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	63
43	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	64
45	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	65
59	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	72
61	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	73
63	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	74
65	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	75
67	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	76
69	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:21:23.344672	f	\N	28	posts	77
71	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:45:38.211445	f	\N	28	posts	78
73	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:45:38.211445	f	\N	28	posts	79
75	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:45:38.211445	f	\N	28	posts	80
77	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:45:38.211445	f	\N	28	posts	81
79	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:45:38.211445	f	\N	28	posts	82
82	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:50:03.275139	f	\N	28	posts	83
84	New post by meow	Your friend has recently posted new post! Come on and check it!	2025-07-17 13:50:03.275139	f	\N	28	posts	84
86	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:28:32.925838	f	\N	9	posts	85
87	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:28:32.925838	f	\N	24	posts	85
88	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:28:32.925838	f	\N	28	posts	85
90	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:28:32.925838	f	\N	20	posts	85
91	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:28:32.925838	f	\N	27	posts	85
92	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:28:32.925838	f	\N	8	posts	85
93	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:41:04.597305	f	\N	9	posts	86
94	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:41:04.597305	f	\N	24	posts	86
95	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:41:04.597305	f	\N	28	posts	86
97	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:41:04.597305	f	\N	20	posts	86
98	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:41:04.597305	f	\N	27	posts	86
99	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-19 20:41:04.597305	f	\N	8	posts	86
100	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-21 18:50:26.819134	f	\N	9	posts	87
101	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-21 18:50:26.819134	f	\N	24	posts	87
102	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-21 18:50:26.819134	f	\N	28	posts	87
104	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-21 18:50:26.819134	f	\N	20	posts	87
105	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-21 18:50:26.819134	f	\N	27	posts	87
106	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-21 18:50:26.819134	f	\N	8	posts	87
108	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	9	posts	88
109	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	24	posts	88
110	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	28	posts	88
111	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	29	posts	88
113	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	20	posts	88
114	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	27	posts	88
115	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	8	posts	88
116	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	9	posts	89
117	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	24	posts	89
118	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	28	posts	89
119	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	29	posts	89
121	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	20	posts	89
122	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	27	posts	89
123	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-26 23:58:09.931983	f	\N	8	posts	89
124	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	t	2025-07-28 20:16:46.974088	9	posts	90
125	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	t	2025-07-28 20:16:46.974088	24	posts	90
126	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	t	2025-07-28 20:16:46.974088	28	posts	90
127	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	t	2025-07-28 20:16:46.974088	29	posts	90
129	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	t	2025-07-28 20:16:46.974088	20	posts	90
130	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	t	2025-07-28 20:16:46.974088	27	posts	90
131	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	t	2025-07-28 20:16:46.974088	8	posts	90
132	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	f	\N	9	posts	91
133	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	f	\N	24	posts	91
134	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	f	\N	28	posts	91
135	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	f	\N	29	posts	91
137	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	f	\N	20	posts	91
138	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	f	\N	27	posts	91
139	New post by georbayn	Your friend has recently posted new post! Come on and check it!	2025-07-28 20:11:43.818815	f	\N	8	posts	91
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.posts (id, content, created_at, author_id, title, is_deleted, slug, deleted_at, is_edited, edited_at, reference, is_reposted, reposted_at) FROM stdin;
12	<p>мвамвамвамваваммва</p>	2025-06-20 22:44:00.061273	6	попко	f	4fdd797f8aa64eba	\N	t	2025-07-01 23:16:19.840999	\N	\N	\N
9	<p>а ти ?b</p>	2025-06-09 17:00:33.283077	6	сасал мяу?	t	326bae7ee62a4b24	2025-07-28 21:05:08.957101	t	2025-07-28 14:19:08.486111	\N	\N	\N
11	<p>аааааа <strong>аааа<span style="font-size: 18pt;">чччч</span></strong></p>	2025-06-20 19:42:45.01456	6	vdfvdfvdf	t	515ffb7764ea4db9	2025-07-28 21:05:09.942162	f	\N	\N	\N	\N
14	<p>мяу)</p>	2025-06-24 23:18:02.325818	19	ппвпв	t	34928da82b724fa7	2025-07-14 16:43:23.031241	t	2025-07-01 23:23:06.695556	\N	\N	\N
10	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	9	just testing guys!	f	97a9006f846e4a29	2025-06-26 13:44:36.471519	f	\N	\N	\N	\N
31	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	t	a3805d99b07d440b	2025-06-26 13:45:50.957418	f	\N	10	t	2025-06-26 13:45:28.294256
35	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	t	680dbbac375141f6	2025-06-26 15:26:44.227982	f	\N	10	t	2025-06-26 14:10:18.239816
36	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	t	a66bb5b743db459b	2025-06-26 15:37:02.983483	f	\N	10	t	2025-06-26 15:26:44.227982
37	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	f	f8b3e5ec522b4074	\N	f	\N	10	t	2025-06-26 15:37:02.983483
30	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	t	be807e12d83d460f	2025-06-26 13:45:28.294256	f	\N	10	t	2025-06-26 13:45:19.112904
32	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	t	a7dcd1a62a43467a	2025-06-26 13:46:04.8063	f	\N	10	t	2025-06-26 13:45:50.957418
33	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	t	a620ae45c4fc4dab	2025-06-26 14:09:01.793035	f	\N	10	t	2025-06-26 13:46:04.8063
25	<p>мяу)ууууууу</p>	2025-06-25 12:26:51.707167	19	а ваф ваф ва ва	t	f489d34d228e47df	2025-06-26 13:20:04.985453	f	\N	\N	f	\N
24	<p>мяу)</p>	2025-06-25 12:20:29.884542	19	сосать член мой б стро	t	bb32aed9e4f34bed	2025-06-26 13:20:06.250223	f	\N	\N	f	\N
22	<p>фиваивафифваифва</p>	2025-06-09 17:00:33.283077	19	мямяумяумя	t	a0c70e0c31f74ded	2025-06-26 13:20:09.231285	f	\N	9	t	2025-06-25 01:42:00.026744
21	<p>приветули __!!!</p>	2025-06-25 01:41:55.015574	19		t	bf77af2d96f545c2	2025-06-26 13:20:11.120092	f	\N	\N	f	\N
20	<p>аааааа <strong>аааа<span style="font-size: 18pt;">чччч</span></strong></p>	2025-06-20 19:42:45.01456	19		t	12e82076a700497e	2025-06-26 13:20:12.535274	f	\N	11	t	2025-06-25 01:30:52.608479
19	<p>мвамвамвамваваммва</p>	2025-06-25 01:16:01.385916	19		t	e55011d0efd1483e	2025-06-26 13:20:14.057319	f	\N	12	t	2025-06-25 01:16:01.385916
16	<p>пениса)</p>	2025-06-25 00:47:20.788622	19		t	213778bb78d64b6e	2025-07-14 16:43:26.12675	f	\N	13	t	2025-06-25 00:47:20.788622
13	<p>пениса)</p>	2025-06-24 19:41:29.634138	19	мяу)	t	ad2183a9daea4d27	2025-07-14 16:43:29.864785	t	2025-07-01 23:21:44.742203	\N	\N	\N
27	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	t	281530f8ef5c4b57	2025-06-26 13:43:07.664545	f	\N	10	t	2025-06-26 13:34:15.206935
17	<p>пениса)</p>	2025-06-25 00:47:37.153516	19		t	ae15809d4bca4b36	2025-07-28 21:05:06.290313	f	\N	13	t	2025-06-25 00:47:37.153516
23	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-25 12:17:48.078139	19	just testing guys!	t	824f4c65e434458b	2025-06-26 13:20:07.965667	f	\N	\N	f	\N
41	<p>а ти ?</p>	2025-06-09 17:00:33.283077	28	сасал мяу?	t	7416168b76954929	2025-07-13 17:29:38.668411	f	\N	9	t	2025-07-13 17:29:35.917266
42	<p>а ти ?</p>	2025-06-09 17:00:33.283077	28	сасал мяу?	t	fb63b62e3dba4319	2025-07-13 17:29:59.675657	f	\N	9	t	2025-07-13 17:29:41.498402
43	<p>а ти ?</p>	2025-06-09 17:00:33.283077	28	сасал мяу?	t	77442e9d98004f6a	2025-07-13 17:30:05.27264	f	\N	9	t	2025-07-13 17:29:59.675657
44	<p>а ти ?</p>	2025-06-09 17:00:33.283077	28	сасал мяу?	t	a3b271a1d4a74a13	2025-07-13 17:30:08.654743	f	\N	9	t	2025-07-13 17:30:07.275557
77	<p>1</p>	2025-07-17 13:31:17.23763	8	1	f	596408a9f9c94aaf	\N	f	\N	\N	f	\N
78	<p>2</p>	2025-07-17 13:49:26.917275	8	2	f	a9217621c55d4a44	\N	f	\N	\N	f	\N
79	<p>2</p>	2025-07-17 13:49:27.723023	8	2	f	f0bc2dc3b890463f	\N	f	\N	\N	f	\N
80	<p>2</p>	2025-07-17 13:49:28.116685	8	2	f	6e68c5dda8294c92	\N	f	\N	\N	f	\N
81	<p>2</p>	2025-07-17 13:49:28.424509	8	2	f	44614931aada4313	\N	f	\N	\N	f	\N
82	<p>2</p>	2025-07-17 13:49:28.721483	8	2	f	e2a1d71032fc4dc0	\N	f	\N	\N	f	\N
83	<p>3</p>	2025-07-17 16:47:38.69717	8	3	f	91bc9997d229407c	\N	f	\N	\N	f	\N
84	<p>3</p>	2025-07-17 16:48:01.299452	8	3	f	bbb7d1d4c094407d	\N	f	\N	\N	f	\N
57	<p>ff</p>	2025-07-14 16:23:36.078223	20	ff	t	bbf2891d01e347c3	2025-07-14 16:23:42.752061	f	\N	\N	f	\N
45	<p>о</p>	2025-07-13 18:20:15.565647	19	о	t	bfb8fd7825e7449f	2025-07-14 16:42:37.687847	f	\N	\N	f	\N
56	<p>dvfvvfvf</p>	2025-07-13 19:11:56.235584	19	vddfvvdf	t	9035ab3ce2324bde	2025-07-14 16:42:39.611716	f	\N	\N	f	\N
55	<p>sss</p>	2025-07-13 18:46:27.717749	19	ss	t	f9ff066402e14cd6	2025-07-14 16:42:41.8396	f	\N	\N	f	\N
54	<p>sdvbfvsdf</p>	2025-07-13 18:37:33.904129	19	gjcnr	t	06984ee97bb74ced	2025-07-14 16:42:44.639814	f	\N	\N	f	\N
53	<p>meow</p>	2025-07-13 18:27:50.703163	19	new post	t	dc285fc40cde41ef	2025-07-14 16:42:47.335303	f	\N	\N	f	\N
52	<p>meow</p>	2025-07-13 18:27:32.206626	19	new post	t	cb97c85be3124a75	2025-07-14 16:42:49.602607	f	\N	\N	f	\N
51	<p>n</p>	2025-07-13 18:22:50.037659	19	n	t	43c9defa415c49dc	2025-07-14 16:42:51.294672	f	\N	\N	f	\N
50	<p>b</p>	2025-07-13 18:22:39.019387	19	b	t	68420644359d42fa	2025-07-14 16:42:53.616419	f	\N	\N	f	\N
49	<p>b</p>	2025-07-13 18:22:30.568175	19	b	t	260b300a139244c6	2025-07-14 16:42:56.113188	f	\N	\N	f	\N
48	<p>j</p>	2025-07-13 18:22:10.106158	19	j	t	9f9df2a7d5c14200	2025-07-14 16:42:57.936743	f	\N	\N	f	\N
47	<p>j</p>	2025-07-13 18:21:16.865357	19	j	t	c7cef37389f24099	2025-07-14 16:43:00.162318	f	\N	\N	f	\N
46	<p>j</p>	2025-07-13 18:20:53.136556	19	j	t	6aca2676679a4c56	2025-07-14 16:43:03.173978	f	\N	\N	f	\N
58	<p>ну дя)</p>	2025-07-16 20:44:58.573107	19	нов й пост	f	28ba83f0043d4f18	\N	f	\N	\N	f	\N
59	<p>2</p>	2025-07-16 21:16:12.560793	19	1	f	0cf3b322d97d4d9f	\N	f	\N	\N	f	\N
60	<p>a</p>	2025-07-16 21:16:52.727867	19	a	f	73b0fa2ea5194a13	\N	f	\N	\N	f	\N
61	<p>1</p>	2025-07-17 13:31:04.827036	8	1	f	4f88499654174514	\N	f	\N	\N	f	\N
62	<p>1</p>	2025-07-17 13:31:05.726498	8	1	f	9b5eaa805c0744f5	\N	f	\N	\N	f	\N
63	<p>1</p>	2025-07-17 13:31:06.563597	8	1	f	0946c7cfd9c8467e	\N	f	\N	\N	f	\N
64	<p>1</p>	2025-07-17 13:31:07.193311	8	1	f	9b180a78703744e5	\N	f	\N	\N	f	\N
65	<p>1</p>	2025-07-17 13:31:07.948415	8	1	f	a3089beee3b64290	\N	f	\N	\N	f	\N
66	<p>1</p>	2025-07-17 13:31:08.600599	8	1	f	1cbf3b1eb2b247f6	\N	f	\N	\N	f	\N
67	<p>1</p>	2025-07-17 13:31:09.316578	8	1	f	93bb45ca254c43a3	\N	f	\N	\N	f	\N
68	<p>1</p>	2025-07-17 13:31:09.957633	8	1	f	13f74bfe00604bcb	\N	f	\N	\N	f	\N
69	<p>1</p>	2025-07-17 13:31:10.61506	8	1	f	0a12888408f745c1	\N	f	\N	\N	f	\N
70	<p>1</p>	2025-07-17 13:31:11.327394	8	1	f	51737bd1456e484f	\N	f	\N	\N	f	\N
71	<p>1</p>	2025-07-17 13:31:12.029229	8	1	f	148aa4f8e8cc4533	\N	f	\N	\N	f	\N
72	<p>1</p>	2025-07-17 13:31:12.681478	8	1	f	739031df6776440c	\N	f	\N	\N	f	\N
73	<p>1</p>	2025-07-17 13:31:13.343397	8	1	f	b9470f67113145aa	\N	f	\N	\N	f	\N
74	<p>1</p>	2025-07-17 13:31:13.986838	8	1	f	2d6f6e58cc83424c	\N	f	\N	\N	f	\N
75	<p>1</p>	2025-07-17 13:31:14.689522	8	1	f	41b79da30ddf481b	\N	f	\N	\N	f	\N
76	<p>1</p>	2025-07-17 13:31:15.313456	8	1	f	14dade61ec624f10	\N	f	\N	\N	f	\N
38	<p><img src="/static/uploads/c6442f641a374163aca6cb0a1a92f1ad.jpg" alt="" width="1024" height="1280"></p>	2025-06-29 00:39:23.609986	19	весело	t	cbd653e1a74045b8	2025-07-14 16:43:05.55882	f	\N	\N	f	\N
29	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	f	be0834fb128349e9	\N	f	\N	10	t	2025-06-26 13:44:36.471519
26	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	t	a56f64af32614f63	2025-06-26 13:42:44.158709	f	\N	10	t	2025-06-26 13:21:58.597671
28	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	t	e94b0d1eb8e04e7e	2025-06-26 13:43:09.158247	f	\N	10	t	2025-06-26 13:42:46.869279
85	<p>вв<br><img src="/static/uploads/aa01894e5ae746f2bfe0ec59ad9a6112.jpg" alt="" width="736" height="736"></p>	2025-07-19 20:29:37.495631	6	123	f	26d93aedb3004dc6	\N	f	\N	\N	f	\N
34	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-10 00:08:12.857087	19	just testing guys!	t	ce7d8e79bcbe4908	2025-06-26 14:10:18.239816	f	\N	10	t	2025-06-26 14:09:01.793035
18	<p>sup, just wanna try how this work. wanna see those cuty kittens? idc, <strong>just watch them </strong>^^<br><img src="/static/uploads/4619538cd21747a79077837038641d2e.jpg" alt="" width="251" height="300"> &nbsp; <img src="/static/uploads/3f74403704334f7c95e58a4526a32339.jpg" alt="" width="257" height="300"><br><br></p>	2025-06-25 00:50:47.880162	19	just testing guys!	f	d93ed34465a74a8f	\N	f	\N	10	t	2025-06-25 00:50:47.880162
88	<p><img alt="" height="1280" src="https://wtyxtyyiuelqcfsdyixh.supabase.co/storage/v1/object/public/posts/users/photo_2025-06-25_00-08-11.jpg" width="1024"/></p>	2025-07-26 23:58:33.008695	6		f	b38bca9e89e94ef0	\N	f	\N	\N	f	\N
89	<p><img src="https://wtyxtyyiuelqcfsdyixh.supabase.co/storage/v1/object/public/posts/users/mceclip0.jpg"/></p>	2025-07-27 00:01:53.886863	6		f	f69080dabfef45c8	\N	f	\N	\N	f	\N
86	<p><img alt="" height="552" src="../../static/uploads/bc3d849061d74dd19d50df4b0376a137.jpg" width="736"/></p>	2025-07-19 20:41:27.664668	6	йцs	f	80018746f4d54567	\N	t	2025-07-19 20:48:10.257266	\N	f	\N
87	<p><br/><br/>1<br/><br/></p>	2025-07-21 18:50:42.018919	6	123	f	f692ad8ffdc84b83	\N	f	\N	\N	f	\N
90	<p>&lt;p style="text-align: left;"&gt;Привет!&lt;br&gt;Это &lt;strong&gt;мой &lt;/strong&gt;ПЕРВЫЙ пост! Вот &lt;em&gt;кстати&lt;/em&gt;,&lt;span style="font-size: 12pt;"&gt; фоточка &lt;span style="text-decoration: underline;"&gt;смешная&lt;/span&gt;&lt;span style="color: rgb(126, 140, 141);"&gt; (чуть миленькая)&lt;/span&gt;:&lt;/span&gt;&lt;br&gt;&lt;img src="blob:http://127.0.0.1:5000/e322c32f-dd36-485f-b49e-4f519c204209"&gt;&lt;/p&gt;<br/>&lt;hr&gt;<br/>&lt;p style="text-align: left;"&gt;Кстати говоря, какие мысли у вас вызывают следующие слова:&lt;br&gt;&lt;em data-start="302" data-end="448"&gt;"Человек &amp;mdash; это канат, натянутый между зверем и сверхчеловеком &amp;mdash; канат над бездной. То, что в человеке велико, &amp;mdash; это то, что он мост, а не цель."&lt;/em&gt;&lt;br data-start="448" data-end="451"&gt;(Из "Так говорил Заратустра")&lt;/p&gt;<br/>&lt;hr&gt;<br/>&lt;p style="text-align: left;"&gt;Также, хочу у вас спросить: что не так в этом коде? Ответы пишите в комментариях под постом!&lt;/p&gt;<br/>&lt;p&gt;&lt;code&gt;import json&lt;/code&gt;&lt;/p&gt;<br/>&lt;p&gt;&lt;code&gt;class TaskManager:&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; def __init__(self, filename):&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; self.filename = filename&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; self.tasks = self.load_tasks()&lt;/code&gt;&lt;/p&gt;<br/>&lt;p&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; def load_tasks(self):&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; with open(self.filename, 'r') as f:&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; return json.load(f)&lt;/code&gt;&lt;/p&gt;<br/>&lt;p&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; def add_task(self, title, completed=False):&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; task = {'title': title, 'completed': completed}&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; self.tasks.append(task)&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; self.save_tasks()&lt;/code&gt;&lt;/p&gt;<br/>&lt;p&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; def save_tasks(self):&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; with open(self.filename, 'w') as f:&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; json.dump(self.tasks, f, indent=4)&lt;/code&gt;&lt;/p&gt;<br/>&lt;p&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; def list_tasks(self):&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; for idx, task in enumerate(self.tasks):&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; status = '✓' if task['completed'] else '✗'&lt;/code&gt;&lt;br&gt;&lt;code&gt;&amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp; print(f"{idx + 1}. {task['title']} [{status}]")&lt;/code&gt;&lt;/p&gt;<br/>&lt;p&gt;&lt;code&gt;manager = TaskManager('tasks.json')&lt;/code&gt;&lt;br&gt;&lt;code&gt;manager.add_task('Fix the bug')&lt;/code&gt;&lt;br&gt;&lt;code&gt;manager.list_tasks()&lt;br&gt;&lt;/code&gt;&lt;/p&gt;<br/>&lt;hr&gt;<br/>&lt;p&gt;Всего хорошего и доброго времени суток!&lt;/p&gt;</p>	2025-07-28 20:16:40.933898	6	йцук	t	da535bd8bd624bac	2025-07-28 20:16:46.964079	f	\N	\N	f	\N
8	<p style="text-align: left;">ssПривет!<br>Это <strong>мой </strong>ПЕРВЫЙ пост! Вот <em>кстати</em>,<span style="font-size: 12pt;"> фоточка <span style="text-decoration: underline;">смешная</span><span style="color: rgb(126, 140, 141);"> (чуть миленькая)</span>:</span><br><img src="/static/uploads/cf6b5984b92e435ab84382e846ab2d44.jpg"></p>\r\n<hr>\r\n<p style="text-align: left;">Кстати говоря, какие мысли у вас вызывают следующие слова:<br><em data-start="302" data-end="448">"Человек &mdash; это канат, натянутый между зверем и сверхчеловеком &mdash; канат над бездной. То, что в человеке велико, &mdash; это то, что он мост, а не цель."</em><br data-start="448" data-end="451">(Из "Так говорил Заратустра")</p>\r\n<hr>\r\n<p style="text-align: left;">Также, хочу у вас спросить: что не так в этом коде? Ответы пишите в комментариях под постом!</p>\r\n<p><code>import json</code></p>\r\n<p><code>class TaskManager:</code><br><code>&nbsp; &nbsp; def __init__(self, filename):</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; self.filename = filename</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; self.tasks = self.load_tasks()</code></p>\r\n<p><code>&nbsp; &nbsp; def load_tasks(self):</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; with open(self.filename, 'r') as f:</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; return json.load(f)</code></p>\r\n<p><code>&nbsp; &nbsp; def add_task(self, title, completed=False):</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; task = {'title': title, 'completed': completed}</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; self.tasks.append(task)</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; self.save_tasks()</code></p>\r\n<p><code>&nbsp; &nbsp; def save_tasks(self):</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; with open(self.filename, 'w') as f:</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; json.dump(self.tasks, f, indent=4)</code></p>\r\n<p><code>&nbsp; &nbsp; def list_tasks(self):</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; for idx, task in enumerate(self.tasks):</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; status = '✓' if task['completed'] else '✗'</code><br><code>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; print(f"{idx + 1}. {task['title']} [{status}]")</code></p>\r\n<p><code>manager = TaskManager('tasks.json')</code><br><code>manager.add_task('Fix the bug')</code><br><code>manager.list_tasks()<br></code></p>\r\n<hr>\r\n<p>Всего хорошего и доброго времени суток!</p>	2025-06-09 16:39:10.088312	6	My first post !v	f	ae07aef8e1d14d69	\N	t	2025-07-01 21:56:08.821968	\N	\N	\N
\.


--
-- Data for Name: reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reports (id, author_id, reference_table, reference_id, created_at) FROM stdin;
\.


--
-- Data for Name: user_verifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_verifications (user_id, verification_code, code_expiration) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password_hash, email, is_verified, picture, is_banned, banned_at) FROM stdin;
19	penis	scrypt:32768:8:1$RXazeSHdUvv6iJsb$34d40ffb5dddfac6f10826e63b7a2b9b22ac800569f86a3e7d71a42a981add4cbaa67c994b8d82f327e2fbef338692f41e10bc82467da1923fad33ce75aaf7c5	normchelll@gmail.com	t	35126e0829734222.jpg	f	\N
20	newuser	scrypt:32768:8:1$4e50S0DLeLxkMMC2$d6957452c94a83cde996be5bdcd66a280dcd7e9128b13847d95abfaab82eb0e69578e91271e9f233dd49fc4e78c7339517b09c5448f3b68c066d843df412577b	newuser@gmail.com	t	1cb3dd41be8e4116.jpg	f	\N
25	безмозглый	scrypt:32768:8:1$gIUb9L28JfF8SWnk$8f5cf4f3c3de4295cccaf61ce0b43dfd8d755464846bd769543b779f6c40dbd70e5ac7a6d636cfabfa31d9ae89f15f623ff04ab1f6232cdb133bcd1c61bb5e9f	vsdfvadfvadvafd@gmail.com	t	8f65057ea44d4f5a.jpg	f	\N
18	normchell	scrypt:32768:8:1$0PvL18Eq7nPKN0wW$cd9f9669ef1dbd09daf8526c052f8e9e6c65b294958bca7d6c65743cc83e536b881df57030cc8e0ef8914dbeee03f0bdb993c132981c34c544b4f750663a0e8b	normchell@gmail.com	t	default.png	f	\N
24	qwer1234	scrypt:32768:8:1$JJMJ8DxIcbfI3Vs4$ba07dd870c7c41a7be05466df9e00bce2321f3fb532c344699e44b74140e46697bfa81e6326c76af35f600686db72e9aaf14b448de94454520c20fd41bf62b76	qweb@gmail.com	t	default.png	f	\N
27	ghostlmst	scrypt:32768:8:1$gKHxUziQRIVcewyS$3968257d3bf9f707ab3ac38b4e7ab4370889e9300233cc7528a3e94beeb4b5cec3c4af304741167e42cc4cf1fbd2229ecc748e03889ef2e38f79feeeb0751469	ghostlmst@gmail.com	t	default.png	f	\N
9	guy	scrypt:32768:8:1$fEmuCibUJYytCC2I$81767da138f772dbf6e0f1d0b4bdf01e3c095803bf7f0b2d7c5387273b066e4aec825feb509c8972bf011b708ef2fc6f85892360936847ab02ad9b05c444964c	guy@gmail.com	t	c1d692e336b640d8.jpg	f	\N
7	обезьяна	scrypt:32768:8:1$Y0CtVGBCEtQxdYvK$3ac0803cded02dc77fd2e793e75cd0bdb6308f1c6785ccb43a73916136e9687b9f8053a66f3cc76d840665f06328571b08aca3ec31b1ee699c2da76890e81d43	creativeemail@gmail.com	t	a03732359ae448ea.jpg	f	\N
8	meow	scrypt:32768:8:1$HCOf2vIr3jixWdG4$4c9d8dcc82f390775f6a1c29ae9fc2b93d6f63a8c6a8aaab4f549ae6d909eaa9c8c1abc20bb3086043573f0f76993fe919fc27963c2a03eaa4f6d10e390afb1d	hello@gmail.com	t	d1c368bf6e764764.jpg	f	\N
28	some_account	scrypt:32768:8:1$EZJZPiyWgRFZkXzV$991ba8a44a3ed52e1f3da97c17d0c129ba3503200ca34aed83f4e124432b14c966437f93213202eae8896b9b1f8b737d242c0ba19da18f9dd90b0a4f93475db0	whyplovu@gmail.com	t	default.png	f	\N
29	itsgeorbayn	scrypt:32768:8:1$q5Ushx5CT9kQEDao$d478b84f89cac2a09e5629fc3f60fe5347b2483cacf798b3d2db2121fd036366216137d7d195034e6b176171b78ede9ba3598ef6ae63c4a5d447b37a000201b0	itsgeorbayn@gmail.com	t	default.png	f	\N
30	george.baynak	scrypt:32768:8:1$G8PfNC0kmLUZp3y1$57df7355462d2b4179813b93104fc0f2405778436cff69d7f3fcc41d33479ae28829c84e489f3604c0f59a43d6d3c67961c614e98b6c6a4de7c7c12983cdec2c	george.baynak@gmail.com	t	default.png	f	\N
6	georbayn	scrypt:32768:8:1$8uxoqjhe4V8FvKCj$d71ee82b2959b7073f4b87da9f8d9cf8e8527e66efd6de78156353160aed5cfe665b5464e7cb2e655cc812a1014407e21445a8fce4258cac715e53e6c177f561	georbayn@gmail.com	t	179a4ef80e8b4dfe.jpg	f	2025-07-11 12:49:05.286206
\.


--
-- Name: admin_permissions_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admin_permissions_user_id_seq', 1, false);


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comments_id_seq', 32, true);


--
-- Name: friendships_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.friendships_id_seq', 30, true);


--
-- Name: likes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.likes_id_seq', 52, true);


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.messages_id_seq', 152, true);


--
-- Name: news_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.news_id_seq', 139, true);


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.posts_id_seq', 91, true);


--
-- Name: reports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reports_id_seq', 22, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 30, true);


--
-- Name: admin_permissions admin_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_permissions
    ADD CONSTRAINT admin_permissions_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: friendships friendships_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friendships
    ADD CONSTRAINT friendships_pkey PRIMARY KEY (id);


--
-- Name: likes likes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: news news_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_pkey PRIMARY KEY (id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: posts posts_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_slug_key UNIQUE (slug);


--
-- Name: reports reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: admin_permissions admin_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_permissions
    ADD CONSTRAINT admin_permissions_user_id_fkey FOREIGN KEY (id) REFERENCES public.users(id);


--
-- Name: comments comments_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- Name: friendships friendships_user1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friendships
    ADD CONSTRAINT friendships_user1_id_fkey FOREIGN KEY (user1_id) REFERENCES public.users(id);


--
-- Name: friendships friendships_user2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friendships
    ADD CONSTRAINT friendships_user2_id_fkey FOREIGN KEY (user2_id) REFERENCES public.users(id);


--
-- Name: likes likes_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- Name: likes likes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: messages messages_receiver_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_receiver_fkey FOREIGN KEY (receiver) REFERENCES public.users(id);


--
-- Name: messages messages_reference_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_reference_fkey FOREIGN KEY (reference) REFERENCES public.messages(id);


--
-- Name: messages messages_sender_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_fkey FOREIGN KEY (sender) REFERENCES public.users(id);


--
-- Name: news news_recipient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_recipient_id_fkey FOREIGN KEY (recipient_id) REFERENCES public.users(id);


--
-- Name: posts posts_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: posts posts_reference_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_reference_fkey FOREIGN KEY (reference) REFERENCES public.posts(id);


--
-- Name: reports reports_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: user_verifications user_verifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_verifications
    ADD CONSTRAINT user_verifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--


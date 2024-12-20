PGDMP  9    .                |            pharmacy    17.2    17.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16389    pharmacy    DATABASE     �   CREATE DATABASE pharmacy WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE pharmacy;
                     postgres    false            �            1259    16406    medical_log    TABLE       CREATE TABLE public.medical_log (
    log_id integer NOT NULL,
    email character varying(255) NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    total_price numeric(10,2) NOT NULL,
    purchase_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.medical_log;
       public         heap r       postgres    false            �            1259    16405    medical_log_log_id_seq    SEQUENCE     �   CREATE SEQUENCE public.medical_log_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.medical_log_log_id_seq;
       public               postgres    false    221            �           0    0    medical_log_log_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.medical_log_log_id_seq OWNED BY public.medical_log.log_id;
          public               postgres    false    220            �            1259    16391    products    TABLE     �   CREATE TABLE public.products (
    id integer NOT NULL,
    drugname character varying(100) NOT NULL,
    price numeric(10,2) NOT NULL,
    stock integer NOT NULL,
    form character varying(50),
    category character varying(100)
);
    DROP TABLE public.products;
       public         heap r       postgres    false            �            1259    16390    products_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.products_id_seq;
       public               postgres    false    218            �           0    0    products_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;
          public               postgres    false    217            �            1259    16397    users    TABLE     �   CREATE TABLE public.users (
    email character varying(255) NOT NULL,
    name character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.users;
       public         heap r       postgres    false            ,           2604    16409    medical_log log_id    DEFAULT     x   ALTER TABLE ONLY public.medical_log ALTER COLUMN log_id SET DEFAULT nextval('public.medical_log_log_id_seq'::regclass);
 A   ALTER TABLE public.medical_log ALTER COLUMN log_id DROP DEFAULT;
       public               postgres    false    221    220    221            *           2604    16394    products id    DEFAULT     j   ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);
 :   ALTER TABLE public.products ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    218    217    218            �          0    16406    medical_log 
   TABLE DATA           f   COPY public.medical_log (log_id, email, product_id, quantity, total_price, purchase_date) FROM stdin;
    public               postgres    false    221   �       �          0    16391    products 
   TABLE DATA           N   COPY public.products (id, drugname, price, stock, form, category) FROM stdin;
    public               postgres    false    218   �       �          0    16397    users 
   TABLE DATA           G   COPY public.users (email, name, password_hash, created_at) FROM stdin;
    public               postgres    false    219   `&       �           0    0    medical_log_log_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.medical_log_log_id_seq', 1, false);
          public               postgres    false    220            �           0    0    products_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.products_id_seq', 1, false);
          public               postgres    false    217            3           2606    16412    medical_log medical_log_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.medical_log
    ADD CONSTRAINT medical_log_pkey PRIMARY KEY (log_id);
 F   ALTER TABLE ONLY public.medical_log DROP CONSTRAINT medical_log_pkey;
       public                 postgres    false    221            /           2606    16396    products products_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public                 postgres    false    218            1           2606    16404    users users_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (email);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    219            4           2606    16413 "   medical_log medical_log_email_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.medical_log
    ADD CONSTRAINT medical_log_email_fkey FOREIGN KEY (email) REFERENCES public.users(email) ON DELETE CASCADE;
 L   ALTER TABLE ONLY public.medical_log DROP CONSTRAINT medical_log_email_fkey;
       public               postgres    false    219    221    4657            5           2606    16418 '   medical_log medical_log_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.medical_log
    ADD CONSTRAINT medical_log_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;
 Q   ALTER TABLE ONLY public.medical_log DROP CONSTRAINT medical_log_product_id_fkey;
       public               postgres    false    218    4655    221            �      x������ � �      �   p  x�}Z�r�8}��b�`� xã�8Nj��w��VM�$Q66�"����� H�"4o)O����9����Ywz[�`k��ߓ�	ž�M]�����l���9���W�
gV����u5����`Ofk��4�ps��4ájS�ސ�ڞ��2IȘ��O�ꆪ�m�2v�f����d͋Ի�v�-���{9���K5�mw���������y��]��l��A7L�(y�>%�l�K����2���~0zSU���C�v����\J�J��q��	{_�3o����>Ĝ}n�Wm\����~�:[�q���ָp���p��J���^�R��t���u�\���`�@E2��.��D�m�ξtU�8wu�cw\�f칫v��-�I��N�Ҡ���f�B�]�e�6��������nf���Q�\b��Y=9*u��δν�dX��z	W���ўP
7�B�gM|
$1u�v��K����}3��M8wm"�K�]L�(J`k��Ǘ�gm����v'${2�i`lj4������̊��]�`�NgGOv{���o��¹C����G��w��w�,|���4E襪�&R�P�,���*�Gv�oQy��{:o�[�t�-1ia���� �cGm�2�&*���,�����n��<	o���YR��S���X���מ�0����KmZ�k�-�*��� %0��e^x����b2����<�
~�c%s���پ:�)�����`h�aBC߉���"d�z{�2!]�d�2T�m��>�D��4T?�N��7M-�hF�*�hpS������f�R~��R��uUë��#ԼUg�Oѕ�%�k�t��-_�u�"��U�1�ޓa�!b]�4cq�	��mbDG~mv��+�+ʙ�"Vc����w�}��U�Ӓ`��]u��1'ĩL8�ñѮ�ӔƊ�%�G��z���R-nҙq���@K(�<ە3`\R� ?�4��D&�:��$�y�;� \^w�h�߼ �jG�.�c#��=� F�j�4 N=��s��ߊ�CM�*W׸���U]ma�A �CѸk�J��F����2�̙b�N�֣C'ؓ�r�#{vW�ɯ(d@�1��zb"�h�@����o��J����|��cD�,O�G�M7g�I��1���<s�U5S�"�O���y�~�nWќ���R���w��v�C�U�z����\���;�פ]�Ю�(d�[�,�#�����|���t�RsK��7�`�N�dtnK2�� �f�T�s�L1 ժ��gi��5C8�`��S��� W��3��a�'�U��� �P�
q	|EIFG��0���.�g4OW�)I����dU���+!��+;/}ÕW!��=R���1wfy�`%�h7�#W�0D�*�����`GKw�,��KH�ׇ�?nJ��@�t�z0M��e���p8A�'��p��eɞ�@q���$��T�;�T�3�D���\��;��\���1zRT$ �A9��ݸ�,�(��L��ث�ݔ$]p�&Ũ�֕UnyB����W�GYe���^�G�Ū�r���_��Le��TA�뤑��۰�줊��v�+c��	-�!i^�K���7#��㿐>{5�<��l/&u�m�s`Op�Y�!�P;쉔Wg^��ƫ��D*k�0��#���r��=�]£:W7V�$s�v�����q�c�|����~�Ԃ$���C���m`�Z��,q%�#�� ��%}�U���}��M����Zp��g&��2Ԟ�0�V��$H�� pl8�:���-}Q���d����ƽ6�Ї�ŏ ������t�n�Q� �i�7\�3��!d��/���d/_e
 ,mf��-�~��q�����u�̂Z���Їp�u:5�g,�"q�bv�ըP���[�'�⬄�ve4Ah����-������;/�����c��x���5I��Y��qA�.�t�d��+��;$�zH�#+N�t�/�=$�����#�^c6��!3�h-��v��M�"/����~��9����FEz�o��T��p�K����6,@���O�;��HyP+q��i3A��ys<�4-I�?6n]Jq�*ʡ���c�Uٓ8~�I��{��E]Fm˰�#_��|cE�9���t�y۰~�1 -@	�H3�qT<q��:���vdl��D@U�.��l��@x��3=�x�L�������T^����3�����~��%� ���)��:�(���(�}������*Hoc������R�gu���YG\���iK?�����WQ�� ��P�[�����Is&��{Q7!"�~b/W��|�f���v�w�HCd9�ntN��/�|Y�#�3����t�r�o9{@�:r���^
�gNHS3JztM<�<ql
U�̹Z�;!Ǌ����@ś7��΋�~�UzT\7���@�m�݄g�x��)��C�My�R�/�h��wz<��-A����������a��y1��<�� /́��ַ�v΋�����VOV£��i�"a �����I0<��@?���9KGҼ��B��͖v�Aj����'����l|�X�L�����0��ϥ��ZX��[�gk���r�w�6E�$��p�14r�./!�%�om�9���g�ѧ�:��x�A���_�A�B�����?��7ڱ��sZ����֫/i=ُ΃y�8K��NS�d���1/S�hGk�)��*�p��?�c�㞕�:g��n�Y
�n���erL��L����4)QA�|��d����Yb��9������[+��6�,��/K׊���������/�\	�Ι���i���H����q��DA�)r��P��F�}f$��,[=&ϋ�r�x���"��f�(Z�z݌Apu��9LQ 'M���d��D�P��P�D��R�^B��:��lM�������^�A�      �      x������ � �     
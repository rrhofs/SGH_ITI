begin;

--Parte dos usuários
create table cargos (id serial primary key, descricao text, ativo boolean);
insert into cargos (descricao, ativo) values ('Administrador', true), ('Gerente', true),
												('Atendente', True), ('Governança', true);
create table usuarios (id serial primary key, nome varchar(255), senha text, ativo boolean);
create table usuarios_cargos (usuarios_id integer references usuarios(id), cargos_id integer references cargos(id));

--Parte da estrutura predial
create table predios (id serial primary key, nome varchar(255), ativo boolean);
create table quartos (id serial primary key, numero varchar(255), predio_id integer references predios(id), qt_banheiros integer, lotacao integer, cozinha boolean, custo double precision, ativo boolean, compartilhado boolean);

--Parte dos clientes
create table clientes (cnpj_cpf varchar(14) primary key, nome varchar(255), cep varchar(8), logradouro text, numero text, complemento text, telefone varchar(11), email text, ativo boolean);
insert into clientes (cnpj_cpf, nome, ativo) values ('-1', 'Governança', true);

--Parte dos servicos, produtos e conta
create table conta (id serial primary key, valor double precision, desconto double precision, ativa boolean, fechada boolean, dt_abertura timestamp, dt_fechamento timestamp, cliente_id varchar(14) references clientes(cnpj_cpf));
insert into conta (id, ativa, fechada, cliente_id) values (-1, true, false, '-1');
create table servicos (id serial primary key, descricao text, custo double precision, desconto double precision, ativo boolean);
create table produtos (id serial primary key, descricao text, custo double precision, desconto double precision, ativo boolean);
create table detalhes_conta (id serial primary key, cliente_id varchar(14) references clientes(cnpj_cpf), conta_id integer references conta(id), dt_inicial timestamp, dt_final timestamp, quarto_id integer references quartos(id), nro_pessoas integer);

commit;

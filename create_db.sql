create table users
(
    chat_id   bigint            not null
        constraint users_pk
            primary key,
    username  text,
    full_name text,
    referral  integer,
    kedo_user_id  bigint,
    id        serial            not null,
    balance   integer default 0 not null
);

alter table users
    owner to postgres;

create unique index users_id_uindex
    on users (id);

create table lentamark
(
    event_id   bigint            not null
        constraint lentamark_pk
            primary key,
    event_date  timestamp default current_timestamp
);

alter table lentamark
    owner to postgres;

create unique index event_id_uindex
    on lentamark (event_id);
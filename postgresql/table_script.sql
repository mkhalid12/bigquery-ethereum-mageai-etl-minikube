CREATE SCHEMA ethereum;
CREATE TABLE  ethereum.token_transfers (
        token_address text,
        from_address text,
        to_address text,
        "value" numeric(78),
        transaction_hash text ,
        log_index text ,
        block_timestamp timestamp,
        block_number bigint,
        block_hash text,
        PRIMARY KEY  (transaction_hash, log_index)
);


CREATE TABLE ethereum.tokens
 (
    address text,
    symbol text,
    "name" text,
    decimals text,
    total_supply numeric(78),
    block_timestamp timestamp,
    block_number bigint,
    block_hash text,
    PRIMARY KEY (address, block_number)
);

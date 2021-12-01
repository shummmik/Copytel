-- object: public."tbNewMessage" | type: TABLE --
-- DROP TABLE IF EXISTS public."tbNewMessage" CASCADE;
CREATE TABLE IF NOT EXISTS public."tbNewMessage"
(
    id bigserial NOT NULL,
    message jsonb NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE public."tbNewMessage"
    OWNER to telegram;

COMMENT ON TABLE public."tbNewMessage"
    IS 'table for new messages';


CREATE INDEX json_index_gin
    ON public."tbNewMessage" USING gin
    (message jsonb_path_ops)
;



CREATE INDEX json_index_peerid_gin
    ON public."tbNewMessage" USING GIN
    ((message -> 'peer_id'))
;


CREATE INDEX json_index_fromid_gin
    ON public."tbNewMessage" USING GIN
    ((message -> 'from_id'))
;








-- object: public."tbDelMessage" | type: TABLE --
-- DROP TABLE IF EXISTS public."tbDelMessage" CASCADE;
CREATE TABLE IF NOT EXISTS public."tbDelMessage"
(
    id bigserial NOT NULL,
    message jsonb NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE public."tbDelMessage"
    OWNER to telegram;

COMMENT ON TABLE public."tbDelMessage"
    IS 'table for del messages';


CREATE INDEX del_json_index_gin
    ON public."tbDelMessage" USING gin
    (message jsonb_path_ops)
;






-- object: public."tbEditMessage" | type: TABLE --
-- DROP TABLE IF EXISTS public."tbEditMessage" CASCADE;
CREATE TABLE IF NOT EXISTS public."tbEditMessage"
(
    id bigserial NOT NULL,
    message jsonb NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE public."tbEditMessage"
    OWNER to telegram;

COMMENT ON TABLE public."tbEditMessage"
    IS 'table for edit messages';



CREATE INDEX edit_json_index_gin
    ON public."tbEditMessage" USING gin
    (message jsonb_path_ops)
;



CREATE INDEX edit_json_index_peerid_gin
    ON public."tbEditMessage" USING GIN
    ((message -> 'peer_id'))
;


CREATE INDEX edit_json_index_fromid_gin
    ON public."tbEditMessage" USING GIN
    ((message -> 'from_id'))
;

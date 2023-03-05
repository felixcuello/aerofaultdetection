-- SCADA information
CREATE TABLE scada(
        uuid UUID DEFAULT gen_random_uuid() NOT NULL        
);

CREATE INDEX id_scada_idx ON public.scada USING btree(uuid);

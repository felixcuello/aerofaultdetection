-- SCADA information
CREATE TABLE site(
        uuid UUID DEFAULT gen_random_uuid() NOT NULL,
        site_number VARCHAR(32) NOT NULL

);

CREATE INDEX id_site_idx ON public.site USING btree(uuid);

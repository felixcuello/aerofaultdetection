-- Store sensors
CREATE TABLE sensor (
        uuid UUID DEFAULT gen_random_uuid() NOT NULL,
        datalogger_serial VARCHAR(32) NOT NULL,
        sensor_type VARCHAR(32) NOT NULL,
        sequence_no INTEGER
);

CREATE INDEX id_uuid_idx ON public.sensor USING btree(uuid);
CREATE INDEX id_sensor_idx ON public.sensor USING btree(sensor_type, sequence_no);

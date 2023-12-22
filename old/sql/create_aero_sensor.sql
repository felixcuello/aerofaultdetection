-- Store sensors
CREATE TABLE aero_sensor (
        uuid UUID DEFAULT gen_random_uuid() PRIMARY KEY NOT NULL,
        datalogger_id VARCHAR(32) NOT NULL,
        sensor_type VARCHAR(32) NOT NULL,
        sensor_seq INTEGER
);

CREATE INDEX id_aero_sensor_uuid_idx ON public.aero_sensor USING btree(uuid);
CREATE INDEX id_aero_sensor_idx ON public.aero_sensor USING btree(datalogger_id, sensor_type, sensor_seq);

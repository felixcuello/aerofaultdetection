---------------------------------------------------------------
-- Sensor-Sample relationship
---------------------------------------------------------------
CREATE TABLE aero_sample_type (
       uuid UUID DEFAULT gen_random_uuid() PRIMARY KEY NOT NULL,
       sensor_uuid UUID NOT NULL,
       sample_type VARCHAR(32) NOT NULL,
       sample_unit VARCHAR(32) NOT NULL
);

ALTER TABLE aero_sample_type
      ADD CONSTRAINT fk_aero_sample_sensor FOREIGN KEY (sensor_uuid) REFERENCES aero_sensor (uuid),
      ADD CONSTRAINT unique_sample_type UNIQUE (sample_type, sample_unit);

CREATE INDEX id_aero_sample_type_idx ON public.aero_sample_type USING btree(sensor_uuid);



---------------------------------------------------------------
-- Sample table
---------------------------------------------------------------
CREATE TABLE aero_sample (
       datetime TIMESTAMP NOT NULL,
       sample_type_uuid UUID NOT NULL,
       sample_value FLOAT
);
ALTER TABLE aero_sample
      ADD CONSTRAINT fk_aero_sample_type FOREIGN KEY (sample_type_uuid) REFERENCES aero_sample_type (uuid);

CREATE INDEX id_aero_sample_idx ON public.aero_sample USING btree(sample_type_uuid);

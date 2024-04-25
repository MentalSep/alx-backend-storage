-- Create an index on the first letter of the 'name' column for faster searches
CREATE INDEX idx_name_first ON names (name(1));

-- Trigger to reset valid_email only on email change
DELIMITER //
CREATE TRIGGER validate_email_update BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
  IF NEW.email <> OLD.email THEN
    SET NEW.valid_email = 0;
  END IF;
END;
//
DELIMITER ;

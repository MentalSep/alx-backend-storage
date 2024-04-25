-- Create stored procedure ComputeAverageScoreForUser
-- DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser (
  IN user_id INT
)
BEGIN
  DECLARE total_score INT;
  DECLARE num_corrections INT;

  -- Calculate total score and number of corrections for the user
  SELECT SUM(score), COUNT(*)
  INTO total_score, num_corrections
  FROM corrections
  WHERE corrections.user_id = user_id;

  -- Update user's average score
  IF num_corrections > 0 THEN
    SET total_score = total_score / num_corrections;
  ELSE
    SET total_score = 0;  -- Set NULL for no corrections
  END IF;

  UPDATE users
  SET average_score = total_score
  WHERE id = user_id;
END;
//
DELIMITER ;

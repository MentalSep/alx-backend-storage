-- Stored procedure to calculate and update user's average weighted score
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
  IN user_id INT
)
BEGIN
  DECLARE total_weighted_score FLOAT;
  DECLARE total_weight INT;

  SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
  INTO total_weighted_score, total_weight
  FROM corrections
  INNER JOIN projects ON corrections.project_id = projects.id
  WHERE corrections.user_id = user_id;

  IF total_weight > 0 THEN
    SET total_weighted_score = total_weighted_score / total_weight;
  ELSE
    SET total_weighted_score = NULL;
  END IF;

  UPDATE users
  SET average_score = total_weighted_score
  WHERE id = user_id;
END;
//
DELIMITER ;

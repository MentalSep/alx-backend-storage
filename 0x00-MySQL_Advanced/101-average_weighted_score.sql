-- Stored procedure to update average weighted score for all users
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
  UPDATE users u
  INNER JOIN (
    SELECT user_id, SUM(score * weight) / SUM(weight) AS average_weighted_score
    FROM corrections
    INNER JOIN projects ON project_id = id
    GROUP BY user_id
  ) AS weighted_scores ON u.id = weighted_scores.user_id
  SET u.average_score = weighted_scores.average_weighted_score;
END;
//
DELIMITER ;

-- script that creates a trigger that decreases the
-- quantity of an item after adding a new order.
DROP TRIGGER IF EXISTS update_qty;
DELIMITER $$
CREATE TRIGGER update_qty
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END $$
DELIMITER ;


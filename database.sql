DROP TABLE contains;
DROP TABLE takes_from;
DROP TABLE has;
DROP TABLE orders;
DROP TABLE staff_absent_days;
DROP TABLE bill;
DROP TABLE customer;
DROP TABLE food_items;
DROP TABLE staff;
DROP TABLE inventory_items;
DROP TABLE supplier;


CREATE TABLE inventory_items
(
  itemID INT NOT NULL AUTO_INCREMENT,
  item_name VARCHAR(30) NOT NULL,
  total_quantity INT NOT NULL,
  category VARCHAR(30),
  PRIMARY KEY (itemID)
);

CREATE TABLE staff
(
  staff_id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(30) NOT NULL,
  dob DATE NOT NULL,
  address VARCHAR(150) NOT NULL,
  salary FLOAT NOT NULL,
  phone VARCHAR(15) NOT NULL,
  designation VARCHAR(25) NOT NULL,
  PRIMARY KEY (staff_id)
);

CREATE TABLE supplier
(
  sup_id INT NOT NULL AUTO_INCREMENT,
  supplier_name VARCHAR(30) NOT NULL,
  address VARCHAR(150) NOT NULL,
  email VARCHAR(50),
  mobile INT NOT NULL,
  website VARCHAR(50),
  PRIMARY KEY (sup_id)
);

CREATE TABLE customer
(
  name VARCHAR(30) NOT NULL,
  phone INT NOT NULL,
  customer_ID INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (customer_ID)
);

CREATE TABLE orders
(
  order_id INT NOT NULL AUTO_INCREMENT,
  payment_status VARCHAR(10) NOT NULL,
  date_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  payment_mode VARCHAR(10) NOT NULL,
  amount FLOAT NOT NULL,
  customer_ID INT NOT NULL,
  staff_id INT NOT NULL,
  PRIMARY KEY (order_id),
  FOREIGN KEY (customer_ID) REFERENCES customer(customer_ID),
  FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

CREATE TABLE food_items
(
  food_id INT NOT NULL AUTO_INCREMENT,
  description VARCHAR(100),
  name VARCHAR(50) NOT NULL,
  price FLOAT NOT NULL,
  PRIMARY KEY (food_id)
);

CREATE TABLE contains
(
  quantity INT NOT NULL,
  order_id INT NOT NULL,
  food_id INT NOT NULL,
  PRIMARY KEY (order_id, food_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (food_id) REFERENCES food_items(food_id)
);

CREATE TABLE takes_from
(
  quantity INT NOT NULL,
  staff_id INT NOT NULL,
  itemID INT NOT NULL,
  PRIMARY KEY (staff_id, itemID),
  FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
  FOREIGN KEY (itemID) REFERENCES inventory_items(itemID)
);

CREATE TABLE staff_absent_days
(
  absent_days DATE NOT NULL,
  staff_id INT NOT NULL,
  PRIMARY KEY (absent_days, staff_id),
  FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

CREATE TABLE bill
(
  bill_no INT NOT NULL AUTO_INCREMENT,
  date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  total_amount FLOAT NOT NULL,
  sup_id INT NOT NULL,
  PRIMARY KEY (bill_no),
  FOREIGN KEY (sup_id) REFERENCES supplier(sup_id)
);

CREATE TABLE has
(
  quantity INT NOT NULL,
  bill_no INT NOT NULL,
  itemID INT NOT NULL,
  PRIMARY KEY (bill_no, itemID),
  FOREIGN KEY (bill_no) REFERENCES bill(bill_no),
  FOREIGN KEY (itemID) REFERENCES inventory_items(itemID)
);

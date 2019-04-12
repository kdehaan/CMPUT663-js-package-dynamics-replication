CREATE DATABASE npmversions;

CREATE USER 'npmversions'@'localhost' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON npmversions.* TO 'npmversions'@'localhost';

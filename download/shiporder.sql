# Generating the DDL lines 
 #------------------------------------------------#
create table shiporder ( orderperson text, orderid varchar(30) NOT NULL  PRIMARY KEY );
create table shipto ( name text, address text, city text, country text, orderid varchar(30), FOREIGN KEY (orderid) REFERENCES shiporder(orderid));
create table item ( title text, note text NOT NULL , quantity int, price numeric, itemid varchar(30) NOT NULL  PRIMARY KEY , itemdate date NOT NULL , orderid varchar(30), FOREIGN KEY (orderid) REFERENCES shiporder(orderid));
create table test ( name text, address text, city text, country text, itemid varchar(30), FOREIGN KEY (itemid) REFERENCES item(itemid));
# Generating the DML lines 
 #------------------------------------------------#

INSERT INTO shiporder (orderperson, orderid ) VALUES  ( 'SALHI ANAS', 'test' ) , ( 'SALHI ANAS', 'test2' ) ;
INSERT INTO shipto (name, address, city, country, orderid ) VALUES  ( 'SALHI', 'Semlalia', 'Marrakech', 'Morocco', 'test' ) , ( 'SALHI', 'Semlalia', 'Marrakech', 'Morocco', 'test2' ) ;
INSERT INTO item (title, note, quantity, price, itemid, itemdate, orderid ) VALUES  ( 'Notebook', null, '60', '15', 'item1', '2020-08-12', 'test' ) , ( 'Notebook', null, '60', '15', 'item2', '2020-08-12', 'test2' ) ;
INSERT INTO test (name, address, city, country, itemid ) VALUES  ( 'test', 'test', 'test', 'morocco', 'item1' ) , ( 'test', 'test', 'test', 'morocco', 'item2' ) ;
drop table if exists user;
create table user (
  name VARCHAR(50),
  account VARCHAR(50),
  password VARCHAR(100),
  country VARCHAR(10),
  phoneNumber VARCHAR(20),
  wechat VARCHAR(20),
  twitter VARCHAR(50),
  facebook VARCHAR(50),
  qq VARCHAR(20),
  status VARCHAR(10)
);
drop table if exists groups;
create table groups (
  groupName VARCHAR(50),
  groupId Varchar(20)
);
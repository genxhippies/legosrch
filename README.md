## Database Initialize                                                                                                  
execute mysql as root                                                                                                   
```                                                                                                                     
mysql> CREATE DATABASE legosrch CHARACTER SET utf8;                                                                     
mysql> CREATE USER 'legosrch_admin'@'localhost' IDENTIFIED BY 'somepassword';                                           
mysql> GRANT ALL ON legosrch.* TO 'legosrch_admin'@'localhost';                                                         
```                                                                                                                     

add my.cnf                                                                                                              
```                                                                                                                     
# my.cnf                                                                                                                
[client]                                                                                                                
database = legosrch                                                                                                     
user = legosrch_admin                                                                                                   
password = PASSWORD                                                                                                     
default-character-set = utf8                                                                                            
```

## Reference URL

http://lego.wikia.com/wiki/Category:Sets_by_item_number
http://api.wikia.com/wiki/Documentation


1099  curl 'http://lego.wikia.com/api/v1/Articles/Details/?titles=10188_Death_Star'
1103  curl 'http://lego.wikia.com/api/v1/Articles/AsSimpleJson/?id=3175'

1106  curl 'http://lego.wikia.com/api/v1/Articles/List/?category=Sets_by_item_number'
1107  curl 'http://lego.wikia.com/api/v1/Articles/List/?category=10000_sets'
1112  curl 'http://lego.wikia.com/api/v1/Articles/List/?category=10000_sets&offset=page|313030313920524542454c20424c4f434b4144452052554e4e4552|4358'


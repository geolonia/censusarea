/* pref 県 */
create table pref as 
select pref_name as name ,st_union(geometry) as geometry 
from allarea 
where hcode = 8101 
group by pref_name;

/* city 区のない市町村（東京23区を含む） */
create table city as 
select pref ,city ,city_name as name ,st_union(geometry) as geometry 
from allarea 
where 
hcode = 8101 and 
(substr(city_name ,length(city_name),1)<>'区' or 
(substr(city_name ,length(city_name),1)='区' and (substr(gst_name ,length(gst_name),1)='区')))
group by pref ,city ,city_name;

/* city_s 区のある市町村（東京23区は含まない） */
create table city_s as 
select pref ,substr(city,1,1) as city,gst_name as name ,st_union(geometry) as geometry 
from allarea 
where 
hcode = 8101 and 
(substr(city_name ,length(city_name),1)='区' and (substr(gst_name ,length(gst_name),1)='市'))
group by pref ,substr(city,1,1) ,gst_name;

/* city_area_sb 区を持つ市の区 */
create table city_sb as 
select pref ,city ,city_name as name ,st_union(geometry) as geometry 
from allarea 
where 
hcode = 8101 and 
(substr(city_name ,length(city_name),1)='区' and substr(gst_name ,length(gst_name),1)='市')
group by pref ,city ,city_name;

/* c_area（ビュー） H27国勢調査小地域 */
create view c_area as 
select s_name as name ,geometry 
from allarea
where hcode = 8101 ;

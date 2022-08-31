# zermelo api v:__version__
![GitHub Logo](https://ozhw.zportal.nl/static/v/21.09j64/img/zermelo2013.svg)
# documentation


## install

```properties
pip install zermeloapi
```

## how to import
```python
import zermeloapi
```
## initializing
```python
zermelo = zermeloapi.zermelo(school, username, password, teacher=False, version=3)
```
## get token
```python
token = zermelo.get_token()
```
if u wand to u can give the school username and password again but u don't need to in that case u can use `get_token(school,username,password)`
## get access token
```python
access_token = zermelo.get_access_token()
```
again if u wand to u can give the school and username again but u don't need to in that case u can use `get_access_token(school,username)`
## get raw schedule
```python
raw_schedule = zermelo.get_schedule()
```
u can give the week number and or year of u wand to else it uses the current year/week u can use `get_schedule(week=this_week)`,`get_schedule(year=this_year)`or`get_schedule(year=this_year,week=this_week)`
## get schedule
```python
raw_schedule = zermelo.get_schedule()
```
u can give the week number and or year of u wand to else it uses the current year/week u can use `get_schedule(week=this_week)`,`get_schedule(year=this_year)`or`get_schedule(year=this_year,week=this_week)`and u you can pass a rawshedule from get_raw_shedule()
## sort schedule
```python
sorted_schedule = zermelo.sort_schedule()
```
like before u can give the week and year but u can also give the schedule from [`get_schedule()`](#get-schedule) instead to sort it defaults to getting it self but if u give it uses that one u can do that by using it like this `sort_schedule(schedule)` for the week and year it is the same syntax
## readable schedule
```python
readable = zermelo.readable_schedule()
```
again u can give it week and year with the same syntax as before also you can give it a sorted schedule (output from [`sort_schedule()`](#sort-schedule)) by using `readable_schedule(sorted_schedule)`
## print schedule
```python
zermelo.print_schedule()
```
yes u can use it like this `zermelo.print_schedule(zermelo.readable_schedule())` but **WHY** if u wand that use it like that just `print(zermelo.readable_schedule())` the only use is that it defaults to `zermelo.readable_schedule()`
# [source code](https://github.com/btpv/zermeloapi)
```python
__init__.py
```
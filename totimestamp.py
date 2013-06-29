from datetime import datetime,time,date

def _time_totimestamp(time_obj):
	return (((time_obj.hour*60 + time_obj.minute)*60) + time_obj.second) + time_obj.microsecond/1000000

def _date_totimestamp(date_obj):
	return (date_obj - date(1970,1,1)).total_seconds()

def _datetime_totimestamp(datetime_obj):
	return totimestamp(datetime_obj.date()) + totimestamp(datetime_obj.time())

def totimestamp(obj):
	if type(obj) is time:
		return _time_totimestamp(obj)
	elif type(obj) is date:
		return _date_totimestamp(obj)
	elif type(obj) is datetime:
		return _datetime_totimestamp(obj)


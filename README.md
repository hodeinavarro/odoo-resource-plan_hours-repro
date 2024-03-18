We have a project which has multiple shift types, to solve this while staying as native as possible within Odoo,
we thought about creating multiple `resource.calendar` entries, and add a new `calendar_id` field linked to a `planning.role`.
Doing so allows us to create the `planning.slot.template`'s for each role (in this case, a shift), and compute the durations
with the linked calendar instead of the companys calendar.

With the given example, where a guard will start at 21:00 and end on 08:00 of the next day, the expected `end_time` and
`duration_days` are 8 and 1 respectively.

The issue is located at the `plan_hours` function from `enterprise/resource/models/resource.py`, more precisely:

```python
def plan_hours(self, hours, day_dt, compute_leaves=False, domain=None, resource=None):
	# hours: 11
	# day_dt: datetime.datetime(2024, 3, 18, 21, 0, tzinfo=<DstTzInfo 'Europe/Madrid' CET+1:00:00 STD>)
	# compute_leaves: True
	# ...
	if hours >= 0:
		delta = timedelta(days=14)
		for n in range(100):
			dt = day_dt + delta * n
			for start, stop, meta in get_intervals(dt, dt + delta)[resource_id]:
				interval_hours = (stop - start).total_seconds() / 3600
				if hours <= interval_hours:
					return revert(start + timedelta(hours=hours))
				hours -= interval_hours
		return False
```

The variable `stop` is using `999999` milliseconds, which produces the issue when `hours -= interval_hours` is evaluated

```python
# hours: 11
# interval_hours: 2.999999999722222

# hours (next loop): 8.000000000277778
# interval_hours (next loop): 8
```

Since `hours` is bigger than `interval_hours`, instead of returning `dt(2024, 3, 19, 8)`, it continues evaluating the loop until
`dt(2024, 3, 19, 21, 0, 0, 1)` is returned.

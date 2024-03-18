from datetime import datetime

from pytz import timezone

Calendar = self.env['resource.calendar']

madrid = 'Europe/Madrid'

calendar = Calendar.create({
    'name': 'Calendar',
    'tz': madrid,
    'attendance_ids': [
        (0, 0, {
                'name': 'Monday', 'dayofweek': '0', 'day_period': 'afternoon', 'hour_from': 21, 'hour_to': 24,
        }),
        (0, 0, {
                'name': 'Tuesday (Monday cont.)', 'dayofweek': '1', 'day_period': 'morning', 'hour_from': 0, 'hour_to': 8,
        }),
        (0, 0, {
                'name': 'Tuesday', 'dayofweek': '1', 'day_period': 'afternoon', 'hour_from': 21, 'hour_to': 24,
        }),
        (0, 0, {
                'name': 'Wednesday (Tuesday cont.)', 'dayofweek': '2', 'day_period': 'morning', 'hour_from': 0, 'hour_to': 8,
        }),
        (0, 0, {
                'name': 'Wednesday', 'dayofweek': '2', 'day_period': 'afternoon', 'hour_from': 21, 'hour_to': 24,
        }),
        (0, 0, {
                'name': 'Thursday (Wednesday cont.)', 'dayofweek': '3', 'day_period': 'morning', 'hour_from': 0, 'hour_to': 8,
        }),
        (0, 0, {
                'name': 'Thursday', 'dayofweek': '3', 'day_period': 'afternoon', 'hour_from': 21, 'hour_to': 24,
        }),
        (0, 0, {
                'name': 'Friday (Thursday cont.)', 'dayofweek': '4', 'day_period': 'morning', 'hour_from': 0, 'hour_to': 8,
        }),
    ]
})

tz = timezone(madrid)
dt = tz.localize(datetime(2024, 3, 18, 21))

calendar.plan_hours(11, dt, compute_leaves=True)

# Result: datetime.datetime(2024, 3, 19, 21, 0, 0, 1, tzinfo=<DstTzInfo 'Europe/Madrid' CET+1:00:00 STD>)
# Expected: datetime.datetime(2024, 3, 19, 8, 0, 0, 1, tzinfo=<DstTzInfo 'Europe/Madrid' CET+1:00:00 STD>)

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, NumberAttribute, JSONAttribute, UTCDateTimeAttribute


class Room(Model):
    class Meta:
        table_name = "Room"
        region = "us-west-2"

    roomname= UnicodeAttribute(hash_key=True)
    password = UnicodeAttribute()
    timesession=NumberAttribute()
    online=NumberAttribute()


# Room.create_table(read_capacity_units=1, write_capacity_units=1)

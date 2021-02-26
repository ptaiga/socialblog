# https://www.psycopg.org/docs/advanced.html#adapting-new-types

from psycopg2.extensions import adapt, register_adapter, AsIs

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def adapt_point(point):
    # x = adapt(point.x).getquoted()
    # y = adapt(point.y).getquoted()
    return AsIs("'(%s, %s)'" % (point.x, point.y))

register_adapter(Point, adapt_point)

# cur.execute("INSERT INTO atable (apoint) VALUES (%s)", (Point(1.23, 4.56),))

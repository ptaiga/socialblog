from math import sin, cos, acos, asin, sqrt, atan2, radians

def get_distance(lat1, lon1, lat2, lon2):
    # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    # https://en.wikipedia.org/wiki/Great-circle_distance

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # https://en.wikipedia.org/wiki/Great-circle_distance#Computational_formulas
    # https://en.wikipedia.org/wiki/Vincenty%27s_formulae
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    # https://yandex.ru/blog/mapsapi/26933
    # https://en.wikipedia.org/wiki/Great-circle_distance#Formulae
    # distance = R * acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))

    # https://en.wikipedia.org/wiki/Great-circle_distance#Computational_formulas
    # https://en.wikipedia.org/wiki/Haversine_formula
    # distance = 2 * R * asin(sqrt(sin((lat2 - lat1)/2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1)/2) ** 2))

    return distance

if __name__ == '__main__':
    lat1 = radians(52.2296756)
    lon1 = radians(21.0122287)
    lat2 = radians(52.406374)
    lon2 = radians(16.9251681)
    print("Result:", get_distance(lat1, lon1, lat2, lon2))
    print("Should be:", 278.546, "km")

    # https://yandex.ru/maps/2/saint-petersburg/?ll=30.250649%2C59.937351&mode=routes&rl=30.246171%2C59.938385~0.005161%2C0.000092&rtext=59.938390%2C30.246171~59.938477%2C30.251342&rtt=pd&ruri=~&z=16
    lat1, lon1 = radians(59.938390), radians(30.246171)
    lat2, lon2 = radians(59.938477), radians(30.251342)
    print("Result:", get_distance(lat1, lon1, lat2, lon2))
    print("Should be:", 0.288, "km")


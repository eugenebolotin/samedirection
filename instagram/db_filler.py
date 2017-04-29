from models import City

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

with open('locations.txt', 'r') as myfile:
    data=chunks(myfile.read().split('\r')[5:], 5)

for row in data:
    print row[0]
    City.create(
        rank=int(row[0]),
        city=row[1],
        country=row[2],
        tourists_millions=float(row[3]),
        ig_link=row[4]
    )
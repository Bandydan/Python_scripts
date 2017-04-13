#!/usr/bin/python2.7 -tt
#importing a library to work with MySQL
import MySQLdb

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "micecloud.settings")

current_dir = os.path.abspath(os.path.dirname(__file__))
micecloud_app_path = os.path.join(current_dir, '..', '..', 'micecloud')
sys.path.append(micecloud_app_path)

from dashboard.services.models import Service, VenuesRoom, Photo

#creating database connection
db = MySQLdb.connect('localhost', 'root', '12345', 'ean')
#creating a cursor
cursor = db.cursor()
#execute a query in the terms of cursor
cursor.execute('SELECT VERSION()')
# fetching one result from the cursor
data = cursor.fetchone()
print "Database version : %s " % data

query = " \
    SELECT \
        propertyattributelink.EANHotelID, \
        activepropertylist.Name, \
        activepropertylist.Address1, \
        propertyattributelink.PropertyDescription \
        activepropertylist.StarRating, \
        attributelist.AttributeDesc, \
        propertyattributelink.AttributeID, \
        propertyattributelink.AppendTxt \
    FROM \
        propertyattributelink \
        INNER JOIN attributelist ON propertyattributelink.AttributeID = attributelist.AttributeID \
        INNER JOIN activepropertylist ON activepropertylist.EANHotelID = propertyattributelink.EANHotelID \
        INNER JOIN propertydescriptionlist ON activepropertylist.EANHotelID = propertydescriptionlist.EANHotelID \
    WHERE \
        propertyattributelink.AttributeID IN(2593, 81, 3637) \
        AND activepropertylist.Country = 'DE' \
        AND propertyattributelink.AppendTxt <> '' \
        AND activepropertylist.StarRating >= 3.0 \
    LIMIT 5 \
"

result = []
try:
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        print row[6]
        if row[6] == 2593:
            print row[6]

        exit()
        row_data = {
            'EANId': row[0],
            'name': row[1],
            'address': row[2],
            'description': row[3],
            'rating': row[4],
            'attr_desc': row[5],
            'attr_id': row[6],
            'number_of_spaces': 0,
            'append_txt': row[7],
        }


        result.append(row_data)
    print result[3]

except:
    raise
    print "Error: unable to fetch data"

# disconnect from server
db.close()




def create_location(location_data):
    return Service.objects.create(
        category='location',
        address=createAddressFromDict(service_data['address']),
        name=service_data['service_name'],
        use_short_description=False,
        is_visible=True,
        options=getServiceOptions(service_data),
        expedia_id=service_data['expedia_id'],
    )








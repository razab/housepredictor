from extractor import sanitize_record
import psycopg2
import traceback

import datetime


class ExtractionPipeline(object):
    """Pipeline that sanitizes the items
    if the `sanitize` flag is set in the spider."""

    def track_exists(self, track_id):
        cur = self.conn.cursor()
        cur.execute("""SELECT "GlobalId" FROM items WHERE "GlobalId" ="""+str(track_id))
        return cur.fetchone() is not None


    def open_spider(self, spider):
        self.sanitize = spider.sanitize  # check the flag's state

    def process_item(self, item, spider):

        KEY_NAMES1 = [
            'AantalBadkamers',
            'AantalKamers',
            'BijdrageVVE',
            'Energielabel.Definitief',
            'Energielabel.Index',
            'Energielabel.NietBeschikbaar',
            'Energielabel.NietVerplicht',
            'ErfpachtBedrag',
            'Inhoud',
            'PerceelOppervlakte',
            'ServiceKosten',
            'SoortPlaatsing',
            'WoonOppervlakte',
            'WGS84_X',
            'WGS84_Y',
            'Koopprijs',
            'PublicatieDatum',
            'GelegenOp',
            'Bouwjaar',
            'AantalWoonlagen',
            'Aanvaarding',
            'Bouwvorm',
            'BronCode',
            'GlobalId',
            'Energielabel.Label',
            'PermanenteBewoning',
            'SchuurBerging',
            'Soort-aanbod',
            'TuinLigging',
            'Woonplaats',
            'VolledigeOmschrijving',
            'Voorzieningen',
            'GarageVoorzieningen',
            'SoortDak',
            'GarageIsolatie',
            'Ligging',
            'EigendomsSituatie',
            'SchuurBergingIsolatie',
            'Bijzonderheden',
            'BalkonDakterras',
            'WarmWater',
            'SoortWoning',
            'Verwarming',
            'Garage',
            'Isolatie',
            'SchuurBergingVoorzieningen',
            'ShortURL',
            'Plaats',
            'Postcode',
            'IsSearchable',
            'IsVerhuurd', 
            'IsVerkocht', 
            'IsVerkochtOfVerhuurd',
            'MakelaarId',
            'MakelaarNaam',
            'Adres'
            
        ]


        sanitized_item = sanitize_record(item)

        cur = self.conn.cursor()

        """ Get current date/time to track last day the item appeared in API """
        date_stamp = datetime.datetime.now().strftime(("%Y-%m-%d %H:%M"))


        """ Check if item actually exists in the database (True or False)"""
        global_id = item.get('GlobalId')
        item_exists = self.track_exists(global_id)

        """ If item exists, update its price to be the price of latest listing.
            Also, update the last day of record to current date """

        """ If item does not exist, create a new record,
            and add current date as latest date item appeared in API """
        if item_exists:
            cur.execute("""UPDATE items set "Koopprijs"='"""+str(item.get('Koopprijs'))+"""', "LastDayofRecord"='"""+date_stamp+ """' where "GlobalId"="""+str(global_id))
            self.conn.commit()
        else:    
            try:
                vals = ["'" + str(sanitized_item[x]).replace("'","") + "'" for x in KEY_NAMES1]
                vals_str_list = ["%s"] * len(vals)
                vals_str = ", ".join(vals)
                vals_str = vals_str + ", '" + date_stamp + "'"
                cur.execute("INSERT INTO items VALUES ("+vals_str+")")
                self.conn.commit()
            except:
                traceback.print_exc()
                inpt = input('c')



        cur.close()
        # sanititze or no depending on the flag
        if not self.sanitize:
            return item
        return sanitized_item

    def __init__(self):

        """ Initializes database connection
        """

        self.conn = psycopg2.connect("dbname='funda' user='postgres' host='localhost' password='funda123'")

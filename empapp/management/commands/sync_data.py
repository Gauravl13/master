from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch,helpers
import psycopg2


class Command(BaseCommand):
    help = 'Syncs data from PostgreSQL to Elasticsearch and deletes synced data from PostgreSQL'

    def handle(self, *args, **options):
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            dbname='deep',
            user='postgres',
            password='123456'
        )
        cur = conn.cursor()

        # Connect to Elasticsearch
        es = Elasticsearch('http://localhost:9200/')

        # Retrieve data from PostgreSQL
        cur.execute('SELECT * FROM empapp_employee')
        rows = cur.fetchall()
        print(rows)

        # Bulk index data into Elasticsearch
        actions = []
        for row in rows:
            data_dict = {
                '_index': 'userinformation',
                '_id': row[0],
                'emp_id':row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'mobileno': row[4],
                'gender': row[5],
                'created_at': row[6],
                'updated_at': row[7],

            }
            actions.append(data_dict)
            print(actions)

        # es.index(index='userinformation', body=data_dict,id=row[0])
        helpers.bulk(es,actions,index='userinformation')

        # Delete synced data from PostgreSQL
        cur.execute('DELETE FROM empapp_employee')
        conn.commit()

        # Close PostgreSQL connection
        cur.close()
        conn.close()

        self.stdout.write(self.style.SUCCESS('Data synced and deleted successfully'))

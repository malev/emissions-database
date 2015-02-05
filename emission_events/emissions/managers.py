from django.db import connection, models
from models import *


class EmissionQuerySet(models.QuerySet):
    def function():
        pass


class EmissionManager(models.Manager):
    def emissions_per_year_and_month(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                DATE_PART('YEAR', began_date) as Year,
                DATE_PART('MONTH', began_date) as Month,
                COUNT(*) as Entries
            FROM emissions_emissionevent
            GROUP BY Year, Month""")

        output = {}
        for row in cursor.fetchall():
            year = str(int(row[0]))
            month = str(int(row[1]))
            if year in output:
                output[year][month] = int(row[2])
            else:
                output[year] = {month: int(row[2])}
        return output

    def emissions_per_year(self, year):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT count(*)
            FROM emissions_emissionevent
            WHERE emissions_emissionevent.began_date >='%i-01-01'
            AND emissions_emissionevent.began_date <= '%i-12-31'
            """ % (year, year))
        return int(cursor.fetchall()[0][0])


    def get_queryset(self):
        type_of_emissions = [
            'air-shutdown',
            'air-startup',
            'emissions-event',
            'emissions-event-emergency-resp',
            'excess-opacity',
            'maintenance'
        ]
        return super(EmissionManager, self).\
            get_queryset().\
            filter(type_of_emission__in=type_of_emissions)


class RegulatedEntitiesManager(models.Manager):
    def ranking_per_year(self):
        cursor = connection.cursor()
        cursor.execute("""
            select
                emissions_regulatedentity.id,
                emissions_regulatedentity.name,
                emissions_regulatedentity.county,
                emissions_regulatedentity.regulated_entity_rn_number,
                emissions_regulatedentity.nearest_zipcode,
                count(*) as freq
            from emissions_emissionevent join emissions_regulatedentity
            ON (emissions_regulatedentity.regulated_entity_rn_number = emissions_emissionevent.regulated_entity_rn_number)
            WHERE emissions_emissionevent.type_of_emission in (
              'air-shutdown',
              'air-startup',
              'emissions-event',
              'emissions-event-emergency-resp',
              'excess-opacity',
              'maintenance'
            )
            AND began_date >= '2015-01-01'
            group by
                emissions_regulatedentity.id,
                emissions_regulatedentity.name,
                emissions_regulatedentity.regulated_entity_rn_number,
                emissions_regulatedentity.county
            order by freq DESC
            limit 10""")
        result_list = []
        for row in cursor.fetchall():
            p = self.model(
                id=row[0],
                name=row[1],
                county=row[2],
                regulated_entity_rn_number=row[3],
                nearest_zipcode=row[4])
            p.num_events = row[5]
            result_list.append(p)

        return result_list

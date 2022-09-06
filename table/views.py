from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
import datetime
from table.models import event
import arrow

# Create your views here.

class Index(ListView, HttpResponse):
    model = event
    template_name = 'table/index.html'

    def __str__(self):
        return "Table.Index CBV"

    def get(self, request, *args, **kwargs):
        # #  what a bizarre construction
        #
        # end = datetime.datetime.today() + datetime.timedelta(weeks=52)
        # delta = end - start
        # dates = []
        # weeks = []
        #
        # #  roll back to the previous monday
        # start = start - datetime.timedelta(days=start.weekday())  - datetime.timedelta(days=1)
        #
        # for d in range(delta.days + 1):
        #     date = start + datetime.timedelta(days=d)
        #     #
        #     #
        #     #
        #     #
        #     # if date.day == 1 and date.month == 1:
        #     #         dates.append(date.strftime('%d %b %Y'))
        #     # elif date.day == 1:
        #     #         dates.append(date.strftime('%d %b %y'))
        #     # else:
        #     dates.append(date.strftime('%d %b %y'))
        #
        #     if d % 7 == 0:
        #         weeks.append(dates)
        #         dates = []
        # weeks = weeks[1:]

        # force the database seed
        # event.objects.all().delete()
        # self.seed()  # it's pretty quick - can leave this here all the time, I reckon
        display_start = datetime.datetime.now()  # +  datetime.timedelta(days=7)
        # wind back to a Monday
        while display_start.weekday() != 0:
            display_start = display_start - datetime.timedelta(days=1)
        # display_start = display_start - datetime.timedelta(days=(6 - display_start.weekday()))


        # events = event.objects.all()
        events = event.objects.filter(Q(start_date__gte=display_start)).order_by('start_date', 'render_type',  )
        context = { 'events': events }
        return render(request, 'table/index.html', context)

    def seed(self):

        ''' Here, the idea is to make sure the database of events has a
        full year of events(type=10:'date') in advance
        To be called on a maintenance schedule
        '''

        # get the last date in the database
        # if it is less than a year away, add enough dates to make it over a year
        # if it is more than a year away, do nothing

        # get the last date in the database (first one in a descending order of start date)
        last_record = event.objects.filter(render_type=10).order_by('-start_date').first()

        last_date = arrow.utcnow()
        if last_record is not None and last_record.start_date is not None:
            last_date = arrow.get(last_record.start_date)

        # if it is less than a year away, add a year's worth of dates
        # being deliberately generous with the definition of year
        rightnow = arrow.get(datetime.datetime.utcnow())
        rightnow = rightnow - datetime.timedelta(weeks=2)

        #      TODO : make sure generation finishes on a Sunday!

        year_from_now = rightnow.shift(weeks=60)
        if last_date < year_from_now:
            # add up to ~year's worth of dates
            # Wind forward to a sunday
            while year_from_now.weekday() != 6:
                year_from_now = year_from_now + datetime.timedelta(days=1)
            delta = year_from_now - last_date
            days = [rightnow.shift(days=i) for i in range(delta.days + 1)]
            for day in days:
                e = event()
                e.start_date = day.datetime.date()
                e.end_date = day.datetime.date()
                e.name = 'date entry'
                e.render_type = 10

                e.week = day.strftime('%V')
                date_exists_in_table = event.objects.filter(start_date=e.start_date, render_type=10).first()
                if date_exists_in_table is None:
                    e.save()
        else:
            # do nothing
            pass
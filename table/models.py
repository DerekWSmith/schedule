
from django.db import models



# Create your models here.


class event(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(default='', null=True, blank=True)

    '''
    So the type is used like this:
    The event table should contain one 'event' - type 'date' for every date in the calendar
    We then add 'real' events to the event table.
    Getting all objects in start date order then, return something like this:
    Start date  TYPE        Description
    2022-01-01  date         
    2022-01-01  normal      Appointment with Dr. Smith
    2022-01-01  normal      Appointment with Dr. Jones  
    2022-01-02  date        
    2022-01-02  normal      Public holiday
    2022-01-02  normal      Attend foot clinic
    2022-01-02  normal      Attend ankle clinic
    2022-01-02  normal      Work your way up to the knee clinic
    
    This means at rendering time, we can just iterate through the list and render the date (when the type is date) 
    and all other events types  with the same date are content : they are appointments on that date
    
    
    NOTE: The types that follow are rendering flags - they indicate hoe the renderer sould treat these.
    The types are not user-used or user-useful information
    Ordering by render type makes perfect sense - we want to render the date first, then the appointments, then the holidays, etc.
    '''
    EVENT_RENDER_TYPE = (
        (10, 'date'),  # in essence, this is the header
        (30, 'public holiday'),
        (50, 'all day'),
        (70, 'default'),
    )

    render_type = models.IntegerField(choices=EVENT_RENDER_TYPE, null=True, blank=True)

    start = models.DateTimeField()
    # the following field is calculated on save
    week = models.CharField(max_length=2, null=True, blank=True)
    end = models.DateTimeField()
    # duration = models.DurationField()  # calculable

    location = models.CharField(max_length=100, default='none', null=True, blank=True)
    address = models.CharField(max_length=100, default='none', null=True, blank=True)
    resource = models.CharField(max_length=100, default='none', null=True, blank=True)

    # the following allow for 'repeat every 1 hour, repeat every 3 weeks, repeat every 10 years' etc
    # and one day, I might implement it. But not today.
    repeat_every = models.IntegerField(default=0, null=True, blank=True)  # eg repeat every 7 (and then the unit Day) means weekly
    repeat_unit = models.TextChoices('repeat', 'Hour Day Week Month Year' )

    # paticularly repeating items - since they are not entered manually, they could be overlooked
    # this is the hook for an alerting system
    alert_options = models.CharField(max_length=100, default='none', null=True,
                                     blank=True)  # just a barebones of an idea for now

    # the following allow for sequncing of events - and one day, I might even implement this
    dependant_upon = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                       related_name="eventdependson")
    required_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name="eventrequiredby")

    class Meta:
        db_table = 'event'
        ordering = ['start', 'render_type']

    def __str__(self):
        if self.name:
            return self.name
        return ''

    def get_units(self):
        if self.repeat_every > 1:
            return self.repeat_unit._value_ + 's'
        else:
            return self.repeat_unit._value_

    def get_duration(self):
        if self.end and self.start:
            return self.end - self.start

    def get_week(self):
        ''' This is a class method
        It returns the week number that the self.start date is in
        '''
        return self.start.strftime("%V")

    # overide the save method, calulating week
    # so we can later groupby / orderby week when reading the events from database
    # def save(self, *args, **kwargs):
    #     if not self.week :
    #         if self.start:
    #             self.week = self.start.strftime("%V")
    #     super(event, self).save(*args, **kwargs)


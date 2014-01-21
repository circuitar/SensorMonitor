from django.db import models


class SensorType(models.Model):
    name = models.CharField(max_length=100)
    code = models.SlugField(max_length=50)
    min_value = models.FloatField()
    max_value = models.FloatField()
    units = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Sensor Type'
        verbose_name_plural = 'Sensor Types'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class SensorData(models.Model):
    value = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(SensorType, related_name='data')

    class Meta:
        verbose_name = 'Sensor Data'
        verbose_name_plural = 'Sensor Data'
        ordering = ['-time']

    def __unicode__(self):
        return u'%s - %s - %.5f' % (self.time, self.type, self.value)

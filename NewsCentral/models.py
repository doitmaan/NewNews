from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


# Create your models here.


class STOCK(models.Model):
    stockId = models.CharField(max_length=5000, primary_key=True, unique=True)
    LastSearched = models.DateTimeField(auto_now=True)  # every time it is saved

    def __str__(self):
        """A string representation of the model."""
        return str(self.stockId)


class LINK(models.Model):
    auto_increment_id = models.AutoField(primary_key=True, null=False)
    stcok = models.ForeignKey(STOCK, related_name='LinksUrls', on_delete=models.CASCADE)
    linkUrl = models.URLField(default='', unique=True, max_length=1000)
    publish_date = models.DateTimeField(blank=True, null=True)
    added_date = models.DateTimeField(auto_now=True)
    imageLinkUrl = models.URLField(default='', max_length=1000)
    title = models.TextField(default='')

    def __str__(self):
        """A string representation of the model."""
        return str(self.stcok)

    class Meta:
        # ensures unique combination, prevents duplicate 'restaurants'
        unique_together = ((
                               'stcok',
                               'linkUrl'
                           ),)


class TEXTARTIC(models.Model):
    id = models.AutoField(primary_key=True)
    stcokId = models.ForeignKey(STOCK, on_delete=models.CASCADE)
    textArticle = models.TextField()
    added_date = models.DateField(default=timezone.now)

    def __str__(self):
        """A string representation of the model."""
        return self.id


class HIST(models.Model):
    stcokId = models.ForeignKey(STOCK, on_delete=models.CASCADE)
    histogram = JSONField()
    added_date = models.DateField(default=timezone.now)

    def __str__(self):
        """A string representation of the model."""
        return str(self.stcokId) + " " + str(self.added_date)
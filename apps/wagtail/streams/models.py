from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class ReviewFamily(models.Model):
    
    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Review Family")
        verbose_name_plural = _("Review Families")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ReviewFamily_detail", kwargs={"pk": self.pk})

class ReviewPlatform(models.Model):

    name = models.CharField(_("Name"), max_length=50) 
    score = models.FloatField("Score", blank=True, null=True)
    link = models.URLField(_("Link"), max_length=1024, blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    star_icon = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("ReviewPaltform")
        verbose_name_plural = _("ReviewPaltforms")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ReviewPaltform_detail", kwargs={"pk": self.pk})


class Review(models.Model):

    family = models.ManyToManyField("streams.ReviewFamily")
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True)
    platform = models.ForeignKey("streams.ReviewPlatform", on_delete=models.SET_NULL, null=True)
    review = models.TextField(_("Review"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return self.review

    def get_absolute_url(self):
        return reverse("Review_detail", kwargs={"pk": self.pk})
        
    def get_families(self):
        return "\n".join([p.name for p in self.family.all()])

class Colour(models.Model):

    name = models.CharField(max_length=32) 
    hex_code = models.CharField(max_length=6)

    class Meta:
        verbose_name = _("Colour")
        verbose_name_plural = _("Colours")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Colour_detail", kwargs={"pk": self.pk})

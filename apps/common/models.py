from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class District(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    soato = models.CharField(max_length=255, verbose_name=_("soato"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
        db_table = "districts"


class Region(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_("district"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

from django.db import models
from django.utils.translation import gettext_lazy as _


class CaptionedFile(models.Model):
    caption = models.CharField(max_length=200, verbose_name=_('caption'))
    publication = models.FileField(upload_to='captioned-files', verbose_name=_('Uploaded File'))

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = _('Captioned File')
        verbose_name_plural = _('Captioned Files')


class UncaptionedFile(models.Model):
    publication = models.FileField(upload_to='uncaptioned-files', verbose_name=_('Uploaded File'))

    def __str__(self):
        return self.publication.name

    class Meta:
        verbose_name = _('Uncaptioned File')
        verbose_name_plural = _('Uncaptioned Files')

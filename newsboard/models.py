from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import CharBlock, RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index

from authentication.models import User


# Create your models here.
class NewsIndexPage(Page):
    introduction = models.CharField(max_length=250, blank=False, null=False)

    content_panels = Page.content_panels + [
        FieldPanel('introduction')
    ]
    subpage_types = ['newsboard.NewsPage']
    parent_page_types = ['home.HomePage']


class NewsPage(Page):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    main_title = models.CharField(max_length=200, blank=False)
    introduction = models.CharField(max_length=250, blank=False)
    body = StreamField([
        ('heading', CharBlock()),
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True)
    date_published = models.DateTimeField(auto_now_add=True)

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('main_title'),
        FieldPanel('introduction'),
        FieldPanel('body'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('main_title'),
        index.SearchField('introduction'),
        index.SearchField('body'),
        index.SearchField('author'),
    ]

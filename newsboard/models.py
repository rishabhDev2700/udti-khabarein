from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import CharBlock, RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index

from authentication.models import User


# Create your models here.
class NewsTag(TaggedItemBase):
    content_object = ParentalKey(
        'NewsPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class NewsIndexPage(Page):
    introduction = models.CharField(max_length=250, blank=False, null=False)

    content_panels = Page.content_panels + [
        FieldPanel('introduction')
    ]
    subpage_types = ['newsboard.NewsPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = NewsPage.objects.live().public().order_by('-date_published')

        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            print(tags)
            all_posts = all_posts.filter(tags__slug__in=[tags])
            print(all_posts)

        context["posts"] = all_posts
        return context


class NewsPage(Page):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    main_title = models.CharField(max_length=200, blank=False)
    cover = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
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
        FieldPanel('cover'),
        FieldPanel('introduction'),
        FieldPanel('body'),
        FieldPanel('tags'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('main_title'),
        index.SearchField('introduction'),
        index.SearchField('body'),
        index.SearchField('author'),
    ]

    tags = ClusterTaggableManager(through=NewsTag, blank=True)

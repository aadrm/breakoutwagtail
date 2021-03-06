"""flexible page"""
from django.db import models

from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from apps.wagtail.home.models import MyPage
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from apps.wagtail.streams import blocks

class FlexPage(MyPage):
    """Flexible page class""" 

    template = "flex/flex_page.html"

    # header_image = models.ForeignKey(
    #     "wagtailimages.Image", 
    #     null=True,
    #     blank=True,
    #     verbose_name=_("Header Image"), 
    #     on_delete=models.SET_NULL,
    #     related_name="+",
    # )

    content = StreamField(
        [
            ('section', blocks.SectionBlock()),
            ('banner', blocks.ImgBannerSeparator()),
        ],
        null=True,
        blank=True,
    )

    content_panels = MyPage.content_panels + [
        StreamFieldPanel("content"),
    ]


    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"


class InfoPage(MyPage):
    """Info page class"""
    template = "flex/info_page.html"

    # header_image = models.ForeignKey(
    #     "wagtailimages.Image", 
    #     null=True,
    #     blank=True,
    #     verbose_name=_("Banner Image"), 
    #     on_delete=models.SET_NULL,
    #     related_name="+",
    #     help_text="limit the file size to 200kb, recommended dimensions 1200x500",
    # )

    is_numbered = models.BooleanField(_("Enumerate Paragraphs"), default=False)

    content = StreamField(
        [
            ("info_paragraph", blocks.InfoParagraphBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = MyPage.content_panels + [
        FieldPanel('is_numbered'),
        StreamFieldPanel('content'),

    ]

    class Meta:
        verbose_name = "Info Page"
        verbose_name_plural = "Info Pages"


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(WagtailCaptchaEmailForm, MyPage):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content = StreamField(
        [
            ('section', blocks.SectionBlock()),
            ('banner', blocks.ImgBannerSeparator()),
        ],
        null=True,
        blank=True,
    )


    content_2 = StreamField(
        [
            ('section', blocks.SectionBlock()),
            ('banner', blocks.ImgBannerSeparator()),
        ],
        null=True,
        blank=True,
    )

    submitted_title = models.CharField('submitted title', max_length=50, blank=True, null=True)
    submitted_text = RichTextField(blank=True)

    landing_page_template = 'flex/form_page.html'

    content_panels = AbstractEmailForm.content_panels + [
        # FormSubmissionsPanel(),
        ImageChooserPanel('header_image'),
        StreamFieldPanel('content'),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        StreamFieldPanel('content_2'),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
        FieldPanel('submitted_title'),
        FieldPanel('submitted_text'),
    ]

    promote_panels = MyPage.promote_panels

    def get_context(self, request):
        context = super().get_context(request)
        fields = self.get_form_fields()
        print(fields)
        return context


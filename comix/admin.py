from django.contrib import admin

# Register your models here.
from comix.models import Genre, Issue, Series, Publisher, Tag

admin.site.register(Genre)
admin.site.register(Series)
admin.site.register(Publisher)
admin.site.register(Tag)


admin.site.site_header = "RTS Comics Admin"
admin.site.site_title = "RTS Comics Admin"

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('gcd_id',
        'catalog_id',
        'gcd_series',
        'in_gcd_flag',
        'volume',
        'number',
        'issue_text',
        'edition',
        'publication_date',
        'gcd_notes',
        'notes',
        'grade',
        'grade_notes',
        'cover_image',
        'image_scanned',
        'indicia_date',
        'inserts',
        'scarcity_notes',
        'added_date',
        'genre',
        'price',
        'quantity',
        'status',
        'sold_date')
    list_filter = ('number',)
    search_fields = ('catalog_id',)
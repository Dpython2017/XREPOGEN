from django.contrib import admin
from .models import Student, Marks
# Register your models here.


class MarksAdmin(admin.ModelAdmin):
    list_display = ("id","student","m_sc","lang","lit","hindi","ssc","maths","gsc","computer",
                    "gk","drawing","writing","recite","reading","story_telling")
    search_fields = ("student",)
    list_filter = ("student",)
    list_display_links = ("id",)
    list_per_page = 100
    list_editable = ("student","m_sc","lang","lit","hindi","ssc","maths","gsc","computer",
                    "gk","drawing","writing","recite","reading","story_telling")


admin.site.register(Student)
admin.site.register(Marks,MarksAdmin)
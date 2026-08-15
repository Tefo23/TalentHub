from django.contrib import admin

from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "employer",
        "employment_type",
        "status",
        "deadline",
        "created_at",
    )

    list_filter = (
        "status",
        "employment_type",
    )

    search_fields = (
        "title",
        "employer__company_name",
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "job",
        "candidate",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "job__title",
        "candidate__profile__user__username",
    )
from django.contrib import admin

from .models import Location, Spot, Plan, Report, Fav, Comment


class LocationInline(admin.TabularInline):
    model = Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'p_name', 'p_code', 'm_name', 'm_code')


class SpotInline(admin.StackedInline):
    model = Spot
    extra = 1


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_plan', 'created_at')

    def get_plan(self, obj):
        return obj.plan.name


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'duration', 'created_at')

    inlines = [SpotInline]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_plan', 'get_username', 'created_at')

    def get_plan(self, obj):
        return obj.plan.name

    def get_username(self, obj):
        return obj.user.username


@admin.register(Fav)
class FavAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_username', 'get_plan_name', 'created_at')

    def get_username(self, obj):
        return obj.user.username

    def get_plan_name(self, obj):
        return obj.plan.name


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_username', 'get_plan_name', 'text', 'created_at')

    def get_username(self, obj):
        return obj.user.username

    def get_plan_name(self, obj):
        return obj.plan.name

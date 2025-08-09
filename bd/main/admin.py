from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from main.core.infrastructure.persistence.database.models.bd import BD
from main.core.infrastructure.persistence.database.models.book import Book
from main.core.infrastructure.persistence.database.models.collection import Collection
from main.core.infrastructure.persistence.database.models.profile import Profile
from main.core.infrastructure.persistence.database.models.user import AppUser


@admin.register(BD)
class BDAdmin(admin.ModelAdmin):
    list_display = (
        'album', 'series', 'number', 'writer', 'illustrator', 'publisher',
        'publication_date', 'rating', 'collection_link', 'cover_preview'
    )
    search_fields = ('album', 'series', 'writer', 'illustrator', 'publisher')
    list_filter = ('publication_date', 'deluxe_edition', 'collection__title')
    list_select_related = ('collection',)
    readonly_fields = ('cover_preview',)

    def cover_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px;"/>', obj.image)
        return "-"
    cover_preview.short_description = "Aperçu couverture"

    def collection_link(self, obj):
        return format_html('<a href="/admin/main/collection/{}/change/">{}</a>', obj.collection.id, obj.collection.title)
    collection_link.short_description = "Collection"

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'writer', 'translator', 'publisher', 'collection',
        'style', 'origin_language', 'publication_date', 'collection_link', 'cover_preview'
    )
    search_fields = ('title', 'writer', 'publisher', 'style', 'origin_language', 'collection__title')
    list_filter = ('publication_date', 'collection__title')
    list_select_related = ('collection',)
    readonly_fields = ('cover_preview',)

    def cover_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px;"/>', obj.image)
        return "-"
    cover_preview.short_description = "Aperçu couverture"

    def collection_link(self, obj):
        return format_html(
            '<a href="/admin/main/collection/{}/change/">{}</a>',
            obj.collection.id,
            obj.collection.title
        )
    collection_link.short_description = "Collection"

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'doc_id', 'sheet_name', 'profile', 'token', 'account_count')
    search_fields = ('title', 'doc_id')
    filter_horizontal = ('accounts',)
    list_select_related = ('profile',)

    def account_count(self, obj):
        return obj.accounts.count()
    account_count.short_description = "Utilisateurs liés"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ('username', 'email', 'is_staff', 'current_collection')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'current_collection')
    fieldsets = (
        ("Infos de connexion", {"fields": ("username", "password")}),
        ("Infos personnelles", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Relations", {"fields": ("current_collection",)}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

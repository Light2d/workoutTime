from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TeamMember, LastEvent, CustomUser, Article, SportGround, SportGroundImage, Event, LastEventImage, Notification
from forum.models import ForumThread, ForumPost
from django.utils.html import format_html


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'full_name', 'email', 'birth_date', 'is_active', 'is_staff', 'date_joined', 'activation_code']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'full_name', 'email']
    ordering = ['date_joined']

    fieldsets = (
        (None, {
            'fields': ('username', 'full_name', 'email', 'password')
        }),
        ('Personal info', {
            'fields': ('birth_date', 'profile_photo')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Activation', {
            'fields': ('activation_code',)  # Добавляем поле для активации
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'email', 'password1', 'password2', 'birth_date', 'activation_code')
        }),
    )

    readonly_fields = ('activation_code',)  # Сделаем код активации только для чтения

    filter_horizontal = ('groups', 'user_permissions')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience', 'photo_preview')
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" style="height: 50px;"/>'
        return "Нет изображения"
    photo_preview.allow_tags = True
    photo_preview.short_description = "Превью фото"
    
class LastEventImageInline(admin.TabularInline):  
    model = LastEventImage
    extra = 1  # Кол-во пустых форм для добавления новых изображений
    fields = ['image']  # только поле image для отображения

@admin.register(LastEvent)  # Регистрация только один раз
class LastEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date', 'photo_preview')  # Добавлен метод preview
    ordering = ('-date',)  # Сортировка по дате (по убыванию)
    search_fields = ('title',)  # Поиск по названию
    inlines = [LastEventImageInline]  # Вставка изображений в форме

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height: 50px;"/>', obj.photo.url)
        return "Нет изображения"
    photo_preview.short_description = "Превью фото"
    
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    ordering = ('-date',)
    search_fields = ('title', 'description')
    
admin.site.register(CustomUser, CustomUserAdmin)

class SportGroundImageInline(admin.TabularInline):
    model = SportGroundImage
    extra = 1  

@admin.register(SportGround)
class SportGroundAdmin(admin.ModelAdmin):
    inlines = [SportGroundImageInline]
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'event_type')
    search_fields = ('title',)
    list_filter = ('event_type',)
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'is_read', 'created_at', 'mark_as_read_button')
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
    ordering = ('-created_at',)

    # Добавим кнопку для пометки уведомления как прочитанное
    def mark_as_read_button(self, obj):
        if not obj.is_read:
            return format_html(
                '<a class="button" href="{}">Отметить как прочитанное</a>',
                f'/admin/your_app/notification/{obj.pk}/mark_as_read/'
            )
        return "Прочитано"
    mark_as_read_button.short_description = "Статус"

    # Разрешим редактирование только определённых полей
    readonly_fields = ('recipient', 'message', 'is_read', 'created_at')
    
    
class ForumPostInline(admin.TabularInline):
    model = ForumPost
    extra = 1
    fields = ('author', 'content', 'parent', 'created_at')
    readonly_fields = ('created_at',)
    
@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)
    inlines = [ForumPostInline]

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'thread', 'parent', 'created_at')
    search_fields = ('content', 'author__username')
    list_filter = ('created_at', 'thread')

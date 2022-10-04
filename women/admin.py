from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published') # вместо photo, пишем get_html_photo
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update') # порядок и список редактируемых полей, который следует отображать в форме редактирования
    readonly_fields = ('time_create', 'time_update', 'get_html_photo') # добавим нередактируемые поля с данными из модели. Только после этой строки мы можем добавить их для отображения в панели, в поле fields

    def get_html_photo(self, object):   # делаем возврат html кода в виде миниатюры вместо ссылки на фото в админке. Параметр object будет ссылаться на текущую запись списка
        if object.photo: #не у всех объектов есть фото, поэтому, чтобы исключить возникновение ошибки при обработки запроса...
            return mark_safe(f"<img src='{object.photo.url}' width=50>") # обращаемся к объекту women и у него есть атрибут photo и взять url изображения. Функция mark_safe позволяет избежать экранирования тэгов

    get_html_photo.short_description = 'Миниатюра'

    save_on_top = True #добавим меню редактирования записью в топе

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ('name',)}

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = "Админ-панель сайта о женщинах"  # переопределяем title
admin.site.site_header = "Админ-панель сайта о женщинах - 2"   # переопределяем header

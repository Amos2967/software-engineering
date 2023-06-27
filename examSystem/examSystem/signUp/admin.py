from django.contrib import admin

# Register your models here.
from .models import Student, Teacher, Paper, Question, ExamPlace, Grade

admin.site.site_header = '英语四六级报考系统后台'
admin.site.site_title = '英语四六级报考系统'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # 要显示哪些信息
    list_display = ('id', 'name', 'sex', 'school', 'dept', 'major', 'password', 'email', 'birth', 'f_score', 's_score')
    list_display_links = ('id', 'name')  # 点击哪些信息可以进入编辑页面
    search_fields = ['name', 'dept', 'major', 'birth']  # 指定要搜索的字段，将会出现一个搜索框让管理员搜索关键词
    list_filter = ['name', 'dept', 'major', 'birth']  # 指定列表过滤器，右边将会出现一个快捷的过滤选项


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sex', 'dept', 'password', 'email', 'birth')
    list_display_links = ('id', 'name')
    search_fields = ['name', 'dept', 'birth']
    list_filter = ['name', 'dept']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'optionA', 'optionB', 'optionC', 'optionD', 'answer', 'level', 'score')


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('id', 'tid', 'type')


@admin.register(ExamPlace)
class ExamPlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'number', 'entry_number', 'pid', )


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('sid', 'pid', 'type', 'grade',)
    list_display_links = ('sid', 'grade')

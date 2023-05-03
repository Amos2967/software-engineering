from django.db import models

# Create your models here.

# 为性别,学院 指定备选字段
SEX = (
    ('男', '男'),
    ('女', '女'),
)
DEPT = (
    ('计算机与通信学院', '计算机与通信学院'),
    ('电气与自动化学院', '电气与自动化学院'),
    ('外国语学院', '外国语学院'),
    ('理学院', '理学院'),
)
EXAM_TYPE = (
    ('CET4', 'CET4'),
    ('CET6', 'CET6'),
)


# 学生表
class Student(models.Model):
    id = models.CharField('学号', max_length=20, primary_key=True)
    name = models.CharField('姓名', max_length=20)
    sex = models.CharField('性别', max_length=4, choices=SEX, default='男')
    school = models.CharField("在读学校", max_length=128, null=True)
    dept = models.CharField('学院', max_length=20, choices=DEPT, default=None)
    major = models.CharField('专业', max_length=20, default=None)
    password = models.CharField('密码', max_length=20, default='123456')
    email = models.EmailField('邮箱', default=None)
    birth = models.DateField('出生日期')
    f_score = models.IntegerField("四级成绩", default=0)
    s_score = models.IntegerField("六级成绩", default=0)

    class Meta:
        db_table = 'student'
        verbose_name = '学生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 教师表
class Teacher(models.Model):
    id = models.CharField("教工号", max_length=20, primary_key=True)
    name = models.CharField('姓名', max_length=20)
    sex = models.CharField('性别', max_length=4, choices=SEX, default='男')
    dept = models.CharField('学院', max_length=20, choices=DEPT, default=None)
    email = models.EmailField('邮箱', default=None)
    password = models.CharField('密码', max_length=20, default='000000')
    birth = models.DateField('出生日期')

    class Meta:
        db_table = 'teacher'
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Question(models.Model):
    ANSWER = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    LEVEL = {
        ('1', 'easy'),
        ('2', 'general'),
        ('3', 'difficult'),
    }
    id = models.AutoField(primary_key=True)
    title = models.TextField('题目')
    optionA = models.CharField('A选项', max_length=30)
    optionB = models.CharField('B选项', max_length=30)
    optionC = models.CharField('C选项', max_length=30)
    optionD = models.CharField('D选项', max_length=30)
    answer = models.CharField('答案', max_length=10, choices=ANSWER)
    level = models.CharField('等级', max_length=10, choices=LEVEL)
    score = models.IntegerField('分数', default=1)

    class Meta:
        db_table = 'question'
        verbose_name = '单项选择题库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<%s:%s>' % (self.id, self.title)


class Paper(models.Model):
    id = models.CharField(verbose_name="试卷编号", max_length=10, primary_key=True)
    type = models.CharField("试卷类别", max_length=128, choices=EXAM_TYPE, default='CET4')
    qid = models.ManyToManyField(Question)  # 试卷编号和题号是多对多关系
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # 添加外键

    class Meta:
        db_table = 'paper'
        verbose_name = '试卷'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 考点信息表
class ExamPlace(models.Model):
    id = models.CharField("考点编号", max_length=20, primary_key=True)
    type = models.CharField("试卷类别", max_length=128, choices=EXAM_TYPE, default='CET4')
    name = models.CharField("考点名称", max_length=128)
    number = models.IntegerField("总体容量")
    entry_number = models.IntegerField(verbose_name="已报名数量", default=0)
    time = models.DateTimeField(default=0)
    # 添加外键,关联置空，因为试卷没了但考场还在，试卷注明是四级还是六级
    pid = models.ForeignKey(Paper, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'exam_place'
        verbose_name = '考点'
        verbose_name_plural = verbose_name


# 不同考试场次会有不同的成绩记录
class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Student, on_delete=models.CASCADE, default='')  # 添加外键
    pid = models.ForeignKey(ExamPlace, on_delete=models.CASCADE, default='')  # 添加外键
    type = models.CharField("考试类别", max_length=128, choices=EXAM_TYPE, default='CET4')
    grade = models.IntegerField(default=-1)

    def __str__(self):
        return '<%s:%s:%s>' % (self.sid, self.type, self.grade)

    class Meta:
        db_table = 'grade'
        verbose_name = '成绩'
        verbose_name_plural = verbose_name




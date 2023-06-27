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
ID_TYPE = (
    ('中华人民共和国居民身份证', '中华人民共和国居民身份证'),
    ('港澳居民来往内地通行证', '港澳居民来往内地通行证'),
    ('台湾居民来往大陆通行证', '台湾居民来往大陆通行证'),
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
    ID_type = models.CharField('证件类型', max_length=20, choices=ID_TYPE, default='中华人民共和国居民身份证')
    ID_NO = models.CharField('证据号码', max_length=20, default=None)
    degree = models.CharField('学历', max_length=20, default=None)
    notes = models.CharField('备注', max_length=20, default=None)

    # 現在的工作是跳转和增加条目

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
    score = models.IntegerField('分数', default=2)

    class Meta:
        db_table = 'question'
        verbose_name = '单项选择题库'
        verbose_name_plural = verbose_name


class SubQuestion(models.Model):
    LEVEL = {
        ('1', 'easy'),
        ('2', 'general'),
        ('3', 'difficult'),
    }
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.id)

    title = models.TextField('题目')
    level = models.CharField('等级', max_length=10, choices=LEVEL)
    totalScore = models.IntegerField('总分', default=10)

    class Meta:
        db_table = 'subQuestion'
        verbose_name = '主观题库'
        verbose_name_plural = verbose_name


class StuSubQues(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Student, on_delete=models.CASCADE, default='')  # 添加外键
    sqid = models.ForeignKey(SubQuestion, on_delete=models.CASCADE, default='')  # 添加外键
    answer = models.CharField('学生答案', max_length=300, default='None')
    score = models.IntegerField('学生得分', default=0)

    class Meta:
        db_table = 'StuSubQues'
        verbose_name = '学生所答主观题'
        verbose_name_plural = verbose_name


class Paper(models.Model):
    id = models.CharField(verbose_name="试卷编号", max_length=10, primary_key=True)
    type = models.CharField("试卷类别", max_length=128, choices=EXAM_TYPE, default='CET4')
    qid = models.ManyToManyField(Question)  # 试卷编号和客观题号是多对多关系
    sqid = models.ManyToManyField(SubQuestion)  # 试卷编号和主观题号是多对多关系
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
    Ispay = models.CharField("支付状态", max_length=20, default='0')
    # '0'是没缴费，‘1’是缴费
    # 不该加到这里，支付状态应该是学生和考试表的一个级联，我们先加，看看能不能正常显示
    # 需要新建一个视图而不是表，目前看起来没问题，只需要给一个默认值
    # 但是在管理员add的html找不到相关信息。。。。。绝了

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
    type = models.CharField("考试类别", max_length=129, choices=EXAM_TYPE, default='CET4')
    grade = models.IntegerField(default=-1)
    objectGrade = models.IntegerField(default=-1)
    subjectGrade = models.IntegerField(default=-1)

    def __str__(self):
        return '<%s:%s:%s>' % (self.sid, self.type, self.grade)

    class Meta:
        db_table = 'grade'
        verbose_name = '成绩'
        verbose_name_plural = verbose_name

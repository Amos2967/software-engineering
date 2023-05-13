from django.shortcuts import render, redirect
from django.template import RequestContext
from signUp import models
from .forms import SignUpForm

 
# Create your views here.

# 报考系统首页
def index(request):
    return render(request, 'index.html')


# 学生登陆 视图函数
def studentLogin(request):
    if request.method == 'POST':
        # 获取表单信息
        stuId = request.POST.get('id')
        password = request.POST.get('password')
        print("id", stuId, "password", password)
        # 通过学号获取该学生实体
        student = models.Student.objects.get(id=stuId)
        print(student)
        if password == student.password:  # 登录成功
            # 查询考点信息
            place = models.ExamPlace.objects.all().order_by("time")
            # 查询成绩信息
            grade = models.Grade.objects.filter(sid=student.id)
            # 查询考试信息（exam是有报名的place)
            grade_pid = []
            for i in range(len(grade)):
                grade_pid.append(grade[i].pid)
            # __in表示数据库中的in操作符，等价于id in grade_pid
            exam = models.ExamPlace.objects.filter(id__in=grade_pid)
            # 渲染index模板
            return render(request, 'index.html', {'student': student, 'place': place, 'exam': exam, 'grade': grade})

        else:
            return render(request, 'index.html', {'message': '密码不正确'})


# 教师登陆 视图函数
def teacherLogin(request):
    if request.method == 'POST':
        teaId = request.POST.get('id')
        password = request.POST.get('password')
        teacher = models.Teacher.objects.get(id=teaId)
        print(teaId)
        if password == teacher.password:  # 登录成功
            # 实现成绩统计功能
            # 在试卷表 paper 找到该老师发布的试题
            paper = models.Paper.objects.filter(tid=teaId)

            data1 = models.Grade.objects.filter(type='CET4', grade__lt=360).count()
            data2 = models.Grade.objects.filter(type='CET4', grade__gte=360, grade__lt=425).count()
            data3 = models.Grade.objects.filter(type='CET4', grade__gte=425, grade__lt=500).count()
            data4 = models.Grade.objects.filter(type='CET4', grade__gte=500, grade__lt=600).count()
            data5 = models.Grade.objects.filter(type='CET4', grade__gte=600).count()

            data6 = models.Grade.objects.filter(type='CET6', grade__lt=360).count()
            data7 = models.Grade.objects.filter(type='CET6', grade__gte=360, grade__lt=425).count()
            data8 = models.Grade.objects.filter(type='CET6', grade__gte=425, grade__lt=500).count()
            data9 = models.Grade.objects.filter(type='CET6', grade__gte=500, grade__lt=600).count()
            data10 = models.Grade.objects.filter(type='CET6', grade__gte=600).count()

            data_1 = {'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4, 'data5': data5}
            data_2 = {'data6': data6, 'data7': data7, 'data8': data8, 'data9': data9, 'data10': data10}

            print("数量：", data2)
            return render(request, 'teacher.html',
                          {'teacher': teacher, 'paper': paper, 'data_1': data_1, 'data_2': data_2})

        else:
            return render(request, 'index.html', {'message': '密码不正确'})


# 报名四级
def cet4(request):
    # 用户提交了报名表单
    if request.method == "POST":
        stuId = request.POST.get('id')
        place_id = request.POST.get('place_id')
        student = models.Student.objects.get(id=stuId)
        examPlace = models.ExamPlace.objects.get(id=place_id)

        cet4_form = SignUpForm(request.POST)
        if cet4_form.is_valid():
            # 四级考试一旦通过，就只能考一次
            if student.f_score >= 425:
                message = "您的四级考试已通过，不允许再次报考！"
                return render(request, 'cet4.html', locals())
            # 用与下面的是否重复报名判断
            grade_entry = models.Grade.objects.filter(sid=stuId, pid=examPlace.id)
            # 判断是否重复报名
            if grade_entry:
                message = "请勿重复报名！"
                return render(request, 'cet4.html', locals())
            else:
                message = "报名成功！请按时参加考试！"
                # 创建一条数据,以新建grade对象表示报名，但此时成绩取默认值-1
                # 注意这边create要带参数直接创建，不然外键会报错，注意这边外键命名,不大一样，跟本地mysql数据库吻合
                new_grade = models.Grade.objects.create(sid_id=stuId, pid_id=examPlace.id, type='CET4')
                new_grade.save()
                # 考点容量减1,报考人数加1
                examPlace.entry_number += 1
                examPlace.save()
                return render(request, 'cet4.html', locals())
    # 用户点击“报名”按钮进入
    else:
        stuId = request.GET.get('sid')
        placeId = request.GET.get('pid')
        student = models.Student.objects.get(id=stuId)
        examPlace = models.ExamPlace.objects.get(id=placeId)
        cet4_form = SignUpForm(
            initial={"name": student.name, "school": student.school, "id": student.id, "email": student.email,
                     "place_id": examPlace.id})
        return render(request, 'cet4.html', locals())


# 报名六级
def cet6(request):
    # 用户提交了报名表单
    if request.method == "POST":
        stuId = request.POST.get('id')
        place_id = request.POST.get('place_id')
        student = models.Student.objects.get(id=stuId)
        examPlace = models.ExamPlace.objects.get(id=place_id)

        cet6_form = SignUpForm(request.POST)
        if cet6_form.is_valid():
            # 六级考试要求四级分数>=425
            if student.f_score < 425:
                message = "您未通过四级考试，无法报考六级"
                return render(request, 'cet6.html', locals())
            # 用与下面的是否重复报名判断
            grade_entry = models.Grade.objects.filter(sid=stuId, pid=examPlace.id)
            # 判断是否重复报名
            if grade_entry:
                message = "请勿重复报名！"
                return render(request, 'cet6.html', locals())
            else:
                message = "报名成功！请按时参加考试！"
                # 创建一条数据,以新建grade对象表示报名，但此时成绩取默认值-1
                # 注意这边create要带参数直接创建，不然外键会报错，注意这边外键命名,不大一样，跟本地mysql数据库吻合
                new_grade = models.Grade.objects.create(sid_id=stuId, pid_id=examPlace.id, type='CET6')
                new_grade.save()
                # 考点容量减1,报考人数加1
                examPlace.entry_number += 1
                examPlace.save()
                return render(request, 'cet6.html', locals())
    # 用户点击“报名”按钮进入
    else:
        stuId = request.GET.get('sid')
        placeId = request.GET.get('pid')
        student = models.Student.objects.get(id=stuId)
        examPlace = models.ExamPlace.objects.get(id=placeId)
        cet6_form = SignUpForm(
            initial={"name": student.name, "school": student.school, "id": student.id, "email": student.email,
                     "place_id": examPlace.id})
        return render(request, 'cet6.html', locals())


# 学生考试 的视图函数
def startExam(request):
    sid = request.GET.get('sid')
    placeId = request.GET.get('pid')

    student = models.Student.objects.get(id=sid)
    place = models.ExamPlace.objects.get(id=placeId)
    paper = models.Paper.objects.filter(id=place.pid)
    return render(request, 'exam.html', {'student': student, 'place': place, 'paper': paper})


# 计算由exam.html模版传过来的数据计算成绩
def calGrade(request):
    if request.method == 'POST':
        # 得到学号和科目
        sid = request.POST.get('sid')
        placeId = request.POST.get('pid')

        # 重新生成Student实例，Paper实例，Place实例，名字和index中for的一致，可重复渲染
        student = models.Student.objects.get(id=sid)
        place = models.ExamPlace.objects.get(id=placeId)
        grades = models.Grade.objects.get(sid=sid, pid=placeId)

        # 计算该门考试的学生成绩
        question = models.Paper.objects.filter(id=place.pid).values("qid").values('qid__id', 'qid__answer',
                                                                                  'qid__score')
        mygrade = 0  # 初始化一个成绩为0
        for q in question:
            qId = str(q['qid__id'])  # int 转 string,通过qid找到题号
            myans = request.POST.get(qId)  # 通过 qid 得到学生关于该题的作答
            # print(myans)
            okans = q['qid__answer']  # 得到正确答案
            # print(okans)
            if myans == okans:  # 判断学生作答与正确答案是否一致
                mygrade += q['qid__score']  # 若一致,得到该题的分数,累加mygrade变量

        # Grade表更新数据
        grades.grade = mygrade
        grades.save()
        # print(mygrade)

        # Student表更新数据,取更大的
        if place.type == 'CET4':
            student.f_score = max(mygrade, student.f_score)
        else:
            student.s_score = max(mygrade, student.s_score)

        # 重新渲染index.html模板
        place = models.ExamPlace.objects.all().order_by("time")
        grade = models.Grade.objects.filter(sid=sid)
        # 查询考试信息（exam是有报名的place)
        grade_pid = []
        for i in range(len(grade)):
            grade_pid.append(grade[i].pid)
        # __in表示数据库中的in操作符，等价于id in grade_pid
        exam = models.ExamPlace.objects.filter(id__in=grade_pid)
        return render(request, 'index.html', {'student': student, 'place': place, 'exam': exam, 'grade': grade})


# 教师按条件查询学生
def queryStudent(request):
    # 获取教师查询的条件值
    sid = request.GET.get('id')
    sex = request.GET.get('sex')
    type = request.GET.get('type')

    # 获取老师的id
    tid = request.GET.get('tid')
    teacher = models.Teacher.objects.get(id=tid)
    paper = models.Paper.objects.filter(tid=tid)  # 奇怪,啥也没有
    print(teacher.id)
    # print(sid,sex,subject)
    from django.db import connection, transaction
    cursor = connection.cursor()
    sql = "select * from grade,student where student.id=grade.sid_id " \
          "and student.id like %s and grade.type like %s and student.sex like %s and '1'='1'"
    val = ('%' + sid + '%', '%' + type + '%', '%' + sex + '%')
    cursor.execute(sql, val)
    result = dictfetchall(cursor)
    # print(result)
    return render(request, 'teacher.html', {'teacher': teacher, 'result': result, 'paper': paper})


# 教师退出
def logOut(request):
    return redirect('/')


# 将使用原生sql语句查到的结果由tuple类型转换为dictionary(字典)类型
def dictfetchall(cursor):
    # 将游标返回的结果保存到一个字典对象中
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

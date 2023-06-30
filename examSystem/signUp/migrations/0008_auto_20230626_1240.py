# Generated by Django 3.0.3 on 2023-06-26 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signUp', '0007_auto_20230626_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subquestion',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='subquestion',
            name='score',
        ),
        migrations.AlterField(
            model_name='question',
            name='level',
            field=models.CharField(choices=[('3', 'difficult'), ('1', 'easy'), ('2', 'general')], max_length=10, verbose_name='等级'),
        ),
        migrations.AlterField(
            model_name='subquestion',
            name='level',
            field=models.CharField(choices=[('3', 'difficult'), ('1', 'easy'), ('2', 'general')], max_length=10, verbose_name='等级'),
        ),
        migrations.CreateModel(
            name='StuSubQues',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer', models.CharField(default='None', max_length=300, verbose_name='学生答案')),
                ('score', models.IntegerField(default=0, verbose_name='学生得分')),
                ('sid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='signUp.Student')),
                ('sqid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='signUp.SubQuestion')),
            ],
            options={
                'verbose_name': '学生所答主观题',
                'verbose_name_plural': '学生所答主观题',
                'db_table': 'StuSubQues',
            },
        ),
    ]
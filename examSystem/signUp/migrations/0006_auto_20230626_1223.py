# Generated by Django 3.0.3 on 2023-06-26 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUp', '0005_auto_20230626_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='level',
            field=models.CharField(choices=[('1', 'easy'), ('2', 'general'), ('3', 'difficult')], max_length=10, verbose_name='等级'),
        ),
        migrations.AlterField(
            model_name='question',
            name='score',
            field=models.IntegerField(default=2, verbose_name='分数'),
        ),
        migrations.AlterField(
            model_name='subquestion',
            name='answer',
            field=models.CharField(default=None, max_length=100, verbose_name='学生答案'),
        ),
        migrations.AlterField(
            model_name='subquestion',
            name='level',
            field=models.CharField(choices=[('1', 'easy'), ('2', 'general'), ('3', 'difficult')], max_length=10, verbose_name='等级'),
        ),
        migrations.AlterField(
            model_name='subquestion',
            name='totalScore',
            field=models.IntegerField(default=10, verbose_name='总分'),
        ),
    ]

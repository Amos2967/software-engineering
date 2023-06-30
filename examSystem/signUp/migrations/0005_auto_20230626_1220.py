# Generated by Django 3.0.3 on 2023-06-26 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUp', '0004_auto_20230626_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='level',
            field=models.CharField(choices=[('1', 'easy'), ('3', 'difficult'), ('2', 'general')], max_length=10, verbose_name='等级'),
        ),
        migrations.AlterField(
            model_name='subquestion',
            name='answer',
            field=models.CharField(default='', max_length=100, verbose_name='学生答案'),
        ),
        migrations.AlterField(
            model_name='subquestion',
            name='level',
            field=models.CharField(choices=[('1', 'easy'), ('3', 'difficult'), ('2', 'general')], max_length=10, verbose_name='等级'),
        ),
    ]
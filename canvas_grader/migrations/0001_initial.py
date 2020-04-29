# Generated by Django 3.0.5 on 2020-04-29 04:07

import canvas_grader.models.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_id', canvas_grader.models.fields.CanvasIdField()),
                ('name', models.CharField(max_length=50)),
                ('points_possible', models.FloatField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('html_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='CanvasUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', canvas_grader.models.fields.CanvasIdField()),
                ('name', models.CharField(max_length=50)),
                ('sortable_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', canvas_grader.models.fields.CanvasIdField()),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'unique_together': {('user_id', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_id', canvas_grader.models.fields.CanvasIdField()),
                ('speed_grader_url', models.URLField(null=True)),
                ('question_count', models.IntegerField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Assignment')),
            ],
            options={
                'unique_together': {('assignment', 'quiz_id')},
            },
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', canvas_grader.models.fields.CanvasIdField()),
                ('question_name', models.CharField(max_length=100)),
                ('question_text', models.TextField()),
                ('question_type', models.CharField(max_length=50)),
                ('points_possible', models.FloatField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_id', canvas_grader.models.fields.CanvasIdField()),
                ('posted_at', models.DateTimeField(null=True)),
                ('preview_url', models.URLField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Assignment')),
                ('canvas_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.CanvasUser')),
            ],
            options={
                'unique_together': {('assignment', 'submission_id')},
            },
        ),
        migrations.CreateModel(
            name='SubmissionHistoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_history_id', canvas_grader.models.fields.CanvasIdField()),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Submission')),
            ],
            options={
                'unique_together': {('submission', 'submission_history_id')},
            },
        ),
        migrations.CreateModel(
            name='SubmissionDatum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('quiz_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.QuizQuestion')),
                ('submission_history_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.SubmissionHistoryItem')),
            ],
            options={
                'unique_together': {('quiz_question', 'submission_history_item')},
            },
        ),
        migrations.CreateModel(
            name='QuizQuestionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', canvas_grader.models.fields.CanvasIdField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Quiz')),
            ],
            options={
                'unique_together': {('quiz', 'group_id')},
            },
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='quiz_question_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.QuizQuestionGroup'),
        ),
        migrations.CreateModel(
            name='GradingView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Quiz')),
            ],
            options={
                'unique_together': {('quiz', 'name')},
            },
        ),
        migrations.CreateModel(
            name='GradingGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('grading_view', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.GradingView')),
            ],
            options={
                'unique_together': {('name', 'grading_view')},
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', canvas_grader.models.fields.CanvasIdField()),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Domain')),
            ],
            options={
                'unique_together': {('course_id', 'domain')},
            },
        ),
        migrations.AddField(
            model_name='canvasuser',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Domain'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Course'),
        ),
        migrations.CreateModel(
            name='AssessmentItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('comment', models.TextField()),
                ('submission_datum', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.SubmissionDatum')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Domain')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('token', 'domain')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='quizquestion',
            unique_together={('quiz', 'question_id')},
        ),
        migrations.CreateModel(
            name='GroupQuestionLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grading_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.GradingGroup')),
                ('quiz_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.QuizQuestion')),
            ],
            options={
                'unique_together': {('quiz_question', 'grading_group')},
            },
        ),
        migrations.CreateModel(
            name='CourseLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas_grader.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='canvasuser',
            unique_together={('user_id', 'domain')},
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together={('assignment_id', 'course')},
        ),
    ]

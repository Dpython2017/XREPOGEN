from django.db import models


class ReportSample(models.Model):
    header = models.CharField(max_length=255)
    sub_heading = models.CharField(max_length=255, null=True, blank=True)
    display_details = models.JSONField(null=True, blank=True)
    image = models.ImageField(upload_to='formats')


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=255)

    def __str__(self):
        return self.teacher_name


class Student(models.Model):
    student_roll = models.IntegerField()
    student_class = models.CharField(max_length=255, default="III-D")
    student_name = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.student_name


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    m_sc = models.CharField(max_length=10, null=True, blank=True)
    lang = models.CharField(max_length=10, null=True, blank=True)
    lit = models.CharField(max_length=10, null=True, blank=True)
    hindi = models.CharField(max_length=10, null=True, blank=True)
    ssc = models.CharField(max_length=10, null=True, blank=True)
    maths = models.CharField(max_length=10, null=True, blank=True)
    gsc = models.CharField(max_length=10, null=True, blank=True)
    computer = models.CharField(max_length=10, null=True, blank=True)
    gk = models.CharField(max_length=10, null=True, blank=True)
    drawing = models.CharField(max_length=10, null=True, blank=True)
    writing = models.CharField(max_length=10, null=True, blank=True)
    recite = models.CharField(max_length=10, null=True, blank=True)
    reading = models.CharField(max_length=10, null=True, blank=True)
    story_telling = models.CharField(max_length=10, null=True, blank=True)
    physics = models.CharField(max_length=10, null=True, blank=True)
    chemistry = models.CharField(max_length=10, null=True, blank=True)
    geography = models.CharField(max_length=10, null=True, blank=True)
    bio = models.CharField(max_length=10, null=True, blank=True)
    commerce = models.CharField(max_length=10, null=True, blank=True)


    @property
    def total(self):
        total = 0
        if self.computer == 'Ab':
            pass
        else:
            total += int(self.computer)

        if self.maths == 'Ab':
            pass
        else:
            total += int(self.maths)

        if self.gk == 'Ab':
            pass
        else:
            total += int(self.gk)

        if self.gsc == 'Ab':
            pass
        else:
            total += int(self.gsc)

        if self.hindi == 'Ab':
            pass
        else:
            total += int(self.hindi)

        if self.lang == 'Ab':
            pass
        else:
            total += int(self.lang)

        if self.lit == 'Ab':
            pass
        else:
            total += int(self.lit)

        if self.ssc == 'Ab':
            pass
        else:
            total += int(self.ssc)

        if self.m_sc == 'Ab':
            pass
        else:
            total += int(self.m_sc)

        return total

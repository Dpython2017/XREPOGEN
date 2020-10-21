from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from fpdf import FPDF
import shutil
from .forms import StudentCreationForm, MarksCreationForm
from .models import Marks, Student
from wsgiref.util import FileWrapper


class Dashboard(FormView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        files_path = "pdfs"

        shutil.make_archive("pdfs/REPORT_CARD", 'zip', files_path)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File type is not .csv, please upload a CSV file')
            return HttpResponseRedirect(reverse("index"))
        try:
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            lines = lines[1:]
            for line in lines:
                fields = line.split(",")
                student_data_dict = {"student_roll": fields[0],
                                     "student_class": "III-B",
                                     "student_name": fields[1] + "," + fields[2]}
                if Student.objects.filter(student_name=student_data_dict['student_name']):
                    pass
                else:
                    form = StudentCreationForm(student_data_dict)
                    if form.is_valid():
                        form.save()
                    else:
                        messages.error(request, "form save error")

                obj = Student.objects.get(student_roll=fields[0])
                student_marks = {"student": obj, "m_sc": fields[3], "lang": fields[4],
                                 "lit": fields[5], "hindi": fields[6], "ssc": fields[7],
                                 "maths": fields[8], "gsc": fields[9], "computer": fields[10],
                                 "gk": fields[11], "drawing": fields[12], "writing": fields[13],
                                 "recite": fields[14], "reading": fields[15], "story_telling": fields[16]}

                form_marks = MarksCreationForm(student_marks)
                if form_marks.is_valid():
                    form_marks.save()

            messages.success(request, "Uploaded Successfully", extra_tags='alert')
            create_pdf(request.user.username)
            return HttpResponseRedirect(reverse("index"))
        except Exception as e:
            print("there")
            messages.error(request, "Unable to upload CVS file. " + repr(e))

            return HttpResponseRedirect(reverse("index"))


def create_pdf(username):
    print("here")

    # Since we do not need to draw lines anymore, there is no need to separate
    # headers from data matrix.
    data = Marks.objects.all()

    for row in data:
        pdf = FPDF(format='letter', unit='in')

        # Add new page. Without this you cannot create the document.
        pdf.add_page()

        # Remember to always put one of these at least once.
        pdf.set_font('Times', '', 14.0)

        # Effective page width, or just epw
        epw = pdf.w - 2 * pdf.l_margin

        # Set column width to 1/4 of effective page width to distribute content
        # evenly across table and page
        col_width = epw / 4 * 1.3
        th = pdf.font_size

        # Line break equivalent to 4 lines
        pdf.ln(1.2 * th)

        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(epw, 0.0, "St. Conrad's Inter College", align='C')
        pdf.ln(0.3)

        pdf.cell(ln=0, h=0, align='L', w=0, txt="", border=1)
        pdf.ln(0.3)
        pdf.set_font('Times', 'B', 12.0)
        pdf.cell(epw, 0.0, "Half Yearly Examination (2020-21)", align='C')
        pdf.set_font('Times', '', 14.0)
        pdf.ln(0.5)

        pdf.set_font('Times', '', 14.0)
        pdf.cell(0, 0.0, "Student Name - {}".format(row.student.student_name.upper()), align='L')
        pdf.set_font('Times', '', 14.0)
        pdf.ln(0.5)

        pdf.set_font('Times', '', 14.0)
        pdf.cell(0, 0.0, "Class - III - B ", align='L')
        pdf.set_font('Times', '', 14.0)
        pdf.ln(0.5)

        pdf.set_font('Times', '', 14.0)
        pdf.cell(0, 0.0, "Roll No. -{}".format(row.student.student_roll), align='L')
        pdf.set_font('Times', '', 14.0)
        pdf.ln(0.5)

        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(col_width, 2 * th, "Subject Name", align='C', border=1)
        pdf.cell(col_width, 2 * th, "Maximum Marks", align='C', border=1)
        pdf.cell(col_width, 2 * th, "Marks Obtained", align='C', border=1)

        pdf.set_font('Times', '', 12.0)

        user = Marks.objects.get(pk=row.pk)

        pdf.ln(2 * th)
        pdf.cell(col_width, 2 * th, "Moral Science", align='C', border=1)
        pdf.cell(col_width, 2 * th, "40", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.m_sc, align='C', border=1)
        pdf.ln(2 * th)

        pdf.cell(col_width, 2 * th, "English Language", align='C', border=1)
        pdf.cell(col_width, 2 * th, "40", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.lang, align='C', border=1)
        pdf.ln(2 * th)

        pdf.cell(col_width, 2 * th, "English Literature", align='C', border=1)
        pdf.cell(col_width, 2 * th, "40", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.lit, align='C', border=1)
        pdf.ln(2 * th)

        pdf.cell(col_width, 2 * th, "Hindi", align='C', border=1)
        pdf.cell(col_width, 2 * th, "40", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.hindi, align='C', border=1)
        pdf.ln(2 * th)

        pdf.cell(col_width, 2 * th, "Social Studies", align='C', border=1)
        pdf.cell(col_width, 2 * th, "40", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.ssc, align='C', border=1)
        pdf.ln(2 * th)

        pdf.cell(col_width, 2 * th, "Maths", align='C', border=1)
        pdf.cell(col_width, 2 * th, "40", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.maths, align='C', border=1)
        pdf.ln(2 * th)

        pdf.cell(col_width, 2 * th, "General Science", align='C', border=1)
        pdf.cell(col_width, 2 * th, "40", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.gsc, align='C', border=1)
        pdf.ln(2 * th)

        pdf.cell(col_width, 2 * th, "Computer", align='C', border=1)
        pdf.cell(col_width, 2 * th, "40", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.computer, align='C', border=1)
        pdf.ln(2 * th)

        pdf.cell(col_width, 2 * th, "General Knowledge", align='C', border=1)
        pdf.cell(col_width, 2 * th, "40", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.gk, align='C', border=1)
        pdf.ln(2 * th)

        pdf.cell(col_width, 2 * th, "Drawing", align='C', border=1)
        pdf.cell(col_width, 2 * th, "-", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.drawing, align='C', border=1)
        pdf.ln(2 * th)
        pdf.cell(col_width, 2 * th, "Writing", align='C', border=1)
        pdf.cell(col_width, 2 * th, "-", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.writing, align='C', border=1)
        pdf.ln(2 * th)
        pdf.cell(col_width, 2 * th, "Recitation", align='C', border=1)
        pdf.cell(col_width, 2 * th, "-", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.recite, align='C', border=1)
        pdf.ln(2 * th)
        pdf.cell(col_width, 2 * th, "Reading", align='C', border=1)
        pdf.cell(col_width, 2 * th, "-", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.reading, align='C', border=1)
        pdf.ln(2 * th)

        pdf.cell(col_width, 2 * th, "Story Telling", align='C', border=1)
        pdf.cell(col_width, 2 * th, "", align='C', border=1)
        pdf.cell(col_width, 2 * th, user.story_telling, align='C', border=1)
        pdf.ln(2 * th)

        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(col_width, 2 * th, "Total", align='C', border=1)
        pdf.cell(col_width, 2 * th, "360", align='C', border=1)
        pdf.cell(col_width, 2 * th, "{}".format(user.total), align='C', border=1)
        import os
        os.mkdir('pdfs/',username)
        pdf.output('pdfs/{}/{}-{}.pdf'.format(username,row.student.student_roll, row.student.student_name.upper()), 'F')

        import time
        pdf.ln(2 * th)
        print(pdf)


class FormatView(TemplateView):
    template_name = "test_formats.html"



class ViewPics(TemplateView):

    template_name = 'view_pics.html'


class CreateTemplate(TemplateView):
    template_name = 'createReport.html'
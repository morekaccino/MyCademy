from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from academy.models import *
from django.db.models import Max
from django.utils import timezone

# Create your views here.
def _class(request):
    current_user = request.user.id
    if request.user.is_authenticated:
        all_classes = Class.objects.filter(tutor_id__exact=current_user)
        context = {'classes': all_classes}
        return render(request=request, template_name='class/class_root.html', context=context)
    else:
        return HttpResponse("Please login first")


def _section(request, course, section):
    current_user = request.user.id
    if request.user.is_authenticated:
        the_class = Class.objects.filter(tutor_id__exact=current_user,
                                         course__course_name__iexact=course,
                                         section__iexact=section, )
        sessions = Session.objects.filter(class_name_id=the_class[0].id)
        context = {'classes': the_class,
                   'sessions': sessions,
                   'course': course,
                   'section': section,
                   'color1': the_class[0].color1,
                   'color2': the_class[0].color2
                   }
        return render(request=request, template_name='class/class_section.html', context=context)
    else:
        return HttpResponse("Please login first")


def _session(request, course, section, session):
    current_user = request.user.id
    if request.user.is_authenticated:
        the_class = Class.objects.filter(tutor_id__exact=current_user,
                                         course__course_name__iexact=course,
                                         section__iexact=section,
                                         )
        sessions = Session.objects.filter(class_name_id=the_class[0].id,
                                          pk=session,
                                          )
        attendances = AttendanceRecord.objects.filter(session_id__exact=sessions[0].id)
        all_students = the_class[0].students
        context = {'classes': the_class,
                   'sessions': sessions,
                   'attendances': attendances,
                   'all_students': all_students,
                   'course': course,
                   'section': section,
                   'session': session,
                   'color1': the_class[0].color1,
                   'color2': the_class[0].color2}
        return render(request=request, template_name='class/class_attendance.html', context=context)
    else:
        return HttpResponse("Please login first")


def api_attendance(request, course, section, session, student_id, status):
    current_user = request.user.id
    if request.user.is_authenticated:
        try:
            the_class = Class.objects.get(tutor_id__exact=current_user,
                                          course__course_name__iexact=course,
                                          section__iexact=section,
                                          )
            session = Session.objects.get(class_name_id=the_class.id,
                                          pk=session,
                                          )
            try:
                attendances = AttendanceRecord.objects.get(session_id__exact=session.id,
                                                           student_id__exact=student_id)
                attendances.status = status
                attendances.save()
                return HttpResponse(status + " saved")
            except:
                new_attendance = AttendanceRecord(session_id=session.id,
                                                  student_id=student_id,
                                                  status=status)
                new_attendance.save()
                return HttpResponse(status + " saved")

        except Exception as E:
            return HttpResponse("Error: " + str(E))
    else:
        return HttpResponse("UnAuthenticated request")


def api_section_last_session(request, course, section):
    current_user = request.user.id
    if request.user.is_authenticated:
        try:
            the_class = Class.objects.get(tutor_id__exact=current_user,
                                          course__course_name__iexact=course,
                                          section__iexact=section,
                                          )
            session = Session.objects.filter(class_name_id=the_class.id).aggregate(Max('session_nember'))
            max_session = 0
            print(session)
            try:
                if session['session_nember__max'] != None:
                    max_session = session['session_nember__max']
            except Exception as E:
                max_session = 0
            return HttpResponse(str(int(max_session) + 1))
        except Exception as E:
            return HttpResponse("Error: " + str(E))
    else:
        return HttpResponse("UnAuthenticated request")


def api_section_create(request, course, section):
    current_user = request.user.id
    if request.user.is_authenticated:
        try:
            the_class = Class.objects.get(tutor_id__exact=current_user,
                                          course__course_name__iexact=course,
                                          section__iexact=section,
                                          )
            session = Session.objects.filter(class_name_id=the_class.id).aggregate(Max('session_nember'))
            max_session = 0
            print(session)
            try:
                if session['session_nember__max'] != None:
                    max_session = session['session_nember__max']
            except Exception as E:
                max_session = 0
            new_session = Session(session_nember=int(max_session) + 1,
                                  class_name_id=the_class.id,
                                  date_datetime=timezone.now(),
                                  start_datetime=timezone.now(),
                                  end_datetime=timezone.now(),
                                  )
            new_session.save()
            return HttpResponse(str(int(max_session) + 1) + "created")
        except Exception as E:
            return HttpResponse("Error: " + str(E))
    else:
        return HttpResponse("UnAuthenticated request")

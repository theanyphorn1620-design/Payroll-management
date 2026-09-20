import calendar
from decimal import Decimal

from django.utils import timezone

from .models import Attendance, Employee, LeavePolicy, Payslip


def check_in_by_token(token):
    employee = Employee.objects.get(qr_token=token, is_active=True)
    today = timezone.localdate()

    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        date=today,
        defaults={
            'status': Attendance.Status.PRESENT,
            'check_in': timezone.localtime().time(),
        },
    )
    already_checked_in = not created
    return employee, attendance, already_checked_in


def generate_payslip(employee, month, year):
    salary_structure = employee.salary_structure

    allowances = salary_structure.house_allowance + salary_structure.transport_allowance
    basic_pay = salary_structure.basic_salary

    days_in_month = calendar.monthrange(year, month)[1]
    absent_days = Attendance.objects.filter(
        employee=employee,
        date__year=year,
        date__month=month,
        status=Attendance.Status.ABSENT,
    ).count()

    per_day_pay = basic_pay / Decimal(days_in_month)
    absence_deduction = (per_day_pay * absent_days).quantize(Decimal('0.01'))

    leave_policy = LeavePolicy.get_solo()
    leave_days = Attendance.objects.filter(
        employee=employee,
        date__year=year,
        date__month=month,
        status=Attendance.Status.LEAVE,
    ).count()
    excess_leave_days = max(0, leave_days - leave_policy.free_days_per_month)
    leave_deduction = (leave_policy.excess_deduction_per_day * excess_leave_days).quantize(Decimal('0.01'))

    total_deductions = (
        salary_structure.tax_deduction
        + salary_structure.other_deduction
        + absence_deduction
        + leave_deduction
    )
    net_pay = basic_pay + allowances - total_deductions

    payslip, _ = Payslip.objects.update_or_create(
        employee=employee,
        month=month,
        year=year,
        defaults={
            'basic_pay': basic_pay,
            'total_allowances': allowances,
            'total_deductions': total_deductions,
            'absent_days': absent_days,
            'absence_deduction': absence_deduction,
            'leave_days': leave_days,
            'leave_deduction': leave_deduction,
            'net_pay': net_pay,
        },
    )
    return payslip

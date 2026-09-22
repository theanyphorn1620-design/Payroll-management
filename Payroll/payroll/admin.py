from django.contrib import admin

from .models import Attendance, Employee, Holiday, LeavePolicy, Payslip, SalaryStructure


@admin.register(LeavePolicy)
class LeavePolicyAdmin(admin.ModelAdmin):
    list_display = ['free_days_per_month', 'excess_deduction_per_day']


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'description']
    list_filter = ['date']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'employee_id',
        'first_name',
        'last_name',
        'department',
        'position',
        'employment_type',
        'is_active',
        'termination_date',
        'user',
    ]
    list_filter = ['employment_type', 'department', 'is_active']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email', 'national_id']


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ['employee', 'basic_salary', 'effective_date']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status']
    list_filter = ['status', 'date']


@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = [
        'employee',
        'month',
        'year',
        'net_pay',
        'status',
        'payment_date',
        'payment_method',
        'generated_at',
    ]
    list_filter = ['status', 'payment_method', 'month', 'year']

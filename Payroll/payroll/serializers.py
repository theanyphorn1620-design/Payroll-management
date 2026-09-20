from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Attendance, Employee, LeavePolicy, Payslip, SalaryStructure


class LeavePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavePolicy
        fields = ['id', 'free_days_per_month', 'excess_deduction_per_day']


class SalaryStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructure
        fields = [
            'id',
            'employee',
            'basic_salary',
            'house_allowance',
            'transport_allowance',
            'tax_deduction',
            'other_deduction',
            'effective_date',
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'date', 'status', 'check_in', 'check_out']


class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = [
            'id',
            'employee',
            'month',
            'year',
            'basic_pay',
            'total_allowances',
            'total_deductions',
            'absent_days',
            'absence_deduction',
            'leave_days',
            'leave_deduction',
            'net_pay',
            'status',
            'generated_at',
        ]
        read_only_fields = [
            'basic_pay',
            'total_allowances',
            'total_deductions',
            'absent_days',
            'absence_deduction',
            'leave_days',
            'leave_deduction',
            'net_pay',
            'generated_at',
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    salary_structure = SalaryStructureSerializer(read_only=True)
    has_login = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'employee_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'department',
            'position',
            'date_joined',
            'is_active',
            'salary_structure',
            'qr_token',
            'national_id',
            'bank_account_number',
            'employment_type',
            'has_login',
            'password',
        ]
        read_only_fields = ['qr_token']

    def get_has_login(self, obj) -> bool:
        return obj.user_id is not None

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        employee = Employee.objects.create(**validated_data)
        self._sync_login(employee, password)
        return employee

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        employee = super().update(instance, validated_data)
        self._sync_login(employee, password)
        return employee

    def _sync_login(self, employee, password):
        if not password:
            return

        if employee.user_id:
            user = employee.user
            user.set_password(password)
            user.save()
        else:
            user = User.objects.create_user(
                username=employee.employee_id,
                email=employee.email,
                password=password,
            )
            employee.user = user
            employee.save(update_fields=['user'])

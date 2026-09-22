import uuid

from django.conf import settings
from django.db import models


class Employee(models.Model):
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full Time'
        PART_TIME = 'part_time', 'Part Time'
        CONTRACT = 'contract', 'Contract'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='employee_profile',
    )
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    date_joined = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    national_id = models.CharField(max_length=50, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    employment_type = models.CharField(
        max_length=10, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME
    )

    def __str__(self):
        return f'{self.employee_id} - {self.first_name} {self.last_name}'


class SalaryStructure(models.Model):
    employee = models.OneToOneField(
        Employee, on_delete=models.CASCADE, related_name='salary_structure'
    )
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    house_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    effective_date = models.DateField()

    def __str__(self):
        return f'Salary structure for {self.employee}'


class LeavePolicy(models.Model):
    free_days_per_month = models.PositiveSmallIntegerField(default=2)
    excess_deduction_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=5)

    @classmethod
    def get_solo(cls):
        policy, _ = cls.objects.get_or_create(pk=1)
        return policy

    def __str__(self):
        return f'{self.free_days_per_month} free leave days/month, ${self.excess_deduction_per_day}/extra day'


class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.name} ({self.date})'


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LEAVE = 'leave', 'Leave'
        HALF_DAY = 'half_day', 'Half Day'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.employee} - {self.date} - {self.status}'


class Payslip(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        APPROVED = 'approved', 'Approved'
        PAID = 'paid', 'Paid'

    class PaymentMethod(models.TextChoices):
        BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
        CASH = 'cash', 'Cash'
        CHEQUE = 'cheque', 'Cheque'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payslips')
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    basic_pay = models.DecimalField(max_digits=12, decimal_places=2)
    total_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    absent_days = models.PositiveSmallIntegerField(default=0)
    absence_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    leave_days = models.PositiveSmallIntegerField(default=0)
    leave_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, blank=True
    )
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f'Payslip {self.employee} {self.month}/{self.year}'

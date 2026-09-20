from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AttendanceViewSet,
    EmployeeViewSet,
    PayslipViewSet,
    SalaryStructureViewSet,
    leave_policy,
    login_view,
    me_view,
    payroll_summary,
)

router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')
router.register('salary-structures', SalaryStructureViewSet)
router.register('attendances', AttendanceViewSet, basename='attendance')
router.register('payslips', PayslipViewSet, basename='payslip')

urlpatterns = router.urls + [
    path('reports/payroll-summary/', payroll_summary, name='payroll-summary'),
    path('leave-policy/', leave_policy, name='leave-policy'),
    path('auth/login/', login_view, name='auth-login'),
    path('auth/me/', me_view, name='auth-me'),
]

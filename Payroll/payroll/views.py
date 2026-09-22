import datetime

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import Attendance, Employee, Holiday, LeavePolicy, Payslip, SalaryStructure
from .serializers import (
    AttendanceSerializer,
    EmployeeSerializer,
    HolidaySerializer,
    LeavePolicySerializer,
    PayslipSerializer,
    SalaryStructureSerializer,
)
from .services import check_in_by_token, generate_payslip


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


def _employee_payload(user):
    employee = getattr(user, 'employee_profile', None)
    return EmployeeSerializer(employee).data if employee else None


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {
            'token': token.key,
            'is_staff': user.is_staff,
            'employee': _employee_payload(user),
        }
    )


@api_view(['GET'])
def me_view(request):
    return Response(
        {
            'is_staff': request.user.is_staff,
            'employee': _employee_payload(request.user),
        }
    )


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Employee.objects.none()
        if user.is_staff:
            return Employee.objects.all()
        return Employee.objects.filter(user=user)


class HolidayViewSet(viewsets.ModelViewSet):
    serializer_class = HolidaySerializer
    permission_classes = [IsStaffOrReadOnly]
    queryset = Holiday.objects.all()

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        tomorrow = timezone.localdate() + datetime.timedelta(days=1)
        holidays = Holiday.objects.filter(date=tomorrow)
        return Response(HolidaySerializer(holidays, many=True).data)


class SalaryStructureViewSet(viewsets.ModelViewSet):
    serializer_class = SalaryStructureSerializer
    permission_classes = [IsAdminUser]
    queryset = SalaryStructure.objects.all()


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Attendance.objects.none()
        if user.is_staff:
            return Attendance.objects.all()
        return Attendance.objects.filter(employee__user=user)

    @action(
        detail=False,
        methods=['post'],
        url_path='check-in',
        permission_classes=[permissions.IsAuthenticated],
    )
    def check_in(self, request):
        token = request.data.get('token')

        try:
            employee, attendance, already_checked_in = check_in_by_token(token)
        except (Employee.DoesNotExist, ValidationError, ValueError, TypeError):
            return Response({'detail': 'Invalid QR code.'}, status=status.HTTP_404_NOT_FOUND)

        own_employee = getattr(request.user, 'employee_profile', None)
        if not request.user.is_staff and own_employee != employee:
            return Response(
                {'detail': 'This QR code does not belong to your account.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                'employee_name': f'{employee.first_name} {employee.last_name}',
                'date': attendance.date,
                'check_in': attendance.check_in,
                'already_checked_in': already_checked_in,
            }
        )


class PayslipViewSet(viewsets.ModelViewSet):
    serializer_class = PayslipSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Payslip.objects.none()
        if user.is_staff:
            return Payslip.objects.all()
        return Payslip.objects.filter(employee__user=user)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def generate(self, request):
        employee_id = request.data.get('employee')
        month = request.data.get('month')
        year = request.data.get('year')

        employee = Employee.objects.get(pk=employee_id)
        payslip = generate_payslip(employee, int(month), int(year))
        serializer = self.get_serializer(payslip)
        return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAdminUser])
def leave_policy(request):
    policy = LeavePolicy.get_solo()

    if request.method == 'PUT':
        serializer = LeavePolicySerializer(policy, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    return Response(LeavePolicySerializer(policy).data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def payroll_summary(request):
    today = timezone.localdate()
    month = int(request.query_params.get('month', today.month))
    year = int(request.query_params.get('year', today.year))

    payslips = Payslip.objects.filter(month=month, year=year)

    totals = payslips.aggregate(
        total_net_pay=Sum('net_pay'),
        total_basic_pay=Sum('basic_pay'),
        total_allowances=Sum('total_allowances'),
        total_deductions=Sum('total_deductions'),
        headcount=Count('id'),
    )

    by_department = (
        payslips.values('employee__department')
        .annotate(total_net_pay=Sum('net_pay'), employee_count=Count('id'))
        .order_by('employee__department')
    )

    return Response(
        {
            'month': month,
            'year': year,
            'total_net_pay': totals['total_net_pay'] or 0,
            'total_basic_pay': totals['total_basic_pay'] or 0,
            'total_allowances': totals['total_allowances'] or 0,
            'total_deductions': totals['total_deductions'] or 0,
            'headcount': totals['headcount'] or 0,
            'by_department': [
                {
                    'department': row['employee__department'] or 'Unassigned',
                    'total_net_pay': row['total_net_pay'],
                    'employee_count': row['employee_count'],
                }
                for row in by_department
            ],
        }
    )

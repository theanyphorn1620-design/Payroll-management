<script setup>
import { ref, onMounted } from 'vue'
import QRCode from 'qrcode'
import { mdiAccountCircle, mdiCalendarCheck, mdiFileDocument, mdiQrcode } from '@mdi/js'
import api from '@/lib/api.js'
import { useAuthStore } from '@/stores/auth.js'
import SectionMain from '@/components/SectionMain.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import CardBox from '@/components/CardBox.vue'
import PillTag from '@/components/PillTag.vue'
import BaseIcon from '@/components/BaseIcon.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'

const authStore = useAuthStore()
const employee = authStore.employee

const attendances = ref([])
const payslips = ref([])
const qrDataUrl = ref('')

const statusPillColor = {
  present: 'success',
  absent: 'danger',
  leave: 'warning',
  half_day: 'info',
}

const payslipStatusPillColor = {
  draft: 'warning',
  approved: 'info',
  paid: 'success',
}

const fetchAttendances = () => {
  api.get('attendances/').then((result) => {
    attendances.value = result.data
  })
}

const fetchPayslips = () => {
  api.get('payslips/').then((result) => {
    payslips.value = result.data
  })
}

onMounted(() => {
  fetchAttendances()
  fetchPayslips()

  if (employee?.qr_token) {
    const checkInUrl = `${window.location.origin}${import.meta.env.BASE_URL}#/check-in/${employee.qr_token}`
    QRCode.toDataURL(checkInUrl, { width: 200 }).then((dataUrl) => {
      qrDataUrl.value = dataUrl
    })
  }
})
</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiAccountCircle" title="My Portal" main />

      <div class="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
        <CardBox class="lg:col-span-2">
          <h3 class="mb-4 text-lg font-bold">{{ employee?.first_name }} {{ employee?.last_name }}</h3>
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div>
              <div class="text-xs text-gray-500 dark:text-slate-400">Employee ID</div>
              <div>{{ employee?.employee_id }}</div>
            </div>
            <div>
              <div class="text-xs text-gray-500 dark:text-slate-400">Email</div>
              <div>{{ employee?.email }}</div>
            </div>
            <div>
              <div class="text-xs text-gray-500 dark:text-slate-400">Department</div>
              <div>{{ employee?.department || '—' }}</div>
            </div>
            <div>
              <div class="text-xs text-gray-500 dark:text-slate-400">Position</div>
              <div>{{ employee?.position || '—' }}</div>
            </div>
            <div>
              <div class="text-xs text-gray-500 dark:text-slate-400">Employment Type</div>
              <div class="capitalize">{{ employee?.employment_type?.replace('_', ' ') }}</div>
            </div>
            <div>
              <div class="text-xs text-gray-500 dark:text-slate-400">Date Joined</div>
              <div>{{ employee?.date_joined }}</div>
            </div>
          </div>
        </CardBox>

        <CardBox class="flex flex-col items-center justify-center text-center">
          <h3 class="mb-3 flex items-center gap-2 text-lg font-bold">
            <BaseIcon :path="mdiQrcode" /> My Check-in Code
          </h3>
          <img v-if="qrDataUrl" :src="qrDataUrl" alt="My attendance QR code" />
          <p class="mt-2 text-xs text-gray-500 dark:text-slate-400">Scan once a day to check in</p>
        </CardBox>
      </div>

      <SectionTitleLineWithButton :icon="mdiCalendarCheck" title="My Attendance" />

      <CardBox has-table class="mb-6">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="attendance in attendances" :key="attendance.id">
              <td data-label="Date">{{ attendance.date }}</td>
              <td data-label="Status">
                <PillTag :label="attendance.status" :color="statusPillColor[attendance.status]" small />
              </td>
            </tr>
            <tr v-if="!attendances.length">
              <td colspan="2" class="text-center">No attendance records yet</td>
            </tr>
          </tbody>
        </table>
      </CardBox>

      <SectionTitleLineWithButton :icon="mdiFileDocument" title="My Payslips" />

      <CardBox has-table>
        <table>
          <thead>
            <tr>
              <th>Period</th>
              <th>Basic pay</th>
              <th>Allowances</th>
              <th>Deductions</th>
              <th>Net pay</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payslip in payslips" :key="payslip.id">
              <td data-label="Period">{{ payslip.month }}/{{ payslip.year }}</td>
              <td data-label="Basic pay">{{ payslip.basic_pay }}</td>
              <td data-label="Allowances">{{ payslip.total_allowances }}</td>
              <td data-label="Deductions">{{ payslip.total_deductions }}</td>
              <td data-label="Net pay"><b>{{ payslip.net_pay }}</b></td>
              <td data-label="Status">
                <PillTag :label="payslip.status" :color="payslipStatusPillColor[payslip.status]" small />
              </td>
            </tr>
            <tr v-if="!payslips.length">
              <td colspan="6" class="text-center">No payslips yet</td>
            </tr>
          </tbody>
        </table>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>

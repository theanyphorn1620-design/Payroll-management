<script setup>
import { computed, ref, onMounted } from 'vue'
import {
  mdiAccountMultiple,
  mdiCalendarCheck,
  mdiCurrencyUsd,
  mdiChartTimelineVariant,
  mdiFileDocument,
} from '@mdi/js'
import api from '@/lib/api.js'
import SectionMain from '@/components/SectionMain.vue'
import CardBoxWidget from '@/components/CardBoxWidget.vue'
import CardBox from '@/components/CardBox.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'

const today = new Date().toISOString().slice(0, 10)
const employeeCount = ref(0)
const presentToday = ref(0)
const payslips = ref([])

const fetchEmployeeCount = () => {
  api.get('employees/').then((result) => {
    employeeCount.value = result.data.length
  })
}

const currentMonthNetPayroll = computed(() => {
  const now = new Date()
  const month = now.getMonth() + 1
  const year = now.getFullYear()
  return payslips.value
    .filter((payslip) => payslip.month === month && payslip.year === year)
    .reduce((total, payslip) => total + Number(payslip.net_pay), 0)
    .toFixed(2)
})

const recentPayslips = computed(() => payslips.value.slice(0, 5))

const fetchPresentToday = () => {
  api.get('attendances/', { params: { date: today, status: 'present' } }).then((result) => {
    presentToday.value = result.data.filter((a) => a.date === today && a.status === 'present').length
  })
}

const fetchPayslips = () => {
  api.get('payslips/').then((result) => {
    payslips.value = result.data
  })
}

onMounted(() => {
  fetchEmployeeCount()
  fetchPresentToday()
  fetchPayslips()
})
</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiChartTimelineVariant" title="Payroll Overview" main />

      <div class="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-4">
        <CardBoxWidget
          trend="Live"
          trend-type="up"
          color="text-emerald-500"
          :icon="mdiAccountMultiple"
          :number="employeeCount"
          label="Employees"
        />
        <CardBoxWidget
          trend="Today"
          trend-type="up"
          color="text-blue-500"
          :icon="mdiCalendarCheck"
          :number="presentToday"
          label="Present Today"
        />
        <CardBoxWidget
          trend="This month"
          trend-type="up"
          color="text-purple-500"
          :icon="mdiCurrencyUsd"
          :number="currentMonthNetPayroll"
          prefix="$"
          label="Net Payroll"
        />
        <CardBoxWidget
          trend="Total"
          trend-type="up"
          color="text-yellow-500"
          :icon="mdiFileDocument"
          :number="payslips.length"
          label="Payslips Generated"
        />
      </div>

      <SectionTitleLineWithButton :icon="mdiFileDocument" title="Recent Payslips" />

      <CardBox has-table>
        <table>
          <thead>
            <tr>
              <th>Period</th>
              <th>Basic pay</th>
              <th>Allowances</th>
              <th>Deductions</th>
              <th>Net pay</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payslip in recentPayslips" :key="payslip.id">
              <td data-label="Period">{{ payslip.month }}/{{ payslip.year }}</td>
              <td data-label="Basic pay">{{ payslip.basic_pay }}</td>
              <td data-label="Allowances">{{ payslip.total_allowances }}</td>
              <td data-label="Deductions">{{ payslip.total_deductions }}</td>
              <td data-label="Net pay"><b>{{ payslip.net_pay }}</b></td>
            </tr>
            <tr v-if="!recentPayslips.length">
              <td colspan="5" class="text-center">No payslips generated yet</td>
            </tr>
          </tbody>
        </table>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>

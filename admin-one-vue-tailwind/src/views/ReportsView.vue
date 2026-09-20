<script setup>
import { ref, watch } from 'vue'
import { mdiChartBar, mdiCurrencyUsd, mdiAccountMultiple, mdiCalculator } from '@mdi/js'
import api from '@/lib/api.js'
import SectionMain from '@/components/SectionMain.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import CardBox from '@/components/CardBox.vue'
import CardBoxWidget from '@/components/CardBoxWidget.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'

const monthOptions = [
  { id: 1, label: 'January' },
  { id: 2, label: 'February' },
  { id: 3, label: 'March' },
  { id: 4, label: 'April' },
  { id: 5, label: 'May' },
  { id: 6, label: 'June' },
  { id: 7, label: 'July' },
  { id: 8, label: 'August' },
  { id: 9, label: 'September' },
  { id: 10, label: 'October' },
  { id: 11, label: 'November' },
  { id: 12, label: 'December' },
]

const today = new Date()
const selectedMonth = ref(monthOptions[today.getMonth()])
const selectedYear = ref(today.getFullYear())

const summary = ref({
  total_net_pay: 0,
  total_basic_pay: 0,
  total_allowances: 0,
  total_deductions: 0,
  headcount: 0,
  by_department: [],
})

const fetchSummary = () => {
  api
    .get('reports/payroll-summary/', {
      params: {
        month: selectedMonth.value?.id ?? selectedMonth.value,
        year: selectedYear.value,
      },
    })
    .then((result) => {
      summary.value = result.data
    })
}

watch([selectedMonth, selectedYear], fetchSummary, { immediate: true })
</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiChartBar" title="Payroll Reports" main />

      <div class="mb-6 grid grid-cols-1 gap-6 md:grid-cols-2">
        <FormField label="Month">
          <FormControl v-model="selectedMonth" :options="monthOptions" />
        </FormField>
        <FormField label="Year">
          <FormControl v-model="selectedYear" type="number" />
        </FormField>
      </div>

      <div class="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-4">
        <CardBoxWidget
          trend="Selected period"
          trend-type="up"
          color="text-emerald-500"
          :icon="mdiCurrencyUsd"
          :number="summary.total_net_pay"
          prefix="$"
          label="Net Payroll"
        />
        <CardBoxWidget
          trend="Selected period"
          trend-type="up"
          color="text-blue-500"
          :icon="mdiCalculator"
          :number="summary.total_basic_pay"
          prefix="$"
          label="Basic Pay"
        />
        <CardBoxWidget
          trend="Selected period"
          trend-type="up"
          color="text-purple-500"
          :icon="mdiCurrencyUsd"
          :number="summary.total_deductions"
          prefix="$"
          label="Deductions"
        />
        <CardBoxWidget
          trend="Selected period"
          trend-type="up"
          color="text-yellow-500"
          :icon="mdiAccountMultiple"
          :number="summary.headcount"
          label="Payslips"
        />
      </div>

      <SectionTitleLineWithButton :icon="mdiAccountMultiple" title="Net Payroll by Department" />

      <CardBox has-table>
        <table>
          <thead>
            <tr>
              <th>Department</th>
              <th>Employees paid</th>
              <th>Net payroll</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in summary.by_department" :key="row.department">
              <td data-label="Department">{{ row.department }}</td>
              <td data-label="Employees paid">{{ row.employee_count }}</td>
              <td data-label="Net payroll">${{ row.total_net_pay }}</td>
            </tr>
            <tr v-if="!summary.by_department.length">
              <td colspan="3" class="text-center">No payslips for this period</td>
            </tr>
          </tbody>
        </table>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>

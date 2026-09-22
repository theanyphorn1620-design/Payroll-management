<script setup>
import { ref, onMounted, computed } from 'vue'
import { mdiFileDocument, mdiPlus, mdiPencil, mdiCogOutline } from '@mdi/js'
import api from '@/lib/api.js'
import SectionMain from '@/components/SectionMain.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import CardBox from '@/components/CardBox.vue'
import CardBoxModal from '@/components/CardBoxModal.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import PillTag from '@/components/PillTag.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'

const statusPillColor = {
  draft: 'warning',
  approved: 'info',
  paid: 'success',
}

const employees = ref([])
const payslips = ref([])

const statusOptions = [
  { id: 'draft', label: 'Draft' },
  { id: 'approved', label: 'Approved' },
  { id: 'paid', label: 'Paid' },
]

const paymentMethodOptions = [
  { id: 'bank_transfer', label: 'Bank Transfer' },
  { id: 'cash', label: 'Cash' },
  { id: 'cheque', label: 'Cheque' },
]

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

const emptyForm = () => ({
  employee: '',
  month: monthOptions[new Date().getMonth()],
  year: new Date().getFullYear(),
})

const form = ref(emptyForm())
const isModalActive = ref(false)
const errorMessage = ref('')

const employeeMap = computed(() => {
  const map = {}
  employees.value.forEach((employee) => {
    map[employee.id] = `${employee.first_name} ${employee.last_name}`
  })
  return map
})

const fetchEmployees = () => {
  api.get('employees/').then((result) => {
    employees.value = result.data
  })
}

const fetchPayslips = () => {
  api.get('payslips/').then((result) => {
    payslips.value = result.data
  })
}

const openCreateModal = () => {
  form.value = emptyForm()
  errorMessage.value = ''
  isModalActive.value = true
}

const submitForm = () => {
  errorMessage.value = ''
  const payload = {
    ...form.value,
    employee: form.value.employee?.id ?? form.value.employee,
    month: form.value.month?.id ?? form.value.month,
  }

  api
    .post('payslips/generate/', payload)
    .then(() => {
      isModalActive.value = false
      fetchPayslips()
    })
    .catch((error) => {
      errorMessage.value =
        error?.response?.data?.detail ?? 'Could not generate payslip. Does the employee have a salary structure?'
    })
}

const isStatusModalActive = ref(false)
const statusModalPayslip = ref(null)
const statusModalValue = ref(null)
const statusModalPaymentDate = ref('')
const statusModalPaymentMethod = ref(null)

const openStatusModal = (payslip) => {
  statusModalPayslip.value = payslip
  statusModalValue.value = statusOptions.find((o) => o.id === payslip.status)
  statusModalPaymentDate.value = payslip.payment_date || new Date().toISOString().slice(0, 10)
  statusModalPaymentMethod.value =
    paymentMethodOptions.find((o) => o.id === payslip.payment_method) || paymentMethodOptions[0]
  isStatusModalActive.value = true
}

const submitStatus = () => {
  const statusId = statusModalValue.value?.id ?? statusModalValue.value
  const payload = { status: statusId }

  if (statusId === 'paid') {
    payload.payment_date = statusModalPaymentDate.value
    payload.payment_method = statusModalPaymentMethod.value?.id ?? statusModalPaymentMethod.value
  }

  api.patch(`payslips/${statusModalPayslip.value.id}/`, payload).then(() => {
    isStatusModalActive.value = false
    fetchPayslips()
  })
}

const isPolicyModalActive = ref(false)
const leavePolicy = ref({ free_days_per_month: 2, excess_deduction_per_day: 5 })

const fetchLeavePolicy = () => {
  api.get('leave-policy/').then((result) => {
    leavePolicy.value = result.data
  })
}

const openPolicyModal = () => {
  isPolicyModalActive.value = true
}

const submitPolicy = () => {
  api.put('leave-policy/', leavePolicy.value).then((result) => {
    leavePolicy.value = result.data
    isPolicyModalActive.value = false
  })
}

onMounted(() => {
  fetchEmployees()
  fetchPayslips()
  fetchLeavePolicy()
})
</script>

<template>
  <CardBoxModal
    v-model="isModalActive"
    title="Generate Payslip"
    is-form
    button="success"
    button-label="Generate"
    has-cancel
    @confirm="submitForm"
  >
    <FormField label="Employee">
      <FormControl
        v-model="form.employee"
        :options="employees.map((e) => ({ id: e.id, label: `${e.first_name} ${e.last_name}` }))"
      />
    </FormField>
    <FormField label="Month">
      <FormControl v-model="form.month" :options="monthOptions" />
    </FormField>
    <FormField label="Year">
      <FormControl v-model="form.year" type="number" required />
    </FormField>
    <p v-if="errorMessage" class="text-red-600 dark:text-red-500">{{ errorMessage }}</p>
  </CardBoxModal>

  <CardBoxModal
    v-model="isStatusModalActive"
    title="Update Payslip Status"
    is-form
    button="success"
    button-label="Save"
    has-cancel
    @confirm="submitStatus"
  >
    <FormField label="Status">
      <FormControl v-model="statusModalValue" :options="statusOptions" />
    </FormField>
    <template v-if="statusModalValue?.id === 'paid'">
      <FormField label="Payment date">
        <FormControl v-model="statusModalPaymentDate" type="date" required />
      </FormField>
      <FormField label="Payment method">
        <FormControl v-model="statusModalPaymentMethod" :options="paymentMethodOptions" />
      </FormField>
    </template>
  </CardBoxModal>

  <CardBoxModal
    v-model="isPolicyModalActive"
    title="Leave Policy"
    is-form
    button="success"
    button-label="Save"
    has-cancel
    @confirm="submitPolicy"
  >
    <FormField label="Free leave days per month" help="Leave days up to this amount are not deducted from salary">
      <FormControl v-model="leavePolicy.free_days_per_month" type="number" required />
    </FormField>
    <FormField label="Deduction per extra day ($)" help="Charged per leave day beyond the free allowance">
      <FormControl v-model="leavePolicy.excess_deduction_per_day" type="number" required />
    </FormField>
  </CardBoxModal>

  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiFileDocument" title="Payslips" main>
        <BaseButtons>
          <BaseButton :icon="mdiCogOutline" label="Leave Policy" color="whiteDark" @click="openPolicyModal" />
          <BaseButton :icon="mdiPlus" label="Generate Payslip" color="info" @click="openCreateModal" />
        </BaseButtons>
      </SectionTitleLineWithButton>

      <CardBox has-table>
        <table>
          <thead>
            <tr>
              <th>Employee</th>
              <th>Period</th>
              <th>Basic pay</th>
              <th>Allowances</th>
              <th>Deductions</th>
              <th>Absent days</th>
              <th>Leave days</th>
              <th>Net pay</th>
              <th>Status</th>
              <th>Paid On</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payslip in payslips" :key="payslip.id">
              <td data-label="Employee">{{ employeeMap[payslip.employee] }}</td>
              <td data-label="Period">{{ payslip.month }}/{{ payslip.year }}</td>
              <td data-label="Basic pay">{{ payslip.basic_pay }}</td>
              <td data-label="Allowances">{{ payslip.total_allowances }}</td>
              <td data-label="Deductions">{{ payslip.total_deductions }}</td>
              <td data-label="Absent days">{{ payslip.absent_days }}</td>
              <td data-label="Leave days">
                {{ payslip.leave_days }}
                <span v-if="Number(payslip.leave_deduction) > 0" class="text-red-500">
                  (-${{ payslip.leave_deduction }})
                </span>
              </td>
              <td data-label="Net pay"><b>{{ payslip.net_pay }}</b></td>
              <td data-label="Status" class="lg:w-40">
                <BaseButtons type="justify-start lg:justify-end" no-wrap>
                  <PillTag
                    :label="statusOptions.find((o) => o.id === payslip.status)?.label"
                    :color="statusPillColor[payslip.status]"
                    small
                  />
                  <BaseButton color="info" :icon="mdiPencil" small @click="openStatusModal(payslip)" />
                </BaseButtons>
              </td>
              <td data-label="Paid On">
                <span v-if="payslip.payment_date">
                  {{ payslip.payment_date }} ({{ paymentMethodOptions.find((o) => o.id === payslip.payment_method)?.label }})
                </span>
                <span v-else class="text-gray-500 dark:text-slate-400">—</span>
              </td>
            </tr>
            <tr v-if="!payslips.length">
              <td colspan="10" class="text-center">No payslips generated yet</td>
            </tr>
          </tbody>
        </table>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>

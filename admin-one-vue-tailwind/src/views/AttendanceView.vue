<script setup>
import { ref, onMounted, computed } from 'vue'
import {
  mdiCalendarCheck,
  mdiPlus,
  mdiPencil,
  mdiTrashCan,
  mdiAccountCheck,
  mdiAccountCancel,
  mdiAccountClock,
  mdiAccountMinus,
} from '@mdi/js'
import api from '@/lib/api.js'
import SectionMain from '@/components/SectionMain.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import CardBox from '@/components/CardBox.vue'
import CardBoxModal from '@/components/CardBoxModal.vue'
import CardBoxWidget from '@/components/CardBoxWidget.vue'
import PillTag from '@/components/PillTag.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'

const employees = ref([])
const attendances = ref([])

const statusOptions = [
  { id: 'present', label: 'Present' },
  { id: 'absent', label: 'Absent' },
  { id: 'leave', label: 'Leave' },
  { id: 'half_day', label: 'Half Day' },
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

const ALL_EMPLOYEES = { id: 'all', label: 'All Employees' }

const emptyForm = () => ({
  id: null,
  employee: '',
  date: '',
  status: statusOptions[0],
})

const form = ref(emptyForm())
const isModalActive = ref(false)
const isDeleteModalActive = ref(false)
const deleteTarget = ref(null)

const today = new Date()
const filterEmployee = ref(ALL_EMPLOYEES)
const filterMonth = ref(monthOptions[today.getMonth()])
const filterYear = ref(today.getFullYear())

const employeeOptions = computed(() => [
  ALL_EMPLOYEES,
  ...employees.value.map((e) => ({ id: e.id, label: `${e.first_name} ${e.last_name}` })),
])

const employeeMap = computed(() => {
  const map = {}
  employees.value.forEach((employee) => {
    map[employee.id] = `${employee.first_name} ${employee.last_name}`
  })
  return map
})

const statusLabel = (statusId) => statusOptions.find((o) => o.id === statusId)?.label ?? statusId

const statusPillColor = {
  present: 'success',
  absent: 'danger',
  leave: 'warning',
  half_day: 'info',
}

const filteredAttendances = computed(() => {
  const employeeId = filterEmployee.value?.id ?? filterEmployee.value
  const month = filterMonth.value?.id ?? filterMonth.value

  return attendances.value.filter((attendance) => {
    const [year, attendanceMonth] = attendance.date.split('-').map(Number)
    const matchesEmployee = employeeId === 'all' || attendance.employee === employeeId
    const matchesMonth = attendanceMonth === month
    const matchesYear = year === filterYear.value
    return matchesEmployee && matchesMonth && matchesYear
  })
})

const summaryCounts = computed(() => {
  const counts = { present: 0, absent: 0, leave: 0, half_day: 0 }
  filteredAttendances.value.forEach((attendance) => {
    if (counts[attendance.status] !== undefined) {
      counts[attendance.status] += 1
    }
  })
  return counts
})

const fetchEmployees = () => {
  api.get('employees/').then((result) => {
    employees.value = result.data
  })
}

const fetchAttendances = () => {
  api.get('attendances/').then((result) => {
    attendances.value = result.data
  })
}

const openCreateModal = () => {
  form.value = emptyForm()
  isModalActive.value = true
}

const openEditModal = (attendance) => {
  form.value = {
    id: attendance.id,
    employee: employeeOptions.value.find((o) => o.id === attendance.employee) ?? '',
    date: attendance.date,
    status: statusOptions.find((o) => o.id === attendance.status),
  }
  isModalActive.value = true
}

const submitForm = () => {
  const payload = {
    employee: form.value.employee?.id ?? form.value.employee,
    date: form.value.date,
    status: form.value.status?.id ?? form.value.status,
  }

  const request = form.value.id
    ? api.put(`attendances/${form.value.id}/`, payload)
    : api.post('attendances/', payload)

  request.then(() => {
    isModalActive.value = false
    fetchAttendances()
  })
}

const confirmDelete = (attendance) => {
  deleteTarget.value = attendance
  isDeleteModalActive.value = true
}

const deleteAttendance = () => {
  api.delete(`attendances/${deleteTarget.value.id}/`).then(() => {
    isDeleteModalActive.value = false
    fetchAttendances()
  })
}

onMounted(() => {
  fetchEmployees()
  fetchAttendances()
})
</script>

<template>
  <CardBoxModal
    v-model="isModalActive"
    :title="form.id ? 'Edit Attendance' : 'Record Attendance'"
    is-form
    button="success"
    :button-label="form.id ? 'Save' : 'Create'"
    has-cancel
    @confirm="submitForm"
  >
    <FormField label="Employee">
      <FormControl
        v-model="form.employee"
        :options="employees.map((e) => ({ id: e.id, label: `${e.first_name} ${e.last_name}` }))"
      />
    </FormField>
    <FormField label="Date">
      <FormControl v-model="form.date" type="date" required />
    </FormField>
    <FormField label="Status">
      <FormControl v-model="form.status" :options="statusOptions" />
    </FormField>
  </CardBoxModal>

  <CardBoxModal
    v-model="isDeleteModalActive"
    title="Remove record"
    button="danger"
    button-label="Remove"
    has-cancel
    @confirm="deleteAttendance"
  >
    <p>Are you sure you want to remove this attendance record?</p>
  </CardBoxModal>

  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiCalendarCheck" title="Attendance" main>
        <BaseButton :icon="mdiPlus" label="Record Attendance" color="info" @click="openCreateModal" />
      </SectionTitleLineWithButton>

      <div class="mb-6 grid grid-cols-1 gap-6 md:grid-cols-3">
        <FormField label="Employee">
          <FormControl v-model="filterEmployee" :options="employeeOptions" />
        </FormField>
        <FormField label="Month">
          <FormControl v-model="filterMonth" :options="monthOptions" />
        </FormField>
        <FormField label="Year">
          <FormControl v-model="filterYear" type="number" />
        </FormField>
      </div>

      <div class="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-4">
        <CardBoxWidget
          trend="This period"
          trend-type="up"
          color="text-emerald-500"
          :icon="mdiAccountCheck"
          :number="summaryCounts.present"
          label="Present"
        />
        <CardBoxWidget
          trend="This period"
          trend-type="down"
          color="text-red-500"
          :icon="mdiAccountCancel"
          :number="summaryCounts.absent"
          label="Absent"
        />
        <CardBoxWidget
          trend="This period"
          trend-type="alert"
          color="text-yellow-500"
          :icon="mdiAccountClock"
          :number="summaryCounts.leave"
          label="Leave"
        />
        <CardBoxWidget
          trend="This period"
          trend-type="alert"
          color="text-blue-500"
          :icon="mdiAccountMinus"
          :number="summaryCounts.half_day"
          label="Half Day"
        />
      </div>

      <CardBox has-table>
        <table>
          <thead>
            <tr>
              <th>Employee</th>
              <th>Date</th>
              <th>Status</th>
              <th />
            </tr>
          </thead>
          <tbody>
            <tr v-for="attendance in filteredAttendances" :key="attendance.id">
              <td data-label="Employee">{{ employeeMap[attendance.employee] }}</td>
              <td data-label="Date">{{ attendance.date }}</td>
              <td data-label="Status">
                <PillTag :label="statusLabel(attendance.status)" :color="statusPillColor[attendance.status]" small />
              </td>
              <td class="whitespace-nowrap before:hidden lg:w-1">
                <BaseButtons type="justify-start lg:justify-end" no-wrap>
                  <BaseButton color="info" :icon="mdiPencil" small @click="openEditModal(attendance)" />
                  <BaseButton color="danger" :icon="mdiTrashCan" small @click="confirmDelete(attendance)" />
                </BaseButtons>
              </td>
            </tr>
            <tr v-if="!filteredAttendances.length">
              <td colspan="4" class="text-center">No attendance records for this filter</td>
            </tr>
          </tbody>
        </table>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>

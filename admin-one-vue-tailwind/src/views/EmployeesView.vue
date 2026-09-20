<script setup>
import { ref, onMounted } from 'vue'
import QRCode from 'qrcode'
import { mdiAccountMultiple, mdiPlus, mdiPencil, mdiTrashCan, mdiQrcode, mdiKeyVariant } from '@mdi/js'
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
import FormCheckRadio from '@/components/FormCheckRadio.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'

const employees = ref([])

const employmentTypeOptions = [
  { id: 'full_time', label: 'Full Time' },
  { id: 'part_time', label: 'Part Time' },
  { id: 'contract', label: 'Contract' },
]

const emptyForm = () => ({
  id: null,
  employee_id: '',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  department: '',
  position: '',
  date_joined: '',
  is_active: true,
  national_id: '',
  bank_account_number: '',
  employment_type: employmentTypeOptions[0],
})

const form = ref(emptyForm())
const isModalActive = ref(false)
const isDeleteModalActive = ref(false)
const deleteTarget = ref(null)
const isQrModalActive = ref(false)
const qrEmployee = ref(null)
const qrDataUrl = ref('')
const checkInUrl = ref('')

const fetchEmployees = () => {
  api.get('employees/').then((result) => {
    employees.value = result.data
  })
}

const openCreateModal = () => {
  form.value = emptyForm()
  isModalActive.value = true
}

const openEditModal = (employee) => {
  form.value = {
    ...employee,
    employment_type: employmentTypeOptions.find((o) => o.id === employee.employment_type),
  }
  isModalActive.value = true
}

const submitForm = () => {
  const payload = { ...form.value }
  delete payload.salary_structure
  payload.employment_type = form.value.employment_type?.id ?? form.value.employment_type

  const request = payload.id
    ? api.put(`employees/${payload.id}/`, payload)
    : api.post('employees/', payload)

  request.then(() => {
    isModalActive.value = false
    fetchEmployees()
  })
}

const confirmDelete = (employee) => {
  deleteTarget.value = employee
  isDeleteModalActive.value = true
}

const deleteEmployee = () => {
  api.delete(`employees/${deleteTarget.value.id}/`).then(() => {
    isDeleteModalActive.value = false
    fetchEmployees()
  })
}

const openQrModal = (employee) => {
  qrEmployee.value = employee
  checkInUrl.value = `${window.location.origin}${import.meta.env.BASE_URL}#/check-in/${employee.qr_token}`
  QRCode.toDataURL(checkInUrl.value, { width: 240 }).then((dataUrl) => {
    qrDataUrl.value = dataUrl
  })
  isQrModalActive.value = true
}

const isLoginModalActive = ref(false)
const loginEmployee = ref(null)
const loginPassword = ref('')

const openLoginModal = (employee) => {
  loginEmployee.value = employee
  loginPassword.value = ''
  isLoginModalActive.value = true
}

const submitLogin = () => {
  api.patch(`employees/${loginEmployee.value.id}/`, { password: loginPassword.value }).then(() => {
    isLoginModalActive.value = false
    fetchEmployees()
  })
}

onMounted(fetchEmployees)
</script>

<template>
  <CardBoxModal
    v-model="isModalActive"
    :title="form.id ? 'Edit Employee' : 'Add Employee'"
    is-form
    button="success"
    :button-label="form.id ? 'Save' : 'Create'"
    has-cancel
    @confirm="submitForm"
  >
    <FormField label="Employee ID">
      <FormControl v-model="form.employee_id" required />
    </FormField>
    <FormField label="First name">
      <FormControl v-model="form.first_name" required />
    </FormField>
    <FormField label="Last name">
      <FormControl v-model="form.last_name" required />
    </FormField>
    <FormField label="Email">
      <FormControl v-model="form.email" type="email" required />
    </FormField>
    <FormField label="Phone">
      <FormControl v-model="form.phone" />
    </FormField>
    <FormField label="Department">
      <FormControl v-model="form.department" />
    </FormField>
    <FormField label="Position">
      <FormControl v-model="form.position" />
    </FormField>
    <FormField label="Date joined">
      <FormControl v-model="form.date_joined" type="date" required />
    </FormField>
    <FormField label="Employment type">
      <FormControl v-model="form.employment_type" :options="employmentTypeOptions" />
    </FormField>
    <FormField label="National ID">
      <FormControl v-model="form.national_id" />
    </FormField>
    <FormField label="Bank account number">
      <FormControl v-model="form.bank_account_number" />
    </FormField>
    <FormField>
      <FormCheckRadio
        name="is_active"
        label="Active"
        type="switch"
        v-model="form.is_active"
        :input-value="true"
      />
    </FormField>
  </CardBoxModal>

  <CardBoxModal
    v-model="isDeleteModalActive"
    title="Remove employee"
    button="danger"
    button-label="Remove"
    has-cancel
    @confirm="deleteEmployee"
  >
    <p>Are you sure you want to remove <b>{{ deleteTarget?.first_name }} {{ deleteTarget?.last_name }}</b>?</p>
  </CardBoxModal>

  <CardBoxModal v-model="isQrModalActive" title="Attendance QR Code" button="info" button-label="Close">
    <div class="text-center">
      <p class="mb-4">
        <b>{{ qrEmployee?.first_name }} {{ qrEmployee?.last_name }}</b> scans this once a day to check in.
      </p>
      <img v-if="qrDataUrl" :src="qrDataUrl" alt="Attendance QR code" class="mx-auto" />
      <p class="mt-4 text-xs break-all text-gray-500 dark:text-slate-400">{{ checkInUrl }}</p>
    </div>
  </CardBoxModal>

  <CardBoxModal
    v-model="isLoginModalActive"
    title="Set Login Password"
    is-form
    button="success"
    button-label="Save"
    has-cancel
    @confirm="submitLogin"
  >
    <p class="mb-4">
      Username for <b>{{ loginEmployee?.first_name }} {{ loginEmployee?.last_name }}</b> is their Employee ID:
      <b>{{ loginEmployee?.employee_id }}</b>
    </p>
    <FormField label="Password">
      <FormControl v-model="loginPassword" type="password" required />
    </FormField>
  </CardBoxModal>

  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiAccountMultiple" title="Employees" main>
        <BaseButton :icon="mdiPlus" label="Add Employee" color="info" @click="openCreateModal" />
      </SectionTitleLineWithButton>

      <CardBox has-table>
        <table>
          <thead>
            <tr>
              <th>Employee ID</th>
              <th>Name</th>
              <th>Department</th>
              <th>Position</th>
              <th>Employment Type</th>
              <th>Date joined</th>
              <th>Status</th>
              <th>Login</th>
              <th />
            </tr>
          </thead>
          <tbody>
            <tr v-for="employee in employees" :key="employee.id">
              <td data-label="Employee ID">{{ employee.employee_id }}</td>
              <td data-label="Name">{{ employee.first_name }} {{ employee.last_name }}</td>
              <td data-label="Department">{{ employee.department }}</td>
              <td data-label="Position">{{ employee.position }}</td>
              <td data-label="Employment Type">{{ employmentTypeOptions.find((o) => o.id === employee.employment_type)?.label }}</td>
              <td data-label="Date joined">{{ employee.date_joined }}</td>
              <td data-label="Status">
                <PillTag
                  :label="employee.is_active ? 'Active' : 'Inactive'"
                  :color="employee.is_active ? 'success' : 'danger'"
                  small
                />
              </td>
              <td data-label="Login">
                <PillTag
                  :label="employee.has_login ? 'Enabled' : 'None'"
                  :color="employee.has_login ? 'success' : 'light'"
                  small
                />
              </td>
              <td class="whitespace-nowrap before:hidden lg:w-1">
                <BaseButtons type="justify-start lg:justify-end" no-wrap>
                  <BaseButton color="success" :icon="mdiQrcode" small @click="openQrModal(employee)" />
                  <BaseButton color="whiteDark" :icon="mdiKeyVariant" small @click="openLoginModal(employee)" />
                  <BaseButton color="info" :icon="mdiPencil" small @click="openEditModal(employee)" />
                  <BaseButton color="danger" :icon="mdiTrashCan" small @click="confirmDelete(employee)" />
                </BaseButtons>
              </td>
            </tr>
            <tr v-if="!employees.length">
              <td colspan="9" class="text-center">No employees yet</td>
            </tr>
          </tbody>
        </table>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>

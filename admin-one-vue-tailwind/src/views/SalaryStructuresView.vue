<script setup>
import { ref, onMounted, computed } from 'vue'
import { mdiCurrencyUsd, mdiPlus, mdiTrashCan } from '@mdi/js'
import api from '@/lib/api.js'
import SectionMain from '@/components/SectionMain.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import CardBox from '@/components/CardBox.vue'
import CardBoxModal from '@/components/CardBoxModal.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'

const employees = ref([])
const structures = ref([])

const emptyForm = () => ({
  employee: '',
  basic_salary: '',
  house_allowance: 0,
  transport_allowance: 0,
  tax_deduction: 0,
  other_deduction: 0,
  effective_date: '',
})

const form = ref(emptyForm())
const isModalActive = ref(false)
const isDeleteModalActive = ref(false)
const deleteTarget = ref(null)

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

const fetchStructures = () => {
  api.get('salary-structures/').then((result) => {
    structures.value = result.data
  })
}

const openCreateModal = () => {
  form.value = emptyForm()
  isModalActive.value = true
}

const submitForm = () => {
  const payload = {
    ...form.value,
    employee: form.value.employee?.id ?? form.value.employee,
  }

  api.post('salary-structures/', payload).then(() => {
    isModalActive.value = false
    fetchStructures()
  })
}

const confirmDelete = (structure) => {
  deleteTarget.value = structure
  isDeleteModalActive.value = true
}

const deleteStructure = () => {
  api.delete(`salary-structures/${deleteTarget.value.id}/`).then(() => {
    isDeleteModalActive.value = false
    fetchStructures()
  })
}

onMounted(() => {
  fetchEmployees()
  fetchStructures()
})
</script>

<template>
  <CardBoxModal
    v-model="isModalActive"
    title="Set Salary Structure"
    is-form
    button="success"
    button-label="Save"
    has-cancel
    @confirm="submitForm"
  >
    <FormField label="Employee">
      <FormControl
        v-model="form.employee"
        :options="employees.map((e) => ({ id: e.id, label: `${e.first_name} ${e.last_name}` }))"
      />
    </FormField>
    <FormField label="Basic salary">
      <FormControl v-model="form.basic_salary" type="number" required />
    </FormField>
    <FormField label="House allowance">
      <FormControl v-model="form.house_allowance" type="number" />
    </FormField>
    <FormField label="Transport allowance">
      <FormControl v-model="form.transport_allowance" type="number" />
    </FormField>
    <FormField label="Tax deduction">
      <FormControl v-model="form.tax_deduction" type="number" />
    </FormField>
    <FormField label="Other deduction">
      <FormControl v-model="form.other_deduction" type="number" />
    </FormField>
    <FormField label="Effective date">
      <FormControl v-model="form.effective_date" type="date" required />
    </FormField>
  </CardBoxModal>

  <CardBoxModal
    v-model="isDeleteModalActive"
    title="Remove salary structure"
    button="danger"
    button-label="Remove"
    has-cancel
    @confirm="deleteStructure"
  >
    <p>Are you sure you want to remove this salary structure?</p>
  </CardBoxModal>

  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiCurrencyUsd" title="Salary Structures" main>
        <BaseButton :icon="mdiPlus" label="Set Salary" color="info" @click="openCreateModal" />
      </SectionTitleLineWithButton>

      <CardBox has-table>
        <table>
          <thead>
            <tr>
              <th>Employee</th>
              <th>Basic salary</th>
              <th>House allowance</th>
              <th>Transport allowance</th>
              <th>Tax deduction</th>
              <th>Other deduction</th>
              <th>Effective date</th>
              <th />
            </tr>
          </thead>
          <tbody>
            <tr v-for="structure in structures" :key="structure.id">
              <td data-label="Employee">{{ employeeMap[structure.employee] }}</td>
              <td data-label="Basic salary">{{ structure.basic_salary }}</td>
              <td data-label="House allowance">{{ structure.house_allowance }}</td>
              <td data-label="Transport allowance">{{ structure.transport_allowance }}</td>
              <td data-label="Tax deduction">{{ structure.tax_deduction }}</td>
              <td data-label="Other deduction">{{ structure.other_deduction }}</td>
              <td data-label="Effective date">{{ structure.effective_date }}</td>
              <td class="whitespace-nowrap before:hidden lg:w-1">
                <BaseButtons type="justify-start lg:justify-end" no-wrap>
                  <BaseButton color="danger" :icon="mdiTrashCan" small @click="confirmDelete(structure)" />
                </BaseButtons>
              </td>
            </tr>
            <tr v-if="!structures.length">
              <td colspan="8" class="text-center">No salary structures yet</td>
            </tr>
          </tbody>
        </table>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>

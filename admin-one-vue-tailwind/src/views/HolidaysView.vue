<script setup>
import { ref, onMounted } from 'vue'
import { mdiCalendarStar, mdiPlus, mdiPencil, mdiTrashCan } from '@mdi/js'
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

const holidays = ref([])

const emptyForm = () => ({
  id: null,
  name: '',
  date: '',
  description: '',
})

const form = ref(emptyForm())
const isModalActive = ref(false)
const isDeleteModalActive = ref(false)
const deleteTarget = ref(null)

const fetchHolidays = () => {
  api.get('holidays/').then((result) => {
    holidays.value = result.data
  })
}

const openCreateModal = () => {
  form.value = emptyForm()
  isModalActive.value = true
}

const openEditModal = (holiday) => {
  form.value = { ...holiday }
  isModalActive.value = true
}

const submitForm = () => {
  const request = form.value.id
    ? api.put(`holidays/${form.value.id}/`, form.value)
    : api.post('holidays/', form.value)

  request.then(() => {
    isModalActive.value = false
    fetchHolidays()
  })
}

const confirmDelete = (holiday) => {
  deleteTarget.value = holiday
  isDeleteModalActive.value = true
}

const deleteHoliday = () => {
  api.delete(`holidays/${deleteTarget.value.id}/`).then(() => {
    isDeleteModalActive.value = false
    fetchHolidays()
  })
}

onMounted(fetchHolidays)
</script>

<template>
  <CardBoxModal
    v-model="isModalActive"
    :title="form.id ? 'Edit Holiday' : 'Add Holiday'"
    is-form
    button="success"
    :button-label="form.id ? 'Save' : 'Create'"
    has-cancel
    @confirm="submitForm"
  >
    <FormField label="Name">
      <FormControl v-model="form.name" required />
    </FormField>
    <FormField label="Date">
      <FormControl v-model="form.date" type="date" required />
    </FormField>
    <FormField label="Description">
      <FormControl v-model="form.description" type="textarea" />
    </FormField>
  </CardBoxModal>

  <CardBoxModal
    v-model="isDeleteModalActive"
    title="Remove holiday"
    button="danger"
    button-label="Remove"
    has-cancel
    @confirm="deleteHoliday"
  >
    <p>Are you sure you want to remove <b>{{ deleteTarget?.name }}</b>?</p>
  </CardBoxModal>

  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiCalendarStar" title="Holidays" main>
        <BaseButton :icon="mdiPlus" label="Add Holiday" color="info" @click="openCreateModal" />
      </SectionTitleLineWithButton>

      <CardBox has-table>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Date</th>
              <th>Description</th>
              <th />
            </tr>
          </thead>
          <tbody>
            <tr v-for="holiday in holidays" :key="holiday.id">
              <td data-label="Name">{{ holiday.name }}</td>
              <td data-label="Date">{{ holiday.date }}</td>
              <td data-label="Description">{{ holiday.description }}</td>
              <td class="whitespace-nowrap before:hidden lg:w-1">
                <BaseButtons type="justify-start lg:justify-end" no-wrap>
                  <BaseButton color="info" :icon="mdiPencil" small @click="openEditModal(holiday)" />
                  <BaseButton color="danger" :icon="mdiTrashCan" small @click="confirmDelete(holiday)" />
                </BaseButtons>
              </td>
            </tr>
            <tr v-if="!holidays.length">
              <td colspan="4" class="text-center">No holidays scheduled yet</td>
            </tr>
          </tbody>
        </table>
      </CardBox>
    </SectionMain>
  </LayoutAuthenticated>
</template>

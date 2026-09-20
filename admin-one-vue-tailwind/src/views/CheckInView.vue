<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { mdiCheckCircle, mdiAlertCircle, mdiClockOutline } from '@mdi/js'
import api from '@/lib/api.js'
import SectionFullScreen from '@/components/SectionFullScreen.vue'
import CardBox from '@/components/CardBox.vue'
import BaseIcon from '@/components/BaseIcon.vue'
import LayoutGuest from '@/layouts/LayoutGuest.vue'

const route = useRoute()

const state = ref('loading')
const result = ref(null)
const errorMessage = ref('')

onMounted(() => {
  api
    .post('attendances/check-in/', { token: route.params.token })
    .then((response) => {
      result.value = response.data
      state.value = 'success'
    })
    .catch((error) => {
      errorMessage.value = error?.response?.data?.detail ?? 'Something went wrong. Please try again.'
      state.value = 'error'
    })
})
</script>

<template>
  <LayoutGuest>
    <SectionFullScreen v-slot="{ cardClass }" bg="purplePink">
      <CardBox :class="cardClass" class="text-center">
        <div v-if="state === 'loading'" class="py-6">
          <BaseIcon :path="mdiClockOutline" size="64" w="w-16" h="h-16" class="mx-auto mb-4 text-gray-400" />
          <p>Checking you in...</p>
        </div>

        <div v-else-if="state === 'success'" class="py-6">
          <BaseIcon :path="mdiCheckCircle" size="64" w="w-16" h="h-16" class="mx-auto mb-4 text-emerald-500" />
          <h1 class="mb-2 text-xl font-bold">
            {{ result.already_checked_in ? 'Already checked in' : 'Checked in!' }}
          </h1>
          <p class="mb-1">{{ result.employee_name }}</p>
          <p class="text-gray-500 dark:text-slate-400">{{ result.date }} — {{ result.check_in }}</p>
        </div>

        <div v-else class="py-6">
          <BaseIcon :path="mdiAlertCircle" size="64" w="w-16" h="h-16" class="mx-auto mb-4 text-red-500" />
          <h1 class="mb-2 text-xl font-bold">Check-in failed</h1>
          <p class="text-gray-500 dark:text-slate-400">{{ errorMessage }}</p>
        </div>
      </CardBox>
    </SectionFullScreen>
  </LayoutGuest>
</template>

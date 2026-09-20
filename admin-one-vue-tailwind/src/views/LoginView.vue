<script setup>
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { mdiAccount, mdiAsterisk } from '@mdi/js'
import { useAuthStore } from '@/stores/auth.js'
import SectionFullScreen from '@/components/SectionFullScreen.vue'
import CardBox from '@/components/CardBox.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import LayoutGuest from '@/layouts/LayoutGuest.vue'

const form = reactive({
  username: '',
  password: '',
})

const errorMessage = ref('')
const isSubmitting = ref(false)

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const submit = () => {
  errorMessage.value = ''
  isSubmitting.value = true

  authStore
    .login(form.username, form.password)
    .then(() => {
      const fallback = authStore.role === 'admin' ? '/dashboard' : '/my-portal'
      router.push(route.query.redirect || fallback)
    })
    .catch(() => {
      errorMessage.value = 'Invalid username or password.'
    })
    .finally(() => {
      isSubmitting.value = false
    })
}
</script>

<template>
  <LayoutGuest>
    <SectionFullScreen v-slot="{ cardClass }" bg="purplePink">
      <CardBox :class="cardClass" is-form @submit.prevent="submit">
        <FormField label="Username" help="Your login or employee ID">
          <FormControl v-model="form.username" :icon="mdiAccount" name="username" autocomplete="username" />
        </FormField>

        <FormField label="Password" help="Please enter your password">
          <FormControl
            v-model="form.password"
            :icon="mdiAsterisk"
            type="password"
            name="password"
            autocomplete="current-password"
          />
        </FormField>

        <p v-if="errorMessage" class="mb-4 text-red-600 dark:text-red-500">{{ errorMessage }}</p>

        <template #footer>
          <BaseButtons>
            <BaseButton type="submit" color="info" label="Login" :disabled="isSubmitting" />
          </BaseButtons>
        </template>
      </CardBox>
    </SectionFullScreen>
  </LayoutGuest>
</template>

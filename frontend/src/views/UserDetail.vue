<!-- src/views/UserDetail.vue -->
<template>
  <div v-if="user" class="user-detail-container p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl">User Details</h1>
      <div class="flex gap-2">
        <Button label="Edit" icon="pi pi-pencil" class="p-button-warning" @click="editUser" />
        <Button label="Delete" icon="pi pi-trash" class="p-button-danger" @click="confirmDelete" />
      </div>
    </div>

    <div class="grid">
      <div class="col-12 md:col-6">
        <div class="p-3 surface-100 border-round">
          <div class="mb-3">
            <label class="block text-600 mb-2">Username</label>
            <p class="text-900 font-medium">{{ user.username }}</p>
          </div>
          <div class="mb-3">
            <label class="block text-600 mb-2">Roles</label>
            <p class="text-900 font-medium">{{ user.roles.join(', ') }}</p>
          </div>
          <div class="mb-3">
            <label class="block text-600 mb-2">Timezone</label>
            <p class="text-900 font-medium">{{ user.preferences.timezone }}</p>
          </div>
          <div class="mb-3">
            <label class="block text-600 mb-2">Account Status</label>
            <p class="text-900 font-medium">
              <i
                :class="
                  user.active
                    ? 'pi pi-check-circle text-green-500'
                    : 'pi pi-times-circle text-red-500'
                "
              ></i>
              {{ user.active ? 'Active' : 'Inactive' }}
            </p>
          </div>
          <div>
            <label class="block text-600 mb-2">Created At</label>
            <p class="text-900 font-medium">
              {{ new Date(user.created_ts * 1000).toLocaleString() }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- User Edit Dialog -->
    <Dialog v-model:visible="userDialogVisible" header="Edit User" modal class="p-fluid">
      <div class="p-field">
        <label>Username</label>
        <InputText v-model="editedUser.username" />
      </div>
      <div class="p-field">
        <label>Password</label>
        <InputText
          type="password"
          v-model="editedUser.password"
          placeholder="Leave blank to keep current password"
        />
      </div>
      <div class="p-field">
        <label>Roles</label>
        <Dropdown v-model="editedUser.roles" :options="roleOptions" multiple />
      </div>
      <div class="p-field">
        <label>Timezone</label>
        <Dropdown v-model="editedUser.preferences.timezone" :options="timezoneOptions" />
      </div>
      <div class="p-field">
        <label>Account Status</label>
        <Dropdown
          v-model="editedUser.active"
          :options="[
            { label: 'Active', value: true },
            { label: 'Inactive', value: false },
          ]"
        />
      </div>
      <template #footer>
        <Button
          label="Cancel"
          icon="pi pi-times"
          class="p-button-text"
          @click="userDialogVisible = false"
        />
        <Button label="Update" icon="pi pi-check" @click="saveUser" />
      </template>
    </Dialog>

    <!-- Confirmation Dialog -->
    <Dialog v-model:visible="deleteConfirmVisible" header="Confirm Delete" modal>
      <p>Are you sure you want to delete this user?</p>
      <template #footer>
        <Button
          label="No"
          icon="pi pi-times"
          class="p-button-text"
          @click="deleteConfirmVisible = false"
        />
        <Button label="Yes" icon="pi pi-check" class="p-button-danger" @click="deleteUser" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const user = ref(null)
const userDialogVisible = ref(false)
const deleteConfirmVisible = ref(false)
const editedUser = ref(null)

// Predefined options
const roleOptions = ['admin', 'manager', 'tester']
const timezoneOptions = [
  'America/New_York',
  'Europe/London',
  'Asia/Tokyo',
  'Australia/Sydney',
  'Europe/Berlin',
  // Add more timezones as needed
]

// Fetch user details
const fetchUserDetails = async () => {
  try {
    const response = await axios.get(`/users/${route.params.id}`)
    user.value = response.data
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to fetch user details',
      life: 3000,
    })
  }
}

// Open edit dialog
const editUser = () => {
  editedUser.value = { ...user.value }
  userDialogVisible.value = true
}

// Save user
const saveUser = async () => {
  try {
    await axios.put(`/users/${route.params.id}`, editedUser.value)
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'User updated successfully',
      life: 3000,
    })

    // Refresh user details
    await fetchUserDetails()
    userDialogVisible.value = false
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.response?.data?.error || 'Failed to update user',
      life: 3000,
    })
  }
}

// Confirm delete
const confirmDelete = () => {
  deleteConfirmVisible.value = true
}

// Delete user
const deleteUser = async () => {
  try {
    await axios.delete(`/users/${route.params.id}`)
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'User deleted successfully',
      life: 3000,
    })
    router.push('/')
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to delete user',
      life: 3000,
    })
  }
}

// Fetch user details on component mount
onMounted(fetchUserDetails)
</script>

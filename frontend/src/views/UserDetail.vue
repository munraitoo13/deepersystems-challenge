<template>
  <div v-if="user" class="user-detail-container">
    <!-- heading -->
    <div class="heading">
      <h1 class="text-2xl">User Details</h1>

      <div class="actions-btns">
        <Button label="Edit" icon="pi pi-pencil" class="p-button-warning" @click="confirmEdit" />
        <Button label="Delete" icon="pi pi-trash" class="p-button-danger" @click="confirmDelete" />
      </div>
    </div>

    <!-- user details -->
    <div class="details-card">
      <div class="details">
        <div>
          <label class="card-label">Username</label>
          <p class="text-900 font-medium">{{ user.username }}</p>
        </div>

        <div>
          <label class="card-label">Roles</label>
          <p class="text-900 font-medium">{{ user.roles.join(', ') }}</p>
        </div>

        <div>
          <label class="card-label">Timezone</label>
          <p class="text-900 font-medium">{{ user.preferences.timezone }}</p>
        </div>

        <div>
          <label class="card-label">Account Status</label>
          <p class="text-900 font-medium">
            {{ user.active ? 'Active' : 'Inactive' }}
          </p>
        </div>

        <div>
          <label class="card-label">Created At</label>
          <p class="text-900 font-medium">
            {{ new Date(user.created_ts * 1000).toLocaleString() }}
          </p>
        </div>

        <div>
          <label class="card-label">Updated At</label>
          <p class="text-900 font-medium">
            {{ user.updated_ts ? new Date(user.updated_ts * 1000).toLocaleString() : 'N/A' }}
          </p>
        </div>
      </div>
    </div>

    <!-- edit user dialog -->
    <Dialog v-model:visible="userDialogVisible" header="Edit User" modal class="p-fluid">
      <Fluid class="edit-user-form">
        <div>
          <label>Username</label>
          <InputText v-model="editedUser.username" />
        </div>

        <div>
          <label>Password</label>
          <InputText
            type="password"
            v-model="editedUser.password"
            placeholder="Leave blank to keep current password"
          />
        </div>

        <div>
          <label>Roles</label>
          <MultiSelect v-model="editedUser.roles" :options="roleOptions" />
        </div>

        <div>
          <label>Timezone</label>
          <Select v-model="editedUser.preferences.timezone" :options="timezoneOptions" />
        </div>

        <div>
          <label>Account Status</label>
          <Select
            v-model="editedUser.active"
            :options="[
              { label: 'Active', value: true },
              { label: 'Inactive', value: false },
            ]"
            option-label="label"
            option-value="value"
          />
        </div>
      </Fluid>

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

    <!-- delete confirm dialog -->
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

    <!-- edit confirm dialog -->
    <Dialog v-model:visible="editConfirmVisible" header="Confirm Edit" modal>
      <p>Are you sure you want to edit this user?</p>
      <template #footer>
        <Button
          label="No"
          icon="pi pi-times"
          class="p-button-text"
          @click="editConfirmVisible = false"
        />
        <Button label="Yes" icon="pi pi-check" class="p-button-danger" @click="editUser" />
      </template>
    </Dialog>
  </div>
</template>

<style>
.user-detail-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}
.actions-btns {
  display: flex;
  gap: 1rem;
}
.heading {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}
.details-card {
  background: #fff;
  padding: 2rem 3rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: fit-content;
}
.details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}
.card-label {
  font-weight: bold;
  font-size: 1.5rem;
}
.details p {
  margin-top: 0.25rem;
}
.edit-user-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>

<script setup>
import { ref, onMounted } from 'vue'
import { timezoneOptions, roleOptions } from '@/constants/constants'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import instance from '@/plugins/axios'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const user = ref(null)
const userDialogVisible = ref(false)
const deleteConfirmVisible = ref(false)
const editedUser = ref(null)
const editConfirmVisible = ref(false)

// Fetch user details
const fetchUserDetails = async () => {
  try {
    const response = await instance.get(`/users/${route.params.id}`)
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
  editConfirmVisible.value = false
  userDialogVisible.value = true
}

// Save user
const saveUser = async () => {
  try {
    await instance.put(`/users/${route.params.id}`, editedUser.value)
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

// Confirm delete
const confirmEdit = () => {
  editConfirmVisible.value = true
}

// Delete user
const deleteUser = async () => {
  try {
    await instance.delete(`/users/${route.params.id}`)
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

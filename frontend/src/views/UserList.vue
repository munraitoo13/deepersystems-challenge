<template>
  <div class="user-list-container p-4">
    <h1 class="text-2xl mb-4">User Management</h1>

    <Button label="Create New User" icon="pi pi-plus" class="mb-4" @click="openCreateUserDialog" />

    <!-- users table -->
    <DataTable :value="users" :loading="loading" class="p-datatable-striped">
      <Column field="username" header="Username">
        <template #body="{ data }">
          <router-link
            :to="{ name: 'UserDetail', params: { id: data._id } }"
            class="text-blue-600 hover:underline"
          >
            {{ data.username }}
          </router-link>
        </template>
      </Column>
      <Column field="roles" header="Roles">
        <template #body="{ data }">
          {{ data.roles.join(', ') }}
        </template>
      </Column>
      <Column field="preferences.timezone" header="Timezone">
        <template #body="{ data }">
          {{ data.preferences.timezone }}
        </template>
      </Column>
      <Column header="Active">
        <template #body="{ data }">
          <i :class="data.active ? 'pi pi-check text-green-500' : 'pi pi-times text-red-500'"></i>
        </template>
      </Column>
      <Column header="Actions">
        <template #body="{ data }">
          <div class="flex gap-2">
            <Button
              icon="pi pi-pencil"
              class="p-button-warning p-button-sm"
              @click="confirmEdit(data)"
            />
            <Button
              icon="pi pi-trash"
              class="p-button-danger p-button-sm"
              @click="confirmDelete(data)"
            />
          </div>
        </template>
      </Column>
    </DataTable>

    <!-- create/edit dialog -->
    <Dialog v-model:visible="userDialogVisible" :header="dialogHeader" modal class="p-fluid">
      <div class="p-field">
        <label>Username</label>
        <InputText v-model="currentUser.username" />
      </div>
      <div class="p-field">
        <label>Password</label>
        <InputText
          type="password"
          v-model="currentUser.password"
          :placeholder="isEditing ? 'Leave blank to keep current password' : ''"
        />
      </div>
      <div class="p-field">
        <label>Roles</label>
        <Dropdown v-model="currentUser.roles" :options="roleOptions" multiple />
      </div>
      <div class="p-field">
        <label>Timezone</label>
        <Dropdown v-model="currentUser.preferences.timezone" :options="timezoneOptions" />
      </div>
      <template #footer>
        <Button
          label="Cancel"
          icon="pi pi-times"
          class="p-button-text"
          @click="userDialogVisible = false"
        />
        <Button :label="isEditing ? 'Update' : 'Create'" icon="pi pi-check" @click="saveUser" />
      </template>
    </Dialog>

    <!-- delete confirmation dialog -->
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

    <!-- edit confirmation dialog -->
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

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import instance from '@/plugins/axios'

const toast = useToast()
const users = ref([])
const loading = ref(false)
import { timezoneOptions, roleOptions } from '@/constants/constants'
const userDialogVisible = ref(false)
const deleteConfirmVisible = ref(false)
const editConfirmVisible = ref(false)
const currentUser = ref({
  username: '',
  password: '',
  roles: [],
  preferences: { timezone: '' },
})
const isEditing = ref(false)
const userToDelete = ref(null)
const userToEdit = ref(null)

// fetch all users
const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await instance.get('/users')
    users.value = response.data
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to fetch users',
      life: 3000,
    })
  } finally {
    loading.value = false
  }
}

// open create user dialog
const openCreateUserDialog = () => {
  currentUser.value = {
    username: '',
    password: '',
    roles: [],
    preferences: { timezone: '' },
  }
  isEditing.value = false
  userDialogVisible.value = true
}

// Confirm edit
const confirmEdit = (user) => {
  userToEdit.value = user
  editConfirmVisible.value = true
}

// edits user
const editUser = (user) => {
  currentUser.value = { ...userToEdit.value }
  isEditing.value = true
  userDialogVisible.value = true
  editConfirmVisible.value = false
}

// saves user (create or update)
const saveUser = async () => {
  try {
    if (isEditing.value) {
      await instance.put(`/users/${currentUser.value._id}`, currentUser.value)
      toast.add({
        severity: 'success',
        summary: 'Success',
        detail: 'User updated successfully',
        life: 3000,
      })
    } else {
      await instance.post('/users', currentUser.value)
      toast.add({
        severity: 'success',
        summary: 'Success',
        detail: 'User created successfully',
        life: 3000,
      })
    }

    fetchUsers()
    userDialogVisible.value = false
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.response?.data?.error || 'Failed to save user',
      life: 3000,
    })
  }
}

// confirm deletion
const confirmDelete = (user) => {
  userToDelete.value = user
  deleteConfirmVisible.value = true
}

// deletes user
const deleteUser = async () => {
  try {
    await instance.delete(`/users/${userToDelete.value._id}`)
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'User deleted successfully',
      life: 3000,
    })
    fetchUsers()
    deleteConfirmVisible.value = false
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to delete user',
      life: 3000,
    })
  }
}

// fetch users on component mount
onMounted(fetchUsers)
</script>

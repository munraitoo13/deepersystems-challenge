<template>
  <div class="container">
    <h1 class="heading">User Management</h1>

    <Button
      label="Create User"
      icon="pi pi-plus"
      class="new-user-btn"
      @click="openCreateUserDialog"
    />

    <!-- users table -->
    <DataTable :value="users" :loading="loading" class="p-datatable-striped">
      <Column field="username" header="Username">
        <template #body="{ data }">
          <router-link :to="{ name: 'UserDetail', params: { id: data._id } }" class="user-link">
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
      <Column header="Updated At">
        <template #body="{ data }">
          {{
            data.updated_ts
              ? new Date(data.updated_ts * 1000).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: '2-digit',
                  day: '2-digit',
                })
              : 'N/A'
          }}
        </template>
      </Column>
      <Column header="Created At">
        <template #body="{ data }">
          {{
            new Date(data.created_ts * 1000).toLocaleDateString('en-US', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
            })
          }}
        </template>
      </Column>
      <Column header="Actions">
        <template #body="{ data }">
          <div class="action-btns">
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
      <Fluid class="create-edit-form">
        <div class="">
          <label>Username</label>
          <InputText v-model="currentUser.username" />
        </div>
        <div class="">
          <label>Password</label>
          <InputText
            type="password"
            v-model="currentUser.password"
            :placeholder="isEditing ? 'Leave blank to keep current password' : ''"
          />
        </div>
        <div class="">
          <label>Roles</label>
          <MultiSelect v-model="currentUser.roles" :options="roleOptions" multiple />
        </div>
        <div class="">
          <label>Timezone</label>
          <Select v-model="currentUser.preferences.timezone" :options="timezoneOptions" />
        </div>
        <div>
          <label>Account Status</label>
          <Select
            v-model="currentUser.active"
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
  active: true,
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
    active: true,
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
  currentUser.value.active = currentUser.value.active ?? 'true'

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

<style scoped>
.heading {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.new-user-btn {
  margin-bottom: 1rem;
}

.action-btns {
  display: flex;
  gap: 0.5rem;
}

.user-link {
  text-decoration: none;
  color: #34d399;
}
.user-link:hover {
  text-decoration: underline;
}
.create-edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>

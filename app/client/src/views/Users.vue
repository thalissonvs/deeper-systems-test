<template>
  <v-container>
    <v-card>
      <v-card-title>
        User List
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      
      <v-data-table
        :headers="headers"
        :items="users"
        :search="search"
        :loading="loading"
        class="elevation-1"
        item-value="_id"
      >
        <template #[`item.username`]="props">
          <a 
            @click="viewUser(props.item)" 
            class="clickable-username"
          >
            {{ props.item.username }}
          </a>
        </template>
        
        <template #[`item.active`]="props">
          <v-chip
            :color="props.item.active ? 'green' : 'red'"
            :text-color="'white'"
            size="small"
          >
            {{ props.item.active ? 'Active' : 'Inactive' }}
          </v-chip>
        </template>
        
        <template #[`item.actions`]="props">
          <div class="d-flex">
            <v-icon
              size="small"
              class="mr-2"
              @click="editUser(props.item)"
            >
              mdi-pencil
            </v-icon>
            <v-icon
              size="small"
              @click="deleteUser(props.item)"
            >
              mdi-delete
            </v-icon>
          </div>
        </template>
      </v-data-table>
      
      <v-card-actions>
        <v-btn
          color="primary"
          @click="openNewUserDialog"
        >
          New User
        </v-btn>
      </v-card-actions>
    </v-card>
    
    <!-- Dialog for adding/editing user form -->
    <v-dialog
      v-model="dialog"
      max-width="500px"
    >
      <v-card>
        <v-card-title>
          {{ formTitle }}
        </v-card-title>
        
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.username"
                  label="Username"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.password"
                  label="Password"
                  type="password"
                  :disabled="editMode"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-checkbox
                  v-model="editedItem.active"
                  label="Active"
                ></v-checkbox>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.preferences.timezone"
                  label="Timezone"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-combobox
                  v-model="editedItem.roles"
                  label="Roles"
                  multiple
                  chips
                ></v-combobox>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="close"
          >
            Cancel
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="dialogConfirmEdit = true"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Dialog to confirm edit -->
    <v-dialog
      v-model="dialogConfirmEdit"
      max-width="500px"
    >
      <v-card>
        <v-card-title class="text-h5">Confirm User Changes</v-card-title>
        <v-card-text>
          Are you sure you want to save these changes?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="dialogConfirmEdit = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="confirmEdit"
          >
            Confirm
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Dialog to confirm deletion -->
    <v-dialog
      v-model="dialogDelete"
      max-width="500px"
    >
      <v-card>
        <v-card-title class="text-h5">Are you sure you want to delete this user?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="closeDelete"
          >
            Cancel
          </v-btn>
          <v-btn
            color="red darken-1"
            text
            @click="deleteItemConfirm"
          >
            Confirm
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '../api/config'

export default {
  name: 'UsersPage',
  setup() {
    // Router and route
    const router = useRouter()
    const route = useRoute()
    
    // Reactive state
    const search = ref('')
    const loading = ref(false)
    const dialog = ref(false)
    const dialogDelete = ref(false)
    const dialogConfirmEdit = ref(false)
    const editMode = ref(false)
    const users = ref([])
    const editedIndex = ref(-1)
    
    const headers = [
      { title: 'Username', align: 'start', sortable: true, key: 'username' },
      { title: 'Roles', align: 'start', sortable: true, key: 'rolesAsString' },
      { title: 'Timezone', align: 'start', sortable: true, key: 'timezone' },
      { title: 'Is Active?', align: 'center', sortable: true, key: 'active' },
      { title: 'Last Updated At', align: 'start', sortable: true, key: 'updated_ts_formatted' },
      { title: 'Created At', align: 'start', sortable: true, key: 'created_ts_formatted' },
      { title: 'Actions', align: 'center', sortable: false, key: 'actions' }
    ]
    
    const defaultItem = {
      username: '',
      password: '',
      roles: [],
      preferences: {
        timezone: 'UTC'
      },
      active: true
    }
    
    const editedItem = reactive({...defaultItem})
    
    // Computed properties
    const formTitle = computed(() => {
      return editedIndex.value === -1 ? 'New User' : 'Edit User'
    })
    
    // Methods
    const fetchUsers = async () => {
      loading.value = true
      try {
        const response = await apiClient.get('/users')
        users.value = response.data.map(user => {
          const preferences = user.preferences || { timezone: 'UTC' }
          return {
            ...user,
            rolesAsString: (user.roles || []).join(', '),
            created_ts_formatted: formatDate(user.created_ts),
            updated_ts_formatted: formatDate(user.updated_ts || user.created_ts),
            timezone: preferences.timezone || 'UTC',
            preferences: preferences
          }
        })
        console.log('Processed data:', users.value)
      } catch (err) {
        console.error('Error loading users:', err)
      } finally {
        loading.value = false
      }
    }
    
    const formatDate = (timestamp) => {
      if (!timestamp) return 'N/A'
      
      const date = new Date(timestamp * 1000)
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }
    
    const viewUser = (item) => {
      router.push({ name: 'UserDetails', params: { id: item._id } })
    }
    
    const editUser = (item) => {
      editedIndex.value = users.value.indexOf(item)
      Object.assign(editedItem, item)
      editMode.value = true
      dialog.value = true
    }
    
    const deleteUser = (item) => {
      editedIndex.value = users.value.indexOf(item)
      Object.assign(editedItem, item)
      dialogDelete.value = true
    }
    
    const openNewUserDialog = () => {
      Object.assign(editedItem, defaultItem)
      editMode.value = false
      dialog.value = true
    }
    
    const deleteItemConfirm = async () => {
      try {
        await apiClient.delete(`/users/${editedItem._id}`)
        users.value.splice(editedIndex.value, 1)
      } catch (err) {
        console.error('Error deleting user:', err)
      }
      closeDelete()
    }
    
    const confirmEdit = async () => {
      await save()
      dialogConfirmEdit.value = false
    }
    
    const save = async () => {
      if (editedIndex.value > -1) {
        // Editing existing user
        try {
          const response = await apiClient.put(`/users/${editedItem._id}`, editedItem)
          // Add formatted fields to result
          const userData = response.data
          const preferences = userData.preferences || { timezone: 'UTC' }
          const updatedUser = {
            ...userData,
            rolesAsString: (userData.roles || []).join(', '),
            created_ts_formatted: formatDate(userData.created_ts),
            updated_ts_formatted: formatDate(userData.updated_ts || userData.created_ts),
            timezone: preferences.timezone || 'UTC',
            preferences: preferences
          }
          Object.assign(users.value[editedIndex.value], updatedUser)
        } catch (err) {
          console.error('Error updating user:', err)
        }
      } else {
        // Creating new user
        try {
          const response = await apiClient.post('/users', editedItem)
          // Add formatted fields to result
          const userData = response.data
          const preferences = userData.preferences || { timezone: 'UTC' }
          const newUser = {
            ...userData,
            rolesAsString: (userData.roles || []).join(', '),
            created_ts_formatted: formatDate(userData.created_ts),
            updated_ts_formatted: formatDate(userData.updated_ts || userData.created_ts),
            timezone: preferences.timezone || 'UTC',
            preferences: preferences
          }
          users.value.push(newUser)
        } catch (err) {
          console.error('Error creating user:', err)
        }
      }
      close()
    }
    
    const close = () => {
      dialog.value = false
      setTimeout(() => {
        Object.assign(editedItem, defaultItem)
        editedIndex.value = -1
      })
    }
    
    const closeDelete = () => {
      dialogDelete.value = false
      setTimeout(() => {
        Object.assign(editedItem, defaultItem)
        editedIndex.value = -1
      })
    }
    
    const editUserById = async (userId) => {
      try {
        const response = await apiClient.get(`/users/${userId}`)
        const user = response.data
        
        // Add formatted fields to match the table format
        const preferences = user.preferences || { timezone: 'UTC' }
        const formattedUser = {
          ...user,
          rolesAsString: (user.roles || []).join(', '),
          created_ts_formatted: formatDate(user.created_ts),
          updated_ts_formatted: formatDate(user.updated_ts || user.created_ts),
          timezone: preferences.timezone || 'UTC',
          preferences: preferences
        }
        
        Object.assign(editedItem, formattedUser)
        editMode.value = true
        dialog.value = true
      } catch (err) {
        console.error('Error loading user for edit:', err)
      }
    }
    
    // Lifecycle hooks and watchers
    onMounted(() => {
      fetchUsers()
      // Check if we need to edit a user based on query param
      if (route.query.edit) {
        editUserById(route.query.edit)
      }
    })
    
    // Expose to template
    return {
      search,
      loading,
      dialog,
      dialogDelete,
      dialogConfirmEdit,
      editMode,
      headers,
      users,
      editedIndex,
      editedItem,
      defaultItem,
      formTitle,
      fetchUsers,
      formatDate,
      viewUser,
      editUser,
      deleteUser,
      openNewUserDialog,
      deleteItemConfirm,
      confirmEdit,
      save,
      close,
      closeDelete,
      editUserById
    }
  }
}
</script>

<style>
.clickable-username {
  color: #1976d2;
  text-decoration: none;
  cursor: pointer;
}
.clickable-username:hover {
  text-decoration: underline;
}
</style> 
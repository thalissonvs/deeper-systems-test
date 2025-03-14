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
              @click="viewUser(props.item)"
            >
              mdi-eye
            </v-icon>
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
    
    <!-- Dialog for adding/editing user -->
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
            @click="save"
          >
            Save
          </v-btn>
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
import apiClient from '../api/config'

export default {
  name: 'UsersPage',
  data: () => ({
    search: '',
    loading: false,
    dialog: false,
    dialogDelete: false,
    editMode: false,
    headers: [
      { title: 'Username', align: 'start', sortable: true, key: 'username' },
      { title: 'Roles', align: 'start', sortable: true, key: 'rolesAsString' },
      { title: 'Timezone', align: 'start', sortable: true, key: 'timezone' },
      { title: 'Is Active?', align: 'center', sortable: true, key: 'active' },
      { title: 'Last Updated At', align: 'start', sortable: true, key: 'updated_ts_formatted' },
      { title: 'Created At', align: 'start', sortable: true, key: 'created_ts_formatted' },
      { title: 'Actions', align: 'center', sortable: false, key: 'actions' }
    ],
    users: [],
    editedIndex: -1,
    editedItem: {
      username: '',
      password: '',
      roles: [],
      preferences: {
        timezone: 'UTC'
      },
      active: true
    },
    defaultItem: {
      username: '',
      password: '',
      roles: [],
      preferences: {
        timezone: 'UTC'
      },
      active: true
    }
  }),
  
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New User' : 'Edit User'
    }
  },
  
  mounted() {
    this.fetchUsers()
  },
  
  methods: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await apiClient.get('/users')
        this.users = response.data.map(user => {
          const preferences = user.preferences || { timezone: 'UTC' };
          return {
            ...user,
            rolesAsString: (user.roles || []).join(', '),
            created_ts_formatted: this.formatDate(user.created_ts),
            updated_ts_formatted: this.formatDate(user.updated_ts || user.created_ts),
            timezone: preferences.timezone || 'UTC',
            preferences: preferences
          }
        })
        console.log('Processed data:', this.users)
      } catch (error) {
        console.error('Error loading users:', error)
      } finally {
        this.loading = false
      }
    },
    
    formatDate(timestamp) {
      if (!timestamp) return 'N/A'
      
      const date = new Date(timestamp * 1000)
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    },
    
    viewUser(item) {
      this.$router.push({ name: 'UserDetails', params: { id: item._id } })
    },
    
    editUser(item) {
      this.editedIndex = this.users.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.editMode = true
      this.dialog = true
    },
    
    deleteUser(item) {
      this.editedIndex = this.users.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },
    
    openNewUserDialog() {
      this.editedItem = Object.assign({}, this.defaultItem)
      this.editMode = false
      this.dialog = true
    },
    
    async deleteItemConfirm() {
      try {
        await apiClient.delete(`/users/${this.editedItem._id}`)
        this.users.splice(this.editedIndex, 1)
      } catch (error) {
        console.error('Error deleting user:', error)
      }
      this.closeDelete()
    },
    
    async save() {
      if (this.editedIndex > -1) {
        // Editing existing user
        try {
          const response = await apiClient.put(`/users/${this.editedItem._id}`, this.editedItem)
          // Add formatted fields to result
          const userData = response.data;
          const preferences = userData.preferences || { timezone: 'UTC' };
          const updatedUser = {
            ...userData,
            rolesAsString: (userData.roles || []).join(', '),
            created_ts_formatted: this.formatDate(userData.created_ts),
            updated_ts_formatted: this.formatDate(userData.updated_ts || userData.created_ts),
            timezone: preferences.timezone || 'UTC',
            preferences: preferences
          }
          Object.assign(this.users[this.editedIndex], updatedUser)
        } catch (error) {
          console.error('Error updating user:', error)
        }
      } else {
        // Creating new user
        try {
          const response = await apiClient.post('/users', this.editedItem)
          // Add formatted fields to result
          const userData = response.data;
          const preferences = userData.preferences || { timezone: 'UTC' };
          const newUser = {
            ...userData,
            rolesAsString: (userData.roles || []).join(', '),
            created_ts_formatted: this.formatDate(userData.created_ts),
            updated_ts_formatted: this.formatDate(userData.updated_ts || userData.created_ts),
            timezone: preferences.timezone || 'UTC',
            preferences: preferences
          }
          this.users.push(newUser)
        } catch (error) {
          console.error('Error creating user:', error)
        }
      }
      this.close()
    },
    
    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    
    closeDelete() {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    }
  }
}
</script> 
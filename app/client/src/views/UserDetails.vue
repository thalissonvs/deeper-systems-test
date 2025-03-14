<template>
  <v-container>
    <v-card v-if="user">
      <v-card-title>
        User Details
        <v-spacer></v-spacer>
        <v-btn
          icon
          @click="router.go(-1)"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-title>Username</v-list-item-title>
              <v-list-item-subtitle>{{ user.username }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-title>Status</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip
                  :color="user.active ? 'green' : 'red'"
                  :text-color="'white'"
                  small
                >
                  {{ user.active ? 'Active' : 'Inactive' }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-title>Timezone</v-list-item-title>
              <v-list-item-subtitle>{{ user.preferences?.timezone || 'UTC' }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-title>Creation Date</v-list-item-title>
              <v-list-item-subtitle>{{ formatDate(user.created_ts) }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          
          <v-col cols="12">
            <v-list-item>
              <v-list-item-title>Roles</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip
                  v-for="(role, index) in user.roles"
                  :key="index"
                  class="ma-1"
                  small
                >
                  {{ role }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>
      </v-card-text>
      
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          @click="router.push({ name: 'Users' })"
        >
          Back to List
        </v-btn>
        <v-btn
          color="warning"
          @click="showEditDialog = true"
          class="ml-2"
        >
          Edit
        </v-btn>
        <v-btn
          color="error"
          @click="dialogDelete = true"
          class="ml-2"
        >
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
    
    <v-card v-else-if="loading">
      <v-card-text class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </v-card-text>
    </v-card>
    
    <v-card v-else>
      <v-card-title>
        Error
      </v-card-title>
      <v-card-text>
        User not found.
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          @click="router.push({ name: 'Users' })"
        >
          Back to List
        </v-btn>
      </v-card-actions>
    </v-card>
    
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
            @click="dialogDelete = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="red darken-1"
            text
            @click="deleteUserConfirm"
          >
            Confirm
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Edit User Dialog -->
    <edit-user-dialog
      v-if="showEditDialog"
      :user="user"
      @close="showEditDialog = false"
      @refresh="fetchUser"
    />
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '../api/config'
import EditUserDialog from '../components/EditUserDialog.vue'

export default {
  name: 'UserDetails',
  components: {
    EditUserDialog
  },
  setup() {
    // Router and route
    const router = useRouter()
    const route = useRoute()
    
    // Reactive state
    const user = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const dialogDelete = ref(false)
    const showEditDialog = ref(false)

    // Methods
    const fetchUser = async () => {
      loading.value = true
      try {
        const userId = route.params.id
        const response = await apiClient.get(`/users/${userId}`)
        user.value = response.data
      } catch (err) {
        error.value = 'Error loading user'
        console.error(error.value, err)
      } finally {
        loading.value = false
      }
    }
    
    const formatDate = (timestamp) => {
      if (!timestamp) return 'N/A'
      
      const date = new Date(timestamp * 1000)
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }
    
    const editUser = () => {
      showEditDialog.value = true
    }
    
    const deleteUserConfirm = async () => {
      try {
        await apiClient.delete(`/users/${user.value._id}`)
        router.push({ name: 'Users' })
      } catch (err) {
        console.error('Error deleting user:', err)
      }
      dialogDelete.value = false
    }
    
    // Lifecycle hooks
    onMounted(fetchUser)
    
    // Expose to template
    return {
      user,
      loading,
      error,
      dialogDelete,
      showEditDialog,
      fetchUser,
      formatDate,
      editUser,
      deleteUserConfirm,
      router
    }
  }
}
</script>

<style>
.clickable-chip {
  cursor: pointer;
}
</style> 

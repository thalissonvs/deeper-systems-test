<template>
  <v-container>
    <v-card v-if="user">
      <v-card-title>
        User Details
        <v-spacer></v-spacer>
        <v-btn
          icon
          @click="$router.go(-1)"
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
          @click="$router.push({ name: 'Users' })"
        >
          Back to List
        </v-btn>
        <v-btn
          color="warning"
          @click="editUser"
          class="ml-2"
        >
          Edit
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
          @click="$router.push({ name: 'Users' })"
        >
          Back to List
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import apiClient from '../api/config'

export default {
  name: 'UserDetails',
  data: () => ({
    user: null,
    loading: true,
    error: null
  }),
  
  mounted() {
    this.fetchUser()
  },
  
  methods: {
    async fetchUser() {
      this.loading = true
      try {
        const userId = this.$route.params.id
        const response = await apiClient.get(`/users/${userId}`)
        this.user = response.data
      } catch (error) {
        this.error = 'Error loading user'
        console.error(this.error, error)
      } finally {
        this.loading = false
      }
    },
    
    formatDate(timestamp) {
      if (!timestamp) return 'N/A'
      
      const date = new Date(timestamp * 1000)
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    },
    
    editUser() {
      this.$router.push({ 
        name: 'Users',
        query: { edit: this.user._id }
      })
    }
  }
}
</script> 
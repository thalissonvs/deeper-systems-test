<template>
  <v-dialog
    v-model="dialog"
    max-width="500px"
  >
    <v-card>
      <v-card-title>
        Edit User
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
  </v-dialog>
</template>

<script>
import apiClient from '../api/config'

export default {
  name: 'EditUserDialog',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      dialog: true,
      dialogConfirmEdit: false,
      editedItem: {
        username: '',
        roles: [],
        preferences: {
          timezone: 'UTC'
        },
        active: true
      }
    }
  },
  watch: {
    user: {
      handler(newValue) {
        if (newValue) {
          this.editedItem = Object.assign({}, newValue)
          // Ensure preferences object exists
          if (!this.editedItem.preferences) {
            this.editedItem.preferences = { timezone: 'UTC' }
          }
        }
      },
      immediate: true
    }
  },
  methods: {
    close() {
      this.dialog = false
      this.$emit('close')
    },
    async confirmEdit() {
      try {
        await apiClient.put(`/users/${this.editedItem._id}`, this.editedItem)
        this.$emit('refresh')
        this.dialogConfirmEdit = false
        this.close()
      } catch (error) {
        console.error('Error updating user:', error)
      }
    }
  }
}
</script> 
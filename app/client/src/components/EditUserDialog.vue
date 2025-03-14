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
import { ref, reactive, watch } from 'vue'
import apiClient from '../api/config'

export default {
  name: 'EditUserDialog',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  setup(props, { emit }) {
    // Reactive state
    const dialog = ref(true)
    const dialogConfirmEdit = ref(false)
    const editedItem = reactive({
      username: '',
      roles: [],
      preferences: {
        timezone: 'UTC'
      },
      active: true
    })

    // Watch for changes in the user prop
    watch(() => props.user, (newValue) => {
      if (newValue) {
        // Copy user data to editedItem
        Object.assign(editedItem, JSON.parse(JSON.stringify(newValue)))
        
        // Ensure preferences object exists
        if (!editedItem.preferences) {
          editedItem.preferences = { timezone: 'UTC' }
        }
      }
    }, { immediate: true })

    // Methods
    const close = () => {
      dialog.value = false
      emit('close')
    }

    const confirmEdit = async () => {
      try {
        await apiClient.put(`/users/${editedItem._id}`, editedItem)
        emit('refresh')
        dialogConfirmEdit.value = false
        close()
      } catch (error) {
        console.error('Error updating user:', error)
      }
    }

    // Expose to template
    return {
      dialog,
      dialogConfirmEdit,
      editedItem,
      close,
      confirmEdit
    }
  }
}
</script> 
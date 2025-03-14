<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h4 font-weight-bold">
            Welcome to the Advanced User Management Portal
          </v-card-title>
          <v-card-text>
            <p class="text-body-1">
              This system allows you to manage users, their preferences and permissions with advanced features.
            </p>
            <v-btn
              color="primary"
              class="mt-4"
              :to="{ name: 'Users' }"
            >
              View Users
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'HomePage',
  data: () => ({
    //
  }),
}
</script> 
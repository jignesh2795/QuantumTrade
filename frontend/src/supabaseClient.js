// Supabase client configuration for QuantumTrade frontend
// This is a mock implementation for local development

// Mock Supabase client
const supabase = {
  auth: {
    getSession: () => null,
    onAuthStateChange: (callback) => {
      // Mock implementation
      return {
        data: {
          subscription: {
            unsubscribe: () => {},
          },
        },
      };
    },
    signInWithPassword: async ({ email, password }) => {
      // Mock implementation
      return {
        data: {
          user: {
            id: "mock-user-id",
            email: email,
            user_metadata: {},
          },
        },
        error: null,
      };
    },
    signUp: async ({ email, password }) => {
      // Mock implementation
      return {
        data: {
          user: {
            id: "mock-user-id",
            email: email,
            user_metadata: {},
          },
        },
        error: null,
      };
    },
    signOut: async () => {
      // Mock implementation
      return {
        error: null,
      };
    },
  },
  from: (table) => {
    // Mock implementation
    return {
      select: (columns) => {
        return {
          eq: (column, value) => {
            return {
              single: () => {
                return {
                  data: null,
                  error: null,
                };
              },
              limit: (limit) => {
                return {
                  order: (column, options) => {
                    return {
                      data: [],
                      error: null,
                    };
                  },
                };
              },
            };
          },
        };
      },
      insert: (data) => {
        return {
          select: () => {
            return {
              single: () => {
                return {
                  data: data[0],
                  error: null,
                };
              },
            };
          },
        };
      },
      update: (data) => {
        return {
          eq: (column, value) => {
            return {
              select: () => {
                return {
                  single: () => {
                    return {
                      data: data,
                      error: null,
                    };
                  },
                };
              },
            };
          },
        };
      },
    };
  },
  channel: (name) => {
    return {
      on: (event, options, callback) => {
        return {
          subscribe: () => {
            return {
              data: {
                subscription: {
                  unsubscribe: () => {},
                },
              },
            };
          },
        };
      },
    };
  },
};

export { supabase };

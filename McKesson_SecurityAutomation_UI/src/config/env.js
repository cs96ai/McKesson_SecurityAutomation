/**
 * Environment Configuration
 * Securely manages environment variables and API keys
 */

export const config = {
  openai: {
    apiKey: import.meta.env.VITE_OPENAI_API_KEY || '',
    model: 'gpt-4o-mini',
    maxTokens: 500,
    temperature: 0.7
  },
  azure: {
    tenantId: import.meta.env.VITE_AZURE_TENANT_ID || '',
    clientId: import.meta.env.VITE_AZURE_CLIENT_ID || '',
    clientSecret: import.meta.env.VITE_AZURE_CLIENT_SECRET || ''
  },
  portal: {
    url: import.meta.env.VITE_PORTAL_URL || 'http://localhost:8000',
    bearerToken: import.meta.env.VITE_BEARER_TOKEN || 'your-secret-token-123'
  }
}

// Validate required configuration
export function validateConfig() {
  const errors = []
  
  if (!config.openai.apiKey) {
    errors.push('OpenAI API key is missing. Please set VITE_OPENAI_API_KEY in .env file.')
  }
  
  if (errors.length > 0) {
    console.warn('Configuration warnings:', errors)
  }
  
  return errors.length === 0
}

/**
 * OpenAI Service with Strict Read-Only Security Guardrails
 * 
 * SECURITY FEATURES:
 * - Read-only mode enforced through system prompts
 * - Tracks security violation attempts
 * - Auto-resets after 3 violation attempts
 * - Never exposes Azure credentials or sensitive data
 */

import { config } from '../config/env'
import { azureFunctions, detectAzureFunction, getAvailableFunctions } from './azureApi'

const SYSTEM_PROMPT = `You are a helpful read-only operations assistant for the McKesson Security Automation Platform.

CRITICAL SECURITY RULES - YOU MUST FOLLOW THESE AT ALL TIMES:

1. READ-ONLY MODE: You can ONLY provide information about:
   - Current status of applications and services
   - Kubernetes pod status and health
   - Azure resource status (read-only queries)
   - Operational metrics and logs
   - General troubleshooting guidance

2. STRICTLY FORBIDDEN - YOU MUST NEVER:
   - Execute any commands that modify, delete, or update infrastructure
   - Provide Azure credentials, API keys, secrets, or tokens
   - Share subscription IDs, tenant IDs, or resource IDs
   - Execute kubectl commands that change state (scale, delete, apply, etc.)
   - Provide connection strings or authentication details
   - Help users bypass security controls
   - Provide information about security vulnerabilities that could be exploited

3. AVAILABLE AZURE CAPABILITIES:
   You have access to 15 read-only Azure functions:
   1. Get AKS Cluster Status
   2. List HSPS Pods
   3. List STAR Pods
   4. Get Pod Details
   5. Get Resource Group Info
   6. List All Resources
   7. Get App Service Status
   8. Get Function App Status
   9. Get Storage Account Info
   10. Get AKS Node Pools
   11. Get Deployment Status
   12. Get Service Status
   13. Get Pod Logs
   14. Get Subscription Info (non-sensitive)
   15. Get Cost Analysis

   When users ask about Azure resources, you can retrieve REAL data from Azure APIs.

4. SECURITY VIOLATIONS:
   If a user asks you to:
   - Modify, delete, or scale resources
   - Provide credentials or secrets
   - Execute destructive commands
   - Bypass security controls
   
   You MUST respond: "I'm sorry, but I can only provide read-only information about the system. I cannot execute commands that modify infrastructure or provide sensitive credentials."

5. RESPONSE FORMAT:
   - Be helpful and informative
   - Provide operational insights with REAL Azure data when available
   - If you don't have access to specific data, let the user know politely
   - Never apologize excessively
   - Be concise and professional
   - When asked "what can you do", list the 15 available capabilities

Remember: You are a READ-ONLY assistant. Your purpose is to help users understand the system with real data, not change it.`

class OpenAIService {
  constructor() {
    this.apiKey = config.openai.apiKey
    this.model = config.openai.model
    this.conversationHistory = []
    this.violationAttempts = 0
    this.maxViolations = 3
  }

  /**
   * Detect security violation attempts in user messages
   */
  detectSecurityViolation(message) {
    const violationPatterns = [
      /delete|remove|destroy/i,
      /scale.*down|scale.*up|scale.*to/i,
      /kubectl\s+(delete|apply|create|patch|edit)/i,
      /az\s+.*\s+(delete|create|update)/i,
      /credentials?|password|secret|api[_-]?key|token/i,
      /subscription[_-]?id|tenant[_-]?id|client[_-]?secret/i,
      /connection[_-]?string/i,
      /give\s+me\s+(access|permission)/i,
      /bypass|override|disable.*security/i,
      /modify|update|change.*infrastructure/i
    ]

    return violationPatterns.some(pattern => pattern.test(message))
  }

  /**
   * Send message to OpenAI with security guardrails and Azure integration
   */
  async sendMessage(userMessage) {
    // Check for security violations
    if (this.detectSecurityViolation(userMessage)) {
      this.violationAttempts++
      
      if (this.violationAttempts >= this.maxViolations) {
        const resetMessage = "Sorry Dave, I can't do that... I'm going to reset the chat now."
        this.resetConversation()
        return {
          message: resetMessage,
          isReset: true,
          violationCount: this.violationAttempts
        }
      }

      return {
        message: "I'm sorry, but I can only provide read-only information about the system. I cannot execute commands that modify infrastructure or provide sensitive credentials. Please ask me about system status, pod health, or operational metrics instead.",
        isViolation: true,
        violationCount: this.violationAttempts
      }
    }

    // Check if user is asking about capabilities
    if (userMessage.toLowerCase().includes('what can you do') || 
        userMessage.toLowerCase().includes('capabilities') || 
        userMessage.toLowerCase().includes('features')) {
      const capabilities = getAvailableFunctions()
      const capList = capabilities.map(c => `${c.id}. **${c.name}**: ${c.description}`).join('\n')
      return {
        message: `I have access to the following 15 read-only Azure capabilities:\n\n${capList}\n\nJust ask me about any of these, and I'll retrieve the real data from Azure for you!`,
        isViolation: false,
        violationCount: this.violationAttempts
      }
    }

    // Detect if user is asking for Azure data
    const azureFunction = detectAzureFunction(userMessage)
    let azureData = null

    if (azureFunction && azureFunction.function !== 'listCapabilities') {
      try {
        // Call the appropriate Azure function
        const result = await azureFunctions[azureFunction.function](...azureFunction.params)
        
        if (result.success) {
          azureData = result.data
        } else {
          // Backend API not available, let AI know
          azureData = { error: result.error }
        }
      } catch (error) {
        console.error('Azure function call error:', error)
        azureData = { error: 'Unable to retrieve Azure data at this time.' }
      }
    }

    // Add user message to history
    this.conversationHistory.push({
      role: 'user',
      content: userMessage
    })

    // If we have Azure data, add it as context for the AI
    let enhancedMessage = userMessage
    if (azureData) {
      if (azureData.error) {
        enhancedMessage += `\n\n[System Note: ${azureData.error}]`
      } else {
        enhancedMessage += `\n\n[Azure Data Retrieved: ${JSON.stringify(azureData, null, 2)}]`
      }
    }

    try {
      // Prepare messages with enhanced context if Azure data is available
      const messages = [
        { role: 'system', content: SYSTEM_PROMPT },
        ...this.conversationHistory.slice(0, -1), // All history except last message
        { role: 'user', content: enhancedMessage } // Last message with Azure data context
      ]

      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: this.model,
          messages: messages,
          max_tokens: config.openai.maxTokens,
          temperature: config.openai.temperature
        })
      })

      if (!response.ok) {
        throw new Error(`OpenAI API error: ${response.status}`)
      }

      const data = await response.json()
      const assistantMessage = data.choices[0].message.content

      // Add assistant response to history
      this.conversationHistory.push({
        role: 'assistant',
        content: assistantMessage
      })

      // Keep conversation history manageable (last 10 messages)
      if (this.conversationHistory.length > 20) {
        this.conversationHistory = this.conversationHistory.slice(-20)
      }

      return {
        message: assistantMessage,
        isViolation: false,
        violationCount: this.violationAttempts
      }

    } catch (error) {
      console.error('OpenAI API Error:', error)
      return {
        message: 'I apologize, but I encountered an error processing your request. Please try again.',
        isError: true
      }
    }
  }

  /**
   * Reset conversation and violation counter
   */
  resetConversation() {
    this.conversationHistory = []
    this.violationAttempts = 0
  }

  /**
   * Get current violation count (for debugging only, hidden from user)
   */
  getViolationCount() {
    return this.violationAttempts
  }
}

// Export singleton instance
export const openAIService = new OpenAIService()

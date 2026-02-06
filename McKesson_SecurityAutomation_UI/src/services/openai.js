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

const SYSTEM_PROMPT = `You are a concise, read-only operations assistant for the McKesson Security Automation Platform.

RULES:
1. READ-ONLY: You provide status information only. You CANNOT modify, delete, or scale anything.
2. NEVER share credentials, API keys, secrets, subscription IDs, tenant IDs, or connection strings.
3. If asked to modify infrastructure or reveal secrets, respond: "I can only provide read-only information. I cannot modify infrastructure or share credentials."

AVAILABLE DATA (14 read-only Azure endpoints):
AKS cluster status, HSPS pods, STAR pods, pod details, resource group info, all resources, App Service status, Function App status, storage account info, AKS node pools, deployment status, service status, pod logs, subscription info.

RESPONSE FORMAT:
- Be brief and direct. No filler. No excessive apologies.
- When presenting structured data (pods, resources, deployments, services, node pools), use an HTML table. Example:
  <table><tr><th>Name</th><th>Status</th></tr><tr><td>my-pod</td><td>Running</td></tr></table>
- Use <strong> for emphasis, <br> for line breaks.
- For simple answers, plain text is fine. Only use HTML when it makes the data easier to read.
- Keep responses under 200 words unless the user asks for detail.`

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

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

3. APPROVED READ-ONLY QUERIES:
   - "kubectl get pods" (status only)
   - "kubectl describe pod [name]" (information only)
   - "kubectl logs [pod-name]" (read logs)
   - Azure resource status queries (read-only)
   - Application health checks

4. SECURITY VIOLATIONS:
   If a user asks you to:
   - Modify, delete, or scale resources
   - Provide credentials or secrets
   - Execute destructive commands
   - Bypass security controls
   
   You MUST respond: "I'm sorry, but I can only provide read-only information about the system. I cannot execute commands that modify infrastructure or provide sensitive credentials."

5. RESPONSE FORMAT:
   - Be helpful and informative
   - Provide operational insights
   - Suggest read-only queries the user can run
   - Never apologize excessively
   - Be concise and professional

Remember: You are a READ-ONLY assistant. Your purpose is to help users understand the system, not change it.`

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
   * Send message to OpenAI with security guardrails
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

    // Add user message to history
    this.conversationHistory.push({
      role: 'user',
      content: userMessage
    })

    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: this.model,
          messages: [
            { role: 'system', content: SYSTEM_PROMPT },
            ...this.conversationHistory
          ],
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

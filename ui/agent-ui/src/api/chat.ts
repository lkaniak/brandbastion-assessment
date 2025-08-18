import { toast } from 'sonner'

export interface ChatResponse {
  response: string
  status: string
}

export interface ChatRequest {
  message: string
  files?: File[]
}

export const sendChatMessage = async (
  endpoint: string,
  message: string,
  files?: File[]
): Promise<ChatResponse> => {
  const url = `${endpoint}/chat`

  try {
    const formData = new FormData()
    formData.append('message', message)

    if (files && files.length > 0) {
      files.forEach((file) => {
        formData.append('files', file)
      })
    }

    const response = await fetch(url, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ detail: 'Unknown error' }))
      throw new Error(
        errorData.detail || `HTTP ${response.status}: ${response.statusText}`
      )
    }

    const data = await response.json()
    return data as ChatResponse
  } catch (error) {
    const errorMessage =
      error instanceof Error ? error.message : 'Unknown error occurred'
    toast.error(`Failed to send message: ${errorMessage}`)
    throw error
  }
}

export const sendChatMessageStream = async (
  endpoint: string,
  message: string,
  files?: File[],
  onChunk?: (chunk: any) => void,
  onError?: (error: Error) => void,
  onComplete?: () => void
): Promise<void> => {
  const url = `${endpoint}/chat`

  try {
    const formData = new FormData()
    formData.append('message', message)

    if (files && files.length > 0) {
      files.forEach((file) => {
        formData.append('files', file)
      })
    }

    const response = await fetch(url, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ detail: 'Unknown error' }))
      throw new Error(
        errorData.detail || `HTTP ${response.status}: ${response.statusText}`
      )
    }

    if (!response.body) {
      throw new Error('No response body')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    const processStream = async (): Promise<void> => {
      const { done, value } = await reader.read()

      if (done) {
        onComplete?.()
        return
      }

      buffer += decoder.decode(value, { stream: true })

      // Process Server-Sent Events format
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6) // Remove 'data: ' prefix
          if (data.trim()) {
            try {
              const chunk = JSON.parse(data)
              onChunk?.(chunk)
            } catch (error) {
              // Skip invalid JSON
            }
          }
        }
      }

      await processStream()
    }

    await processStream()
  } catch (error) {
    const errorMessage =
      error instanceof Error ? error.message : 'Unknown error occurred'
    onError?.(new Error(errorMessage))
  }
}

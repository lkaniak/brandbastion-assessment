import { useCallback } from 'react'
import { toast } from 'sonner'
import { usePlaygroundStore } from '@/store'
import useChatActions from '@/hooks/useChatActions'
import { sendChatMessageStream } from '@/api/chat'
import { type UploadedFile } from '@/components/playground/ChatArea/ChatInput/FileUpload'

const useUnifiedChatHandler = () => {
  const setMessages = usePlaygroundStore((state) => state.setMessages)
  const { addMessage, focusChatInput } = useChatActions()
  const selectedEndpoint = usePlaygroundStore((state) => state.selectedEndpoint)
  const setStreamingErrorMessage = usePlaygroundStore(
    (state) => state.setStreamingErrorMessage
  )
  const setIsStreaming = usePlaygroundStore((state) => state.setIsStreaming)

  const handleStreamResponse = useCallback(
    async (message: string, files?: UploadedFile[]) => {
      setIsStreaming(true)

      setMessages((prevMessages) => {
        if (prevMessages.length >= 2) {
          const lastMessage = prevMessages[prevMessages.length - 1]
          const secondLastMessage = prevMessages[prevMessages.length - 2]
          if (
            lastMessage.role === 'agent' &&
            lastMessage.streamingError &&
            secondLastMessage.role === 'user'
          ) {
            return prevMessages.slice(0, -2)
          }
        }
        return prevMessages
      })

      addMessage({
        role: 'user',
        content: message,
        created_at: Math.floor(Date.now() / 1000)
      })

      addMessage({
        role: 'agent',
        content: '',
        tool_calls: [],
        streamingError: false,
        created_at: Math.floor(Date.now() / 1000) + 1
      })

      let lastContent = ''

      try {
        const fileList = files?.map(f => f.file) || []

        await sendChatMessageStream(
          selectedEndpoint,
          message,
          fileList,
          (chunk) => {
            if (chunk.event === 'RunResponseContent' && chunk.content) {
              setMessages((prevMessages) => {
                const newMessages = [...prevMessages]
                const lastMessage = newMessages[newMessages.length - 1]
                if (lastMessage && lastMessage.role === 'agent') {
                  const uniqueContent = chunk.content.replace(lastContent, '')
                  lastMessage.content += uniqueContent
                  lastContent = chunk.content
                }
                return newMessages
              })
            } else if (chunk.event === 'RunCompleted') {
              setMessages((prevMessages) => {
                const newMessages = [...prevMessages]
                const lastMessage = newMessages[newMessages.length - 1]
                if (lastMessage && lastMessage.role === 'agent') {
                  lastMessage.content = chunk.content || lastMessage.content
                }
                return newMessages
              })
            } else if (chunk.event === 'RunError') {
              setMessages((prevMessages) => {
                const newMessages = [...prevMessages]
                const lastMessage = newMessages[newMessages.length - 1]
                if (lastMessage && lastMessage.role === 'agent') {
                  lastMessage.streamingError = true
                }
                return newMessages
              })
              setStreamingErrorMessage(chunk.content || 'Error during run')
            }
          },
          (error) => {
            setMessages((prevMessages) => {
              const newMessages = [...prevMessages]
              const lastMessage = newMessages[newMessages.length - 1]
              if (lastMessage && lastMessage.role === 'agent') {
                lastMessage.streamingError = true
              }
              return newMessages
            })
            setStreamingErrorMessage(error.message)
          },
          () => {
            // Stream completed
          }
        )
      } catch (error) {
        setMessages((prevMessages) => {
          const newMessages = [...prevMessages]
          const lastMessage = newMessages[newMessages.length - 1]
          if (lastMessage && lastMessage.role === 'agent') {
            lastMessage.streamingError = true
          }
          return newMessages
        })
        setStreamingErrorMessage(
          error instanceof Error ? error.message : String(error)
        )
      } finally {
        focusChatInput()
        setIsStreaming(false)
      }
    },
    [
      setMessages,
      addMessage,
      selectedEndpoint,
      setStreamingErrorMessage,
      setIsStreaming,
      focusChatInput
    ]
  )

  return { handleStreamResponse }
}

export default useUnifiedChatHandler

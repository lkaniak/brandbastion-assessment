'use client'
import { useState } from 'react'
import { toast } from 'sonner'
import { TextArea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { usePlaygroundStore } from '@/store'
import useUnifiedChatHandler from '@/hooks/useUnifiedChatHandler'
import { useQueryState } from 'nuqs'
import Icon from '@/components/ui/icon'
import FileUpload, { type UploadedFile } from './FileUpload'

const ChatInput = () => {
  const { chatInputRef } = usePlaygroundStore()

  const { handleStreamResponse } = useUnifiedChatHandler()
  const [selectedAgent] = useQueryState('agent')
  const [teamId] = useQueryState('team')
  const [inputMessage, setInputMessage] = useState('')
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [showFileUpload, setShowFileUpload] = useState(false)
  const isStreaming = usePlaygroundStore((state) => state.isStreaming)

  const handleSubmit = async () => {
    if (!inputMessage.trim() && uploadedFiles.length === 0) return

    const currentMessage = inputMessage || 'Files uploaded'
    setInputMessage('')

    try {
      await handleStreamResponse(currentMessage, uploadedFiles)
      setUploadedFiles([]) // Clear files after upload
    } catch (error) {
      toast.error(
        `Error in handleSubmit: ${
          error instanceof Error ? error.message : String(error)
        }`
      )
    }
  }

  const handleFilesSelected = (files: UploadedFile[]) => {
    setUploadedFiles(files)
  }

  const handleFileRemove = (fileId: string) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId))
  }

  return (
    <div className="relative mx-auto mb-1 flex w-full max-w-2xl flex-col gap-4 font-geist">
      {/* File Upload Section */}
      {showFileUpload && (
        <div className="w-full">
          <FileUpload
            onFilesSelected={handleFilesSelected}
            onFileRemove={handleFileRemove}
            uploadedFiles={uploadedFiles}
            disabled={!(selectedAgent || teamId) || isStreaming}
            maxFiles={10}
            maxFileSize={50}
            acceptedTypes={['image/*', 'video/*', 'audio/*', 'application/pdf', 'text/*']}
          />
        </div>
      )}

      {/* Chat Input Section */}
      <div className="flex w-full items-end justify-center gap-x-2">
        <Button
          onClick={() => setShowFileUpload(!showFileUpload)}
          disabled={!(selectedAgent || teamId) || isStreaming}
          size="icon"
          variant="outline"
          className="rounded-xl"
        >
          <Icon type="plus-icon" />
        </Button>

        <TextArea
          placeholder={'Ask anything'}
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={(e) => {
            if (
              e.key === 'Enter' &&
              !e.nativeEvent.isComposing &&
              !e.shiftKey &&
              !isStreaming
            ) {
              e.preventDefault()
              handleSubmit()
            }
          }}
          className="w-full border border-accent bg-primaryAccent px-4 text-sm text-primary focus:border-accent"
          disabled={!(selectedAgent || teamId)}
          ref={chatInputRef}
        />

        <Button
          onClick={handleSubmit}
          disabled={
            !(selectedAgent || teamId) ||
            (!inputMessage.trim() && uploadedFiles.length === 0) ||
            isStreaming
          }
          size="icon"
          className="rounded-xl bg-primary p-5 text-primaryAccent"
        >
          <Icon type="send" color="primaryAccent" />
        </Button>
      </div>
    </div>
  )
}

export default ChatInput

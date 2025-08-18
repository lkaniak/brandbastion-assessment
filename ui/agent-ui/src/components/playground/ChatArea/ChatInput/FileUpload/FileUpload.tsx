'use client'

import { useState, useRef, useCallback } from 'react'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import Icon from '@/components/ui/icon'
import { cn } from '@/lib/utils'
import Image from 'next/image'

export interface UploadedFile {
  id: string
  file: File
  preview?: string
  size: number
  type: string
  name: string
}

interface FileUploadProps {
  onFilesSelected: (files: UploadedFile[]) => void
  onFileRemove: (fileId: string) => void
  uploadedFiles: UploadedFile[]
  disabled?: boolean
  maxFiles?: number
  maxFileSize?: number // in MB
  acceptedTypes?: string[]
}

const FileUpload = ({
  onFilesSelected,
  onFileRemove,
  uploadedFiles,
  disabled = false,
  maxFiles = 10,
  maxFileSize = 50, // 50MB default
  acceptedTypes = ['image/*', 'video/*', 'audio/*', 'application/pdf', 'text/*']
}: FileUploadProps) => {
  const [isDragOver, setIsDragOver] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const validateFile = useCallback((file: File): string | null => {
    // Check file size
    if (file.size > maxFileSize * 1024 * 1024) {
      return `File ${file.name} is too large. Maximum size is ${maxFileSize}MB.`
    }

    // Check file type
    const isValidType = acceptedTypes.some(type => {
      if (type.endsWith('/*')) {
        const category = type.split('/')[0]
        return file.type.startsWith(category)
      }
      return file.type === type
    })

    if (!isValidType) {
      return `File type ${file.type} is not supported.`
    }

    return null
  }, [maxFileSize, acceptedTypes])

  const processFiles = useCallback((files: FileList | File[]) => {
    const fileArray = Array.from(files)
    const validFiles: UploadedFile[] = []
    const errors: string[] = []

    // Check if adding these files would exceed maxFiles
    if (uploadedFiles.length + fileArray.length > maxFiles) {
      toast.error(`Maximum ${maxFiles} files allowed.`)
      return
    }

    fileArray.forEach(file => {
      const error = validateFile(file)
      if (error) {
        errors.push(error)
      } else {
        const fileId = `${file.name}-${file.size}-${Date.now()}`
        const uploadedFile: UploadedFile = {
          id: fileId,
          file,
          size: file.size,
          type: file.type,
          name: file.name
        }

        // Generate preview for images
        if (file.type.startsWith('image/')) {
          const reader = new FileReader()
          reader.onload = (e) => {
            uploadedFile.preview = e.target?.result as string
            onFilesSelected([...uploadedFiles, ...validFiles])
          }
          reader.readAsDataURL(file)
        }

        validFiles.push(uploadedFile)
      }
    })

    if (errors.length > 0) {
      errors.forEach(error => toast.error(error))
    }

    if (validFiles.length > 0) {
      onFilesSelected([...uploadedFiles, ...validFiles])
    }
  }, [uploadedFiles, maxFiles, validateFile, onFilesSelected])

  const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files) {
      processFiles(files)
    }
    // Reset input value to allow selecting the same file again
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }, [processFiles])

  const handleDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((event: React.DragEvent) => {
    event.preventDefault()
    setIsDragOver(false)
  }, [])

  const handleDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault()
    setIsDragOver(false)

    const files = event.dataTransfer.files
    if (files) {
      processFiles(files)
    }
  }, [processFiles])

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (type: string): 'image' | 'video' | 'audio' | 'file' => {
    if (type.startsWith('image/')) return 'image'
    if (type.startsWith('video/')) return 'video'
    if (type.startsWith('audio/')) return 'audio'
    if (type === 'application/pdf') return 'file'
    return 'file'
  }

  return (
    <div className="w-full">
      {/* File Upload Area */}
      <div
        className={cn(
          'relative border-2 border-dashed rounded-lg p-6 text-center transition-colors',
          isDragOver
            ? 'border-primary bg-primary/5'
            : 'border-muted-foreground/25 hover:border-muted-foreground/50',
          disabled && 'opacity-50 cursor-not-allowed'
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={acceptedTypes.join(',')}
          onChange={handleFileSelect}
          className="hidden"
          disabled={disabled}
        />

        <div className="flex flex-col items-center gap-2">
          <Icon
            type="plus-icon"
            size="lg"
            className="text-muted-foreground"
          />
          <div className="text-sm text-muted-foreground">
            <span className="font-medium">Click to upload</span> or drag and drop
          </div>
          <div className="text-xs text-muted-foreground">
            Max {maxFiles} files, {maxFileSize}MB each
          </div>
        </div>
      </div>

      {/* File List */}
      {uploadedFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          <div className="text-sm font-medium text-foreground">
            Selected Files ({uploadedFiles.length}/{maxFiles})
          </div>
          <div className="space-y-2">
            {uploadedFiles.map((file) => (
              <div
                key={file.id}
                className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg"
              >
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  {file.preview && file.type.startsWith('image/') ? (
                    <Image
                      src={file.preview}
                      alt={file.name}
                      width={40}
                      height={40}
                      className="w-10 h-10 object-cover rounded"
                    />
                  ) : (
                    <div className="w-10 h-10 bg-primary/10 rounded flex items-center justify-center">
                      <Icon type={getFileIcon(file.type)} size="sm" />
                    </div>
                  )}
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">{file.name}</div>
                    <div className="text-xs text-muted-foreground">
                      {formatFileSize(file.size)}
                    </div>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onFileRemove(file.id)}
                  disabled={disabled}
                  className="text-destructive hover:text-destructive"
                >
                  <Icon type="x" size="sm" />
                </Button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default FileUpload

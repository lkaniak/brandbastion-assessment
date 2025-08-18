npm run dev# File Upload Functionality

This document describes the multiple file upload functionality that has been implemented in the Agent UI.

## Features

### FileUpload Component (`src/components/playground/ChatArea/ChatInput/FileUpload/FileUpload.tsx`)

- **Multiple File Selection**: Users can select multiple files at once
- **Drag & Drop Support**: Files can be dragged and dropped onto the upload area
- **File Validation**:
  - File size limits (default: 50MB per file)
  - File type validation (images, videos, audio, PDFs, text files)
  - Maximum file count (default: 10 files)
- **File Preview**: Image files show thumbnails
- **File Management**: Users can remove individual files before upload
- **Progress Feedback**: Visual feedback during drag operations

### Integration with ChatInput

The file upload functionality is integrated into the existing ChatInput component:

- **Toggle Button**: Plus icon button to show/hide the file upload area
- **FormData Support**: Files are sent using FormData when submitting
- **Combined Input**: Users can send both text messages and files together
- **Disabled States**: Upload is disabled when no agent/team is selected or during streaming

## Usage

1. **Enable File Upload**: Click the plus icon button next to the chat input
2. **Select Files**: Either click the upload area to browse files or drag and drop files
3. **Review Files**: See selected files with previews and file information
4. **Remove Files**: Click the X button on any file to remove it
5. **Send**: Click the send button to upload files with an optional message

## File Types Supported

- **Images**: All image formats (JPEG, PNG, GIF, WebP, etc.)
- **Videos**: All video formats (MP4, AVI, MOV, etc.)
- **Audio**: All audio formats (MP3, WAV, FLAC, etc.)
- **Documents**: PDF files
- **Text**: All text file formats

## Configuration

The FileUpload component accepts the following props:

```typescript
interface FileUploadProps {
  onFilesSelected: (files: UploadedFile[]) => void
  onFileRemove: (fileId: string) => void
  uploadedFiles: UploadedFile[]
  disabled?: boolean
  maxFiles?: number        // Default: 10
  maxFileSize?: number     // Default: 50MB
  acceptedTypes?: string[] // Default: ['image/*', 'video/*', 'audio/*', 'application/pdf', 'text/*']
}
```

## Backend Integration

The files are sent to the backend using FormData:

```typescript
const formData = new FormData()
formData.append('message', message)
uploadedFiles.forEach((file, index) => {
  formData.append(`file_${index}`, file.file)
})
```

## Technical Details

### File Processing
- Files are validated before being added to the upload list
- Image files generate base64 previews for display
- File sizes are formatted for display (KB, MB, GB)

### State Management
- File upload state is managed locally in the ChatInput component
- Files are cleared after successful upload
- Upload area can be toggled on/off

### Error Handling
- File validation errors are displayed as toast notifications
- Invalid files are rejected with specific error messages
- Network errors during upload are handled gracefully

## Icons Added

The following icons were added to support the file upload functionality:
- `image`: For image files
- `video`: For video files
- `audio`: For audio files
- `file`: For document and text files

## Future Enhancements

Potential improvements that could be added:
- Upload progress indicators
- File compression for large images
- Batch file operations
- File preview for more file types
- Drag and drop reordering of files

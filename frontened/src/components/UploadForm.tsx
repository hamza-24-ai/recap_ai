"use client"

import React, { useState } from 'react'
import {motion} from "framer-motion"
import  api  from "@/lib/axios"


interface UploadFormProps {
    projectId : number
    onUploadStart : (meetingId: number) => void
}
const UploadForm = ({projectId, onUploadStart} : UploadFormProps) => {
  
    const [file, setFile] = useState<File | null>(null)
    const [title, setTitle] = useState("")
    const [uploading, setUploading] = useState(false)
    const [error,setError] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")

        if (!file) {
            setError(" Please Select a file ")
            return
        }

        setUploading(true)

        try{
            const formData = new FormData()
            formData.append("project_id", String(projectId))
            formData.append("title", title || file.name)
            formData.append("file", file)

            const response = await api.post("/meetings/upload", formData)

            onUploadStart(response.data.id)

            setFile(null)
            setTitle("")
        } catch (err){
            console.log(err)
            const detail = (err as any)?.response?.data?.detail
            setError(typeof detail === "string" ? detail : "Upload failed. Please try again.")
        } finally {
            setUploading(false)
        }
    }
  
    return (
    <div className='bg-white/70 backdrop-blur-2xl border border-white/60 rounded-2xl p-6'>
        <h1 className='font-medium text-slate-800 mb-8'>
            Upload Transcript
        </h1>
        <form onSubmit={handleSubmit}>
            <div>
                <label className='block text-sm font-medium text-slate-600 mb-2'>
                    Meeting Title (Optional)
                </label>
                <input type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder='Weekly Task july-21'
                className='w-full px-4 py-3 text-slate-900 rounded-lg border border-slate-400 bg-white/80 focus:outline-none focus:ring-2 focus:ring-sky-400 transition' 
                />
            </div>
            <div>
                <label className='block text-sm font-medium text-slate-600 mb-2'>
                    Upload Transcipt File (.txt or .docx)
                </label>
                <input type="file" 
                    accept='.txt, .docx'
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="w-full text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-sky-100 file:text-sky-700 file:font-medium hover:file:bg-sky-200 transition cursor-pointer"
                />
            </div>
            {
                error && (
                    <p className='text-sm text-rose-500 bg-rose-50 border border-rose-800 px-3 py-2 rounded-lg'>
                        { error }
                    </p>
                )
            }
            <motion.button
                whileTap={{ scale: 0.98 }}
                type="submit"
                disabled={uploading}
                className="w-full py-2.5 rounded-lg bg-linear-to-r from-sky-500 to-blue-500 text-white font-medium shadow-lg shadow-sky-500/25 hover:shadow-sky-500/40 transition disabled:opacity-60"
                >
                {uploading ? "Uploading..." : "Upload & Process"}
            </motion.button>
        </form>
    </div>
  )
}

export default UploadForm
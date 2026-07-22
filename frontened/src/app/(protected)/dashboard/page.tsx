"use client"

import {motion} from "framer-motion"
import React, { useEffect, useState } from 'react'
import { Project } from "@/types/index"
import Link from "next/link"
import  api  from "@/lib/axios"

const DashboardPage = () => {

    const[showModel, setShowModel] = useState(false)
    const[loading, setLoading] = useState(false)
    const[projects, setProjects] = useState<Project[]>([])
    const[newProjectName, setNewProjectName] = useState("")
    const[creating, setCreating] = useState(false)



    useEffect(() => {
        const fetchProjects = async () => {
            try {
                setLoading(true)
                const response = await api.get("/projects")
                setProjects(response.data)
            } catch(err) {
                console.log(err)
            } finally {
                setLoading(false)
            }
        }

        fetchProjects()
    },[])


    const handleCreateProject = async (e : React.FormEvent) => {
        e.preventDefault()
        if (!newProjectName.trim()) return

        setCreating(true)

        try {
            const response = await api.post("/projects/", {name : newProjectName})
            setProjects((prev) => [...prev, response.data])
            setNewProjectName("")
            setShowModel(false)
        } catch (err) {
            console.log(err)

        } finally{
            setCreating(false)
        }
    }

  return (
    <div className='max-w-5xl mx-auto px-6 py-10'>
        <div className='flex items-center justify-between mb-8'>
            <div>
                <h1 className='text-2xl font-semibold text-slate-800 tracking-tight'>
                    Projects
                </h1>

                <p className='text-slate-500 text-sm mt-1'>
                    Your meeting projects, all in one place
                </p>
            </div>
        </div>
        <motion.button
            whileTap={{ scale : 0.98}}
            onClick={() => setShowModel(true)}
            className="mb-8 px-5 py-2.5 rounded-lg bg-linear-to-r from-sky-500 to-blue-500 text-white font-medium shadow-lg shadow-sky-500/25 hover:shadow-sky-500/40 transition"
        >
            + New Project
        </motion.button>
        {
            loading ? (
                <p className="text-slate-500">
                    Loading Projects ........
                </p>
            ) : projects.length === 0 ? (
                <div className="bg-white/60 backdrop-blur-2xl border border-white/60 rounded-2xl p-10 text-center">

                    <p className="text-slate-600 font-medium">No Projects yet</p>
                    <p className="text-slate-400 text-sm mt-1">
                        Create a project to start Uploading meeting Transcripts
                    </p>
                </div>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {
                        projects.map((project, i) => (
                            <motion.div
                                key={project.id}
                                initial={{ opacity: 0, y: 12 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: i * 0.05 }}
                            >
                                <Link
                                    href={`/projects/${project.id}`}
                                >
                                    <div className="bg-white/70 backdrop-blur-xl border border-white/60 rounded-xl p-5 hover:shadow-lg hover:shadow-sky-900/5 transition cursor-pointer h-full">
                                        <h3 className="font-medium text-slate-800">
                                            {
                                                project.name
                                            }
                                        </h3>
                                        <p className="text-xs text-slate-400 mt-2">
                                            {
                                                new Date(project.created_at).toLocaleDateString()
                                            }
                                        </p>
                                    </div>

                                </Link>
                            </motion.div>
                        ))
                    }
                </div>
            )
        }

        {
            showModel && (
                <div className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm flex items-center justify-center z-50 px-4">
                    <motion.div
                        initial={{ opacity: 0 , scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="bg-white rounded-2xl p-6 w-full max-w-sm shadow-2xl"
                    >
                        <h2 className="text-lg text-slate-800 font-semibold mb-4">
                            New Project
                        </h2>
                        <form onSubmit={handleCreateProject}>
                            <input type="text"
                                autoFocus
                                value={newProjectName}
                                onChange={(e) => setNewProjectName(e.target.value)}
                                placeholder="Marketing Team Weekly Syncs"
                                className="w-full px-4 py-2.5 rounded-lg border border-blue-400 text-slate-900 focus:outline-none focus:ring-2 focus:ring-sky-400 transition"

                            />
                            <div className="flex gap-4 items-center px-3 mt-4">
                                <button
                                    type="button"
                                    onClick={() => setShowModel(false)}
                                    className="flex-1 py-2.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 transition"
                                >
                                    Cancel
                                </button>

                                <button
                                    type="submit"
                                    disabled={creating}
                                    className="flex-1 py-2.5 rounded-lg bg-linear-to-r from-sky-500 to-blue-500 text-white font-medium disabled:opacity-60"
                                >
                                    {
                                        creating ? "Creating...." : "Create"
                                    }
                                </button>
                            </div>

                        </form>
                    </motion.div>
                </div>
            )
        }
    </div>
  )
}

export default DashboardPage
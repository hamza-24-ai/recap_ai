"use client"

import React, { useState } from 'react'
import { motion } from "framer-motion"
import Link from 'next/link'
import { useRouter }  from "next/navigation"
import api from "@/lib/axios"
import { useAuthStore } from "@/context/AuthContext"


const LoginPage = () => {

    const router = useRouter()
    const setAuth = useAuthStore((state) => state.setAuth)

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")
        setLoading(true)

        try{
            const response = await api.post("/auth/login", {email, password})
            const { access_token,access_type, user } = response.data
            
            console.log(access_type)
            setAuth(user,access_token)
            router.push("/dashboard")
        } catch(err : any) {
            setError(err.response?.data?.detail || "Something Went Wrong. Try Again")

        } finally {
            setLoading(false)
        }
    }

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-[#eef6fc]">

        {/* Ambient gradient backgound */}
        <div className='absolute inset-0 bg-linear-to-br from-sky-100 via-blue-50 to-cyan-100'/>
        <div className='absolute -top-32 -left-32 w-96 h-96 bg-sky-300/30 rounded-full blur-3xl'/>
        <div className='absolute -bottom-32 -right-32 w-96 h-96 bg-blue-300/30 rounded-full blur-3xl'/>

        <motion.div
         initial={{ opacity : 0, y: 16}}
         animate={{ opacity: 1, y: 0}}
         transition={{ duration: 0.5, ease: "easeOut"}}
         className='relative w-full max-w-md mx-4'
        >

            <div className='bg-white/70 backdrop-blur-2xl border border-white/60 shadow-xl shadow-sky-900/5 rounded-2xl p-8'>
                <div className='mb-8'>
                    <h1 className='text-2xl font-semibold text-slate-800 tracking-tight'>
                        Welcome Back to Recap Agent
                    </h1>
                    <p className='text-slate-500 text-sm mt-1'>
                        SignIn to pick Where Your meetings left Off
                    </p>

                </div>

                <form onSubmit={handleSubmit}  className='space-y-4'>
                    <div>
                        <label className='block text-sm font-medium text-slate-600 mb-1.5 '>
                            Email
                        </label>
                        <input 
                            type='email'
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className='w-full px-4 py-2.5 rounded-lg border border-slate-200 bg-white/80 text-slate-800 
                            placeholder:text-slate-400 focus:outline-none focus:ring-sky-400 focus:border-transparent transition'
                            placeholder='your@gmail.com'

                        />
                    </div>

                    <div>
                        <label className='block text-sm font-medium text-slate-600 mb-1.5'>
                            Password
                        </label>
                        <input 
                            type='password'
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className='w-full px-4 py-2.5 rounded-lg border border-slate-200 bg-white/80 text-slate-800 
                            placeholder:text-slate-400 focus:outline-none focus:ring-sky-400 focus:border-transparent transition'
                            placeholder='your1324'
                        />
                    </div>

                    {
                        error && (
                            <p className='text-sm text-red-900 border bg-rose-50 border-rose-500 rounded-lg px-3 py-2'>
                                {error}
                            </p>
                        )
                    }

                    <button 
                        type='submit'
                        disabled={loading}
                        className='w-full py-2.5 hover:scale-105 rounded-lg bg-linear-to-r from-sky-500 to-blue-500 text-white font-medium shadow-lg shadow-sky-500/25 hover:shadow-sky-500/40 transition disabled:opacity-60'
                    >
                        {loading ? "Signing in..." : 'Sign In'}
                    </button>
                </form>

                <p className='text-sm text-slate-500 text-center mt-6'>
                    Do not have account?{" "}
                    <Link
                        href="/signup" 
                        className='text-sky-600 font-medium hover:underline'
                    >
                        SignUp
                    </Link>
                </p>

            </div>


        </motion.div>
    </div>
  )
}

export default LoginPage
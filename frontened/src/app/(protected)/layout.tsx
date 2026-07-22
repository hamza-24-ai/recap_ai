"use client"

import React from 'react'
import { useEffect } from "react"
import { usePathname,useRouter } from "next/navigation"
import Link  from "next/link"
import { useAuthStore } from "@/context/AuthContext"

const ProtectedLayout = ( {children} : {children : React.ReactNode} ) => {

    const router = useRouter()
    const pathname = usePathname()
    const { isAuthenticated,user,logout } = useAuthStore()

    useEffect(() => {
        if ( !isAuthenticated ){
            router.push("/login")
        }
    },[])

    const handlelogout = () => {
        logout()
        router.push("/login")
    }

    if (!isAuthenticated) return null

  return (
    <div className='min-h-screen flex relative bg-[#eef6fc]'>
        <div className='absolute inset-0 bg-linear-to-br from-sky-100 via-blue-50 to-cyan-100  pointer-events-none' />

        {/* SideBar of dashboard */}
        <aside className='relative w-64 bg-white/70 backdrop-blur-2xl border-r border-white/60 flex flex-col justify-between p-5'>

            <div className='mb-8'>
                <h2 className='text-2xl text-slate-900 font-semibold'>
                    Recap AI 
                </h2>
                <p className='text-slate-600 font-semibold mt-0.5'>
                    {
                        user?.name
                    }
                </p>

            </div>

            <nav className='flex-1 space-y-1'>
                <Link
                    href="/dashboard"
                    className={`block px-3 py-2 rounded-lg text-sm font-medium transition ${
                        pathname === "/dashboard"
                        ? "bg-sky text-sky-700"
                        : "text-slate-600 hover:bg-slate-100"
                    }`}
                >
                    Dashboard
                </Link>

            </nav>

            <button 
                onClick={handlelogout}
                className='text-slate-700 hover:text-slate-600 hover:bg-slate-200 rounded-lg transition px-2 py-3'
            >
                Logout
            </button>

        </aside>

        <main className='relative flex-1 overflow-y-auto'>
            {children}
        </main>
    </div>
  )
}

export default ProtectedLayout
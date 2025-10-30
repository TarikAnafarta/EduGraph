import React from 'react'
import { Outlet, useNavigate } from 'react-router-dom'

export default function AppLayout(){
  return (
    <div style={{minHeight:'100vh'}}>
      <Outlet />
    </div>
  )
}

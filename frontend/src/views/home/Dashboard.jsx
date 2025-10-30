import React, { useEffect, useRef, useState } from 'react'
import './Dashboard.css'

export default function Dashboard(){
  const [user, setUser] = useState(null)
  const [error, setError] = useState('')
  const [open, setOpen] = useState(false)
  const menuRef = useRef(null)

  function getCSRFToken(){
    const cookies = document.cookie.split(';')
    for(const c of cookies){
      const [n,v] = c.trim().split('=')
      if(n === 'csrftoken') return v
    }
    return ''
  }

  useEffect(()=>{
    function onDocClick(e){
      if(menuRef.current && !menuRef.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('click', onDocClick)
    return ()=> document.removeEventListener('click', onDocClick)
  },[])

  useEffect(()=>{
    const token = localStorage.getItem('authToken')
    if(!token){ window.location.href = '/login'; return }

    async function load(){
      try{
        setError('')
        const res = await fetch('http://localhost:8000/api/users/me/', {
          headers: { 'Authorization': `Token ${token}`, 'Content-Type': 'application/json' }
        })
        if(!res.ok){
          localStorage.removeItem('authToken')
          window.location.href = '/login'
          return
        }
        const data = await res.json()
        if(!data.profile_completed){
          window.location.href = '/complete-profile'
          return
        }
        setUser(data)
      }catch(err){ setError('Kullanıcı bilgileri yüklenemedi') }
    }
    load()
  },[])

  async function logout(){
    const token = localStorage.getItem('authToken')
    try{
      await fetch('http://localhost:8000/api/users/logout/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        }
      })
    }catch(_){ /* ignore */ }
    finally{
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
  }

  const initial = (user?.name || user?.email || 'U').trim().charAt(0).toUpperCase()

  return (
    <div>
      <nav className="navbar">
        <h1>EduGraph</h1>
        <div className="user-info">
          <div className="user-menu" id="user-menu" ref={menuRef}>
            <button className="user-name-btn" id="user-menu-button" aria-haspopup="true" aria-expanded={open} onClick={(e)=>{ e.stopPropagation(); setOpen(o=>!o) }}>
              <span id="user-name">{user ? (user.name || user.email) : 'Yükleniyor...'}</span>
              {user?.profile_picture ? (
                <img id="user-avatar" className="avatar" alt="Profil" src={user.profile_picture} />
              ) : (
                <div id="avatar-fallback" className="avatar-fallback">{initial}</div>
              )}
              <span className="caret">▾</span>
            </button>
            <div className={"dropdown" + (open? ' show':'')} id="user-dropdown" role="menu" aria-hidden={!open}>
              <a href="/profile" id="profile-link">Profilim</a>
              <button id="logout-btn" onClick={logout}>Çıkış Yap</button>
            </div>
          </div>
        </div>
      </nav>

      <div className="container">
        {error && <div id="error-message" className="error-message">{error}</div>}

        <div className="welcome-card">
          <h2>EduGraph'a Hoş Geldiniz!</h2>
          <p>Eğitim müfredatı görselleştirme platformunuz</p>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <h3>📊 Müfredatı Görselleştir</h3>
            <p>Müfredat ilişkilerini ve öğrenme yollarını görselleştirmek için etkileşimli grafikler oluşturun.</p>
            <button className="feature-btn" onClick={()=> window.location.href = '/graph'}>Grafikleri Keşfet</button>
          </div>

          <div className="feature-card">
            <h3>📚 Ders Yönetimi</h3>
            <p>Derslerinizi ve öğrenme hedeflerinizi ekleyin, düzenleyin ve organize edin.</p>
            <button className="feature-btn" onClick={()=> alert('Özellik yakında geliyor!')}>İçerikleri Yönet</button>
          </div>

          <div className="feature-card">
            <h3>📈 İlerlemeyi İzle</h3>
            <p>Öğrenme ilerlemesini izleyin ve geliştirilmesi gereken alanları belirleyin.</p>
            <button className="feature-btn" onClick={()=> alert('Özellik yakında geliyor!')}>Analitikleri Görüntüle</button>
          </div>
        </div>
      </div>
    </div>
  )
}

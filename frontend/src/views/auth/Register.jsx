import React, { useState } from 'react'

export default function RegisterPage(){
  const [name,setName] = useState('')
  const [email,setEmail] = useState('')
  const [password,setPassword] = useState('')
  const [confirmPassword,setConfirmPassword] = useState('')
  const [loading,setLoading] = useState(false)
  const [error,setError] = useState('')
  const [success,setSuccess] = useState('')

  function apiBase(){ return 'http://localhost:8000' }
  function getCSRF(){
    const cookies = document.cookie.split(';')
    for(const c of cookies){ const [n,v] = c.trim().split('='); if(n==='csrftoken') return v }
    return ''
  }

  async function submit(e){
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')
    try{
      if(password !== confirmPassword){ throw new Error('Şifreler eşleşmiyor.') }
      if(password.length < 8){ throw new Error('Şifre en az 8 karakter uzunluğunda olmalıdır.') }
      const res = await fetch(`${apiBase()}/api/users/register/`, {
        method: 'POST',
        headers: {'Content-Type':'application/json','X-CSRFToken': getCSRF()},
        body: JSON.stringify({ name, email, password })
      })
      const data = await res.json()
      if(!res.ok && res.status !== 200){
        const msg = data.message || data.email?.[0] || data.name?.[0] || data.password?.[0] || 'Kayıt başarısız. Lütfen tekrar deneyin.'
        throw new Error(msg)
      }
      setSuccess(data.message || 'Hesap başarıyla oluşturuldu! Doğrulama sayfasına yönlendiriliyorsunuz...')
      setTimeout(()=>{ window.location.href = `/verify?email=${encodeURIComponent(email)}` }, 2000)
    }catch(err){ setError(err.message) } finally { setLoading(false) }
  }

  return (
    <div style={{display:'grid', placeItems:'center', minHeight:'100vh', background:'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}}>
      <form onSubmit={submit} style={{background:'#fff', padding:24, borderRadius:16, width:360, maxWidth:'90%'}}>
        <div style={{textAlign:'center', marginBottom:16}}>
          <h2 style={{marginBottom:6}}>EduGraph'a Katılın</h2>
          <p style={{color:'#666', fontSize:14}}>Başlamak için hesabınızı oluşturun</p>
        </div>
        {error && <div style={{background:'#fee', color:'#c33', padding:8, borderRadius:8, marginBottom:8}}>{error}</div>}
        {success && <div style={{background:'#efe', color:'#3c3', padding:8, borderRadius:8, marginBottom:8}}>{success}</div>}
        <div style={{marginBottom:12}}>
          <label>Ad Soyad</label>
          <input value={name} onChange={e=>setName(e.target.value)} required style={{width:'100%', padding:10, border:'2px solid #e1e1e1', borderRadius:10}} />
        </div>
        <div style={{marginBottom:12}}>
          <label>E-posta Adresi</label>
          <input value={email} onChange={e=>setEmail(e.target.value)} type="email" required style={{width:'100%', padding:10, border:'2px solid #e1e1e1', borderRadius:10}} />
        </div>
        <div style={{marginBottom:6}}>
          <label>Şifre</label>
          <input value={password} onChange={e=>setPassword(e.target.value)} type="password" required style={{width:'100%', padding:10, border:'2px solid #e1e1e1', borderRadius:10}} />
          <div style={{fontSize:12, color:'#666', marginTop:6}}>Şifre en az 8 karakter uzunluğunda olmalıdır</div>
        </div>
        <div style={{marginTop:12, marginBottom:12}}>
          <label>Şifreyi Onayla</label>
          <input value={confirmPassword} onChange={e=>setConfirmPassword(e.target.value)} type="password" required style={{width:'100%', padding:10, border:'2px solid #e1e1e1', borderRadius:10}} />
        </div>
        <button disabled={loading} style={{width:'100%', padding:10, background:'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color:'#fff', border:'none', borderRadius:10, fontWeight:600}}>
          {loading? 'Hesap oluşturuluyor…' : 'Hesap Oluştur'}
        </button>
        <div style={{textAlign:'center', marginTop:16}}>
          <a href="/login" style={{color:'#667eea', textDecoration:'none', fontWeight:500}}>Zaten hesabınız var mı? Giriş yapın</a>
        </div>
      </form>
    </div>
  )
}

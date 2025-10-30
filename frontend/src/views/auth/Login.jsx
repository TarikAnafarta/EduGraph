import React, { useEffect, useMemo, useState } from 'react'

export default function LoginPage(){
  const [email,setEmail] = useState('')
  const [password,setPassword] = useState('')
  const [loading,setLoading] = useState(false)
  const [error,setError] = useState('')
  const [success,setSuccess] = useState('')
  const [showVerifyPrompt, setShowVerifyPrompt] = useState(false)

  const params = useMemo(()=> new URLSearchParams(window.location.search), [])

  useEffect(()=>{
    // If redirected from verify success
    if(params.get('verified') === 'true'){
      const e = params.get('email') || ''
      if(e) setEmail(e)
      setSuccess('Hesabınız doğrulandı. Lütfen giriş yapın.')
    }
  },[params])

  function apiBase(){ return 'http://localhost:8000' }
  function getCSRF(){
    const cookies = document.cookie.split(';')
    for(const c of cookies){ const [n,v] = c.trim().split('='); if(n==='csrftoken') return v }
    return ''
  }
  function clearMessages(){ setError(''); setSuccess(''); setShowVerifyPrompt(false) }

  async function submit(e){
    e.preventDefault()
    clearMessages()
    setLoading(true)
    try{
      const res = await fetch(`${apiBase()}/api/users/login/`, {
        method: 'POST', headers: {'Content-Type':'application/json','X-CSRFToken': getCSRF()},
        body: JSON.stringify({ email, password })
      })
      const data = await res.json()
      if(!res.ok){
        if(res.status === 403 && data.message === 'Account is inactive.'){
          setShowVerifyPrompt(true)
        } else {
          throw new Error(data.detail || data.message || 'Giriş başarısız')
        }
        return
      }
      localStorage.setItem('authToken', data.token)
      // Check profile status
      try{
        const meRes = await fetch(`${apiBase()}/api/users/me/`, { headers: { 'Authorization': `Token ${data.token}`, 'Content-Type':'application/json' } })
        if(meRes.ok){
          const me = await meRes.json()
          if(!me.profile_completed){ window.location.href = '/complete-profile'; return }
        }
      }catch(_){ /* ignore */ }
      window.location.href = '/dashboard'
    }catch(err){ setError(err.message) } finally { setLoading(false) }
  }

  async function resendVerification(){
    clearMessages()
    const currentEmail = email
    if(!currentEmail){ setError('Lütfen e-postayı girin.'); return }
    try{
      const res = await fetch(`${apiBase()}/api/users/resend-verification/`, {
        method:'POST', headers:{ 'Content-Type':'application/json','X-CSRFToken': getCSRF() },
        body: JSON.stringify({ email: currentEmail })
      })
      const data = await res.json()
      if(!res.ok){ throw new Error(data.message || 'Doğrulama kodu gönderilemedi.') }
      setSuccess('Doğrulama kodu gönderildi! Doğrulama sayfasına yönlendiriliyorsunuz...')
      setTimeout(()=> window.location.href = `/verify?email=${encodeURIComponent(currentEmail)}`, 2000)
    }catch(err){ setError(err.message) }
  }

  function goToVerify(){
    const currentEmail = email
    if(!currentEmail){ setError('Lütfen e-postayı girin.'); return }
    window.location.href = `/verify?email=${encodeURIComponent(currentEmail)}`
  }

  return (
    <div style={{display:'grid', placeItems:'center', minHeight:'100vh', background:'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}}>
      <form onSubmit={submit} style={{background:'#fff', padding:24, borderRadius:16, width:360, maxWidth:'90%'}}>
        <div style={{textAlign:'center', marginBottom:16}}>
          <h2 style={{marginBottom:6}}>Hoş Geldiniz</h2>
          <p style={{color:'#666', fontSize:14}}>EduGraph hesabınıza giriş yapın</p>
        </div>
        {error && <div style={{background:'#fee', color:'#c33', padding:8, borderRadius:8, marginBottom:8}}>{error}</div>}
        {success && <div style={{background:'#efe', color:'#3c3', padding:8, borderRadius:8, marginBottom:8}}>{success}</div>}
        <div style={{marginBottom:12}}>
          <label>E-posta Adresi</label>
          <input value={email} onChange={e=>setEmail(e.target.value)} type="email" required style={{width:'100%', padding:10, border:'2px solid #e1e1e1', borderRadius:10}} />
        </div>
        <div style={{marginBottom:12}}>
          <label>Şifre</label>
          <input value={password} onChange={e=>setPassword(e.target.value)} type="password" required style={{width:'100%', padding:10, border:'2px solid #e1e1e1', borderRadius:10}} />
        </div>
        <button disabled={loading} style={{width:'100%', padding:10, background:'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color:'#fff', border:'none', borderRadius:10, fontWeight:600}}>
          {loading? 'Giriş yapılıyor…' : 'Giriş Yap'}
        </button>
        {showVerifyPrompt && (
          <div style={{background:'#fff3cd', color:'#856404', padding:12, borderRadius:10, marginTop:12, textAlign:'center'}}>
            <p>Hesabınız henüz doğrulanmamış.</p>
            <div style={{display:'flex', gap:8, justifyContent:'center', marginTop:8}}>
              <button type="button" onClick={resendVerification} style={{padding:'8px 12px', background:'#667eea', color:'#fff', border:'none', borderRadius:6}}>Doğrulama Kodunu Tekrar Gönder</button>
              <button type="button" onClick={goToVerify} style={{padding:'8px 12px', background:'#667eea', color:'#fff', border:'none', borderRadius:6}}>Doğrulama Kodunu Gir</button>
            </div>
          </div>
        )}
        <div style={{textAlign:'center', marginTop:16}}>
          <a href="/register" style={{color:'#667eea', textDecoration:'none', fontWeight:500}}>Hesabınız yok mu? Kayıt olun</a><br/><br/>
          <a href="/forgot-password" style={{color:'#667eea', textDecoration:'none', fontWeight:500}}>Şifrenizi mi unuttunuz?</a>
        </div>
      </form>
    </div>
  )
}

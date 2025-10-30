import React, { useState } from 'react'

export default function VerifyPage(){
  const [code, setCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const params = new URLSearchParams(window.location.search)
  const email = params.get('email') || ''

  function showError(msg){ setError(msg); setSuccess('') }
  function showSuccess(msg){ setSuccess(msg); setError('') }

  function getCSRFToken(){
    const cookies = document.cookie.split(';')
    for(const c of cookies){ const [n,v] = c.trim().split('='); if(n==='csrftoken') return v }
    return ''
  }

  async function submit(e){
    e.preventDefault()
    if(!email){ showError('E-posta bulunamadı. Lütfen tekrar kayıt olmayı deneyin.'); return }
    if(code.replace(/\D/g,'').length !== 6){ showError('Lütfen 6 haneli doğrulama kodunu girin.'); return }

    setLoading(true)
    try{
      const res = await fetch('http://localhost:8000/api/users/verify/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCSRFToken() },
        body: JSON.stringify({ email, code })
      })
      const data = await res.json()
      if(!res.ok) throw new Error(data.message || 'Doğrulama başarısız. Lütfen tekrar deneyin.')
      showSuccess('Hesap başarıyla doğrulandı! Yönlendiriliyorsunuz...')
      setTimeout(()=>{ window.location.href = `/login?verified=true&email=${encodeURIComponent(email)}` }, 2000)
    }catch(err){ showError(err.message) } finally { setLoading(false) }
  }

  async function resend(){
    if(!email){ showError('E-posta bulunamadı. Lütfen tekrar kayıt olmayı deneyin.'); return }
    try{
      const res = await fetch('http://localhost:8000/api/users/resend-verification/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCSRFToken() },
        body: JSON.stringify({ email })
      })
      const data = await res.json()
      if(!res.ok) throw new Error(data.message || 'Kod tekrar gönderilemedi. Lütfen tekrar deneyin.')
      showSuccess('Doğrulama kodu başarıyla gönderildi!')
    }catch(err){ showError(err.message) }
  }

  return (
    <div style={{display:'grid', placeItems:'center', minHeight:'100vh', background:'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}}>
      <div style={{background:'#fff', padding:24, borderRadius:16, width:400, maxWidth:'92%'}}>
        <div style={{textAlign:'center', marginBottom:16}}>
          <h1 style={{color:'#333', fontSize:24, marginBottom:6}}>Hesabınızı Doğrulayın</h1>
          <p style={{color:'#666', fontSize:14}}>E-postanıza gönderilen doğrulama kodunu girin</p>
        </div>
        {error && <div style={{background:'#fee', color:'#c33', padding:10, borderRadius:10, marginBottom:10, textAlign:'center'}}>{error}</div>}
        {success && <div style={{background:'#efe', color:'#3c3', padding:10, borderRadius:10, marginBottom:10, textAlign:'center'}}>{success}</div>}
        <form onSubmit={submit}>
          <div style={{marginBottom:14}}>
            <label style={{display:'block', marginBottom:6, color:'#555', fontWeight:500}}>Doğrulama Kodu</label>
            <input value={code} onChange={(e)=> setCode(e.target.value.replace(/\D/g,''))} maxLength={6} placeholder="000000" required
                   style={{width:'100%', padding:'12px', border:'2px solid #e1e1e1', borderRadius:10, fontSize:24, letterSpacing:'0.5rem', textAlign:'center'}} />
          </div>
          <button type="submit" disabled={loading} className="auth-button" style={{width:'100%', padding:'12px', background:'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color:'#fff', border:'none', borderRadius:10, fontWeight:600, marginBottom:10}}>
            {loading? 'Doğrulanıyor...' : 'Hesabı Doğrula'}
          </button>
        </form>
        <button onClick={resend} className="auth-button secondary" style={{width:'100%', padding:'10px', background:'transparent', color:'#667eea', border:'2px solid #667eea', borderRadius:10, fontWeight:600}}>
          Kodu Tekrar Gönder
        </button>
        <div style={{textAlign:'center', marginTop:16}}>
          <a href="/login" style={{color:'#667eea', textDecoration:'none', fontWeight:500}}>Giriş Sayfasına Dön</a>
        </div>
      </div>
    </div>
  )
}

import React, { useEffect, useMemo, useState } from 'react'

export default function CompleteProfilePage(){
  const [grade, setGrade] = useState('')
  const [track, setTrack] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const token = useMemo(()=> localStorage.getItem('authToken') || '', [])

  function apiBase(){ return 'http://localhost:8000' }

  useEffect(()=>{
    if(!token){ window.location.href = '/login'; return }
    ;(async ()=>{
      try{
        const res = await fetch(`${apiBase()}/api/users/me/`, { headers:{ 'Authorization': `Token ${token}`, 'Content-Type':'application/json' } })
        if(!res.ok){ localStorage.removeItem('authToken'); window.location.href = '/login'; return }
        const me = await res.json()
        if(me.profile_completed){ window.location.href = '/dashboard'; }
      }catch(e){ /* ignore */ }
    })()
  },[token])

  const grades = [5,6,7,8,9,10,11,12]

  function onChangeGrade(val){
    setGrade(val)
    if(!val){ setTrack(''); return }
    const g = Number(val)
    if(g <= 8){ setTrack('lgs') } else { setTrack('') }
  }

  async function submit(e){
    e.preventDefault()
    setError(''); setSuccess('')
    const g = Number(grade)
    const tr = g <= 8 ? 'lgs' : track
    if(!g || !tr){ setError('Lütfen tüm alanları doldurun.'); return }
    setLoading(true)
    try{
      const res = await fetch(`${apiBase()}/api/users/complete-profile/`, {
        method:'POST', headers:{ 'Authorization': `Token ${token}`, 'Content-Type':'application/json' },
        body: JSON.stringify({ grade: g, track: tr })
      })
      const data = await res.json()
      if(!res.ok){
        let msg = data.grade?.[0] || data.track?.[0] || data.message || 'Profil tamamlanırken bir hata oluştu.'
        setError(msg)
      } else {
        setSuccess('Profil başarıyla tamamlandı! Yönlendiriliyorsunuz...')
        setTimeout(()=> window.location.href = '/dashboard', 1500)
      }
    }catch(err){ setError('Sunucu ile bağlantı kurulamadı. Lütfen tekrar deneyin.') }
    finally{ setLoading(false) }
  }

  return (
    <div style={{minHeight:'100vh', display:'flex', alignItems:'center', justifyContent:'center', padding:16, background:'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}}>
      <div style={{background:'#fff', borderRadius:20, padding:32, boxShadow:'0 20px 60px rgba(0,0,0,0.3)', maxWidth:500, width:'100%'}}>
        <div style={{textAlign:'center', marginBottom:24}}>
          <h1 style={{fontSize:24, color:'#667eea', marginBottom:8}}>📚 EduGraph</h1>
          <p style={{color:'#666', fontSize:14}}>Hesabını Tamamla</p>
        </div>

        <div style={{display:'flex', justifyContent:'space-between', marginBottom:24, position:'relative'}}>
          {[{label:'Kayıt',done:true},{label:'Doğrulama',done:true},{label:'Profil',active:true}].map((s,i)=> (
            <div key={i} style={{flex:1, textAlign:'center', position:'relative'}}>
              {i<2 && <div style={{content:'', position:'absolute', top:15, left:'50%', width:'100%', height:2, background: s.done? '#4caf50':'#e0e0e0', zIndex:0}}/>}
              <div style={{width:30, height:30, borderRadius:'50%', margin:'0 auto 8px', display:'flex', alignItems:'center', justifyContent:'center', fontWeight:600, position:'relative', zIndex:1, background: s.active? '#667eea' : s.done? '#4caf50':'#e0e0e0', color:'#fff'}}>
                {s.done && !s.active ? '✓' : (i+1)}
              </div>
              <div style={{fontSize:12, color: s.active? '#667eea':'#666', fontWeight: s.active? 600:400}}>{s.label}</div>
            </div>
          ))}
        </div>

        <div style={{background:'#e3f2fd', borderLeft:'4px solid #2196f3', padding:16, borderRadius:8, marginBottom:24, fontSize:14, color:'#333', lineHeight:1.6}}>
          <strong>🎓 Hoş geldin!</strong><br/>
          Sana en uygun içeriği sunabilmemiz için lütfen aşağıdaki bilgileri tamamla.
        </div>

        {error && <div style={{background:'#ffebee', color:'#c62828', padding:16, borderRadius:10, marginBottom:16, textAlign:'center', borderLeft:'4px solid #c62828'}}>{error}</div>}
        {success && <div style={{background:'#e8f5e9', color:'#2e7d32', padding:16, borderRadius:10, marginBottom:16, textAlign:'center', borderLeft:'4px solid #2e7d32'}}>{success}</div>}

        <form onSubmit={submit}>
          <div style={{marginBottom:16}}>
            <label htmlFor="grade" style={{display:'block', color:'#333', fontWeight:600, marginBottom:8, fontSize:15}}>Kaçıncı Sınıfta Okuyorsun? *</label>
            <select id="grade" name="grade" required value={grade} onChange={e=> onChangeGrade(e.target.value)} style={{width:'100%', padding:'14px', border:'2px solid #e0e0e0', borderRadius:10, fontSize:16, background:'#fff', transition:'all .3s ease'}}>
              <option value="">Sınıf Seçin</option>
              {grades.map(g=> <option key={g} value={g}>{g}. Sınıf</option>)}
            </select>
          </div>

          <div style={{marginBottom:16}}>
            <label htmlFor="track" style={{display:'block', color:'#333', fontWeight:600, marginBottom:8, fontSize:15}}>Hangi Alan? *</label>
            {/* For 5-8 show read-only LGS field; for 9-12 show dropdown */}
            {grade && Number(grade) <= 8 ? (
              <input id="track-text" value="LGS" readOnly style={{width:'100%', padding:'14px', border:'2px solid #e0e0e0', borderRadius:10, fontSize:16, background:'#f5f5f5', color:'#333'}}/>
            ) : (
              <select id="track" name="track" required disabled={!grade || Number(grade) <= 8} value={track} onChange={e=> setTrack(e.target.value)} style={{width:'100%', padding:'14px', border:'2px solid #e0e0e0', borderRadius:10, fontSize:16, background:'#fff', transition:'all .3s ease'}}>
                <option value="">Alan Seçin</option>
                <option value="sayisal">Sayısal</option>
                <option value="sozel">Sözel</option>
              </select>
            )}
          </div>

          <button type="submit" disabled={loading} className="submit-btn" style={{width:'100%', padding:'16px', background:'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color:'#fff', border:'none', borderRadius:10, fontSize:16, fontWeight:600, cursor:'pointer', transition:'transform .2s ease', marginTop:16}}>
            {loading ? 'Profil tamamlanıyor...' : 'Profili Tamamla ve Devam Et'}
          </button>
        </form>
      </div>
    </div>
  )
}

import React, { useEffect, useMemo, useRef, useState } from 'react'
import './Profile.css'

export default function ProfilePage(){
  const [user, setUser] = useState(null)
  const [token, setToken] = useState('')
  const [alert, setAlert] = useState({ type: '', message: '', show: false })
  const [edit, setEdit] = useState(false)
  // new: controlled edit fields
  const [editName, setEditName] = useState('')
  const [editGrade, setEditGrade] = useState(9)
  const [editTrack, setEditTrack] = useState('lgs')

  const avatarRef = useRef(null)
  const fileInputRef = useRef(null)

  // Cropper refs/state (imperative, mirrors template logic)
  const [circleD, setCircleD] = useState(240)
  const frameRef = useRef(null)
  const maskRef = useRef(null)
  const cropRef = useRef({
    url: null,
    imgEl: null,
    frameEl: null,
    maskEl: null,
    d: 240,
    naturalW: 0,
    naturalH: 0,
    scale: 1,
    minScale: 1,
    offsetX: 0,
    offsetY: 0,
    dragging: false,
    dragStartX: 0,
    dragStartY: 0,
    startOffsetX: 0,
    startOffsetY: 0,
  })
  const [modalOpen, setModalOpen] = useState(false)
  const [cropUrl, setCropUrl] = useState(null)

  function apiBase(){ return 'http://localhost:8000' }
  function getCSRF(){
    const cookies = document.cookie.split(';')
    for(const c of cookies){ const [n,v] = c.trim().split('='); if(n==='csrftoken') return v }
    return ''
  }
  function showAlert(message, type='success'){
    setAlert({ message, type, show: true })
    setTimeout(()=> setAlert(a=> ({...a, show:false})), 5000)
  }

  useEffect(()=>{
    const t = localStorage.getItem('authToken')
    if(!t){ window.location.href = '/login'; return }
    setToken(t)
    ;(async ()=>{
      try{
        const res = await fetch(`${apiBase()}/api/users/me/`, { headers: { 'Authorization': `Token ${t}`, 'Content-Type':'application/json' }})
        if(!res.ok){ localStorage.removeItem('authToken'); window.location.href = '/login'; return }
        const u = await res.json()
        setUser(u)
      }catch(err){ showAlert('Kullanıcı bilgileri yüklenirken bir hata oluştu. Lütfen sayfayı yenileyin.', 'error') }
    })()
  },[])

  function initial(){ return (user?.name || user?.email || 'K').charAt(0).toUpperCase() }

  function toggleEdit(){
    if(!user) return
    setEditName(user.name || '')
    setEditGrade(user.grade ?? 9)
    setEditTrack(user.track || (user.grade && user.grade <= 8 ? 'lgs' : 'sayisal'))
    setEdit(true)
  }
  function cancelEdit(){
    setEdit(false)
  }

  // keep track options aligned with grade
  useEffect(()=>{
    if(!edit) return
    if(editGrade <= 8){ setEditTrack('lgs') }
    else if(editTrack === 'lgs'){ setEditTrack('sayisal') }
  }, [edit, editGrade])

  async function saveProfile(){
    try{
      const name = editName.trim()
      const grade = parseInt(editGrade)
      const track = editGrade <= 8 ? 'lgs' : editTrack
      if(!name){ showAlert('İsim boş bırakılamaz', 'error'); return }
      const res = await fetch(`${apiBase()}/api/users/me/`, {
        method:'PUT', headers:{ 'Authorization': `Token ${token}`, 'Content-Type':'application/json' },
        body: JSON.stringify({ name, grade, track })
      })
      if(!res.ok){
        const err = await res.json()
        let msg = err.message || err.track?.[0] || err.grade?.[0] || 'Profil güncellenirken bir hata oluştu'
        showAlert(msg,'error'); return
      }
      const updated = await res.json()
      setUser(updated)
      setEdit(false)
      showAlert('Profil başarıyla güncellendi! ✓','success')
    }catch(e){ showAlert('Profil güncellenirken bir hata oluştu','error') }
  }

  function toDashboard(){ window.location.href = '/dashboard' }

  // Open file -> open modal and initialize cropper
  function openCropper(file){
    if(cropUrl) URL.revokeObjectURL(cropUrl)
    const url = URL.createObjectURL(file)
    setCropUrl(url)
    setModalOpen(true)
  }

  useEffect(()=>{
    if(!modalOpen) return
    const crop = cropRef.current
    crop.frameEl = frameRef.current
    crop.maskEl = maskRef.current
    crop.imgEl = document.getElementById('crop-image')

    if(!crop.frameEl || !crop.maskEl || !crop.imgEl) return

    // Compute diameter and set frame height + CSS var like template
    const rect = crop.frameEl.getBoundingClientRect()
    const frameW = rect.width || crop.frameEl.clientWidth || 560
    crop.d = Math.floor(frameW - 80)
    crop.d = Math.max(160, Math.min(320, crop.d))
    setCircleD(crop.d)
    crop.frameEl.style.height = crop.d + 'px'
    crop.maskEl.style.setProperty('--d', crop.d + 'px')

    // Load image and initialize scales/offsets
    if(crop.url){ URL.revokeObjectURL(crop.url) }
    crop.url = cropUrl
    crop.imgEl.onload = () => {
      crop.naturalW = crop.imgEl.naturalWidth || crop.imgEl.width
      crop.naturalH = crop.imgEl.naturalHeight || crop.imgEl.height
      const needW = crop.d / crop.naturalW
      const needH = crop.d / crop.naturalH
      crop.minScale = Math.max(needW, needH)
      crop.scale = crop.minScale
      crop.offsetX = 0
      crop.offsetY = 0
      const zoom = document.getElementById('zoom-range')
      const zoomLabel = document.getElementById('zoom-label')
      if(zoom){ zoom.value = '100' }
      if(zoomLabel){ zoomLabel.textContent = '100%' }
      updateCropTransform(crop)
    }
    crop.imgEl.src = cropUrl

    // Drag handlers
    const onDown = (cx, cy) => {
      crop.dragging = true
      crop.dragStartX = cx
      crop.dragStartY = cy
      crop.startOffsetX = crop.offsetX
      crop.startOffsetY = crop.offsetY
    }
    const onMove = (cx, cy) => {
      if(!crop.dragging) return
      const dx = cx - crop.dragStartX
      const dy = cy - crop.dragStartY
      const nextX = crop.startOffsetX + dx
      const nextY = crop.startOffsetY + dy
      const clamped = clampOffsets(crop, nextX, nextY)
      crop.offsetX = clamped.x
      crop.offsetY = clamped.y
      updateCropTransform(crop)
    }
    const onUp = () => { crop.dragging = false }

    const frame = crop.frameEl
    frame.onmousedown = (e)=> onDown(e.clientX, e.clientY)
    window.onmousemove = (e)=> onMove(e.clientX, e.clientY)
    window.onmouseup = onUp

    frame.ontouchstart = (e)=>{ if(e.touches[0]) onDown(e.touches[0].clientX, e.touches[0].clientY) }
    window.ontouchmove = (e)=>{ if(e.touches[0]) onMove(e.touches[0].clientX, e.touches[0].clientY) }
    window.ontouchend = onUp

    // Zoom range
    const zoom = document.getElementById('zoom-range')
    const zoomLabel = document.getElementById('zoom-label')
    if(zoom){
      zoom.oninput = (e)=>{
        const factor = Number(e.target.value)/100
        crop.scale = crop.minScale * factor
        if(zoomLabel){ zoomLabel.textContent = Math.round(factor*100) + '%' }
        // keep image within circle after zoom
        const clamped = clampOffsets(crop, crop.offsetX, crop.offsetY)
        crop.offsetX = clamped.x
        crop.offsetY = clamped.y
        updateCropTransform(crop)
      }
    }

    // Mouse wheel zoom like template
    frame.onwheel = (e) => {
      e.preventDefault()
      const zoomInput = document.getElementById('zoom-range')
      if(!zoomInput) return
      const min = Number(zoomInput.min) || 100
      const max = Number(zoomInput.max) || 300
      const step = e.ctrlKey ? 10 : 5
      let val = Number(zoomInput.value) || 100
      val += (e.deltaY < 0 ? step : -step)
      val = Math.max(min, Math.min(max, val))
      zoomInput.value = String(val)
      const factor = val/100
      crop.scale = crop.minScale * factor
      if(zoomLabel){ zoomLabel.textContent = Math.round(factor*100) + '%' }
      const clamped = clampOffsets(crop, crop.offsetX, crop.offsetY)
      crop.offsetX = clamped.x
      crop.offsetY = clamped.y
      updateCropTransform(crop)
    }

    return ()=>{
      window.onmousemove = null
      window.onmouseup = null
      window.ontouchmove = null
      window.ontouchend = null
      if(frame) frame.onwheel = null
    }
  },[modalOpen, cropUrl])

  function clampOffsets(crop, x, y){
    const W = crop.naturalW * crop.scale
    const H = crop.naturalH * crop.scale
    const maxX = Math.max(0, (W - crop.d)/2)
    const maxY = Math.max(0, (H - crop.d)/2)
    return { x: Math.min(maxX, Math.max(-maxX, x)), y: Math.min(maxY, Math.max(-maxY, y)) }
  }
  function updateCropTransform(crop){
    const img = crop.imgEl
    if(!img) return
    img.style.transform = `translate(-50%, -50%) scale(${crop.scale}) translate(${(crop.offsetX / crop.scale)}px, ${(crop.offsetY / crop.scale)}px)`
  }

  async function saveCropped(){
    const crop = cropRef.current
    const d = crop.d
    const canvas = document.createElement('canvas')
    canvas.width = d; canvas.height = d
    const ctx = canvas.getContext('2d')

    const W = crop.naturalW * crop.scale
    const H = crop.naturalH * crop.scale
    const x = (d/2 - W/2) + crop.offsetX
    const y = (d/2 - H/2) + crop.offsetY

    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0,0,d,d)

    const img = crop.imgEl
    ctx.drawImage(img, x, y, W, H)

    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.92))
    if(!blob){ showAlert('Blob oluşturulamadı','error'); return }

    const form = new FormData()
    form.append('profile_picture', blob, 'profile.jpg')

    try{
      showAlert('Profil resmi yükleniyor...','success')
      const res = await fetch(`${apiBase()}/api/users/me/`, { method:'PATCH', headers:{ 'Authorization': `Token ${token}` }, body: form })
      if(!res.ok){ const err = await res.json(); showAlert(err.message || 'Profil resmi yüklenirken bir hata oluştu','error'); return }
      const updated = await res.json()
      setUser(updated)
      setModalOpen(false)
      showAlert('Profil resmi başarıyla güncellendi! ✓','success')
    }catch(e){ showAlert('Profil resmi yüklenirken bir hata oluştu','error') }
  }

  function onFileChange(e){
    const file = e.target.files?.[0]
    if(!file) return
    if(!file.type.startsWith('image/')){ showAlert('Lütfen bir resim dosyası seçin','error'); return }
    if(file.size > 5*1024*1024){ showAlert('Dosya boyutu en fazla 5MB olabilir','error'); return }
    openCropper(file)
  }

  const trackLabel = (t) => ({ lgs:'LGS', sayisal:'Sayısal', sozel:'Sözel' }[t] || t)

  return (
    <div>
      <div className="navbar">
        <h1 onClick={toDashboard}>📚 EduGraph</h1>
        <div className="user-info">
          <a href="/dashboard" className="back-btn">Geri Dön</a>
        </div>
      </div>

      <div className="container">
        <div className={`alert ${alert.type}`} style={{ display: alert.show ? 'block' : 'none' }}>{alert.message}</div>

        <div className="profile-card">
          <div className="profile-header">
            <div className="avatar-wrapper">
              <div className="profile-avatar" id="avatar" ref={avatarRef}>
                {user?.profile_picture ? (
                  <img src={user.profile_picture} alt="Profile" />
                ) : (
                  initial()
                )}
              </div>
              <button className="avatar-camera-btn" id="avatar-camera-btn" type="button" title="Profil fotoğrafını değiştir" aria-label="Profil fotoğrafını değiştir" onClick={()=> fileInputRef.current?.click()}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="currentColor" aria-hidden="true">
                  <path d="M512 144v288c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V144c0-26.5 21.5-48 48-48h88l12.3-32.9c7-18.7 24.9-31.1 44.9-31.1h125.5c20 0 37.9 12.4 44.9 31.1L376 96h88c26.5 0 48 21.5 48 48zM376 288c0-66.2-53.8-120-120-120s-120 53.8-120 120 53.8 120 120 120 120-53.8 120-120zm-32 0c0 48.5-39.5 88-88 88s-88-39.5-88-88 39.5-88 88-88 88 39.5 88 88z"></path>
                </svg>
              </button>
            </div>
            <input ref={fileInputRef} type="file" accept="image/*" onChange={onFileChange} style={{display:'none'}} />
            <div className="profile-info">
              <h2 id="user-name">{user?.name || 'Yükleniyor...'}</h2>
              <p id="user-email">{user?.email || 'Yükleniyor...'}</p>
            </div>
          </div>

          <div className={`info-grid ${edit? 'edit-mode':''}`} id="info-grid">
            <div className="info-item">
              <label>İsim</label>
              <div className="value" id="user-name-field">
                {edit ? (
                  <input type="text" id="edit-name" value={editName} onChange={e=> setEditName(e.target.value)} />
                ) : (
                  user?.name || '-'
                )}
              </div>
            </div>
            <div className="info-item">
              <label>Sınıf</label>
              <div className="value" id="user-grade">
                {edit ? (
                  <select id="edit-grade" value={editGrade} onChange={e=> setEditGrade(Number(e.target.value))}>
                    {Array.from({length:8},(_,i)=>i+5).map(g=> (
                      <option value={g} key={g}>{g}. Sınıf</option>
                    ))}
                  </select>
                ) : (
                  user?.grade ? `${user.grade}. Sınıf` : '-'
                )}
              </div>
            </div>
            <div className="info-item">
              <label>Alan</label>
              <div className="value" id="user-track">
                {edit ? (
                  editGrade <= 8 ? (
                    <select id="edit-track" value={editTrack} onChange={e=> setEditTrack(e.target.value)}>
                      <option value="lgs">LGS</option>
                    </select>
                  ) : (
                    <select id="edit-track" value={editTrack} onChange={e=> setEditTrack(e.target.value)}>
                      <option value="sayisal">Sayısal</option>
                      <option value="sozel">Sözel</option>
                    </select>
                  )
                ) : (
                  user?.track ? trackLabel(user.track) : '-'
                )}
              </div>
            </div>
            <div className="info-item">
              <label>Üyelik Tarihi</label>
              <div className="value read-only" id="user-joined">
                {user?.date_joined ? new Date(user.date_joined).toLocaleDateString('tr-TR', { year:'numeric', month:'long', day:'numeric' }) : '-'}
              </div>
            </div>
          </div>

          <div className="action-buttons">
            {!edit && <button className="btn btn-primary" id="edit-btn" onClick={toggleEdit}>Profili Düzenle</button>}
            {edit && <button className="btn btn-success" id="save-btn" onClick={saveProfile}>Değişiklikleri Kaydet</button>}
            {edit && <button className="btn btn-secondary" id="cancel-btn" onClick={cancelEdit}>İptal</button>}
          </div>
        </div>
      </div>

      {/* Cropper Modal */}
      <div id="cropper-overlay" className={`modal-overlay ${modalOpen? 'open':''}`} aria-modal="true" role="dialog">
        <div className="modal">
          <div className="modal-header">Profil Fotoğrafını Güncelle</div>
          <div className="modal-body">
            <div id="crop-frame" className="crop-frame" ref={frameRef}>
              <img id="crop-image" alt="crop" />
              <div id="circle-mask" className="circle-mask" ref={maskRef} style={{'--d': circleD + 'px'}}></div>
            </div>
            <div className="controls">
              <div className="range-row">
                <label htmlFor="zoom-range">Yakınlaştır</label>
                <input id="zoom-range" type="range" min="100" max="300" defaultValue="100" />
                <span id="zoom-label" style={{width:48, textAlign:'right', color:'#666', fontSize:'.9rem'}}>100%</span>
              </div>
            </div>
            <div className="modal-actions">
              <button id="reselect-btn" type="button" className="btn-light btn-upload" onClick={()=> fileInputRef.current?.click()}>📤 Dosya Seç</button>
              <button id="cancel-crop-btn" type="button" className="btn-light" onClick={()=> setModalOpen(false)}>İptal</button>
              <button id="save-crop-btn" type="button" className="btn-green" onClick={saveCropped}>Kaydet</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

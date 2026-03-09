import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid } from 'recharts';

export default function App() {
  const [phase, setPhase] = useState(1);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [predictData, setPredictData] = useState({ avg_ticket_price: 3500, booking_abandonment_rate: 0.2, rewards_points: 1000 });
  const [singleRisk, setSingleRisk] = useState(null);

  const getApiUrl = () => {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:8000';
    }
    return 'https://churnguard-api-kbvg.onrender.com';
  };

  const API_BASE_URL = getApiUrl();

  useEffect(() => {
    const timer1 = setTimeout(() => setPhase(2), 3000);
    const timer2 = setTimeout(() => setPhase(3), 5500);
    return () => { clearTimeout(timer1); clearTimeout(timer2); };
  }, []);

  const runPipeline = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE_URL}/api/train`, { target_col: 'is_churned', model_choice: 'XGBoost Classifier' });
      setResult(res.data);
    } catch(err) { 
      alert("Backend Error: " + API_BASE_URL);
    } finally { setLoading(false); }
  };

  const checkPassenger = async () => {
    try {
      const res = await axios.post(`${API_BASE_URL}/api/predict`, {
        avg_ticket_price: parseFloat(predictData.avg_ticket_price) || 0,
        booking_abandonment_rate: parseFloat(predictData.booking_abandonment_rate) || 0,
        rewards_points: parseFloat(predictData.rewards_points) || 0
      });
      setSingleRisk(res.data);
    } catch(err) { alert("Error: " + err.message); }
  };

  const downloadReport = () => {
    window.open(`${API_BASE_URL}/api/download-report`);
  };

  return (
    <div style={{
      margin: 0, padding: 0, height: '100vh', width: '100vw', display: 'flex', justifyContent: 'center', alignItems: 'center',
      background: 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 15%, #16213e 30%, #0f3460 50%, #1a1f3a 70%, #16213e 85%, #0a0e27 100%)',
      fontFamily: '"Sora", sans-serif', overflow: 'auto', position: 'relative'
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&display=swap');
        
        * { box-sizing: border-box; }
        body, html { margin: 0; padding: 0; }
        
        @keyframes indigoGlow { 
          from { opacity: 0; transform: scale(0.7) translateY(30px); filter: blur(20px); }
          70% { transform: scale(1.05); }
          to { opacity: 1; transform: scale(1) translateY(0); filter: blur(0); }
        }
        
        @keyframes titleSlideIn {
          from { opacity: 0; transform: translateY(-50px); filter: blur(10px); }
          to { opacity: 1; transform: translateY(0); filter: blur(0); }
        }
        
        @keyframes subtitleFade {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideDown {
          from { opacity: 0; transform: translateY(-30px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes floatOrb1 {
          0%, 100% { transform: translate(0, 0); }
          50% { transform: translate(80px, -60px); }
        }
        
        @keyframes floatOrb2 {
          0%, 100% { transform: translate(0, 0); }
          50% { transform: translate(-100px, 80px); }
        }
        
        .viewport-bg {
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 100vh;
          z-index: 0;
        }
        
        .viewport-bg::before {
          content: '';
          position: absolute;
          width: 600px;
          height: 600px;
          background: radial-gradient(circle, rgba(0, 173, 239, 0.15), transparent);
          border-radius: 50%;
          top: -200px;
          left: -200px;
          animation: floatOrb1 15s ease-in-out infinite;
          filter: blur(40px);
        }
        
        .viewport-bg::after {
          content: '';
          position: absolute;
          width: 500px;
          height: 500px;
          background: radial-gradient(circle, rgba(0, 188, 212, 0.1), transparent);
          border-radius: 50%;
          bottom: -150px;
          right: -150px;
          animation: floatOrb2 18s ease-in-out infinite;
          filter: blur(50px);
        }

        .content {
          position: relative;
          z-index: 10;
        }
      `}</style>

      <div className="viewport-bg"></div>

      {/* PHASE 1: LOGO INTRO */}
      {phase === 1 && (
        <div className="content" style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '30px', animation: 'indigoGlow 2s ease-out' }}>
          <img src="/indigo-logo.png" alt="Indigo" style={{ height: '220px', width: 'auto', filter: 'drop-shadow(0 0 60px rgba(0, 173, 239, 0.7))', objectFit: 'contain' }} />
          <div style={{ fontSize: '20px', color: '#94a3b8', letterSpacing: '6px', fontWeight: '700', animation: 'subtitleFade 2s ease-out 0.3s both' }}>CHURNGUARD PRO</div>
        </div>
      )}

      {/* PHASE 2: TITLE SPLASH */}
      {phase === 2 && (
        <div className="content" style={{ textAlign: 'center', animation: 'slideDown 1.5s ease-out' }}>
          <h1 style={{ fontSize: '96px', color: '#00adef', margin: 0, fontWeight: '800', textShadow: '0 0 50px rgba(0, 173, 239, 0.8)', letterSpacing: '-2px', animation: 'titleSlideIn 1.2s ease-out' }}>ChurnGuard Pro</h1>
          <p style={{ fontSize: '16px', color: '#cbd5e1', letterSpacing: '8px', marginTop: '25px', fontWeight: '600', animation: 'subtitleFade 1.2s ease-out 0.4s both' }}>PREDICTIVE INTELLIGENCE</p>
          <p style={{ fontSize: '14px', color: '#00adef', marginTop: '25px', fontWeight: '700', animation: 'subtitleFade 1.2s ease-out 0.7s both' }}>By Prabhmeet Singh Ahuja</p>
          <p style={{ fontSize: '12px', color: '#64748b', marginTop: '10px', animation: 'subtitleFade 1.2s ease-out 0.9s both' }}>Powered by XGBoost & SHAP Intelligence</p>
        </div>
      )}

      {/* PHASE 3: MAIN DASHBOARD */}
      {phase === 3 && (
        <div className="content" style={{ 
          background: 'linear-gradient(135deg, rgba(10, 14, 39, 0.96), rgba(26, 31, 58, 0.92))',
          backdropFilter: 'blur(60px)',
          border: '1px solid rgba(0, 173, 239, 0.18)',
          borderRadius: '28px',
          padding: '52px',
          maxWidth: '1500px',
          width: '92%',
          maxHeight: '90vh',
          overflowY: 'auto',
          boxShadow: '0 30px 60px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(0, 173, 239, 0.12)',
          animation: 'slideDown 0.8s ease-out'
        }}>
          
          {/* HEADER */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '45px', paddingBottom: '25px', borderBottom: '1px solid rgba(0, 173, 239, 0.15)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '18px' }}>
              <img src="/indigo-logo.png" alt="Indigo" style={{ height: '60px', width: 'auto', filter: 'drop-shadow(0 0 20px rgba(0, 173, 239, 0.5))', objectFit: 'contain' }} />
              <div>
                <h2 style={{ fontSize: '32px', color: '#00adef', margin: 0, fontWeight: '800', letterSpacing: '1px' }}>ChurnGuard Pro</h2>
                <p style={{ fontSize: '12px', color: '#94a3b8', margin: '5px 0 0 0', letterSpacing: '2px' }}>INDIGO AIRLINES ANALYTICS</p>
              </div>
            </div>
            <button onClick={downloadReport} style={{
              padding: '14px 32px', background: 'linear-gradient(90deg, #00adef, #0088cc)', color: '#fff', border: 'none',
              borderRadius: '12px', fontWeight: '700', cursor: 'pointer', fontSize: '13px', textTransform: 'uppercase', letterSpacing: '1px',
              boxShadow: '0 8px 32px rgba(0, 173, 239, 0.4)', transition: 'all 0.3s', animation: 'slideDown 0.8s ease-out 0.2s both'
            }} onMouseOver={e => e.target.style.transform = 'translateY(-3px)'} onMouseOut={e => e.target.style.transform = 'translateY(0)'}>
              📊 Export Report
            </button>
          </div>

          {/* KPI CARDS */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '22px', marginBottom: '40px' }}>
            {[
              { label: 'Active Records', value: result?.dashboard?.active_passengers || '—', color: '#00adef', idx: 0 },
              { label: 'Churn Rate', value: result?.dashboard?.churn_rate?.toFixed(1) + '%' || '—', color: '#ff6b6b', idx: 1 },
              { label: 'Model Ready', value: result ? '✓ Yes' : '—', color: '#00cc66', idx: 2 }
            ].map(kpi => (
              <div key={kpi.idx} style={{
                background: 'linear-gradient(135deg, rgba(0, 173, 239, 0.1), rgba(0, 188, 212, 0.05))',
                border: '2px solid rgba(0, 173, 239, 0.3)',
                padding: '28px', borderRadius: '16px', transition: 'all 0.3s',
                animation: `slideUp 0.6s ease-out ${0.1 * kpi.idx}s both`
              }} onMouseMove={e => e.currentTarget.style.borderColor = kpi.color} onMouseLeave={e => e.currentTarget.style.borderColor = 'rgba(0, 173, 239, 0.3)'}>
                <div style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '2px', marginBottom: '12px', fontWeight: '700' }}>{kpi.label}</div>
                <div style={{ fontSize: '36px', color: kpi.color, fontWeight: '800' }}>{kpi.value}</div>
              </div>
            ))}
          </div>

          {/* MAIN ACTION */}
          {!result ? (
            <button onClick={runPipeline} disabled={loading} style={{
              width: '100%', padding: '24px', background: `linear-gradient(90deg, #00adef, #0088cc)`, color: '#fff', border: 'none',
              borderRadius: '14px', fontWeight: '800', fontSize: '16px', cursor: 'pointer', textTransform: 'uppercase', letterSpacing: '1.5px',
              boxShadow: '0 12px 40px rgba(0, 173, 239, 0.4)', transition: 'all 0.4s', opacity: loading ? 0.65 : 1,
              animation: 'slideUp 0.8s ease-out'
            }} onMouseOver={e => !loading && (e.target.style.transform = 'translateY(-4px)')} onMouseOut={e => e.target.style.transform = 'translateY(0)'}>
              {loading ? '🔄 TRAINING XGBOOST MODEL...' : '🚀 TRAIN MODEL & ANALYZE DATA'}
            </button>
          ) : (
            <div>
              {/* CHARTS GRID */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px', marginTop: '40px', marginBottom: '40px' }}>
                
                {/* Feature Importance */}
                <div style={{
                  background: 'linear-gradient(135deg, rgba(0, 173, 239, 0.08), rgba(0, 188, 212, 0.04))',
                  border: '2px solid rgba(0, 173, 239, 0.25)', padding: '28px', borderRadius: '16px',
                  animation: 'slideUp 0.6s ease-out 0s both'
                }}>
                  <h3 style={{ fontSize: '14px', color: '#00adef', margin: '0 0 20px 0', textTransform: 'uppercase', letterSpacing: '2px', fontWeight: '800' }}>📊 Feature Importance (SHAP)</h3>
                  <div style={{ height: '320px' }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={result?.feature_importance?.slice(0, 6) || []}>
                        <XAxis dataKey="feature" stroke="#64748b" fontSize={11} />
                        <YAxis stroke="#64748b" fontSize={11} />
                        <Tooltip contentStyle={{ backgroundColor: 'rgba(0, 21, 41, 0.95)', border: '1px solid #00adef', color: '#00adef', borderRadius: '8px' }} />
                        <Bar dataKey="importance" fill="#00adef" radius={[8, 8, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* ROC Curve */}
                <div style={{
                  background: 'linear-gradient(135deg, rgba(0, 173, 239, 0.08), rgba(0, 188, 212, 0.04))',
                  border: '2px solid rgba(0, 173, 239, 0.25)', padding: '28px', borderRadius: '16px',
                  animation: 'slideUp 0.6s ease-out 0.1s both'
                }}>
                  <h3 style={{ fontSize: '14px', color: '#00adef', margin: '0 0 20px 0', textTransform: 'uppercase', letterSpacing: '2px', fontWeight: '800' }}>📈 ROC Curve (Model Reliability)</h3>
                  <div style={{ height: '320px' }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={result?.roc_data || []}>
                        <CartesianGrid stroke="rgba(0, 173, 239, 0.1)" />
                        <XAxis dataKey="fpr" stroke="#64748b" fontSize={11} />
                        <YAxis stroke="#64748b" fontSize={11} />
                        <Tooltip contentStyle={{ backgroundColor: 'rgba(0, 21, 41, 0.95)', border: '1px solid #00cc66', color: '#00cc66', borderRadius: '8px' }} />
                        <Line type="monotone" dataKey="tpr" stroke="#00cc66" strokeWidth={3} dot={false} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Route Risk */}
                <div style={{
                  background: 'linear-gradient(135deg, rgba(0, 173, 239, 0.08), rgba(0, 188, 212, 0.04))',
                  border: '2px solid rgba(0, 173, 239, 0.25)', padding: '28px', borderRadius: '16px',
                  animation: 'slideUp 0.6s ease-out 0.2s both'
                }}>
                  <h3 style={{ fontSize: '14px', color: '#00adef', margin: '0 0 20px 0', textTransform: 'uppercase', letterSpacing: '2px', fontWeight: '800' }}>✈️ Fleet Route Risk</h3>
                  <div style={{ height: '320px' }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={result?.fleet_data || []}>
                        <XAxis dataKey="route" stroke="#64748b" fontSize={11} />
                        <YAxis stroke="#64748b" fontSize={11} />
                        <Tooltip contentStyle={{ backgroundColor: 'rgba(0, 21, 41, 0.95)', border: '1px solid #ff6b6b', color: '#ff6b6b', borderRadius: '8px' }} />
                        <Bar dataKey="risk" fill="#ff6b6b" radius={[8, 8, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Individual Risk */}
                <div style={{
                  background: 'linear-gradient(135deg, rgba(0, 173, 239, 0.08), rgba(0, 188, 212, 0.04))',
                  border: '2px solid rgba(0, 173, 239, 0.25)', padding: '28px', borderRadius: '16px',
                  animation: 'slideUp 0.6s ease-out 0.3s both'
                }}>
                  <h3 style={{ fontSize: '14px', color: '#00adef', margin: '0 0 20px 0', textTransform: 'uppercase', letterSpacing: '2px', fontWeight: '800' }}>🎯 Individual Passenger Risk</h3>
                  
                  <label style={{ fontSize: '11px', color: '#94a3b8', margin: '0 0 6px 0', display: 'block', fontWeight: '700', textTransform: 'uppercase' }}>Ticket Price (₹)</label>
                  <input type="number" placeholder="e.g. 5000" onChange={e => setPredictData({...predictData, avg_ticket_price: e.target.value})} style={{
                    width: '100%', padding: '12px 14px', marginBottom: '12px', background: 'rgba(0, 21, 41, 0.8)', color: '#e0e0e0',
                    border: '1.5px solid rgba(0, 173, 239, 0.2)', borderRadius: '10px', fontSize: '13px', outline: 'none',
                    transition: 'all 0.3s', boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3)'
                  }} onFocus={e => e.target.style.borderColor = '#00adef'} onBlur={e => e.target.style.borderColor = 'rgba(0, 173, 239, 0.2)'} />
                  
                  <label style={{ fontSize: '11px', color: '#94a3b8', margin: '0 0 6px 0', display: 'block', fontWeight: '700', textTransform: 'uppercase' }}>Abandonment Rate (0–1)</label>
                  <input type="number" step="0.1" placeholder="e.g. 0.3" onChange={e => setPredictData({...predictData, booking_abandonment_rate: e.target.value})} style={{
                    width: '100%', padding: '12px 14px', marginBottom: '12px', background: 'rgba(0, 21, 41, 0.8)', color: '#e0e0e0',
                    border: '1.5px solid rgba(0, 173, 239, 0.2)', borderRadius: '10px', fontSize: '13px', outline: 'none',
                    transition: 'all 0.3s', boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3)'
                  }} onFocus={e => e.target.style.borderColor = '#00adef'} onBlur={e => e.target.style.borderColor = 'rgba(0, 173, 239, 0.2)'} />
                  
                  <label style={{ fontSize: '11px', color: '#94a3b8', margin: '0 0 6px 0', display: 'block', fontWeight: '700', textTransform: 'uppercase' }}>6E Rewards Points</label>
                  <input type="number" placeholder="e.g. 1500" onChange={e => setPredictData({...predictData, rewards_points: e.target.value})} style={{
                    width: '100%', padding: '12px 14px', marginBottom: '16px', background: 'rgba(0, 21, 41, 0.8)', color: '#e0e0e0',
                    border: '1.5px solid rgba(0, 173, 239, 0.2)', borderRadius: '10px', fontSize: '13px', outline: 'none',
                    transition: 'all 0.3s', boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3)'
                  }} onFocus={e => e.target.style.borderColor = '#00adef'} onBlur={e => e.target.style.borderColor = 'rgba(0, 173, 239, 0.2)'} />
                  
                  <button onClick={checkPassenger} style={{
                    width: '100%', padding: '12px', background: 'linear-gradient(90deg, #00adef, #0088cc)', color: '#fff', border: 'none',
                    borderRadius: '10px', fontWeight: '700', fontSize: '13px', cursor: 'pointer', textTransform: 'uppercase', letterSpacing: '1px',
                    boxShadow: '0 6px 20px rgba(0, 173, 239, 0.3)', transition: 'all 0.3s'
                  }} onMouseOver={e => e.target.style.transform = 'translateY(-2px)'} onMouseOut={e => e.target.style.transform = 'translateY(0)'}>
                    Analyze Risk
                  </button>
                  
                  {singleRisk && (
                    <div style={{
                      marginTop: '18px', padding: '18px', background: 'rgba(0, 21, 41, 0.85)', borderRadius: '12px',
                      border: `2px solid ${singleRisk.churn_probability > 50 ? '#ff6b6b' : '#00cc66'}`,
                      animation: 'slideUp 0.5s ease-out'
                    }}>
                      <div style={{ fontSize: '42px', fontWeight: '800', color: singleRisk.churn_probability > 50 ? '#ff6b6b' : '#00cc66', marginBottom: '6px' }}>
                        {singleRisk.churn_probability.toFixed(1)}%
                      </div>
                      <div style={{ fontSize: '11px', color: '#94a3b8', marginBottom: '10px' }}>Churn Probability</div>
                      <div style={{ fontSize: '11px', color: '#00adef', fontWeight: '700', padding: '10px', background: 'rgba(0, 173, 239, 0.12)', borderRadius: '8px' }}>
                        {singleRisk.voucher}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* FOOTER ATTRIBUTION */}
              <div style={{
                textAlign: 'center', paddingTop: '30px', borderTop: '1px solid rgba(0, 173, 239, 0.15)',
                animation: 'subtitleFade 0.8s ease-out 0.8s both'
              }}>
                <p style={{ fontSize: '13px', color: '#00adef', margin: '0 0 6px 0', fontWeight: '700', letterSpacing: '1px' }}>✨ Built by Prabhmeet Singh Ahuja</p>
                <p style={{ fontSize: '11px', color: '#64748b', margin: 0 }}>Powered by XGBoost & SHAP | Machine Learning Intelligence Platform</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

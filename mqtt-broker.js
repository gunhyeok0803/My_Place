/* 공개 / 클라우드(EMQX Serverless) 브로커 선택 — mqtt-pose-twin.html · mqtt-pose-send.html 공용.
   배포 주소 · 사용자 이름은 이 기기(localStorage)에 기억한다. 비밀번호는 "이 기기에 비밀번호 저장"을 켰을 때만 저장하고,
   코드와 GitHub에는 넣지 않는다. */
(() => {
  const PUBLIC_URL = 'wss://broker.emqx.io:8084/mqtt';
  const CLOUD_HOST = 'd67192c0.ala.asia-southeast1.emqxsl.com';   // 내 EMQX Serverless 배포 주소 (주소는 공개돼도 괜찮다)
  const KEY = 'khu_broker';
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } };
  const store = s => { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch { /* 기억하기는 편의 기능 */ } };
  const cleanHost = h => h.trim().replace(/^wss?:\/\//, '').replace(/[:/].*$/, '');

  function mount(root) {
    root.innerHTML = `
      <label for="brokerType">브로커</label>
      <select id="brokerType">
        <option value="cloud">클라우드 (EMQX Serverless)</option>
        <option value="public">공개 (broker.emqx.io)</option>
      </select>
      <div id="cloudFields">
        <label for="brokerHost">배포 주소</label>
        <input type="text" id="brokerHost" spellcheck="false" autocomplete="off">
        <label for="brokerUser">사용자 이름</label>
        <input type="text" id="brokerUser" spellcheck="false" autocomplete="username">
        <label for="brokerPass">비밀번호</label>
        <input type="password" id="brokerPass" autocomplete="current-password">
        <label class="check"><input type="checkbox" id="brokerRemember"> 이 기기에 비밀번호 저장 (공용 PC에서는 끄기)</label>
      </div>`;
    const $ = id => root.querySelector('#' + id);
    const saved = load();
    $('brokerType').value = saved.type === 'public' ? 'public' : 'cloud';
    $('brokerHost').value = saved.host || CLOUD_HOST;
    $('brokerUser').value = saved.user || '';
    $('brokerRemember').checked = Boolean(saved.remember);
    $('brokerPass').value = saved.remember ? saved.pass || '' : '';
    const toggle = () => { $('cloudFields').hidden = $('brokerType').value !== 'cloud'; };
    $('brokerType').addEventListener('change', toggle); toggle();

    return {
      // 화면에 적힌 값 (저장 · 검사 없이). 안내 문구용
      info: () => ({ type: $('brokerType').value, host: cleanHost($('brokerHost').value), user: $('brokerUser').value.trim() }),
      // 연결에 쓸 주소와 계정. 빠진 값이 있으면 { error }
      current() {
        if ($('brokerType').value === 'public') {
          store({ ...load(), type: 'public' });
          return { url: PUBLIC_URL, auth: {}, label: '공개' };
        }
        const host = cleanHost($('brokerHost').value), user = $('brokerUser').value.trim(), pass = $('brokerPass').value;
        if (!/^[A-Za-z0-9.-]+$/.test(host)) return { error: '배포 주소를 확인하세요. 예: xxxx.ala.asia-southeast1.emqxsl.com' };
        if (!user || !pass) return { error: '클라우드는 사용자 이름과 비밀번호가 필요합니다.' };
        const remember = $('brokerRemember').checked;
        store({ type: 'cloud', host, user, remember, pass: remember ? pass : undefined });
        return { url: `wss://${host}:8084/mqtt`, auth: { username: user, password: pass }, label: '클라우드' };
      },
      lock(on) { root.querySelectorAll('select, input').forEach(el => { el.disabled = on; }); },
    };
  }

  // CONNACK 4 · 5 = 사용자 이름 · 비밀번호 오류 / 권한 없음 (MQTT 3.1.1)
  const isAuthError = e => e?.code === 4 || e?.code === 5 || /not authori[sz]ed|bad user ?name or password/i.test(e?.message || '');
  globalThis.KhuBroker = { mount, isAuthError };
})();

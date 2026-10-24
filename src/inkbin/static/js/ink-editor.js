// INK Editorial JavaScript Controller

function t(key, fallback = key, params = {}) {
  const dict = window.__INK_I18N__ || {};
  let val = dict[key] !== undefined ? dict[key] : fallback;
  if (params && typeof params === 'object') {
    for (const [k, v] of Object.entries(params)) {
      val = val.replace(new RegExp(`\\{${k}\\}`, 'g'), v);
    }
  }
  return val;
}

document.addEventListener('DOMContentLoaded', () => {
  setupEditor();
  setupLocalHistory();
  setupViewerCopyActions();
  setupMobileNavigation();
});

function setupEditor() {
  const textarea = document.getElementById('paste-content');
  const form = document.getElementById('paste-form');
  const charCountEl = document.getElementById('char-count');
  const byteCountEl = document.getElementById('byte-count');
  const submitBtn = document.getElementById('submit-btn');

  if (!textarea) return;

  // Tab key indentation support
  textarea.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const value = textarea.value;

      textarea.value = value.substring(0, start) + '    ' + value.substring(end);
      textarea.selectionStart = textarea.selectionEnd = start + 4;
      updateStats();
    }
  });

  function updateStats() {
    const text = textarea.value;
    const chars = text.length;
    const bytes = new Blob([text]).size;

    if (charCountEl) {
      const charsText = t('editor.chars', `${chars.toLocaleString()} caracteres`, { count: chars.toLocaleString() });
      charCountEl.innerHTML = `<i class="ti ti-letter-case icon-sm" aria-hidden="true"></i> <span>${charsText}</span>`;
    }
    if (byteCountEl) {
      const maxText = t('editor.bytes_max', 'máx');
      let byteStr = '';
      if (bytes < 1024) {
        byteStr = `${bytes} B`;
      } else if (bytes < 1024 * 1024) {
        byteStr = `${(bytes / 1024).toFixed(1)} KB`;
      } else {
        byteStr = `${(bytes / (1024 * 1024)).toFixed(2)} MB / 1 MB ${maxText}`;
      }
      byteCountEl.innerHTML = `<i class="ti ti-database icon-sm" aria-hidden="true"></i> <span>${byteStr}</span>`;
    }
  }

  textarea.addEventListener('input', updateStats);
  updateStats();

  // Format change hint listener
  const formatSelect = document.getElementById('paste-content-format');
  const base64Hint = document.getElementById('base64-warning-hint');
  if (formatSelect && base64Hint) {
    formatSelect.addEventListener('change', () => {
      base64Hint.style.display = formatSelect.value === 'base64' ? 'flex' : 'none';
    });
  }

  // Async form submission
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const content = textarea.value;
      if (!content.trim()) {
        alert(t('editor.alert_empty', 'Por favor, insira o conteúdo do paste antes de publicar.'));
        return;
      }

      const title = document.getElementById('paste-title')?.value || null;
      const language = document.getElementById('paste-language')?.value || 'plaintext';
      const expiration = document.getElementById('paste-expiration')?.value || 'never';
      const password = document.getElementById('paste-password')?.value || null;
      const contentFormat = formatSelect ? formatSelect.value : 'plaintext';
      const burnAfterRead = Boolean(document.getElementById('paste-burn-after-read')?.checked);

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i class="ti ti-loader animate-spin" aria-hidden="true"></i> <span>${t('editor.publishing_btn', 'Publicando...')}</span>`;
      }

      let contentToSend = content;
      let keyFragment = null;

      try {
        if (contentFormat === 'aes-256-gcm') {
          const key = await generateAesKey();
          contentToSend = await encryptText(content, key);
          keyFragment = await exportKeyToBase64Url(key);
        } else if (contentFormat === 'base64') {
          contentToSend = utf8ToBase64(content);
        }

        const response = await fetch('/api/pastes', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: title || null,
            content: contentToSend,
            language,
            expiration,
            password: password || null,
            content_format: contentFormat,
            burn_after_read: burnAfterRead,
          }),
        });

        if (!response.ok) {
          const err = await response.json();
          alert(err.detail || t('editor.alert_error', 'Ocorreu um erro ao publicar o paste.'));
          return;
        }

        const data = await response.json();
        const fullShareUrl = keyFragment ? `${data.url}#${keyFragment}` : data.url;

        // Save to local history
        saveToLocalHistory({
          slug: data.slug,
          title: data.title || t('viewer.untitled', 'Sem título'),
          language: data.language,
          created_at: data.created_at,
          admin_delete_token: data.admin_delete_token,
          url: fullShareUrl,
          content_format: data.content_format,
          burn_after_read: data.burn_after_read,
        });

        // Show Success Modal
        showSuccessModal(data, keyFragment);
      } catch (err) {
        console.error('Submission error:', err);
        alert(t('editor.alert_network', 'Falha na conexão ao publicar o paste.'));
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<i class="ti ti-upload" aria-hidden="true"></i> <span>${t('editor.submit_btn', 'Publicar texto')}</span>`;
        }
      }
    });
  }
}

// --- Client-Side Cryptography (Web Crypto API) & Base64 ---

function bufferToBase64(buffer) {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

function base64ToBuffer(base64) {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}

function bufferToBase64Url(buffer) {
  const base64 = bufferToBase64(buffer);
  return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function base64UrlToBuffer(base64url) {
  let base64 = base64url.replace(/-/g, '+').replace(/_/g, '/');
  while (base64.length % 4) {
    base64 += '=';
  }
  return base64ToBuffer(base64);
}

function utf8ToBase64(text) {
  const bytes = new TextEncoder().encode(text);
  return bufferToBase64(bytes);
}

function base64ToUtf8(base64) {
  const bytes = base64ToBuffer(base64);
  return new TextDecoder().decode(bytes);
}

async function generateAesKey() {
  if (!window.crypto || !window.crypto.subtle) {
    throw new Error('Web Crypto API não disponível neste navegador.');
  }
  return await window.crypto.subtle.generateKey(
    { name: 'AES-GCM', length: 256 },
    true,
    ['encrypt', 'decrypt']
  );
}

async function encryptText(text, key) {
  const iv = window.crypto.getRandomValues(new Uint8Array(12));
  const encodedText = new TextEncoder().encode(text);
  const ciphertextBuffer = await window.crypto.subtle.encrypt(
    { name: 'AES-GCM', iv: iv },
    key,
    encodedText
  );

  const combined = new Uint8Array(iv.length + ciphertextBuffer.byteLength);
  combined.set(iv, 0);
  combined.set(new Uint8Array(ciphertextBuffer), iv.length);
  return bufferToBase64(combined);
}

async function exportKeyToBase64Url(key) {
  const rawKey = await window.crypto.subtle.exportKey('raw', key);
  return bufferToBase64Url(rawKey);
}

async function importKeyFromBase64Url(base64url) {
  const keyBytes = base64UrlToBuffer(base64url);
  return await window.crypto.subtle.importKey(
    'raw',
    keyBytes,
    { name: 'AES-GCM' },
    false,
    ['decrypt']
  );
}

async function decryptText(base64Combined, key) {
  const combined = base64ToBuffer(base64Combined);
  if (combined.byteLength < 13) {
    throw new Error('Payload cifrado corrompido ou tamanho insuficiente.');
  }
  const iv = combined.slice(0, 12);
  const ciphertext = combined.slice(12);

  const decryptedBuffer = await window.crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: iv },
    key,
    ciphertext
  );
  return new TextDecoder().decode(decryptedBuffer);
}

function showSuccessModal(data, keyFragment = null) {
  const modal = document.getElementById('success-modal');
  if (!modal) {
    const redirectUrl = keyFragment ? `${data.url}#${keyFragment}` : data.url;
    window.location.href = redirectUrl;
    return;
  }

  // Resolve public URL for local and mobile access
  let targetUrl = data.url;
  try {
    const parsed = new URL(data.url, window.location.origin);
    if (parsed.hostname === 'localhost' && window.location.hostname !== 'localhost') {
      parsed.hostname = window.location.hostname;
      parsed.port = window.location.port;
      parsed.protocol = window.location.protocol;
      targetUrl = parsed.toString();
    } else if (!data.url.startsWith('http://') && !data.url.startsWith('https://')) {
      targetUrl = new URL(data.url, window.location.origin).toString();
    }
  } catch (e) {
    targetUrl = data.url;
  }

  if (keyFragment) {
    targetUrl = `${targetUrl}#${keyFragment}`;
  }

  const encryptedNotice = document.getElementById('modal-encrypted-notice');
  if (encryptedNotice) {
    encryptedNotice.style.display = keyFragment ? 'flex' : 'none';
  }

  document.getElementById('modal-slug-url').value = targetUrl;
  document.getElementById('modal-delete-token').textContent = data.admin_delete_token;
  document.getElementById('modal-view-link').href = targetUrl;

  // Render QR Code for mobile scanning
  const qrContainer = document.getElementById('modal-qrcode');
  if (qrContainer) {
    qrContainer.innerHTML = '';
    if (typeof QRCode !== 'undefined') {
      try {
        new QRCode(qrContainer, {
          text: targetUrl,
          width: 128,
          height: 128,
          colorDark: '#0a0a0a',
          colorLight: '#ffffff',
          correctLevel: typeof QRCode.CorrectLevel !== 'undefined' ? QRCode.CorrectLevel.M : 0
        });
      } catch (err) {
        console.error('Failed to generate QR Code:', err);
      }
    }
  }

  modal.style.display = 'flex';
}

function closeSuccessModal() {
  const modal = document.getElementById('success-modal');
  if (modal) {
    modal.style.display = 'none';
  }
}

/**
 * Synchronous clipboard copy fallback via document.execCommand('copy').
 * Highly compatible with Mobile Safari (iOS WebKit), older browsers, and non-secure HTTP contexts.
 * @param {string} text
 * @param {HTMLElement} [sourceEl]
 * @returns {boolean}
 */
function copyUsingExecCommand(text, sourceEl) {
  let successful = false;

  try {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    // Set 16px to prevent iOS Safari auto-zoom on element focus
    textArea.style.fontSize = '16px';
    // Position fixed and off-screen to prevent iOS viewport jumping/scrolling
    textArea.style.position = 'fixed';
    textArea.style.top = '0';
    textArea.style.left = '-9999px';
    textArea.style.width = '2em';
    textArea.style.height = '2em';
    textArea.style.padding = '0';
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';
    textArea.style.background = 'transparent';
    // Set readonly to avoid triggering iOS virtual keyboard
    textArea.setAttribute('readonly', '');

    document.body.appendChild(textArea);

    const selection = window.getSelection();
    const originalRange = selection && selection.rangeCount > 0 ? selection.getRangeAt(0) : null;

    textArea.focus();
    textArea.select();
    textArea.setSelectionRange(0, text.length);

    try {
      successful = document.execCommand('copy');
    } catch (e) {
      successful = false;
    }

    document.body.removeChild(textArea);

    if (selection && originalRange) {
      selection.removeAllRanges();
      selection.addRange(originalRange);
    }

    if (successful) return true;
  } catch (err) {
    successful = false;
  }

  // Secondary fallback for inputs or elements already attached to DOM
  if (!successful && sourceEl) {
    try {
      if (typeof sourceEl.select === 'function') {
        sourceEl.focus();
        if (typeof sourceEl.setSelectionRange === 'function') {
          sourceEl.setSelectionRange(0, (sourceEl.value || '').length);
        } else {
          sourceEl.select();
        }
        successful = document.execCommand('copy');
      } else {
        const selection = window.getSelection();
        if (selection) {
          const range = document.createRange();
          range.selectNodeContents(sourceEl);
          selection.removeAllRanges();
          selection.addRange(range);
          successful = document.execCommand('copy');
          selection.removeAllRanges();
        }
      }
    } catch (e) {
      successful = false;
    }
  }

  return successful;
}

/**
 * Universal cross-browser copy function supporting iOS Safari,
 * non-HTTPS (local development) and modern Clipboard API.
 * @param {string} text
 * @param {HTMLElement} [sourceEl]
 * @returns {Promise<boolean>}
 */
async function copyTextToClipboard(text, sourceEl) {
  if (text === undefined || text === null) {
    text = '';
  }
  text = String(text);

  // 1. Try synchronous execCommand first — preserves user activation on iOS Safari & works on HTTP
  const execSuccess = copyUsingExecCommand(text, sourceEl);
  if (execSuccess) {
    return true;
  }

  // 2. Try modern Clipboard API if supported and in secure context
  if (navigator.clipboard && window.isSecureContext && typeof navigator.clipboard.writeText === 'function') {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      console.warn('navigator.clipboard.writeText failed:', err);
    }
  }

  return false;
}

function copyToClipboard(elementId, feedbackBtnId) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const text = (el.value !== undefined ? el.value : el.textContent) || '';

  const btn = document.getElementById(feedbackBtnId);

  copyTextToClipboard(text, el).then((success) => {
    if (success) {
      if (btn) {
        const originalHtml = btn.innerHTML;
        const originalTitle = btn.getAttribute('title') || '';
        const originalAria = btn.getAttribute('aria-label') || '';
        const hasText = btn.querySelector('span') !== null;
        const copiedText = t('modal.copied', 'Copiado!');

        if (hasText) {
          btn.innerHTML = `<i class="ti ti-check" aria-hidden="true"></i> <span>${copiedText}</span>`;
        } else {
          btn.innerHTML = `<i class="ti ti-check" aria-hidden="true"></i>`;
        }
        btn.setAttribute('aria-label', copiedText);

        setTimeout(() => {
          btn.innerHTML = originalHtml;
          if (originalTitle) btn.setAttribute('title', originalTitle);
          if (originalAria) btn.setAttribute('aria-label', originalAria);
        }, 2000);
      }
    } else {
      if (typeof el.select === 'function') {
        el.focus();
        if (typeof el.setSelectionRange === 'function') {
          el.setSelectionRange(0, (el.value || '').length);
        } else {
          el.select();
        }
      }
      alert(t('clipboard.copy_failed', 'Não foi possível copiar. Selecione o texto e copie manualmente.'));
    }
  });
}

function setupViewerCopyActions() {
  const copyCodeBtn = document.getElementById('copy-code-btn');
  if (copyCodeBtn) {
    copyCodeBtn.addEventListener('click', () => {
      const codeEl = document.getElementById('raw-code');
      if (!codeEl) return;
      const text = codeEl.textContent || '';

      copyTextToClipboard(text, codeEl).then((success) => {
        if (success) {
          const originalHtml = copyCodeBtn.innerHTML;
          const originalTitle = copyCodeBtn.getAttribute('title') || '';
          const originalAria = copyCodeBtn.getAttribute('aria-label') || '';
          const copiedText = t('viewer.code_copied', 'Código copiado!');

          copyCodeBtn.innerHTML = `<i class="ti ti-check" aria-hidden="true"></i> <span>${copiedText}</span>`;
          copyCodeBtn.setAttribute('aria-label', copiedText);

          setTimeout(() => {
            copyCodeBtn.innerHTML = originalHtml;
            if (originalTitle) copyCodeBtn.setAttribute('title', originalTitle);
            if (originalAria) copyCodeBtn.setAttribute('aria-label', originalAria);
          }, 2000);
        } else {
          const selection = window.getSelection();
          if (selection) {
            const range = document.createRange();
            range.selectNodeContents(codeEl);
            selection.removeAllRanges();
            selection.addRange(range);
          }
          alert(t('clipboard.copy_failed', 'Não foi possível copiar. Selecione o texto e copie manualmente.'));
        }
      });
    });
  }
}

window.copyToClipboard = copyToClipboard;
window.copyTextToClipboard = copyTextToClipboard;

function saveToLocalHistory(item) {
  try {
    const history = JSON.parse(localStorage.getItem('inkbin_history') || '[]');
    const filtered = history.filter(h => h.slug !== item.slug);
    filtered.unshift(item);
    const limited = filtered.slice(0, 15);
    localStorage.setItem('inkbin_history', JSON.stringify(limited));
    renderHistoryList(limited);
  } catch (e) {
    console.warn('LocalStorage error', e);
  }
}

function removePasteFromHistory(slug) {
  try {
    const history = JSON.parse(localStorage.getItem('inkbin_history') || '[]');
    const filtered = history.filter(h => h.slug !== slug);
    localStorage.setItem('inkbin_history', JSON.stringify(filtered));
    renderHistoryList(filtered);
  } catch (e) {
    console.warn('LocalStorage error', e);
  }
}

function clearLocalHistory() {
  const confirmMsg = t('nav.clear_history_confirm', 'Tem certeza de que deseja limpar todo o histórico local?');
  if (confirm(confirmMsg)) {
    try {
      localStorage.removeItem('inkbin_history');
      renderHistoryList([]);
    } catch (e) {
      console.warn('LocalStorage error', e);
    }
  }
}

function setupLocalHistory() {
  try {
    const history = JSON.parse(localStorage.getItem('inkbin_history') || '[]');
    renderHistoryList(history);

    const clearBtn = document.getElementById('clear-history-btn');
    if (clearBtn) {
      clearBtn.addEventListener('click', (e) => {
        e.preventDefault();
        clearLocalHistory();
      });
    }
  } catch (e) {
    // Ignore
  }
}

function renderHistoryList(items) {
  const container = document.getElementById('local-history-container');
  const clearBtn = document.getElementById('clear-history-btn');
  if (!container) return;

  if (!items || items.length === 0) {
    if (clearBtn) clearBtn.style.display = 'none';
    container.innerHTML = `<div style="font-size: 12px; color: var(--text-muted); padding: 8px;">${t('nav.no_history', 'Nenhum paste recente neste navegador.')}</div>`;
    return;
  }

  if (clearBtn) clearBtn.style.display = 'inline-flex';

  const deleteTitle = t('nav.delete_item_title', 'Remover do histórico');
  const deleteAria = t('nav.delete_item_aria', 'Remover este paste do histórico');

  container.innerHTML = items.map(item => `
    <div class="history-item-wrapper">
      <a href="/p/${item.slug}" class="history-item">
        <span class="history-title"><i class="ti ti-file-text icon-sm" aria-hidden="true"></i> <span>${escapeHtml(item.title || t('viewer.untitled', 'Sem título'))}</span></span>
        <span class="history-date">${item.language} · ${new Date(item.created_at).toLocaleDateString()}</span>
      </a>
      <button type="button" class="btn-delete-history-item" data-slug="${item.slug}" title="${deleteTitle}" aria-label="${deleteAria}">
        <i class="ti ti-x icon-sm" aria-hidden="true"></i>
      </button>
    </div>
  `).join('');

  container.querySelectorAll('.btn-delete-history-item').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      e.preventDefault();
      const slug = btn.getAttribute('data-slug');
      removePasteFromHistory(slug);
    });
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
}

function setupMobileNavigation() {
  const toggleBtn = document.getElementById('mobile-nav-toggle');
  const sidebar = document.getElementById('app-sidebar');
  const backdrop = document.getElementById('sidebar-backdrop');
  const closeBtn = document.getElementById('sidebar-close-btn');

  if (!toggleBtn || !sidebar || !backdrop) return;

  function openDrawer() {
    document.body.classList.add('sidebar-open');
    toggleBtn.setAttribute('aria-expanded', 'true');
    if (closeBtn) {
      setTimeout(() => closeBtn.focus(), 50);
    }
  }

  function closeDrawer() {
    document.body.classList.remove('sidebar-open');
    toggleBtn.setAttribute('aria-expanded', 'false');
    toggleBtn.focus();
  }

  toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = document.body.classList.contains('sidebar-open');
    if (isOpen) {
      closeDrawer();
    } else {
      openDrawer();
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      closeDrawer();
    });
  }

  backdrop.addEventListener('click', () => {
    closeDrawer();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && document.body.classList.contains('sidebar-open')) {
      closeDrawer();
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024 && document.body.classList.contains('sidebar-open')) {
      document.body.classList.remove('sidebar-open');
      toggleBtn.setAttribute('aria-expanded', 'false');
    }
  });
}
